# Candidates

構築中の候補プロンプトをrevision別に置く。各candidateは解く問題、対象範囲、baseline identity、変更理由、非目標、評価状態を記録する。

| prompt identity | baseline | 変更 | 状態 |
| --- | --- | --- | --- |
| `the-caption-3ce91a4-current-copy-r1` | `the-caption-3ce91a4-current-r1` | 変更なし。null calibration用のbit-identical copy | `not_evaluated` |
| `the-caption-9b3a96a-revision-2-r1` | `the-caption-3ce91a4-current-r2` | 単一root authorityとconditional audit / reviewを含む10 target改訂 | [`observed_n5`](../../evaluations/results/candidate1-expanded12-global-m24-n5_2026-07-15.md) |
| `the-caption-3ce91a4-sa-routing-r1` | `the-caption-3ce91a4-current-r2` | 実装SA routingを維持し、riskとmachine coverageで実装後のaudit / review SAを選ぶ3 target改訂 | [`observed_n5`](../../evaluations/results/candidate2-expanded12-global-m24-n5_2026-07-15.md) |
| `the-caption-3ce91a4-sa-routing-test-boundary-r1` | `the-caption-3ce91a4-sa-routing-r1` | validationでtestを使うだけのtaskへC3を付与しないよう、test contract riskとchange classの境界を限定する1 target改訂 | [`observed_n5`](../../evaluations/results/candidate3-expanded12-global-m24-n5_2026-07-15.md) |
| `the-caption-3ce91a4-executor-discretion-r1` | `the-caption-3ce91a4-sa-routing-test-boundary-r1` | C3のAudit / Review routingを維持し、専用実装SAと必須委任を除去して実装主体をモデル判断へ戻す6 target改訂 | [`observed_n5`](../../evaluations/results/candidate4-expanded12-global-m24-n5_2026-07-15.md) |
| `the-caption-3ce91a4-completion-persistence-r1` | `the-caption-3ce91a4-executor-discretion-r1` | C4の実装主体判断とroutingを維持し、実行開始後の停止を明示済み条件と観測事実へ限定する3 target改訂 | [`observed_n5`](../../evaluations/results/candidate5-expanded12-global-m24-n5_2026-07-16.md) |
| `the-caption-3ce91a4-context-efficiency-r1` | `the-caption-3ce91a4-completion-persistence-r1` | C5の完了志向・実装主体判断・routingを維持し、JIT節参照、SA packet最小化、結果再掲抑制を加える3 target改訂 | [`observed_n5`](../../evaluations/results/candidate6-expanded12-global-m24-n5_2026-07-16.md) |
| `the-caption-3ce91a4-command-evidence-projection-r1` | `the-caption-3ce91a4-completion-persistence-r1` | C5の実装主体判断・完了志向・routingを維持し、required commandの完全evidence保存とmodel-visible outputを分離する3 target改訂 | [`observed_f02_n1`](../../docs/candidate6-candidate8-efficiency-investigation.md#candidate7とcandidate8のf02診断観測) |
| `the-caption-3ce91a4-phase-result-projection-r1` | `the-caption-3ce91a4-command-evidence-projection-r1` | C7のcommand単位projectionを工程間resultへ一般化し、次工程へchanged paths、scoped diff、validation summary、findings、unresolvedだけを渡す3 target改訂 | [`observed_f02_n1`](../../docs/candidate6-candidate8-efficiency-investigation.md#candidate7とcandidate8のf02診断観測) |
| `the-caption-9b3a96a-task-spec-default-precedence-r1` | `the-caption-9b3a96a-revision-2-r1` | C1のcompact構造を維持し、invariant・TaskSpec明示値・change-class defaultの優先順位と解決済み契約のworker bindingを固定する3 target改訂 | [`observed_n5`](../../evaluations/results/candidate9-expanded12-global-m24-n5_2026-07-16.md) |
| `the-caption-9b3a96a-counter-resolution-boundary-r1` | `the-caption-9b3a96a-task-spec-default-precedence-r1` | C9のauthority解決を維持し、非適用を許す責務の`not_applicable`単独を停止理由にせず、applicableなcounterだけに数値domainを適用する1 target改訂 | [`observed_n5`](../../evaluations/results/candidate10-expanded12-global-m24-n5_2026-07-16.md) |

candidate bundleのmanifestは構築時provenanceとしてimmutableに保持する。評価状態の更新はmanifestをin-place変更せず、このindexと独立したevaluation resultで表す。
