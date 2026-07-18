# Candidate38 result-unit evidence binding targeted N=5

## 結論

Candidate38をF05 clarificationとF10 monthly reviewで各5回実行した。F05は5 / 5がscore `4`だった。F10のfinding内容とlocationも5 / 5で正しかったが、iteration 3はnon-root criterion ownerへroot producerをbindしてworkerを起動しなかったため、owner-producer evidence不成立でscore `3`となった。

Candidate38のresult unit制御は、C34 F05で観測したclarification省略とC35 F10で観測したlocation誤差を、この10 runでは再現させなかった。一方、既存PRODUCER先頭の`rootまたはworker`という選択肢と、OWNERのnon-root worker必須条件が競合して見える曖昧さが残った。

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
| `TC-F05-CLARIFY-UNITS-MODE` | 5 | 0 | 5 / 5 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 4 | 1 | 5 / 5 |

F10 iteration 3のrun `79ee8a50e3e242afb8c20ffd0b78dc19`は、`criterion owner = independent response check`と認識しながら`producer = root`を選んだ。child sessionは0件で、rootがreview predicateを実行した。findingはmajor、locationは`src/app/entrypoints/monthly_main.py:25`で正しかった。

## Candidate37 targeted resultとの数値差

両resultは同じcompatibility keyを持つ。差分方向は`Candidate38 - Candidate37`である。

| KPI | Candidate37 | Candidate38 | 差 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 526,440 | 490,181 | -36,259 (-6.89%) |
| median `elapsed_seconds` | 265.577 | 263.048 | -2.528 (-0.95%) |
| 10 run token合計 | 2,484,749 | 2,560,283 | +75,534 (+3.04%) |
| score `4` | 10 | 9 | -1 |

prompt本体はCandidate35比で`+41 bytes`、Candidate37比で`-925 bytes`である。静的sizeだけから実行時token差の原因は断定しない。

## Evidence boundary

- result ID: `325ffdf9e2234c42b391c71347a85ab1`
- result content SHA-256: `ac764a677139a0d83886be204ad4e31eb85cb6ea0657223ba8dd0c4391ba645e`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate38-result-unit-evidence-binding-owner-producer-v8-targeted2-global-m10-n5-20260718-r1`
- valid / rateable run: 10 / 10
- retry / excluded attempt: 0 / 0
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。

