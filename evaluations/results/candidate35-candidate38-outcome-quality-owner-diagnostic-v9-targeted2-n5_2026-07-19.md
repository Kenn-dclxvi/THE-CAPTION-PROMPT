# Candidate35 / Candidate38 outcome quality targeted N=5 comparison

## 結論

Candidate35とCandidate38を、F05 clarificationとF10 monthly reviewで各5回、新しい`outcome-quality-owner-diagnostic-v9`により実行した。両prompt setとも成果内容は10 / 10でscore `4`だった。owner-producer evidenceも両setとも10 / 10で成立した。

Candidate38 - Candidate35のKPI中央値差は、`quality_score = 0.000`、`total_tokens = +41,659`、`elapsed_seconds = +7.357`だった。10 runのtoken合計差は`+255,767`である。

採用、release承認、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1`
- Evaluation set identity: `4564c49730ab0d135bb2a1ff5530d02f49f71808e4ee2c2c4405beca99a1cca7`
- case / iteration: 2 case × `1..5`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model: `gpt-5.6-sol`、reasoning effort `high`
- executor: prompt set別global queue `M=10`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- compatibility key: `5d4d7d7ba3aa2b120560a2f148585c40dea55574dca670adb161b2f9604837da`

v9は成果、operation boundary、required validationを`quality_score`へ入れる。owner-producer evidenceは同じrunから収集し、Scoreへ影響しない診断として保存する。既存v8 resultは変更していない。

## KPI

差分方向はCandidate38 - Candidate35である。

| KPI | Candidate35 | Candidate38 | 差 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 431,645 | 473,304 | +41,659 (+9.65%) |
| median `elapsed_seconds` | 229.816 | 237.173 | +7.357 (+3.20%) |
| 10 run token合計 | 2,073,880 | 2,329,647 | +255,767 (+12.33%) |
| score `4` | 10 | 10 | 0 |

## Case別観測

| case | Candidate35 score 4 | Candidate38 score 4 | C35 token中央値 | C38 token中央値 |
| --- | ---: | ---: | ---: | ---: |
| `TC-F05-CLARIFY-UNITS-MODE` | 5 / 5 | 5 / 5 | 140,609 | 139,408 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 5 / 5 | 5 / 5 | 276,336 | 314,573 |

F05のtoken中央値差は`-1,201`だった。F10のtoken中央値差は`+38,237`だった。今回の全体token差は主にF10で観測された。

## 診断

| 診断 | Candidate35 | Candidate38 |
| --- | ---: | ---: |
| owner-producer evidence eligible | 10 / 10 | 10 / 10 |
| owner-producer evidence inadmissible | 0 | 0 |
| command protocol violation | 5 | 0 |

Candidate35のprotocol violation 5件は、F10 iteration 5における非required commandの診断である。required validation不足、成果欠落、Score低下には結び付いていない。

両setでowner evidenceが全件成立したため、このN=5のScore分布はowner診断をScore gateから外したことによって変化していない。

## Evidence boundary

- Candidate35 result ID: `92cceedd0adf4a489f861fdc15d1566f`
- Candidate35 result content SHA-256: `0542c63ea3ee54a55f39ebff8950c93343f4acffc3fae4c0c34783d08a1de131`
- Candidate38 result ID: `dfad99c8843c431493132cac6cc2a054`
- Candidate38 result content SHA-256: `7339f5d4c88b9dd3ef5bfd30a690a014a1064d2424d8a5a83c62fde8fb5cda8b`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/c35-c38-outcome-quality-owner-diagnostic-v9-targeted2-n5-20260719-r1.json`
- Candidate35 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate35-root-control-only-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-20260719-r1`
- Candidate38 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate38-result-unit-evidence-binding-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-20260719-r1`
- 両campaignともvalid / rateable 10 / 10、retry / excluded 0 / 0である。
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。

N=5の観測であり、過去の低頻度failureが解消または不存在であることを保証しない。

token増加の実行経路分析は[`token trace analysis`](candidate35-candidate38-v9-targeted2-n5-token-trace-analysis_2026-07-19.md)へ分離した。
