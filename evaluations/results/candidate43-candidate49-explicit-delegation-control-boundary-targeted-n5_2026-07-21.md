# Candidate43 / Candidate49 明示委譲制御境界 対象試験 N=5

## 結論

Candidate49はCandidate43のroot `AGENTS.md`を`3,980 → 2,423 bytes`へ39.12%縮小した。A01 / A02とF05 / F10の20件はすべて有効かつ採点可能で、Candidate49は20 / 20件がscore `4`だった。

一方、all-agent `total_tokens`は減らなかった。互換条件を揃えたCandidate43比で、A01 / A02の10件合計は`+167,205`、F05 / F10の10件合計は`+258,556`だった。20件合計では`3,222,367 → 3,648,128`、`+425,761`、`+13.21%`である。

workerは両候補の全20件で0だった。増加の中心はroot input tokenである。特にF10はcommand数が両候補とも50で、Candidate49の入力だけが`689,536 → 945,707`へ増えた。prompt byte数の縮小を実行token削減とみなせない。

Candidate49は事前停止条件の「実行量を減らさずtokenだけが移る」に該当する。A03 / F07、標準14項目、A06へは進めない。Candidate49は`draft / targeted_evaluated / stopped`として保持し、採用、release、本体反映は行わない。

## Prompt差分

- Candidate43: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate49: `the-caption-3ce91a4-explicit-delegation-control-boundary-r1`
- Candidate49 bundle SHA-256: `93c7e9c4a905d79ecd374ae102da0b66abf48e479369aa5d832b659698995187`
- changed target: root `AGENTS.md`だけ
- 未変更target: 18 / 18がCandidate43とbit identity一致
- root prompt: `3,980 → 2,423 bytes`、`199 → 120 words`

Candidate49はCandidate43の`SPEC`、`METHOD`、`RECOVERY`を同一に保った。worker固有の6 labelを、明示された独立producer executionだけへ適用する`DELEGATION`、`CONTEXT`、`COMPLETION`へ置換した。

## A01 / A02 第10版

### 固定条件

- Evaluation set: `the-caption-ambiguity-boundaries-r1`第2版
- Evaluation set identity: `9814b0a53807151e8d4a4f2bf5d089a765e0c9efc66888f77d22616fc98dd8b5`
- case / iteration: A01、A02 × `1..5`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent環境: `agents.max_threads=4`、`memories=false`
- executor: global queue `M=10`
- quality rating: `outcome-boundary-owner-diagnostic-v10`
- compatibility key: `5dec788f14511cfec8d3fbb2a4ff221a5f55400388c4ca0d48541d1ed680e96c`
- token accounting: all-agent `v1`

以前のCandidate43保存結果は、内容が同じfixtureに異なるfile modeが入り、fixture identityが今回と一致しなかった。その結果は変更せず、現行file modeでCandidate43を再実行した。以下はprompt identity以外の互換条件が一致する2結果だけを比較する。

### KPI

差分方向はCandidate49 - Candidate43である。

| KPI | Candidate43 | Candidate49 | 差 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 452,340 | 488,436 | +36,096 (+7.98%) |
| median `elapsed_seconds` | 141.075 | 142.628 | +1.553 (+1.10%) |
| 10 run token合計 | 2,171,599 | 2,338,804 | +167,205 (+7.70%) |
| score `4` | 9 | 10 | +1 |
| score `1` | 1 | 0 | -1 |

Candidate43のscore `1`は、変更とtestを行わず「変更先を明示してください」と返したA01の1件を固定auditが`a01_clarification_disposition_missing`としたものである。意味上の品質差へ一般化しない。

### 項目別

| case | C43 token合計 | C49 token合計 | 合計差 | C43中央値 | C49中央値 | 中央値差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | 512,593 | 569,720 | +57,127 (+11.14%) | 100,779 | 137,338 | +36,559 (+36.28%) |
| A02 | 1,659,006 | 1,769,084 | +110,078 (+6.64%) | 328,954 | 351,098 | +22,144 (+6.73%) |

