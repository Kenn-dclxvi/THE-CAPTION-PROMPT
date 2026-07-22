# Candidate43 / Candidate50 root read batch 対象試験 N=5

## 結論

Candidate50はF05 / F10の逐次model stepを減らした。F05 / F10の10 run合計はCandidate43の`1,050,768`から`629,619` tokenへ減り、差は`-421,149`、`-40.08%`だった。F10のmodel stepは`37 → 22`、input tokenは`689,536 → 444,727`となった。

一方、A01 / A02では探索が広がった。10 run合計は`2,171,599 → 2,512,469` token、差は`+340,870`、`+15.70%`だった。A02のcommandは`38 → 84`、model stepは`48 → 54`となった。

20 run全体は`3,222,367 → 3,142,088` token、`-80,279`、`-2.49%`だった。ただし、F項目の減少がA項目の増加を相殺した値である。root prompt自体も`3,980 → 4,458 bytes`、`+12.01%`になった。対象に依存せず説明とtokenを減らす制御とは判断しない。

Candidate50は事前停止条件の「A02の探索が拡大したままtokenが増える」に該当する。`draft / targeted_evaluated / stopped`として保持し、A03 / F07、標準14項目、A06、採用、release、本体反映へ進めない。

## Prompt差分

- Candidate43: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate50: `the-caption-3ce91a4-root-read-batch-r1`
- Candidate50 bundle SHA-256: `7ba948d567e465cf0e8b6628ca0037e8cc1dae6790901afe0c26aab1c61fc220`
- changed target: root `AGENTS.md`だけ
- 未変更target: 18 / 18がCandidate43とbit identity一致
- root prompt: `3,980 → 4,458 bytes`、`199 → 212 words`

Candidate50はCandidate43の既存9 labelを変更せず、`ROOT_BATCH`を一つ追加した。対象は、`spec_ready=true`後にrootがproducerとなり、順序依存がないread-only predicateだけである。write、test、dependency操作はbatch対象外とした。

## 初回runの除外

最初に作成したCandidate50 campaignは、現行case materializationからLayer 1を再生成した。そのfixture file modeは`0644`だった。比較対象のCandidate43 / Candidate49は`0600`であり、内容が同じでもfixture digestとEvaluation set identityが一致しなかった。

- A01 / A02初回set identity: `69e5bedfa1d20fe458bb0b59cdab368f9dfb50351532383248411d4138cd72f0`
- F05 / F10初回set identity: `4564c49730ab0d135bb2a1ff5530d02f49f71808e4ee2c2c4405beca99a1cca7`
- A01 / A02初回result: `f437748aee534e7883854b0019c4ed18`
- F05 / F10初回result: `1a7a4feeea5c4c3d843526a1e096d685`

初回resultはvalid 10 / 10、score `4` 10 / 10だが、Candidate43との互換比較へ使わない。追記専用resultとして変更せず保持する。

互換runはCandidate43の固定済みLayer 1をcopyして準備した。A01 / A02のset identityは`9814b0a53807151e8d4a4f2bf5d089a765e0c9efc66888f77d22616fc98dd8b5`、F05 / F10は`1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90`でCandidate43と一致した。

## A01 / A02 第10版

### 固定条件

- Evaluation set: `the-caption-ambiguity-boundaries-r1`第2版
- case / iteration: A01、A02 × `1..5`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent環境: `agents.max_threads=4`、`memories=false`
- executor: global queue `M=10`
- quality rating: `outcome-boundary-owner-diagnostic-v10`
- compatibility key: `5dec788f14511cfec8d3fbb2a4ff221a5f55400388c4ca0d48541d1ed680e96c`
- token accounting: all-agent `v1`

### KPI

差分方向はCandidate50 - Candidate43である。

| KPI | Candidate43 | Candidate50 | 差 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 452,340 | 494,692 | +42,352 (+9.36%) |
| median `elapsed_seconds` | 141.075 | 171.278 | +30.203 (+21.41%) |
| 10 run token合計 | 2,171,599 | 2,512,469 | +340,870 (+15.70%) |
| score `4` | 9 | 10 | +1 |
| score `1` | 1 | 0 | -1 |

Candidate43のscore `1`はA01の1件で、編集とtestを行わず「変更先を明示してください」と返したresponseを固定auditが`a01_clarification_disposition_missing`としたものである。この1件から意味上の品質差を一般化しない。

### case別token

| case | C43 token合計 | C50 token合計 | 合計差 | C43中央値 | C50中央値 | 中央値差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | 512,593 | 631,410 | +118,817 (+23.18%) | 100,779 | 135,047 | +34,268 (+34.00%) |
| A02 | 1,659,006 | 1,881,059 | +222,053 (+13.38%) | 328,954 | 373,669 | +44,715 (+13.59%) |

### raw execution

| case | 指標 | Candidate43 | Candidate50 | 差 |
| --- | --- | ---: | ---: | ---: |
| A01 | model step | 25 | 27 | +2 |
| A01 | tool call | 20 | 22 | +2 |
| A01 | command | 22 | 49 | +27 |
| A01 | tool output文字数 | 188,879 | 250,260 | +61,381 (+32.50%) |
| A01 | input token | 505,162 | 619,847 | +114,685 (+22.70%) |
| A02 | model step | 48 | 54 | +6 |
| A02 | tool call | 43 | 49 | +6 |
| A02 | command | 38 | 84 | +46 |
| A02 | tool output文字数 | 1,353,973 | 1,245,390 | -108,583 (-8.02%) |
| A02 | input token | 1,643,220 | 1,860,393 | +217,173 (+13.22%) |

