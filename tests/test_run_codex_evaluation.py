from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.run_codex_evaluation import (
    AdapterError,
    detect_external_failure,
    evaluate_boundary_observations,
    observe_boundary_source,
    prompt_fixture_collisions,
    prompt_set_identity_from_binding,
    render_task,
    validate_boundary_evidence_compatibility,
)


class RunCodexEvaluationTest(unittest.TestCase):
    def make_git_workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path, str]:
        temporary = tempfile.TemporaryDirectory()
        workspace = Path(temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=workspace, check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.invalid"], cwd=workspace, check=True
        )
        (workspace / "tracked.txt").write_text("seed\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt"], cwd=workspace, check=True)
        subprocess.run(["git", "commit", "-qm", "seed"], cwd=workspace, check=True)
        seed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        (workspace / "tracked.txt").write_text("overlay\n", encoding="utf-8")
        subprocess.run(["git", "commit", "-qam", "overlay"], cwd=workspace, check=True)
        return temporary, workspace, seed

    def test_detects_missing_parent_thread_spawn_failure(self) -> None:
        failure = detect_external_failure(
            b"ERROR codex_core::tools::router: error=collab spawn failed: no thread with id: 019f-test\n"
        )
        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure["reason_code"], "codex_collab_parent_thread_missing")

    def test_does_not_exclude_agent_or_noncritical_runtime_errors(self) -> None:
        stderr = b"\n".join(
            [
                b"ERROR codex_core::tools::router: error=timeout_ms must be at least 10000",
                b"WARN codex_analytics::client: failed to send events request",
                b"WARN codex_core::hook_runtime: no rollout found for thread id 019f-test",
                b"ERROR codex_models_manager::manager: failed to refresh available models",
            ]
        )
        self.assertIsNone(detect_external_failure(stderr))

    def test_detects_model_capacity_failure_from_codex_jsonl(self) -> None:
        stdout = b"\n".join(
            [
                b'{"type":"thread.started","thread_id":"019f-test"}',
                b'{"type":"error","message":"Selected model is at capacity. Please try a different model."}',
                b'{"type":"turn.failed","error":{"message":"Selected model is at capacity. Please try a different model."}}',
            ]
        )

        failure = detect_external_failure(b"", stdout)

        self.assertIsNotNone(failure)
        assert failure is not None
        self.assertEqual(failure["reason_code"], "codex_model_at_capacity")

    def test_does_not_match_capacity_text_in_agent_message(self) -> None:
        stdout = b'{"type":"item.completed","item":{"type":"agent_message","text":"Selected model is at capacity."}}\n'

        self.assertIsNone(detect_external_failure(b"", stdout))

    def test_detects_prompt_target_collision_with_fixture_condition(self) -> None:
        case = {"fixture_condition_paths": ["tests/AGENTS.md", "src/domain/example.py"]}
        manifest = {
            "files": [
                {"target": "AGENTS.md"},
                {"target": "tests/AGENTS.md"},
            ]
        }

        self.assertEqual(prompt_fixture_collisions(case, manifest), ["tests/AGENTS.md"])

    def test_validates_immutable_prompt_set_identity_against_bundle(self) -> None:
        digest = "a" * 64
        identity = prompt_set_identity_from_binding(
            {
                "prompt_set_identity": {
                    "name": "prompt-r1",
                    "revision": "r1",
                    "bundle_sha256": digest,
                }
            },
            {"prompt_identity": "prompt-r1", "bundle_sha256": digest},
            digest,
        )
        self.assertEqual(identity["revision"], "r1")

        with self.assertRaisesRegex(AdapterError, "does not match"):
            prompt_set_identity_from_binding(
                {"prompt_set_identity": {"name": "other", "revision": "r1"}},
                {"prompt_identity": "prompt-r1", "bundle_sha256": digest},
                digest,
            )

    def test_binds_one_typed_observation_to_one_predicate(self) -> None:
        temporary, workspace, seed = self.make_git_workspace()
        self.addCleanup(temporary.cleanup)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

        evidence = evaluate_boundary_observations(
            workspace,
            [
                {
                    "observation_id": "head-matches-overlay",
                    "operation_identity": "start-identity",
                    "source": "workspace.git.head_commit",
                    "predicate": {
                        "operator": "string_equals",
                        "expected_context": "prompt_overlay_commit",
                    },
                },
                {
                    "observation_id": "parent-matches-seed",
                    "operation_identity": "start-identity",
                    "source": "workspace.git.parent_commit",
                    "predicate": {"operator": "string_equals", "expected": seed},
                },
                {
                    "observation_id": "worktree-clean",
                    "operation_identity": "start-identity",
                    "source": "workspace.git.status_short",
                    "predicate": {"operator": "string_equals", "expected": ""},
                },
            ],
            {
                "workspace": str(workspace),
                "prompt_overlay_commit": head,
                "prompt_overlay_tree": "tree-id",
            },
        )

        assert evidence is not None
        self.assertEqual(
            [item["status"] for item in evidence["observations"]],
            ["passed", "passed", "passed"],
        )
        self.assertEqual(len(evidence["observations"]), 3)
        self.assertTrue(all("predicate" in item for item in evidence["observations"]))

    def test_boundary_observation_reports_false_predicate_as_failed(self) -> None:
        temporary, workspace, _ = self.make_git_workspace()
        self.addCleanup(temporary.cleanup)

        evidence = evaluate_boundary_observations(
            workspace,
            [
                {
                    "observation_id": "wrong-parent",
                    "operation_identity": "start-identity",
                    "source": "workspace.git.parent_commit",
                    "predicate": {"operator": "string_equals", "expected": "not-the-parent"},
                }
            ],
            {
                "workspace": str(workspace),
                "prompt_overlay_commit": "overlay-id",
                "prompt_overlay_tree": "tree-id",
            },
        )

        assert evidence is not None
        self.assertEqual(evidence["observations"][0]["status"], "failed")

    def test_boundary_source_preserves_meaningful_status_whitespace(self) -> None:
        temporary, workspace, _ = self.make_git_workspace()
        self.addCleanup(temporary.cleanup)
        (workspace / "tracked.txt").write_text("dirty\n", encoding="utf-8")

        observed = observe_boundary_source(
            ["git", "status", "--short", "--", "tracked.txt"], workspace
        )

        self.assertEqual(observed, " M tracked.txt")

    def test_boundary_observation_reports_unavailable_source_without_aborting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            evidence = evaluate_boundary_observations(
                workspace,
                [
                    {
                        "observation_id": "missing-git-head",
                        "operation_identity": "start-identity",
                        "source": "workspace.git.head_commit",
                        "predicate": {"operator": "string_equals", "expected": "head"},
                    }
                ],
                {
                    "workspace": str(workspace),
                    "prompt_overlay_commit": "overlay-id",
                    "prompt_overlay_tree": "tree-id",
                },
            )

        assert evidence is not None
        self.assertEqual(evidence["observations"][0]["status"], "unavailable")

    def test_boundary_observation_rejects_unknown_source_and_duplicate_id(self) -> None:
        context = {
            "workspace": "/tmp/workspace",
            "prompt_overlay_commit": "overlay-id",
            "prompt_overlay_tree": "tree-id",
        }
        observation = {
            "observation_id": "identity",
            "operation_identity": "start-identity",
            "source": "workspace.git.unknown",
            "predicate": {"operator": "string_equals", "expected": "value"},
        }
        with self.assertRaisesRegex(AdapterError, "unsupported boundary observation source"):
            evaluate_boundary_observations(Path("/tmp"), [observation], context)

        observation["source"] = "workspace.path"
        with self.assertRaisesRegex(AdapterError, "duplicate boundary observation id"):
            evaluate_boundary_observations(Path("/tmp"), [observation, observation], context)

    def test_render_task_exposes_typed_evidence_without_changing_taskspec(self) -> None:
        case = {"payload": {"trial_prompt_input": {"task_id": "TC-F10"}}}
        evidence = {
            "schema_version": "the-caption-prompt.boundary-evidence/v1",
            "binding_revision": "one-observation-one-predicate/v1",
            "provenance": {},
            "observations": [{"observation_id": "parent", "status": "passed"}],
        }

        task = render_task(case, evidence)

        self.assertIn('<task-spec-json>\n{\n  "task_id": "TC-F10"', task)
        self.assertIn("<adapter-boundary-evidence-json>", task)
        self.assertIn("raw出力を再取得・再解釈しない", task)

    def test_boundary_evidence_requires_explicit_compatibility_revision(self) -> None:
        declaration = {
            "binding_revision": "one-observation-one-predicate/v1",
            "schema_version": "the-caption-prompt.boundary-evidence/v1",
            "source_policy": "adapter_managed_read_only_registry",
        }
        capsule = {
            "comparison_conditions": {
                "agent_environment": {
                    "adapter_schema_version": "the-caption-prompt.codex-adapter/v4"
                },
                "executor_parameters": {"boundary_evidence": declaration},
            }
        }

        validate_boundary_evidence_compatibility(capsule, [{}])
        with self.assertRaisesRegex(AdapterError, "without boundary observations"):
            validate_boundary_evidence_compatibility(capsule, None)
        capsule["comparison_conditions"]["executor_parameters"].pop("boundary_evidence")
        with self.assertRaisesRegex(AdapterError, "do not bind"):
            validate_boundary_evidence_compatibility(capsule, [{}])


if __name__ == "__main__":
    unittest.main()