両候補とも10 session、child session 0だった。attempted commandはCandidate43が60、Candidate49が81だった。最終response文字数の10件合計は`3,895 → 3,852`で、Candidate49が43文字少なかった。

## F05 / F10 第9版

### 固定条件

- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1`
- Evaluation set identity: `1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90`
- case / iteration: F05 clarification、F10 monthly review × `1..5`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent環境: `agents.max_threads=4`、`memories=false`
- executor: global queue `M=10`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- compatibility key: `937499798438d2a3d9125c0887257badf7f21d460ba3fb6e923fefb2822570c1`
- token accounting: all-agent `v1`

### KPI

| KPI | Candidate43 | Candidate49 | 差 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 178,705 | 294,543 | +115,838 (+64.82%) |
| median `elapsed_seconds` | 86.902 | 118.549 | +31.647 (+36.42%) |
| 10 run token合計 | 1,050,768 | 1,309,324 | +258,556 (+24.61%) |
| score `4` | 10 | 10 | 0 |

### 項目別

| case | C43 token合計 | C49 token合計 | 合計差 | C43中央値 | C49中央値 | 中央値差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F05 | 348,448 | 348,501 | +53 (+0.02%) | 79,272 | 77,730 | -1,542 (-1.95%) |
| F10 | 702,320 | 960,823 | +258,503 (+36.81%) | 98,938 | 216,529 | +117,591 (+118.85%) |

両候補とも10 session、child session 0、attempted command 70だった。F10のcommandは両候補とも50で、参照したroot / `src` authority、固定diff、`monthly_main.py`、`monthly_engine.py`も同じだった。

F10のtoken差`+258,503`のうちinput token差は`+256,171`で99.10%を占めた。最終response文字数の中央値は`591 → 574`で17文字減ったが、Candidate49の1件が絶対pathを含む1,480文字になり、5件合計は`2,948 → 3,737`へ増えた。

## 停止判定

| 事前条件 | 観測 | 判定 |
| --- | --- | --- |
| A01 / A02の禁止境界を保つ | Candidate49は10 / 10 score `4` | 非該当 |
| F05 / F10のrequired responseを失う | Candidate49は10 / 10 score `4` | 非該当 |
| root-only taskで不要なworkerを起動する | 全20件でchild 0 | 非該当 |
| prompt縮小だけを効率化と判断する | bytesは-39.12%、20件tokenは+13.21% | 該当 |
| 実行量を減らさずtokenだけが移る | F10 command同数、input token +37.15% | 該当 |

この停止はCandidate43を採用済みと判断するものではない。Candidate49の変更単位が、今回の対象試験でtokenと説明を同時に減らす根拠にならなかったことだけを示す。

## Evidence

### A01 / A02

- Candidate43 result: `22aae215470a4d2eab9332e5d3a90ab4`
- Candidate43 content SHA-256: `31ad433399c89e7155834a586ae0a6e11105e567006b1ece81f55d8f8591fd28`
- Candidate49 result: `601829e07c814f5f8186cc405bf21787`
- Candidate49 content SHA-256: `7c0e0e9591216ce1e0b020b802f342aa42875dc884fe7a86cbd32637a11eb4ce`
- comparison: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate43-candidate49-ambiguity-v10-20260721-r1/candidate49-minus-candidate43.json`

### F05 / F10

- Candidate43 result: `40103b0900de4f40bfdf5a74c83126ff`
- Candidate43 content SHA-256: `c203251e34a2d485619a96d5303e169572291835c1a7e06cbe7a874cb8224614`
- Candidate49 result: `61e189fce2634677a405bb61b3c760ca`
- Candidate49 content SHA-256: `29fe965196c15b51cf397775f2221bfc80256fab9b881fce297522e3ddf8f312`
- comparison: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate43-candidate49-outcome-v9-20260721-r1/candidate49-minus-candidate43.json`

4 campaignはすべてvalid 10 / 10、retry 0、excluded attempt 0である。quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。非公開raw run log、session情報、一時workspaceはrepositoryへ保存しない。
