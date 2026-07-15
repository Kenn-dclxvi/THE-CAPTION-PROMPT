# Candidates

構築中の候補プロンプトをrevision別に置く。各candidateは解く問題、対象範囲、baseline identity、変更理由、非目標、評価状態を記録する。

| prompt identity | baseline | 変更 | 状態 |
| --- | --- | --- | --- |
| `the-caption-3ce91a4-current-copy-r1` | `the-caption-3ce91a4-current-r1` | 変更なし。null calibration用のbit-identical copy | `not_evaluated` |
| `the-caption-9b3a96a-revision-2-r1` | `the-caption-3ce91a4-current-r2` | 単一root authorityとconditional audit / reviewを含む10 target改訂 | [`observed_n5`](../../evaluations/results/candidate1-expanded12-global-m24-n5_2026-07-15.md) |
| `the-caption-3ce91a4-sa-routing-r1` | `the-caption-3ce91a4-current-r2` | 実装SA routingを維持し、riskとmachine coverageで実装後のaudit / review SAを選ぶ3 target改訂 | [`observed_n5`](../../evaluations/results/candidate2-expanded12-global-m24-n5_2026-07-15.md) |
| `the-caption-3ce91a4-sa-routing-test-boundary-r1` | `the-caption-3ce91a4-sa-routing-r1` | validationでtestを使うだけのtaskへC3を付与しないよう、test contract riskとchange classの境界を限定する1 target改訂 | [`observed_n5`](../../evaluations/results/candidate3-expanded12-global-m24-n5_2026-07-15.md) |

candidate bundleのmanifestは構築時provenanceとしてimmutableに保持する。評価状態の更新はmanifestをin-place変更せず、このindexと独立したevaluation resultで表す。
