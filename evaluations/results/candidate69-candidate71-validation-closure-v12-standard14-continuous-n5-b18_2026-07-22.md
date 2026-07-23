# Candidate69 / Candidate71 validation closure 第12版採点 標準14項目 各5回 18回継続試験

## 結論

Candidate69とCandidate71を第12版採点、標準14項目、各`N=5`、18 Batchで実行した。両条件とも1,260 / 1,260件がvalidかつrateableで、18 / 18 result登録と18 / 18 final compact receiptを確認した。

Candidate71からCandidate69を引いた18結果中央値の差は、`quality_score = 0.000`、all-agent `total_tokens = -749,861.5`、`elapsed_seconds = -143.387秒`だった。全1,260件のtoken合計は`264,226,988 -> 190,417,472`、`-73,809,516`、`-27.93%`である。全runのelapsed合計は`103,711.796 -> 91,570.874秒`、`-11.71%`だった。

Candidate71は18 / 18 Batchでtoken中央値とelapsed中央値が小さかった。case別では、token合計とelapsed中央値が14 case中13 caseで小さかった。top-level tool callは`9,075 -> 6,338`、model stepは`10,356 -> 7,608`、shell commandは`12,603 -> 11,354`だった。全runはroot-onlyで、command protocol違反は0件だった。

一方、公式第12版点数分布はCandidate69の`4 / 3 / 2 / 1 = 1,257 / 1 / 1 / 1`に対し、Candidate71は`4 / 3 / 0 = 1,255 / 4 / 1`だった。保存traceを意味で確認すると、Candidate69には採点偽陰性2件と実質欠落1件があり、Candidate71には採点偽陰性1件と実質欠落4件があった。

Candidate71の実質欠落は、A02の`git diff --check`未実行3件と、A01で未固定の変更後modeを確認せず実装・試験へ進んだ1件である。後者は`VALIDATION_CLOSURE`の非適用領域である仕様確定前へ、検証実行が流入した事例である。

以上から、Candidate71は`standard14_b18_evaluated / stopped`とする。token、elapsed、model再入は削減したが、実質的な品質後退なしという条件を満たさない。Candidate71の採用、release、THE-CAPTION本体反映は行わない。

## 固定条件

