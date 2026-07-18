# Candidate40 operation / result projection boundary targeted N=5

## 結論

Candidate40をF05 clarificationとF10 monthly reviewで各5回、`outcome-quality-owner-diagnostic-v9`により実行した。score分布は`4 / 1 = 9 / 1`だった。F05は5 / 5、F10は4 / 5がscore `4`である。

Candidate40のoperation / result-unit境界は、Candidate38で観測したF10のtool turnを減らさなかった。F10のtool callはCandidate38の74からCandidate40の75へ、model stepは84から85へ増えた。F10 token合計も`+49,106`だった。

Candidate40の10 run token合計はCandidate38比`-179,036`だったが、減少はF05の実行経路差による。F10の実行分割抑制を示す証拠にはならない。

採用、release承認、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- prompt set: `the-caption-3ce91a4-operation-result-projection-boundary-r1`
- bundle SHA-256: `f527426d9ac1d4440ae3e051f204dee2dd1ca6e4f5befd15c6aa1296cabbef94`
- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1`
- Evaluation set identity: `4564c49730ab0d135bb2a1ff5530d02f49f71808e4ee2c2c4405beca99a1cca7`
- case / iteration: 2 case × `1..5`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model: `gpt-5.6-sol`、reasoning effort `high`
- executor: global queue `M=10`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- compatibility key: `5d4d7d7ba3aa2b120560a2f148585c40dea55574dca670adb161b2f9604837da`

## KPI

| KPI | Candidate35 | Candidate38 | Candidate40 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 100.000 |
| median `total_tokens` | 431,645 | 473,304 | 410,324 |
| median `elapsed_seconds` | 229.816 | 237.173 | 224.341 |
| 10 run token合計 | 2,073,880 | 2,329,647 | 2,150,611 |
| score `4` | 10 | 10 | 9 |
| score `1` | 0 | 0 | 1 |

中央値だけではCandidate40 iteration 2のquality低下を表さないため、score分布を併記する。

## F10実行経路

| F10の観測 | Candidate38 | Candidate40 | 差 |
| --- | ---: | ---: | ---: |
| token合計 | 1,612,424 | 1,661,530 | +49,106 |
| `exec` | 59 | 60 | +1 |
| `spawn_agent` | 5 | 5 | 0 |
| `wait_agent` | 10 | 9 | -1 |
| `list_agents` | 0 | 1 | +1 |
| tool call合計 | 74 | 75 | +1 |
| model step | 84 | 85 | +1 |

Candidate40でも、rootとchildがauthorityや開始identityを重複して読むrunがあった。result unitが固有operation / producer / predicate invocationを持たないと固定しても、producer operation内のevidence取得方法は`METHOD`によりexecutor所有である。そのため、境界だけではtool turn数を制御しなかった。

## Score 1 trace

F10 iteration 2のrun `26d3a8333424449ea94d31c634a0f0a8`では、child workerが正しいmajor finding、`monthly_main.py:25`、直接根拠、impactをterminal resultとして返した。

rootは事前task identityの`independent_response_check`とruntime pathの`/root/independent_response_check`を不一致と解釈し、worker resultを`unavailable`としてfinal responseから省略した。保存されたowner-producer collectorはこのworkerをeligibleと判定している。

このfailureは、意図したoperation / result-unit境界ではなく、既存OWNER identityの解釈差である。ただし、user-visible final responseから主要findingが欠落したため、outcome qualityのscore `1`は維持する。

## Owner診断

- F05 score `4`: 5 / 5
- F10 score `4`: 4 / 5
- owner-producer evidence eligible: 9 / 10
- F05 iteration 2はworkerを起動せずrootが正しいclarificationを直接返したため、owner診断だけが不成立だった。
- command protocol violation: 0

## Evidence boundary

- result ID: `2fab1a320e5947a6930066b253b6f4de`
- result content SHA-256: `596232993fe6e9f47ecb987ce8f77a037ad07a3b0c27f9245eedaae8cb753366`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/c35-c38-c40-outcome-quality-owner-diagnostic-v9-targeted2-n5-20260719-r1.json`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate40-operation-result-projection-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-20260719-r1`
- valid / rateable run: 10 / 10
- retry / excluded attempt: 0 / 0
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。

N=5の観測であり、評価範囲外へ一般化しない。

