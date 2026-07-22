# Candidate43 / Candidate67 標準14項目 各5回

## 結論

Candidate67を標準14項目で各5回、合計70回実行した。70件すべてが有効かつ採点可能で、点数は全件`4`だった。除外と失敗は0件だった。

同じ条件のCandidate43も70件すべてが点数`4`である。3 KPI中央値でCandidate67からCandidate43を引いた差は、`quality_score = 0.000`、all-agent `total_tokens = -84,992`、`elapsed_seconds = -9.276秒`だった。

一方、70件のtoken合計はCandidate67が`+48,808`、`+0.28%`多い。Candidate67のA02 iteration 4が`1,070,955 tokens`だったため、反復中央値と70件合計の方向が一致しない。この結果からruntime削減の再現性を確定しない。

標準14項目の観測範囲では、Candidate43からcross-label duplicate 2文を削除しても成果品質とA01 / A02境界を維持した。これは比較材料であり、採用、release、THE-CAPTION本体反映は未判断・未実施である。

## 固定条件

- 評価集合: `the-caption-standard14-r1`第1版
- 評価集合識別値: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`
- Candidate43: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate43 bundle SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- Candidate67: `the-caption-3ce91a4-cross-label-predicate-deduplication-r1`
- Candidate67 bundle SHA-256: `0676b5c34f3fa68e71984f28fa0fc49938fde5b3ee822fe4cffa7522b6bcce87`
- 採点条件: `outcome-boundary-owner-diagnostic-v10`
- 採点条件SHA-256: `987a10b29862b4b75daa73a696ec922cddbce6f84e6cb0459349383f1767c1b4`
- 対象リポジトリ版: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- 使用模型: `gpt-5.6-sol`
- 実行方式: 全体待ち行列、同時実行上限24、各項目5回
- token accounting: root agentと全子sessionの合計、第1版
- 互換条件識別値: `4948b6b613f3d5a809774ba29fa5cc82d0244fd6e1340e618b7b5f5abfaf6236`

Candidate67 profileはCandidate43の標準14 profileから`profile_id`と`prompt_set_identity`だけを変更した。比較viewは両resultのcompatibility keyと互換条件実体の一致を確認して生成した。

## 3 KPI

| prompt set | 点数分布 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | 70件token合計 |
| --- | --- | ---: | ---: | ---: | ---: |
| Candidate43 | `4 = 70` | 100.000 | 3,647,298 | 1,353.458秒 | 17,732,662 |
| Candidate67 | `4 = 70` | 100.000 | 3,562,306 | 1,344.182秒 | 17,781,470 |
| Candidate67 - Candidate43 | — | 0.000 | -84,992（-2.33%） | -9.276秒（-0.69%） | +48,808（+0.28%） |

中央値は14項目をまとめた各反復の値から算出した。70件token合計はKPIの代表値ではないが、反復中央値だけでは見えない偏りを確認する診断値として併記した。

## 反復別KPI

| 反復 | Candidate43 quality | Candidate67 quality | Candidate43 tokens | Candidate67 tokens | token差 | Candidate43 elapsed | Candidate67 elapsed | elapsed差 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100.000 | 100.000 | 3,647,298 | 3,176,753 | -470,545 | 1,439.351秒 | 1,182.200秒 | -257.150秒 |
| 2 | 100.000 | 100.000 | 3,422,707 | 3,547,087 | +124,380 | 1,353.458秒 | 1,443.510秒 | +90.052秒 |
| 3 | 100.000 | 100.000 | 3,740,820 | 3,667,591 | -73,229 | 1,440.509秒 | 1,329.743秒 | -110.766秒 |
| 4 | 100.000 | 100.000 | 3,670,184 | 3,562,306 | -107,878 | 1,328.981秒 | 1,344.182秒 | +15.201秒 |
| 5 | 100.000 | 100.000 | 3,251,653 | 3,827,733 | +576,080 | 1,241.287秒 | 1,415.006秒 | +173.720秒 |

Candidate67のtokenは3 / 5反復、elapsedは2 / 5反復でCandidate43より小さい。反復ごとの方向は揃っていない。

## 区分別token合計

| 区分 | Candidate43 | Candidate67 | Candidate67 - Candidate43 |
| --- | ---: | ---: | ---: |
| F項目12件、各5回 | 15,490,426 | 14,984,423 | -506,003（-3.27%） |
| A01・A02、各5回 | 2,242,236 | 2,797,047 | +554,811（+24.74%） |
| 標準14項目、各5回 | 17,732,662 | 17,781,470 | +48,808（+0.28%） |

A区分の合計差は主にCandidate67 A02 iteration 4の`1,070,955 tokens`による。A02のcase内token中央値はCandidate43より`31,615`小さく、合計と中央値の方向が異なる。

## case別数値

全caseの点数分布は両prompt setとも`4 = 5`だった。

| case | token合計 C43 | token合計 C67 | 合計差 | token中央値 C43 | token中央値 C67 | 中央値差 | elapsed中央値 C43 | elapsed中央値 C67 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 455,061 | 536,441 | +81,380 | 75,325 | 87,458 | +12,133 | 39.802秒 | 40.893秒 | +1.091秒 |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 1,787,175 | 2,260,606 | +473,431 | 331,365 | 299,750 | -31,615 | 135.743秒 | 101.559秒 | -34.184秒 |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 1,062,766 | 1,131,796 | +69,030 | 214,709 | 216,806 | +2,097 | 84.974秒 | 84.762秒 | -0.212秒 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 1,729,308 | 1,837,080 | +107,772 | 347,063 | 375,703 | +28,640 | 112.119秒 | 123.710秒 | +11.592秒 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 1,311,471 | 1,085,992 | -225,479 | 259,117 | 185,980 | -73,137 | 111.068秒 | 108.120秒 | -2.947秒 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 1,124,137 | 1,294,468 | +170,331 | 216,546 | 232,029 | +15,483 | 100.967秒 | 106.652秒 | +5.685秒 |
| `TC-F05-CLARIFY-UNITS-MODE` | 299,778 | 349,042 | +49,264 | 78,992 | 78,461 | -531 | 29.271秒 | 31.072秒 | +1.801秒 |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 480,758 | 299,677 | -181,081 | 85,769 | 78,548 | -7,221 | 44.523秒 | 29.454秒 | -15.069秒 |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 1,772,211 | 2,090,478 | +318,267 | 396,341 | 316,928 | -79,413 | 116.818秒 | 102.668秒 | -14.149秒 |
| `TC-F07-CANONICAL-V4-RUNNER` | 2,250,479 | 2,016,707 | -233,772 | 460,217 | 371,477 | -88,740 | 133.997秒 | 122.059秒 | -11.938秒 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 757,156 | 842,246 | +85,090 | 141,167 | 157,842 | +16,675 | 70.367秒 | 82.608秒 | +12.241秒 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 2,282,726 | 2,104,520 | -178,206 | 386,364 | 485,726 | +99,362 | 136.120秒 | 144.763秒 | +8.643秒 |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 1,273,947 | 952,064 | -321,883 | 274,203 | 198,882 | -75,321 | 117.183秒 | 101.655秒 | -15.528秒 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 1,145,689 | 980,353 | -165,336 | 223,484 | 221,587 | -1,897 | 105.681秒 | 92.849秒 | -12.833秒 |

## 実行経路診断

`top-level tool call`は各root rolloutの`custom_tool_call`と`function_call`を数えた。`reasoning item`と`token_count event`は別に数えた。`shell command`は`all-agent-command-evidence/v5`のattempted commandである。

| 診断値 | Candidate43 | Candidate67 | Candidate67 - Candidate43 |
| --- | ---: | ---: | ---: |
| session | 70 | 70 | 0 |
| child / additional token | 0 | 0 | 0 |
| top-level tool call | 639 | 625 | -14（-2.19%） |
| reasoning item | 548 | 556 | +8（+1.46%） |
| token_count event | 710 | 695 | -15（-2.11%） |
| shell command | 705 | 679 | -26（-3.69%） |

Candidate43とCandidate67は70 / 70件がroot-onlyだった。Candidate67はtool call、token count event、shell commandが少ない一方、reasoning itemは多い。したがって、prompt bytesの削減だけで経路全体が短縮したとは判断しない。

必須command protocol違反は0件だった。`owner-producer-evidence/v1`がdiagnostic-onlyで`inadmissible`とした記録は両resultとも55件である。これは品質点へ使用していない。

## 保存記録

### Candidate67

- profile: `candidate67-cross-label-predicate-deduplication-v10-standard14-global-m24-n5-r1`
- 結果識別子: `a60896a5c9ab47bd920017b5868ca0a5`
- 結果内容SHA-256: `e3b3b1968d92e315c44b0884f2234d26ce1096239f3db89c0383790faa478bbc`
- 実行場所: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate67-cross-label-predicate-deduplication-v10-standard14-global-m24-n5-20260722-r1`
- execution archive SHA-256: `c26911bb247a118704e7c5b3aa0fe7fcb9fa1287062866dd136fa8496b5ecf62`
- final archive SHA-256: `5558cef9c3d1a9947324da700d6031639db02772aa0dbae0001b0eb80e4a5238`
- 有効 / 採点可能 / 除外: 70 / 70 / 0
- 保存状態: 登録済み、圧縮済み

### Candidate43

- 結果識別子: `b62428c2361b435fbd0fc7c8979868e7`
- 結果内容SHA-256: `f09b08972579f2d33bb90ab669a11fc9edfa2c33209a93735ffdf2bd3d7e7226`
- 有効 / 採点可能 / 除外: 70 / 70 / 0

比較viewは次へ保存した。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate67-cross-label-predicate-deduplication-v10-standard14-n5-20260722-r1.json`

Candidate67の状態は`standard14_evaluated`とする。これは以前の対象試験停止判断を削除せず、標準14項目の追加評価を新しい判断材料として追記する状態である。採用、release、本体反映は未判断・未実施である。
