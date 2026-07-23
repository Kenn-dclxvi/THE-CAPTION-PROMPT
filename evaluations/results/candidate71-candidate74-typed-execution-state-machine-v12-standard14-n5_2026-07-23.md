# Candidate71 / Candidate74 typed execution state machine 第12版採点 標準14項目 各5回

## 結論

Candidate74を第12版採点、標準14項目、各`N=5`、global queue `M=24`で実行した。70 / 70件がvalidかつrateableで、score分布は`4 = 70`だった。excluded attempt、workspace failure、command protocol違反、required outcome failureは0件である。

Candidate74の5反復中央値は`quality_score = 100.000`、all-agent `total_tokens = 3,366,548`、`elapsed_seconds = 1,140.329秒`だった。70 run合計は`16,812,026 tokens`、`5,823.466秒`である。

互換なCandidate71 Batch 1をreferenceにした保存result比較では、Candidate74 - Candidate71の中央値差は`quality_score = 0.000`、`total_tokens = +1,247,579`（`+58.88%`）、`elapsed_seconds = +96.870秒`（`+9.28%`）だった。70 run合計差はtokenが`+6,390,858`（`+61.33%`）、elapsedが`+642.972秒`（`+12.41%`）である。

品質維持は今回の70 runで確認した。一方、tokenとelapsedは一つの互換reference resultより増えた。Candidate74を`standard14_evaluated`とし、採用、release、THE-CAPTION本体反映には進めない。比較はCandidate74の1 resultとCandidate71の1 resultであり、反復範囲外へ一般化しない。

## 固定条件

- evaluation set: `the-caption-standard14-r1` revision `r1`
- profile: `candidate74-typed-execution-state-machine-v12-standard14-global-m24-n5-r1`
- quality rating: `outcome-semantic-evidence-normalized-owner-diagnostic-v12`
- model: `gpt-5.6-sol`
- agent environment: Codex CLI `0.144.0`、Python `3.14.5`、memories `false`
- permission: `workspace-write / never`
- schedule: global queue、`M=24`
- repetition: 14 case × `N=5` = 70 slot
- token accounting: all-agent `v1`
- Candidate74 identity: `the-caption-3ce91a4-typed-execution-state-machine-r1`
- Candidate74 bundle SHA-256: `934b51451c99ae5c0594a85edb6b8ee33bfdbf67746749a37a8489f6ef1d239f`
- compatibility key: `d975daefc55ae9914230e5d0fbf03f2f5325ab9f30e3d79f30a4239c7f7b0c78`

## 保存result

- Candidate74 result id: `a5c74ebb0e9640b89bff11aaeb903a59`
- Candidate71 Batch 1 reference result id: `a5ef7fb7a36a43fd8f40c6fa6182a63c`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate74-typed-execution-state-machine-v12-standard14-global-m24-n5-20260723-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- final compact receipt: `batch-001/compact/final-compact-receipt.json`
- comparison view: `candidate71-batch1-candidate74-comparison.json`

## 反復別KPI

| Iteration | quality_score | all-agent total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 3,231,290 | 1,117.428秒 |
| 2 | 100.000 | 3,560,838 | 1,136.487秒 |
| 3 | 100.000 | 3,366,548 | 1,155.207秒 |
| 4 | 100.000 | 3,548,678 | 1,274.015秒 |
| 5 | 100.000 | 3,104,672 | 1,140.329秒 |
| 中央値 | 100.000 | 3,366,548 | 1,140.329秒 |

## case別結果

全caseが5 / 5でscore `4`だった。tokenとelapsedの差はCandidate74 - Candidate71 Batch 1のcase別中央値である。

| Case | score分布 | C74 token中央値 | token差 | C74 elapsed中央値 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 latent mode policy | `4 = 5` | 91,560 | `+8.28%` | 35.147秒 | `-8.17%` |
| A02 repository resolvable routing | `4 = 5` | 389,096 | `+82.79%` | 118.284秒 | `+14.69%` |
| F01 duplicate asset key | `4 = 5` | 253,313 | `+37.90%` | 84.710秒 | `+3.17%` |
| F02 history date bound | `4 = 5` | 434,373 | `+58.54%` | 109.016秒 | `+8.25%` |
| F03 atomic context cleanup | `4 = 5` | 227,805 | `+40.92%` | 104.719秒 | `+19.68%` |
| F04 web audit visibility | `4 = 5` | 273,320 | `+20.66%` | 95.916秒 | `-9.41%` |
| F05 clarify units mode | `4 = 5` | 95,912 | `+202.73%` | 25.104秒 | `+37.72%` |
| F05 out-of-scope deploy | `4 = 5` | 38,953 | `+19.59%` | 24.016秒 | `+0.31%` |
| F06 restore snapshot contract | `4 = 5` | 418,290 | `+159.11%` | 109.814秒 | `+15.88%` |
| F07 canonical V4 runner | `4 = 5` | 400,625 | `+129.57%` | 120.656秒 | `+28.92%` |
| F07 dependency provenance | `4 = 5` | 124,249 | `+43.29%` | 65.490秒 | `+17.02%` |
| F08 CLI reference sync | `4 = 5` | 291,869 | `+73.41%` | 91.795秒 | `+15.94%` |
| F10 entrypoint review | `4 = 5` | 254,771 | `+116.54%` | 103.242秒 | `+22.60%` |
| F10 monthly review | `4 = 5` | 125,149 | `+46.76%` | 55.744秒 | `+10.00%` |

## 診断

- quality audit failure count: 0
- command protocol violation: 0
- workspace failure: 0
- excluded attempt / retry: 0 / 0
- F10 Monthly numeric location: exact 4、mismatch 1。第12版契約どおり数値座標差はdiagnosticでありqualityを下げない。
- owner-producer evidence inadmissible: 55。Candidate71 Batch 1も55件で同数だった。現profileでは`diagnostic_only`でありquality KPIへ入力せず、Candidate74固有の後退とは扱わない。

## 判定境界

今回確認したのはstandard14に対する成果品質と3 KPIである。修正指示書の受入シナリオA〜Qを専用runtime caseとして網羅した試験ではない。構造testの成功とstandard14のscore `4`を、状態機械全体のruntime採用証明へ読み替えない。

KPIの優先順位や閾値は評価基盤へ追加していない。Candidate74の採用、release承認、runtime projectionは未実施である。