A02のtool output文字数は減ったが、commandとmodel stepは増えた。Candidate50は開始identity、inventory、authority読取りを個別commandへ分離してbatchした一方、read対象自体は固定しない。そのため、`rg --files`、広域`rg`、tests / README / history読取りなどの探索集合がrunごとに広がった。

Candidate43は複数のreadを一つのshell commandへ結合するrunが多かった。Candidate50は個別exit evidenceを保つため分離した。この違いだけでcommand数を良否判定しないが、model stepとinput tokenも同時に増えたため、A02でcontext再送を減らしたとはいえない。

## F05 / F10 第9版

### 固定条件

- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1`
- case / iteration: F05 clarification、F10 monthly review × `1..5`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent環境: `agents.max_threads=4`、`memories=false`
- executor: global queue `M=10`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- compatibility key: `937499798438d2a3d9125c0887257badf7f21d460ba3fb6e923fefb2822570c1`
- token accounting: all-agent `v1`

### KPI

| KPI | Candidate43 | Candidate50 | 差 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 178,705 | 119,529 | -59,176 (-33.11%) |
| median `elapsed_seconds` | 86.902 | 83.464 | -3.438 (-3.96%) |
| 10 run token合計 | 1,050,768 | 629,619 | -421,149 (-40.08%) |
| score `4` | 10 | 10 | 0 |

### case別token

| case | C43 token合計 | C50 token合計 | 合計差 | C43中央値 | C50中央値 | 中央値差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F05 | 348,448 | 172,759 | -175,689 (-50.42%) | 79,272 | 34,489 | -44,783 (-56.49%) |
| F10 | 702,320 | 456,860 | -245,460 (-34.95%) | 98,938 | 84,824 | -14,114 (-14.27%) |

### raw execution

| case | 指標 | Candidate43 | Candidate50 | 差 |
| --- | --- | ---: | ---: | ---: |
| F05 | model step | 22 | 10 | -12 |
| F05 | tool call | 17 | 5 | -12 |
| F05 | command | 20 | 20 | 0 |
| F05 | input token | 344,125 | 169,002 | -175,123 (-50.89%) |
| F10 | model step | 37 | 22 | -15 |
| F10 | tool call | 32 | 17 | -15 |
| F10 | command | 55 | 55 | 0 |
| F10 | tool output文字数 | 96,727 | 92,494 | -4,233 (-4.38%) |
| F10 | input token | 689,536 | 444,727 | -244,809 (-35.50%) |

F10のmodel stepはCandidate43の`12 / 5 / 12 / 4 / 4`からCandidate50の`4 / 5 / 4 / 5 / 4`へ収束した。command数を変えずにtool batchへまとめたため、今回狙った逐次context再送の削減はF10で観測できた。

## 停止判定

| 事前条件 | 観測 | 判定 |
| --- | --- | --- |
| F10のmodel stepまたはinput tokenが減らない | step `37 → 22`、input `689,536 → 444,727` | 非該当 |
| A02の探索が拡大したままtokenが増える | command `38 → 84`、step `48 → 54`、token `+13.38%` | 該当 |
| score `4`を失う | Candidate50は20 / 20 score `4` | 非該当 |
| required commandを一つのshellへ結合してexit evidenceを失う | F05 / F10のcommand数は同一、protocol違反0件 | 非該当 |
| read-only以外をbatchする | 複数`exec_command` batchへwrite / testを含めたrunは0件 | 非該当 |

`ROOT_BATCH`は固定されたread集合のreviewには有効だった。しかし、探索型taskではread集合を広げる余地と個別command化のcostを残した。20 run総量の小さな減少だけで標準14項目へ展開しない。別のprompt圧縮や委譲制御をCandidate50へ継ぎ足さない。

## Evidence

### A01 / A02

- Candidate43 result: `22aae215470a4d2eab9332e5d3a90ab4`
- Candidate43 content SHA-256: `31ad433399c89e7155834a586ae0a6e11105e567006b1ece81f55d8f8591fd28`
- Candidate50 result: `0cc5c41040bf432da9b1f64ebdf6354e`
- Candidate50 content SHA-256: `67f61adf763a6b6080eca47bd86240ba230030a6ecb26880a4df512108f488fc`
- comparison: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate43-candidate50-ambiguity-v10-20260721-r1/candidate50-minus-candidate43.json`

### F05 / F10

- Candidate43 result: `40103b0900de4f40bfdf5a74c83126ff`
- Candidate43 content SHA-256: `c203251e34a2d485619a96d5303e169572291835c1a7e06cbe7a874cb8224614`
- Candidate50 result: `229797dea0af4f90be33b3fec3a49ab6`
- Candidate50 content SHA-256: `df32973c50973bbea4fba6a4a76533bf966dcf4bb8e9a551a177c12b7b888722`
- comparison: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate43-candidate50-outcome-v9-20260721-r1/candidate50-minus-candidate43.json`

互換r2の2 campaignはvalid 10 / 10、retry 0、excluded attempt 0である。Candidate50の20 runはすべてroot session 1、child token 0だった。quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。非公開raw run log、session情報、一時workspaceはrepositoryへ保存しない。
