# Candidate71 / Candidate77 triggered exception transition 第12版採点 標準14項目 各5回

## 結論

Candidate77を第12版採点、標準14項目、各`N=5`、global queue `M=24`で実行した。70 / 70件がvalidかつrateableで、score分布は`4 = 70`だった。excluded attempt、workspace failure、command protocol違反、required outcome failureは0件である。

Candidate77の5反復中央値は`quality_score = 100.000`、all-agent `total_tokens = 2,631,001`、`elapsed_seconds = 1,228.933秒`だった。70 run合計は`13,328,833 tokens`、`6,048.242秒`である。

互換なCandidate71 Batch 1をreferenceにした保存result比較では、Candidate77 - Candidate71の中央値差は`quality_score = 0.000`、`total_tokens = +512,032`（`+24.16%`）、`elapsed_seconds = +185.475秒`（`+17.77%`）だった。70 run合計差はtokenが`+2,907,665`（`+27.90%`）、elapsedが`+867.748秒`（`+16.75%`）である。

Candidate76との非対称な参考比較では、Candidate77はscore `3`の1件を解消し、token中央値を`270,381`（`9.32%`）減らした。一方、Candidate71の品質を維持した最短経路よりtokenとelapsedが増えている。例外仕様を条件付きreadへ移しただけでは通常経路への追加costを解消できなかったため、Candidate77を`stopped`とする。採用、release、THE-CAPTION本体反映には進めない。

## 固定条件

- evaluation set: `the-caption-standard14-r1` revision `r1`
- profile: `candidate77-triggered-exception-transition-v12-standard14-global-m24-n5-r1`
- quality rating: `outcome-semantic-evidence-normalized-owner-diagnostic-v12`
- model: `gpt-5.6-sol`
- agent environment: Codex CLI `0.144.0`、Python `3.14.5`、memories `false`
- permission: `workspace-write / never`
- schedule: global queue、`M=24`
- repetition: 14 case × `N=5` = 70 slot
- token accounting: all-agent `v1`
- Candidate77 identity: `the-caption-3ce91a4-triggered-exception-transition-r1`
- Candidate77 bundle SHA-256: `665822f8c99fd1052368d362765bdaa37dc12f34434bcac17db135f5de6ef644`
- compatibility key: `d975daefc55ae9914230e5d0fbf03f2f5325ab9f30e3d79f30a4239c7f7b0c78`

## 保存result

- Candidate77 result id: `748d799b3700433a9c8eac3870bd9439`
- Candidate71 Batch 1 reference result id: `a5ef7fb7a36a43fd8f40c6fa6182a63c`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate77-triggered-exception-transition-v12-standard14-global-m24-n5-20260723-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- final compact receipt: `batch-001/compact/final-compact-receipt.json`
- comparison view: `comparison-c71-c77.json`

## 反復別KPI

| Iteration | quality_score | all-agent total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 2,540,620 | 1,228.933秒 |
| 2 | 100.000 | 2,502,805 | 1,161.809秒 |
| 3 | 100.000 | 2,631,001 | 1,179.298秒 |
| 4 | 100.000 | 2,852,531 | 1,233.563秒 |
| 5 | 100.000 | 2,801,876 | 1,244.637秒 |
| 中央値 | 100.000 | 2,631,001 | 1,228.933秒 |

## case別結果

全caseが5 / 5でscore `4`だった。tokenとelapsedの差はCandidate77 - Candidate71 Batch 1のcase別中央値である。

| Case | score分布 | C77 token中央値 | token差 | C77 elapsed中央値 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 latent mode policy | `4 = 5` | 134,214 | `+58.73%` | 47.231秒 | `+23.40%` |
| A02 repository resolvable routing | `4 = 5` | 389,730 | `+83.09%` | 129.665秒 | `+25.73%` |
| F01 duplicate asset key | `4 = 5` | 310,080 | `+68.80%` | 111.784秒 | `+36.14%` |
| F02 history date bound | `4 = 5` | 363,349 | `+32.62%` | 127.072秒 | `+26.18%` |
| F03 atomic context cleanup | `4 = 5` | 174,463 | `+7.92%` | 99.858秒 | `+14.13%` |
| F04 web audit visibility | `4 = 5` | 260,841 | `+15.15%` | 103.220秒 | `-2.51%` |
| F05 clarify units mode | `4 = 5` | 32,226 | `+1.72%` | 18.362秒 | `+0.74%` |
| F05 out-of-scope deploy | `4 = 5` | 54,900 | `+68.55%` | 39.910秒 | `+66.69%` |
| F06 restore snapshot contract | `4 = 5` | 198,553 | `+23.00%` | 104.959秒 | `+10.75%` |
| F07 canonical V4 runner | `4 = 5` | 348,992 | `+99.98%` | 121.872秒 | `+30.22%` |
| F07 dependency provenance | `4 = 5` | 87,993 | `+1.48%` | 52.739秒 | `-5.76%` |
| F08 CLI reference sync | `4 = 5` | 143,642 | `-14.66%` | 93.186秒 | `+17.70%` |
| F10 entrypoint review | `4 = 5` | 117,696 | `+0.04%` | 81.730秒 | `-2.94%` |
| F10 monthly review | `4 = 5` | 88,798 | `+4.14%` | 62.219秒 | `+22.77%` |

## 診断

- quality audit failure count: 0
- command protocol violation: 0
- workspace failure: 0
- excluded attempt / retry: 0 / 0
- F10 Monthly numeric location: exact 5。数値座標差はなかった。
- owner-producer evidence inadmissible: 55。Candidate71 Batch 1と同数で、現profileでは`diagnostic_only`のためquality KPIへ入力しない。
- root `AGENTS.md`はCandidate71の`4,987 byte`から`6,478 byte`へ増えた。trigger分類と参照命令はroot promptにあるため、毎runのmodel-visible入力になる。これがcost増の一因である可能性はあるが、standard14 resultだけではcaseごとの因果を確定できない。
- case別token中央値がCandidate71以下だったのはF08だけである。非trigger想定のF10 Entryはほぼ同値、F10 Monthlyは`+4.14%`だったが、標準14全体ではA01、A02、F01、F02、F07 canonical、out-of-scope deployの増加を相殺できなかった。

## 判定境界

今回はユーザーの明示指示によりstandard14を直接実行した。Candidate作成前gateで予定したtargeted behavior traceを先に実行していないため、triggerなしの例外仕様readが0件だったことや、trigger時に対応節だけを読んだことは証明していない。standard14のscore `4 = 70`を、例外transitionの適用構造全体のruntime証明へ読み替えない。

今回の事実から言えるのは、品質制御はC71水準へ回復したが、通常構造維持による効率回復はC71水準へ届かなかったことである。KPIの優先順位や閾値を評価基盤へ追加せず、Candidate77は履歴として保持する。
