# Candidate39 owner-aligned result unit targeted N=5

## 結論

Candidate39をF05 clarificationとF10 monthly reviewで各5回実行した。成果内容は10 / 10で満たしたが、F05 iteration 3は独立owner workerを起動せずrootが直接clarificationを返したため、owner-producer evidence不成立でscore `3`となった。score分布は`4 / 3 = 9 / 1`である。

Candidate38のPRODUCER規則を、criterion ownerと同一role identityへ固定しても、独立owner経路の欠落は解消しなかった。したがって、同じ原因に対する追加のprompt文言変更とexpanded 12-case試験には進めない。

採用、release承認、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1`
- case / iteration: 2 case × `1..5`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model: `gpt-5.6-sol`、reasoning effort `high`
- executor: global queue `M=10`
- quality rating: `owner-producer-quality-v8`
- compatibility key: `4fc262a28717c6ded71d250d4d172e404fdb1acb51ae98b4d420e51d1d0e85fb`

## 観測結果

| case | score 4 | score 3 | 内容要件を満たしたrun |
| --- | ---: | ---: | ---: |
| `TC-F05-CLARIFY-UNITS-MODE` | 4 | 1 | 5 / 5 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 5 | 0 | 5 / 5 |

F05 iteration 3のrun `a7d749f507a8476dba560a571d26e602`はchild sessionを起動しなかった。rootは開始identityを確認した後、`daily` / `strict`の選択とstrict時のlive CSV fallback policyを確認する正しいclarificationを直接返した。成果内容、no-drift、single terminal outcomeは成立したが、TaskSpecが指定する`owner=independent boundary check`のproducer evidenceは成立しなかった。

このrunは`33,886 tokens`、`18.810 seconds`であり、独立workerを実行した他runより短い。したがって、Candidate39のKPI低下をprompt効率の改善と解釈しない。

## 互換resultとの数値差

| KPI | Candidate37 | Candidate38 | Candidate39 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 100.000 |
| median `total_tokens` | 526,440 | 490,181 | 454,683 |
| median `elapsed_seconds` | 265.577 | 263.048 | 235.722 |
| 10 run token合計 | 2,484,749 | 2,560,283 | 2,256,683 |
| score `4` | 10 | 9 | 9 |

Candidate39のprompt本体はCandidate35比で`+59 bytes`、Candidate37比で`-907 bytes`である。静的sizeと実行時KPIの因果は、この10 runから断定しない。

## Evidence boundary

- result ID: `3279bf9d495548f083085410959ab8d7`
- result content SHA-256: `d6e784633d374832ba04d22f1e52792db19605056556a3988ddf7b844847212b`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate39-owner-aligned-result-unit-owner-producer-v8-targeted2-global-m10-n5-20260718-r1`
- valid / rateable run: 10 / 10
- retry / excluded attempt: 0 / 0
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。

