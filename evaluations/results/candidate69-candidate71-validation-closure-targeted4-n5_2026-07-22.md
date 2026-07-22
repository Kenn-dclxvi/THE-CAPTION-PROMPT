# Candidate69 / Candidate71 validation closure 対象4項目 各5回

## 結論

Candidate71はCandidate69を直接sourceとし、root `AGENTS.md`へ`VALIDATION_CLOSURE`一labelだけを追加した。Candidate70の`MACHINE_BOUNDARY`、executor parameter、TaskSpec、fixture、permission、required command、quality ratingは変更していない。

Candidate71は20 / 20 valid・rateable・score `4`、root-only、zero drift、command protocol違反0だった。保存済みCandidate69も20 / 20 score `4`であり、成果品質の後退とrequired validation欠落は0件である。

登録済みcomparison viewの中央値はCandidate71 - Candidate69で、`quality_score = 0.0`、all-agent `total_tokens = -577,347`、`elapsed_seconds = -109.786秒`だった。20 run合計はtokenが`6,884,512 -> 4,154,529`、`-39.65%`、elapsedが`2,537.285 -> 2,030.713秒`、`-19.97%`である。

F04、F06、F07 canonicalの正の3 caseは、token、elapsed、top-level tool call、model stepがすべてcase別でも減った。A02もtokenとelapsedが減り、required validationは全5件でartifact変更後に実行された。対象試験の事前gateは通過とする。

Candidate71の現在状態は`targeted_evaluated / gate_passed`である。対象4項目の結果だけで採用、release、THE-CAPTION本体反映は判断しない。標準14項目と継続反復は別の評価段階とする。

## 固定条件

- Candidate69: `the-caption-3ce91a4-model-reentry-decision-boundary-r1`
- Candidate69 bundle SHA-256: `76e6c86fa4cf107ee660d79598e034c384545935982da4983f65d67f65423e87`
- Candidate71: `the-caption-3ce91a4-validation-closure-r1`
- Candidate71 bundle SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- changed target: root `AGENTS.md`だけ
- 評価集合: `the-caption-machine-decision-boundary-targeted4-r1`第1版
- 評価集合識別値: `1d438e885f5300bc177b3409a14044e206199c1e23a114f9b2d3f2ac3a17e8c5`
- 採点条件: `outcome-semantic-location-owner-diagnostic-v11`
- 対象リポジトリ版 / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- memories: disabled
- permission: `workspace-write`、approval `never`
- repetition: A02、F04、F06、F07 canonicalを各`N=5`、global queue `M=24`
- token accounting: all-agent / `v1`
- compatibility key: `da204aaa7a90e75980c458d02b25e651974863cc2094f78592b8c647386553bb`
- excluded attempt: 0 / 0

Candidate69 / Candidate71 profile差は`profile_id`と`prompt_set_identity`だけである。Candidate69は保存済み正本resultを使い、再実行していない。

## 3 KPI

`total_tokens`と`elapsed_seconds`の中央値は、4 caseを同じiteration番号で合計した5反復の中央値である。

| KPI | Candidate69 | Candidate71 | Candidate71 - Candidate69 |
| --- | ---: | ---: | ---: |
| `quality_score`中央値 | 100.000 | 100.000 | 0.000 |
| all-agent `total_tokens`中央値 | 1,391,860 | 814,513 | -577,347（-41.48%） |
| `elapsed_seconds`中央値 | 506.732秒 | 396.946秒 | -109.786秒（-21.67%） |
| 20 run token合計 | 6,884,512 | 4,154,529 | -2,729,983（-39.65%） |
| 20 run elapsed合計 | 2,537.285秒 | 2,030.713秒 | -506.572秒（-19.97%） |
| 公式score `4 / その他` | 20 / 0 | 20 / 0 | 0 / 0 |

| iteration | quality C69 | quality C71 | tokens C69 | tokens C71 | elapsed C69 | elapsed C71 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100.00 | 100.00 | 1,391,860 | 811,345 | 497.221秒 | 377.592秒 |
| 2 | 100.00 | 100.00 | 1,621,858 | 699,101 | 506.732秒 | 345.881秒 |
| 3 | 100.00 | 100.00 | 1,248,949 | 814,513 | 559.771秒 | 396.946秒 |
| 4 | 100.00 | 100.00 | 1,201,462 | 923,565 | 407.794秒 | 441.997秒 |
| 5 | 100.00 | 100.00 | 1,420,383 | 906,005 | 565.767秒 | 468.296秒 |

Candidate71はtokenが5 / 5反復で小さかった。elapsedは4 / 5反復で小さく、iteration 4だけ`+34.203秒`だった。

## case別KPI

