# Candidate71 / Candidate73 terminal closure preserving compression 第12版採点 対象4項目 各5回

## 結論

Candidate71と、`VALIDATION_CLOSURE`の四機能を残して補助変数と重複表現だけを削ったCandidate73を、F06、F05、A01、A02の各`N=5`で比較した。

両条件とも20 / 20件がvalid・rateable・score `4`で、required validation欠落、workspace drift、command protocol違反、child sessionは0件だった。

Candidate73は保存resultのall-agent `total_tokens`中央値を`17,676`、`elapsed_seconds`中央値を`22.086秒`下げた。一方、F06の編集後model再入中央値は`2 -> 3`、20 run token合計は`+205,706`だった。

Candidate73は品質と成功後の追加readなしterminalを維持したが、事前停止条件のmodel再入増加に該当したため、`targeted_evaluated / stopped`とする。標準14項目、B18、採用、release、本体反映へ進めない。

## 固定条件

- Candidate71: `the-caption-3ce91a4-validation-closure-r1`
- Candidate71 bundle SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- Candidate73: `the-caption-3ce91a4-terminal-closure-preserving-compression-r1`
- Candidate73 bundle SHA-256: `ebeec473f6e45bf14c254f7cf7d4312dd06bfa436b92b700c3d7df8631059345`
- changed target: root `AGENTS.md`だけ
- 評価集合: `the-caption-closure-abstraction-targeted4-r1`第1版
- 評価集合識別値: `5d07a172eb79b69cd5b065c4cdc1b57a4b950d44322a4ad43e05d36e30cf9adb`
- 採点条件: `outcome-semantic-evidence-normalized-owner-diagnostic-v12`
- model / reasoning: `gpt-5.6-sol` / `high`
- memories: disabled
- permission: `workspace-write`、approval `never`
- repetition: F06、F05、A01、A02を各`N=5`、global queue `M=24`
- compatibility key: `27ccf76b316ce7623438d28e492b8083e8f6dc6ce37e83d1fc14346bbba1aef2`
- excluded attempt: Candidate71 0 / Candidate73 0

profile差は`profile_id`と`prompt_set_identity`だけである。

## 3 KPI

| 対象 | score分布 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | 20 run token合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Candidate71 | `4 = 20` | 100.000 | 552,025 | 265.696秒 | 2,737,443 |
| Candidate73 | `4 = 20` | 100.000 | 534,349 | 243.610秒 | 2,943,149 |
| Candidate73 - Candidate71 | — | 0.000 | -17,676（-3.20%） | -22.086秒（-8.31%） | +205,706（+7.51%） |

KPI中央値は5 iterationそれぞれの4 case合計から算出した保存resultの中央値である。20 run token合計は分散確認用の診断値であり、別KPIではない。

## case別

| case | token中央値 C71 | token中央値 C73 | token合計 C71 | token合計 C73 | elapsed中央値 C71 | elapsed中央値 C73 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | 115,806 | 81,702 | 603,055 | 474,474 | 46.788秒 | 39.695秒 |
| A02 | 219,690 | 237,251 | 1,185,213 | 1,342,171 | 95.930秒 | 84.531秒 |
| F05 | 34,926 | 34,901 | 193,207 | 174,662 | 25.894秒 | 26.644秒 |
| F06 | 157,863 | 158,035 | 755,968 | 951,842 | 92.529秒 | 100.706秒 |

## 実行経路

| 診断値 | Candidate71 | Candidate73 | 差 |
| --- | ---: | ---: | ---: |
| agent message | 81 | 82 | +1 |
| attempted shell command | 136 | 133 | -3 |
| failed shell command | 3 | 2 | -1 |
| command protocol違反 | 0 | 0 | 0 |
| root以外のsession | 0 | 0 | 0 |

F06の編集後agent message中央値はCandidate71の`2`に対しCandidate73は`3`だった。Candidate73の3 / 5 runが編集後に3 agent messageを生成した。

2 runは、required validationと差分確認を同一model stepから発行し、全成功を一度述べた後、追加toolなしで完了説明をもう一度生成した。1 runはtests全体の集約出力に構造化exit codeがなく、結果有効性を満たさないnonterminalとして同じrequired pytestを再実行した。全成功と有効なresultが揃った後の追加read / validationは0件だった。

F05はartifact変更なし、A01は確認前edit / testなしだった。A02はauthority確定前batchを行わず、編集後agent message中央値は`3 -> 3`だった。

## 判定

| 条件 | 結果 | 判定 |
| --- | --- | --- |
| 20 / 20 valid・rateable、score 4 | 両条件とも成立 | 通過 |
| required validation、zero drift、protocol、root-only | 欠落・違反0 | 通過 |
| F05 / A01 / A02の非適用域 | 確認前edit / testなし、authority探索維持 | 通過 |
| 全成功後に追加read / validationしない | 追加0件 | 通過 |
| F06編集後model再入を増やさない | 中央値`2 -> 3` | 不通過 |
| all-agent tokenを増やさない | 保存result中央値`-3.20%`、20 run合計`+7.51%` | 不通過 |

表面圧縮してもvalidationのtool batchと成功後terminalは保持できた。しかしmodel出力のterminal化はCandidate71と同じ強さでは再現せず、token分散も増えた。Candidate73へ補助文を追加せず、停止する。

## 保存

- Candidate71 result id: `0f1d18323fda4d2cbe3683303d0f8a72`
- Candidate73 result id: `d60833f7a6ca4e8c8510fa8d32187386`
- 両resultはappend-only registryへ登録済み
- 両campaignはexecution evidenceを圧縮済み
- 非公開の生run log、session情報、一時workspaceはrepositoryへ保存しない