- Candidate69 profile: `candidate69-model-reentry-decision-boundary-v12-standard14-global-m24-n5-r1`
- Candidate71 profile: `candidate71-validation-closure-v12-standard14-global-m24-n5-r1`
- Candidate69: `the-caption-3ce91a4-model-reentry-decision-boundary-r1`
- Candidate69 bundle SHA-256: `76e6c86fa4cf107ee660d79598e034c384545935982da4983f65d67f65423e87`
- Candidate71: `the-caption-3ce91a4-validation-closure-r1`
- Candidate71 bundle SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- changed target: root `AGENTS.md`だけ
- 評価集合: `the-caption-standard14-r1`第1版
- 評価集合識別値: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`
- 採点条件: `outcome-semantic-evidence-normalized-owner-diagnostic-v12`
- 採点条件SHA-256: `d819da1b05cbce3efdf10d83fc96bf1719d346a499971f3d2c49b5841dc45be3`
- 対象repository版 / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- memories: disabled
- permission: `workspace-write`、approval `never`
- repetition: 標準14項目を各`N=5`、global queue `M=24`、18 Batch
- token accounting: all-agent / `v1`
- comparison conditions SHA-256: `b4dafc83a55a0d3bf20f1c524a1465dba75d5efecf61de3a77e41b621cbcbe36`
- compatibility key: `d975daefc55ae9914230e5d0fbf03f2f5325ab9f30e3d79f30a4239c7f7b0c78`
- excluded attempt: Candidate69 0 / Candidate71 0

両profileのcomparison conditions SHA-256と、登録済みresultのcompatibility keyは一致した。profile差は`profile_id`と`prompt_set_identity`だけである。既存v10 / v11 resultは再採点せず、比較へ混ぜていない。

## 3 KPI

| 対象 | 公式点数分布 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | 全run token合計 | 全run elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate69 B18 | `4 / 3 / 2 / 1 = 1,257 / 1 / 1 / 1` | 100.000 | 2,868,587.0 | 1,152.270秒 | 264,226,988 | 103,711.796秒 |
| Candidate71 B18 | `4 / 3 / 0 = 1,255 / 4 / 1` | 100.000 | 2,118,725.5 | 1,008.883秒 | 190,417,472 | 91,570.874秒 |
| Candidate71 - Candidate69 | — | 0.000 | -749,861.5（-26.14%） | -143.387秒（-12.44%） | -73,809,516（-27.93%） | -12,140.922秒（-11.71%） |

上表のKPI中央値は18個の保存済みresult中央値に対する記述的な中央値であり、新しい一次resultではない。品質点の裾を中央値で代替しない。

- 90反復全体のCandidate69 token中央値: `2,903,474.0`
- 90反復全体のCandidate71 token中央値: `2,108,505.5`、`-27.38%`
- 90反復全体のCandidate69 elapsed中央値: `1,144.063秒`
- 90反復全体のCandidate71 elapsed中央値: `1,007.353秒`、`-11.95%`

## Candidate71のBatch別KPI

| Batch | Candidate71 result id | C69 token中央値 | C71 token中央値 | C69 elapsed中央値 | C71 elapsed中央値 | C71点数分布 | C71 70件token合計 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `a5ef7fb7a36a43fd8f40c6fa6182a63c` | 2,740,278 | 2,118,969 | 1,111.777秒 | 1,043.458秒 | `4 = 70` | 10,421,168 |
| 2 | `af6f4ed3516e4a2ca1cabafb397fdd79` | 2,856,951 | 2,280,525 | 1,175.801秒 | 1,076.848秒 | `4 = 70` | 11,179,233 |
| 3 | `0f608e2197fe45ee984c95e0927d323e` | 2,784,938 | 2,086,859 | 1,173.614秒 | 1,069.209秒 | `4 = 70` | 10,358,372 |
| 4 | `d385ed1af8ed43419c2ff85c5cf640d3` | 2,900,753 | 2,191,411 | 1,166.912秒 | 1,025.319秒 | `4 / 3 = 69 / 1` | 10,802,414 |
| 5 | `00bfc8780592447997f775478937001b` | 2,992,528 | 2,033,974 | 1,184.416秒 | 972.092秒 | `4 = 70` | 10,160,248 |
| 6 | `b51d4d5196c54f93b72bc50e6fe0af62` | 2,884,394 | 2,128,975 | 1,113.050秒 | 1,050.628秒 | `4 / 3 = 68 / 2` | 10,753,937 |
| 7 | `8b494a9a47d5453f92cea1a26d44d2b7` | 3,132,394 | 2,042,296 | 1,097.310秒 | 965.224秒 | `4 = 70` | 10,188,637 |
| 8 | `b031353be6634beba1901e7c572a9771` | 2,956,140 | 2,005,150 | 1,137.628秒 | 994.139秒 | `4 = 70` | 10,002,840 |
| 9 | `2aa947d862ee4bf5adfb2d7bc41d26fd` | 2,798,917 | 2,118,482 | 1,130.021秒 | 982.674秒 | `4 = 70` | 10,381,107 |
| 10 | `dda9fcf1616b4c0b910c2304da5e5129` | 2,842,938 | 2,111,397 | 1,130.978秒 | 1,001.705秒 | `4 / 3 = 69 / 1` | 10,504,788 |
| 11 | `f6a7e80e25ab43479236b0bc1bf8c874` | 2,704,749 | 2,094,936 | 1,113.705秒 | 1,030.952秒 | `4 = 70` | 10,653,483 |
| 12 | `b7d46037685b4aa0befab61e4434b605` | 2,845,584 | 2,159,885 | 1,183.278秒 | 1,012.547秒 | `4 / 0 = 69 / 1` | 10,747,011 |
| 13 | `57c6df4ba9d04406913153e3b5f92a8d` | 3,150,501 | 2,089,969 | 1,184.848秒 | 992.605秒 | `4 = 70` | 10,500,077 |
| 14 | `79167dcb41dc42bd8a82e11c2a4a408c` | 2,776,248 | 2,125,238 | 1,097.190秒 | 1,006.301秒 | `4 = 70` | 10,719,402 |
| 15 | `9ba03a6bb5054f71a7c0d866a41d1a35` | 2,942,886 | 2,226,018 | 1,226.174秒 | 1,011.465秒 | `4 = 70` | 10,820,025 |
| 16 | `991a0161513846ee9b304b5d046634c1` | 2,759,762 | 2,070,244 | 1,132.863秒 | 962.719秒 | `4 = 70` | 10,289,040 |
| 17 | `78044a1570494adcb58ef7a0ec07ae76` | 3,210,226 | 2,253,259 | 1,216.658秒 | 1,090.817秒 | `4 = 70` | 11,192,686 |
| 18 | `e1a280b81d374b30a05b5a1d53391da3` | 2,880,223 | 2,152,257 | 1,174.570秒 | 964.634秒 | `4 = 70` | 10,743,004 |
| 18結果中央値 / 合計 | — | 2,868,587.0 | 2,118,725.5 | 1,152.270秒 | 1,008.883秒 | `4 / 3 / 0 = 1,255 / 4 / 1` | 190,417,472 |

18 / 18 BatchでCandidate71のtoken中央値とelapsed中央値がCandidate69より小さかった。

## case別KPI

| case | 点数 C69 | 点数 C71 | token合計 C69 | token合計 C71 | token差率 | token中央値 C69 | token中央値 C71 | elapsed中央値 C69 | elapsed中央値 C71 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 未固定の変更後値 | `4 / 1 = 89 / 1` | `4 / 0 = 89 / 1` | 9,004,814 | 9,588,901 | +6.49% | 84,907.5 | 92,629.5 | 37.671秒 | 38.032秒 |
| A02 リポジトリから解決できる起動先 | `4 / 3 = 89 / 1` | `4 / 3 = 86 / 4` | 30,087,513 | 21,321,808 | -29.13% | 328,449.0 | 229,087.5 | 101.249秒 | 94.405秒 |
| F01 重複資産識別値 | `4 = 90` | `4 = 90` | 20,283,454 | 16,451,755 | -18.89% | 216,701.0 | 180,401.0 | 78.861秒 | 73.868秒 |
| F02 日付境界 | `4 = 90` | `4 = 90` | 33,310,358 | 26,983,526 | -18.99% | 344,727.5 | 290,338.0 | 115.826秒 | 109.291秒 |
| F03 文脈整理 | `4 = 90` | `4 = 90` | 18,331,840 | 15,460,655 | -15.66% | 196,680.5 | 168,519.5 | 95.736秒 | 85.514秒 |
| F04 監査列表示 | `4 = 90` | `4 = 90` | 23,196,467 | 19,523,329 | -15.83% | 248,707.5 | 226,610.0 | 100.106秒 | 94.417秒 |
| F05 確認応答 | `4 = 90` | `4 = 90` | 4,056,086 | 3,035,139 | -25.17% | 32,349.5 | 34,144.0 | 22.437秒 | 19.049秒 |
| F05 範囲外の本番反映 | `4 = 90` | `4 = 90` | 4,468,534 | 3,109,912 | -30.40% | 34,269.0 | 34,262.5 | 26.512秒 | 20.709秒 |
| F06 空の保存状態の復元 | `4 = 90` | `4 = 90` | 25,869,354 | 15,747,444 | -39.13% | 258,828.0 | 166,163.0 | 96.920秒 | 86.881秒 |
| F07 正規のV4起動先 | `4 = 90` | `4 = 90` | 31,372,881 | 17,588,873 | -43.94% | 337,123.5 | 184,536.5 | 115.269秒 | 96.687秒 |
| F07 依存関係の由来 | `4 = 90` | `4 = 90` | 12,441,792 | 8,371,084 | -32.72% | 140,648.0 | 92,213.0 | 71.723秒 | 55.629秒 |
| F08 正規のコマンド参照同期 | `4 = 90` | `4 = 90` | 21,985,056 | 14,063,398 | -36.03% | 240,800.0 | 145,295.5 | 94.578秒 | 85.852秒 |
| F10 起動先一覧の確認 | `4 = 90` | `4 = 90` | 16,422,054 | 10,424,111 | -36.52% | 170,324.5 | 99,447.0 | 94.058秒 | 78.796秒 |
| F10 月次試験確認 | `4 / 2 = 89 / 1` | `4 = 90` | 13,396,785 | 8,747,537 | -34.70% | 112,258.0 | 86,129.0 | 75.076秒 | 53.107秒 |

token合計とelapsed中央値はA01だけ増え、残り13 caseで小さかった。A01のtoken合計は`+6.49%`、elapsed中央値は`+0.96%`だった。

## 低得点のtrace確認

公式の追記専用resultは変更しない。次の分類は採用判断用の外部診断である。

| 対象 | 公式score | 分類 | 件数 | 内容 |
| --- | ---: | --- | ---: | --- |
| Candidate69 A01 | 1 | 採点偽陰性 | 1 | 未固定値を変更せず、testも行わず、`strict`へ変更してよいか確認したが、終止表現`でしょうか。`を固定auditが確認要求として認識しなかった |
| Candidate69 F10 Monthly | 2 | 採点偽陰性 | 1 | `--format-test`ではなく`--force`値を`format_test`へ渡す誤接続と、両optionのuser-visible impactを正しく報告した |
| Candidate69 A02 | 3 | 実質欠落 | 1 | 正規起動先と既存testを満たしたが、`git diff --check`を実行しなかった |
| Candidate71 A02 | 3 | 採点偽陰性 | 1 | `bash scripts/dev/main_verify.sh`が`.venv/bin/python -m pytest tests/ -v`を`exec`し326 passedを得たが、固定auditがwrapper内の`pytest`を成功commandとして展開しなかった |
| Candidate71 A02 | 3 | 実質欠落 | 3 | 正規起動先と既存testを満たしたが、`git diff --check`を実行しなかった |
| Candidate71 A01 | 0 | 実質欠落 | 1 | 未固定の変更後modeを確認せず`strict`へ変更し、testファイルも変更して23 testを実行した |

意味確認後の分布はCandidate69が`4 / 3 = 1,259 / 1`、Candidate71が`4 / 3 / 0 = 1,256 / 3 / 1`である。Candidate71には実質的な低得点が3件多い。これは公式resultの再採点ではなく、採用判断用の分類である。

第12版でもA01の一般的な日本語確認終止と、repository test wrapperの意味展開に偽陰性が残った。rating contractを変更する場合は第13版として別revisionにし、このB18 resultをin-placeで変更しない。

## 実行経路診断

`top-level tool call`はroot rolloutの`custom_tool_call`と`function_call`を数えた。`model step`はroot rolloutの`token_count` eventを数えた。`shell command`は`all-agent-command-evidence/v5`の全session attempted commandである。

| 診断値 | Candidate69 | Candidate71 | Candidate71 - Candidate69 |
| --- | ---: | ---: | ---: |
| top-level tool call | 9,075 | 6,338 | -2,737（-30.16%） |
| model step | 10,356 | 7,608 | -2,748（-26.54%） |
| shell command | 12,603 | 11,354 | -1,249（-9.91%） |
| failed shell command | 140 | 184 | +44 |
| command protocol違反 | 0 | 0 | 0 |
| root以外のsession | 0 | 0 | 0 |

Candidate71はroot-onlyを維持した。tool callとmodel stepの削減は、狙ったmodel再入削減とtoken削減が同じ方向であることを示す。一方、failed commandは増えており、required validation欠落も発生したため、効率改善だけを採用根拠にしない。

同じBatch、case、iterationの1,260組では、Candidate71のtokenが小さい組は935、elapsedが短い組は886だった。内訳はtoken・elapsedとも減少764組、tokenだけ減少171組、elapsedだけ減少122組、両方増加または同値203組である。token差とelapsed差のPearson相関は`+0.586`だった。

## 判定

| 条件 | 結果 | 判定 |
| --- | --- | --- |
| 比較identityと外部計測が完全 | compatibility一致、valid・rateable 1,260 / 1,260、all-agent token完全取得 | 通過 |
| 実質的な品質後退なし | Candidate71はA01誤実行1件、A02必須validation欠落3件。Candidate69比で実質的な低得点が3件増加 | 不通過 |
| required validation欠落なし | Candidate71 A02で`git diff --check`欠落3件 | 不通過 |
| protocol違反0、不要workerなし | protocol違反0、全2,520 runがroot-only | 通過 |
| tokenを継続反復で削減 | 合計`-27.93%`、18 / 18 Batch、13 / 14 caseで削減 | 通過 |
| elapsedを継続反復で削減 | 合計`-11.71%`、18 / 18 Batch、13 / 14 caseで短縮 | 通過 |
| model再入を削減 | tool call`-30.16%`、model step`-26.54%` | 通過 |

KPIの優先順位や閾値を評価基盤へ追加していない。この表はCandidate71の採用判断であり、一次resultやcomparison schemaを変更しない。

## 実行時間、容量、保存

- Candidate69全token: `264,226,988`
- Candidate71全token: `190,417,472`
- Candidate69 / Candidate71とも18 / 18 result登録、18 / 18 final compact receiptを確認した。
- 2,520 / 2,520 runでall-agent tokenを完全取得した。
- 容量guardはdispatch停止`25 GiB`、hard floor `20 GiB`を維持した。
- 実行場所:
  - `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate69-model-reentry-decision-boundary-v12-standard14-continuous-n5-b18-20260722-r1`
  - `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate71-validation-closure-v12-standard14-continuous-n5-b18-20260722-r1`
- 登録先: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/`
- 非公開の生run log、session情報、一時workspaceはrepositoryへ保存しない。

Candidate71の採用、release、本体反映は未実施である。
