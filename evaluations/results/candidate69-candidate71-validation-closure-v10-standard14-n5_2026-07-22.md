# Candidate69 / Candidate71 validation closure 標準14項目 各5回

## 結論

Candidate71の標準14項目、各`N=5`を完了した。Candidate71は70 / 70件がvalid・rateable・score `4`で、required validation欠落、command protocol違反、workspace drift、worker起動は0件だった。

保存済みCandidate69比で、5反復のall-agent `total_tokens`中央値は`2,691,522 -> 1,923,837`、`-28.52%`だった。`elapsed_seconds`中央値は`1,104.860 -> 1,031.401秒`、`-6.65%`だった。

70 run合計では、tokenが`13,726,510 -> 9,816,623`、`-28.48%`だった。elapsedは`5,491.756 -> 5,184.819秒`、`-5.59%`だった。

tokenは14 case中13 case、5反復中5反復で小さかった。elapsedは14 case中10 case、5反復中4反復で小さかった。

Candidate71は`standard14_evaluated / gate_passed`とする。品質を維持したままtokenと全体時間を削減したため、標準14項目の事前gateは通過である。ただし、時間はcase別に一様ではないため、採用判断には同条件B18での再現確認を残す。

Candidate69は保存済みresultを使い、再実行していない。Candidate70の`MACHINE_BOUNDARY`は継承していない。executor parameter、TaskSpec、fixture、permission、required command、quality ratingは変更していない。

## 固定条件

