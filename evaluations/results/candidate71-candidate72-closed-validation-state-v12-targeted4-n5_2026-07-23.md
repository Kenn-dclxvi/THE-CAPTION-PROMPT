# Candidate71 / Candidate72 closed validation state 第12版採点 対象4項目 各5回

## 結論

Candidate71の詳細な`VALIDATION_CLOSURE`と、同じ適用域を短いclosed-state表現へ置換したCandidate72を、F06、F05、A01、A02の各`N=5`で比較した。

両条件とも20 / 20件がvalid・rateable・score `4`で、required validation欠落、workspace drift、command protocol違反、child sessionは0件だった。

一方、Candidate72はF06の編集後model再入中央値が`2 -> 3`、F06 token中央値が`157,863 -> 198,552`へ増えた。20 run全体でも保存result中央値のall-agent `total_tokens`が`+92,810`、`elapsed_seconds`が`+2.523秒`だった。

Candidate72は品質を維持したが、短文化でCandidate71のterminal closureを保持できなかったため、`targeted_evaluated / stopped`とする。標準14項目、B18、採用、release、本体反映へ進めない。

## 固定条件

- Candidate71: `the-caption-3ce91a4-validation-closure-r1`
- Candidate71 bundle SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- Candidate72: `the-caption-3ce91a4-closed-validation-state-r1`
- Candidate72 bundle SHA-256: `4e6931afd00c6281f529ebb267f9a6b8b8d0be98de1cc1b2a1a3c36bf8d3dea9`
- changed target: root `AGENTS.md`だけ
- 評価集合: `the-caption-closure-abstraction-targeted4-r1`第1版
- 評価集合識別値: `5d07a172eb79b69cd5b065c4cdc1b57a4b950d44322a4ad43e05d36e30cf9adb`
- 採点条件: `outcome-semantic-evidence-normalized-owner-diagnostic-v12`
- model / reasoning: `gpt-5.6-sol` / `high`
- memories: disabled
- permission: `workspace-write`、approval `never`
- repetition: F06、F05、A01、A02を各`N=5`、global queue `M=24`
- compatibility key: `27ccf76b316ce7623438d28e492b8083e8f6dc6ce37e83d1fc14346bbba1aef2`
- excluded attempt: Candidate71 0 / Candidate72 0

profile差は`profile_id`と`prompt_set_identity`だけである。

## 3 KPI

| 対象 | score分布 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | 20 run token合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Candidate71 | `4 = 20` | 100.000 | 552,025 | 265.696秒 | 2,737,443 |
| Candidate72 | `4 = 20` | 100.000 | 644,835 | 268.219秒 | 3,190,427 |
| Candidate72 - Candidate71 | — | 0.000 | +92,810（+16.81%） | +2.523秒（+0.95%） | +452,984（+16.55%） |

KPI中央値は5 iterationそれぞれの4 case合計から算出した保存resultの中央値である。

## case別

| case | token中央値 C71 | token中央値 C72 | token合計 C71 | token合計 C72 | elapsed中央値 C71 | elapsed中央値 C72 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | 115,806 | 123,486 | 603,055 | 632,123 | 46.788秒 | 42.866秒 |
| A02 | 219,690 | 252,895 | 1,185,213 | 1,340,314 | 95.930秒 | 90.320秒 |
| F05 | 34,926 | 34,173 | 193,207 | 166,865 | 25.894秒 | 24.109秒 |
| F06 | 157,863 | 198,552 | 755,968 | 1,051,125 | 92.529秒 | 103.484秒 |

## 実行経路

| 診断値 | Candidate71 | Candidate72 | 差 |
| --- | ---: | ---: | ---: |
| agent message | 81 | 92 | +11 |
| attempted shell command | 136 | 168 | +32 |
| failed shell command | 3 | 4 | +1 |
| command protocol違反 | 0 | 0 | 0 |
| root以外のsession | 0 | 0 | 0 |

F06の編集後agent message中央値はCandidate71の`2`に対しCandidate72は`3`だった。

Candidate71は、artifact変更後にdiff確認、2本のrequired pytest、変更path確認を同一model stepから発行し、全成功後にそのままterminalへ進んだ。

Candidate72もrequired pytestを同一model stepから発行した。しかし一部runでは、その前にdiffを単独で受領し、全成功後に`nl -ba`で最終行を追加確認した。短いclosed-state表現はvalidation batchを保ったが、batch前後を含むterminal closureを固定しなかった。

F05はCandidate72の5 / 5で2 agent message、4 commandを維持した。A01は両条件とも確認前edit / testが0件だった。A02は編集後agent message中央値`3 -> 3`で、authority探索中のOPENは維持した。

## 判定

| 条件 | 結果 | 判定 |
| --- | --- | --- |
| 20 / 20 valid・rateable、score 4 | 両条件とも成立 | 通過 |
| required validation、zero drift、protocol、root-only | 欠落・違反0 | 通過 |
| F05 / A01 / A02の非適用域 | 確認前edit / testなし、authority探索維持 | 通過 |
| F06編集後model再入を増やさない | 中央値`2 -> 3` | 不通過 |
| all-agent tokenを増やさない | 中央値`+16.81%`、合計`+16.55%` | 不通過 |

OPEN/CLOSED抽象だけへ短縮すると、validationの同時発行は残るが、全成功後の追加read禁止とterminal判断が弱くなる。Candidate71の詳細条件には、単なる試験対策ではなくterminal closureを固定する機能があった。

Candidate72へ補助文を追加しない。標準14項目とB18へ進めず、停止する。

## 保存

- Candidate71 result id: `0f1d18323fda4d2cbe3683303d0f8a72`
- Candidate72 result id: `3a28452508ef4c7f995072bbf12f0bca`
- 両resultはappend-only registryへ登録済み
- 両campaignはexecution evidenceを圧縮済み
- 非公開の生run log、session情報、一時workspaceはrepositoryへ保存しない