| case | score C69 | score C71 | token合計 C69 | token合計 C71 | token差 | elapsed合計 C69 | elapsed合計 C71 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A02 非trigger | 5 / 0 | 5 / 0 | 1,954,526 | 1,417,892 | -536,634（-27.46%） | 657.308秒 | 543.335秒 | -113.973秒（-17.34%） |
| F04 正 | 5 / 0 | 5 / 0 | 1,269,780 | 1,026,001 | -243,779（-19.20%） | 586.239秒 | 509.677秒 | -76.562秒（-13.06%） |
| F06 正 | 5 / 0 | 5 / 0 | 1,352,287 | 911,164 | -441,123（-32.62%） | 602.230秒 | 513.492秒 | -88.738秒（-14.73%） |
| F07 canonical 正 | 5 / 0 | 5 / 0 | 2,307,919 | 799,472 | -1,508,447（-65.36%） | 691.507秒 | 464.208秒 | -227.300秒（-32.87%） |
| 正の3 case合計 | 15 / 0 | 15 / 0 | 4,929,986 | 2,736,637 | -2,193,349（-44.49%） | 1,879.976秒 | 1,487.377秒 | -392.599秒（-20.88%） |

点数列は`4 / その他`の順である。4 caseすべてでtoken合計とelapsed合計が小さかった。

## 実行経路診断

`top-level tool call`はroot rolloutの`custom_tool_call`と`function_call`を数えた。`model step`はroot rolloutの`token_count` eventを数えた。全40 runはsession 1のroot-onlyである。

| case | tool call C69 | tool call C71 | model step C69 | model step C71 | shell command C69 | shell command C71 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A02 | 49 | 38 | 54 | 43 | 47 | 48 |
| F04 | 45 | 37 | 50 | 42 | 54 | 49 |
| F06 | 39 | 31 | 44 | 36 | 83 | 54 |
| F07 canonical | 69 | 25 | 74 | 30 | 76 | 59 |
| 全4 case | 202 | 131 | 222 | 151 | 260 | 210 |
| 正の3 case | 153 | 93 | 168 | 108 | 213 | 162 |

Candidate71は正の3 case合計でtool callとmodel stepを各60減らした。全4 caseではtool callが`-35.15%`、model stepが`-31.98%`、shell commandが`-19.23%`だった。

A02のshell commandだけは`+1`、`+2.13%`である。全5件の保存traceを確認すると、canonical targetの探索と編集が先に完了し、`bash -n run.sh`、`git diff --check`、pytestはその後に成功している。required validationの欠落、変更前validation、validation再試行の増加はない。この1 command差はroute failureではなくrun間の探索ばらつきとして保持する。command数自体はKPIへ昇格させない。

F04のrequired command 15件、F06の10件、F07 canonicalの10件はすべて成功した。command protocol違反、evidence incomplete、not attemptedはすべて0件だった。

## 対象試験gateの判定

| 条件 | 結果 |
| --- | --- |
| 20 / 20 valid・rateable | 通過 |
| 実質的な品質後退0 | 通過 |
| required validation欠落0 | 通過 |
| protocol違反0、zero drift | 通過 |
| root-only | 通過 |
| 正の3 caseでtool call、model step、tokenを削減 | 通過 |
| A02の変更前流入なし | 通過 |
| elapsedを記録し、正の3 case合計で短縮 | 通過 |

Candidate71は対象試験gateを通過した。これはcandidateの採用承認ではない。標準14項目で非対象caseへの流入を確認し、継続反復で品質欠落と処理時間の再現性を確認するまでは`release`とruntime projectionへ進めない。

## 容量と保存

初回dispatchは容量ガードが試験開始前に停止したため、実行runとresultを生成していない。0 validの失敗campaign、未実行の誤準備、rejected preparation、および再生成可能なChrome cacheを削除し、空き28.6 GiBで同じcampaignを準備し直した。登録済みresult、Candidate69比較証跡、npm cacheは削除していない。外部volumeと`MUSIC_SD`は使用していない。

Candidate71の正式campaignは20 / 20件を登録後に圧縮した。完了時の空き容量は約28 GiBである。

## 登録証跡

- Candidate69 result ID: `085f0c567bcb4c3a96dd97938817aa94`
- Candidate69 result content SHA-256: `f7aeba434b2d214d39a18653c9d4cf7e66ceacbf0cc463caffa21b9a423266ef`
- Candidate71 result ID: `5dc74f629d184965a07a439759f93e98`
- Candidate71 result content SHA-256: `80cb028c5c6c5b172a41855febf2fe716225dc94a79f3d0d4289070e20eccad5`
- Candidate71 execution archive SHA-256: `cb0b80f46b5d5384a9fc677727fcad168bfceec42e275481512ac3da40223eba`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/c69-c71-validation-closure-targeted4-n5-20260722-r1.json`

Candidate71の採用、release、本体反映は未判断、未実施である。
