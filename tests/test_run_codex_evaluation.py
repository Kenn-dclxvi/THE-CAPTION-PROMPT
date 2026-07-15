from __future__ import annotations

import unittest

from scripts.run_codex_evaluation import (
    AdapterError,
    detect_external_failure,
    prompt_fixture_collisions,
    prompt_set_identity_from_binding,
)


class RunCodexEvaluationTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
