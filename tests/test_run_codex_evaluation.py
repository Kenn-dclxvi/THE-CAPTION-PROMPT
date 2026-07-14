from __future__ import annotations

import unittest

from scripts.run_codex_evaluation import detect_external_failure


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


if __name__ == "__main__":
    unittest.main()