- Candidate69: `the-caption-3ce91a4-model-reentry-decision-boundary-r1`
- Candidate69 bundle SHA-256: `76e6c86fa4cf107ee660d79598e034c384545935982da4983f65d67f65423e87`
- Candidate71: `the-caption-3ce91a4-validation-closure-r1`
- Candidate71 bundle SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- changed target: root `AGENTS.md`だけ
- 評価集合: `the-caption-standard14-r1`第1版
- 評価集合識別値: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`
- 採点条件: `outcome-boundary-owner-diagnostic-v10`
- 対象リポジトリ版 / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- memories: disabled
- permission: `workspace-write`、approval `never`
- repetition: 標準14項目を各`N=5`、global queue `M=24`
- token accounting: all-agent / `v1`
- compatibility key: `4948b6b613f3d5a809774ba29fa5cc82d0244fd6e1340e618b7b5f5abfaf6236`
- excluded attempt: Candidate69 0 / Candidate71 0

Candidate69 / Candidate71 profile差は`profile_id`と`prompt_set_identity`だけである。

## 3 KPI

`total_tokens`と`elapsed_seconds`の中央値は、14 caseを同じiteration番号で合計した5反復の中央値である。

| KPI | Candidate69 | Candidate71 | Candidate71 - Candidate69 |
| --- | ---: | ---: | ---: |
| `quality_score`中央値 | 100.000 | 100.000 | 0.000 |
| all-agent `total_tokens`中央値 | 2,691,522 | 1,923,837 | -767,685（-28.52%） |
| `elapsed_seconds`中央値 | 1,104.860秒 | 1,031.401秒 | -73.459秒（-6.65%） |
| 70 run token合計 | 13,726,510 | 9,816,623 | -3,909,887（-28.48%） |
| 70 run elapsed合計 | 5,491.756秒 | 5,184.819秒 | -306.937秒（-5.59%） |
| 公式score `4 / その他` | 69 / 1 | 70 / 0 | +1 / -1 |

Candidate69のscore `3`はF10 monthly reviewの既知のlocation mismatchだった。Candidate71は同caseの数値位置を5 / 5で正しく示した。ただし、この1件だけから品質向上を一般化しない。

| iteration | quality C69 | quality C71 | tokens C69 | tokens C71 | token差 | elapsed C69 | elapsed C71 | elapsed差 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 98.21 | 100.00 | 2,825,812 | 1,808,030 | -36.02% | 1,064.571秒 | 995.212秒 | -6.52% |
| 2 | 100.00 | 100.00 | 2,883,163 | 2,185,651 | -24.19% | 1,166.780秒 | 1,104.736秒 | -5.32% |
| 3 | 100.00 | 100.00 | 2,687,450 | 2,037,156 | -24.20% | 1,104.860秒 | 1,088.780秒 | -1.46% |
| 4 | 100.00 | 100.00 | 2,638,563 | 1,923,837 | -27.09% | 1,022.322秒 | 1,031.401秒 | +0.89% |
| 5 | 100.00 | 100.00 | 2,691,522 | 1,861,949 | -30.82% | 1,133.223秒 | 964.689秒 | -14.87% |

## case別KPI

点数列は`score 4 / その他`の順である。tokenとelapsedは各caseの5 run合計である。

| case | 点数 C69 | 点数 C71 | token C69 | token C71 | token差 | elapsed C69 | elapsed C71 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 latent mode policy | 5 / 0 | 5 / 0 | 461,842 | 467,009 | +1.12% | 205.601秒 | 203.519秒 | -1.01% |
| A02 repository-resolvable routing | 5 / 0 | 5 / 0 | 1,502,544 | 1,137,993 | -24.26% | 465.913秒 | 477.543秒 | +2.50% |
| F01 duplicate asset key | 5 / 0 | 5 / 0 | 1,272,198 | 890,233 | -30.02% | 421.207秒 | 411.429秒 | -2.32% |
| F02 history date bound | 5 / 0 | 5 / 0 | 2,022,259 | 1,548,052 | -23.45% | 646.194秒 | 553.561秒 | -14.34% |
| F03 atomic context cleanup | 5 / 0 | 5 / 0 | 1,358,887 | 778,977 | -42.68% | 505.023秒 | 456.670秒 | -9.57% |
| F04 web audit visibility | 5 / 0 | 5 / 0 | 1,138,796 | 894,778 | -21.43% | 472.636秒 | 483.259秒 | +2.25% |
| F05 clarification | 5 / 0 | 5 / 0 | 254,170 | 161,198 | -36.58% | 127.161秒 | 107.375秒 | -15.56% |
| F05 production deploy refusal | 5 / 0 | 5 / 0 | 207,224 | 164,993 | -20.38% | 134.783秒 | 108.787秒 | -19.29% |
| F06 empty snapshot contract | 5 / 0 | 5 / 0 | 1,269,919 | 889,365 | -29.97% | 435.776秒 | 460.334秒 | +5.64% |
| F07 canonical runner | 5 / 0 | 5 / 0 | 1,383,836 | 752,049 | -45.65% | 474.158秒 | 445.351秒 | -6.08% |
| F07 dependency provenance | 5 / 0 | 5 / 0 | 601,317 | 434,644 | -27.72% | 360.138秒 | 308.630秒 | -14.30% |
| F08 CLI reference sync | 5 / 0 | 5 / 0 | 966,293 | 730,899 | -24.36% | 445.364秒 | 451.287秒 | +1.33% |
| F10 entrypoint inventory review | 5 / 0 | 5 / 0 | 714,781 | 535,713 | -25.05% | 457.977秒 | 433.829秒 | -5.27% |
| F10 monthly format-test review | 4 / 1 | 5 / 0 | 572,444 | 430,720 | -24.76% | 339.824秒 | 283.246秒 | -16.65% |

A01だけtokenが`+1.12%`だった。A02、F04、F06、F08はelapsedが`+1.33%`から`+5.64%`だった。これら4 caseも品質は維持し、tool callとmodel stepは減っているため、現時点ではcontrolの逆流ではなく実行時間のばらつきとして扱う。

## 実行経路診断

`top-level tool call`はroot rolloutの`custom_tool_call`と`function_call`を数えた。`model step`はroot rolloutの`token_count` eventを数えた。全140 runはsession 1のroot-onlyだった。

| case | tool call C69 → C71 | model step C69 → C71 | shell command C69 → C71 |
| --- | ---: | ---: | ---: |
| A01 latent mode policy | 18 → 18 | 23 → 23 | 18 → 18 |
| A02 repository-resolvable routing | 41 → 31 | 46 → 36 | 32 → 50 |
| F01 duplicate asset key | 39 → 31 | 44 → 36 | 47 → 44 |
| F02 history date bound | 46 → 37 | 51 → 42 | 75 → 53 |
| F03 atomic context cleanup | 44 → 28 | 49 → 33 | 55 → 42 |
| F04 web audit visibility | 46 → 36 | 51 → 41 | 61 → 55 |
| F05 clarification | 11 → 5 | 16 → 10 | 20 → 20 |
| F05 production deploy refusal | 8 → 5 | 13 → 10 | 20 → 20 |
| F06 empty snapshot contract | 42 → 34 | 47 → 39 | 64 → 55 |
| F07 canonical runner | 46 → 25 | 51 → 30 | 58 → 74 |
| F07 dependency provenance | 29 → 20 | 34 → 25 | 51 → 46 |
| F08 CLI reference sync | 41 → 29 | 46 → 34 | 81 → 85 |
| F10 entrypoint inventory review | 34 → 23 | 39 → 28 | 57 → 59 |
| F10 monthly format-test review | 24 → 16 | 29 → 21 | 50 → 49 |
| 全14 case | 469 → 338 | 539 → 408 | 689 → 670 |

全体ではtool callが`-27.93%`、model stepが`-24.30%`、shell commandが`-2.76%`だった。失敗shell commandは`11 -> 8`、command protocol違反は両方0件だった。

この計測では各runの`model step = tool call + 1`である。この二つは同じ再入回数を別の位置から見た指標であり、独立した二つの効果とは数えない。

70個の対応run差で見ると、tool call差とtoken差のPearson相関は`0.869`、elapsed差との相関は`0.543`だった。shell command差との相関はtokenが`0.185`、elapsedが`0.276`だった。token削減はshell command数よりmodel再入削減と強く対応している。

一方、A02とF07 canonicalはshell commandが増えてもtokenが減った。command数はKPIではなく、required validation欠落や探索拡大を見つける診断指標として保持する。

## 判定

| 条件 | 結果 |
| --- | --- |
| 70 / 70 valid・rateable | 通過 |
| 実質的な品質後退0 | 通過 |
| required validation欠落0 | 通過 |
| protocol違反0、zero drift | 通過 |
| root-only | 通過 |
| token中央値、合計、5反復を削減 | 通過 |
| elapsed中央値と合計を削減 | 通過 |
| case別elapsedが一様に削減 | 未達、14 case中10 caseで削減 |

標準14項目の事前gateは通過とする。case別elapsedの一様削減は採用条件にしない。処理時間は外部ばらつきを含み、全体中央値と合計は削減しているためである。

採用判断は保留する。Candidate69とCandidate43の比較では、標準14項目`N=5`とB18でelapsed差の方向が反転した履歴がある。Candidate71も同条件B18でquality、token、elapsed、required validationの再現性を確認する必要がある。

## 容量と保存

Candidate71の正式campaignは70 / 70件を登録後に圧縮した。完了時の空き容量は約28 GiBである。不要な失敗campaignや誤準備は残していない。外部volumeと`MUSIC_SD`は使用していない。

## 登録証跡

- Candidate69 result ID: `a861676ceede45de97235d2ed9839b3d`
- Candidate69 result content SHA-256: `8e2cc44a961e261d9b836efc8516326252a38f70d2fd94072951582955514e9f`
- Candidate71 result ID: `b251576a67c540c792af5e8de99a3f50`
- Candidate71 result content SHA-256: `a36dc8155c110a458b79a44b3c5d832154bb7a37f254f137007096d93aa32f0a`
- Candidate71 execution archive SHA-256: `15224d802cc7dee7000621258796a370f64a0dbe1f169550025ce1b2cfb550bb`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/c69-c71-validation-closure-v10-standard14-n5-20260722-r1.json`

Candidate71の採用、release、本体反映は未判断、未実施である。
