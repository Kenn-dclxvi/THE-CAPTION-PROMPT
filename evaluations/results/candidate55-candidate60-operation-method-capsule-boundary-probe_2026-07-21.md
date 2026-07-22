# Candidate55 / Candidate60 operation method capsule boundary probe

## 結論

TaskSpec内の局所method capsuleは、F10へ方法を提示しながら、同一A02 taskの次operationへその方法を持ち越さない境界として機能した。ただし、この挙動はCandidate55とCandidate60の両方で成立したため、Candidate60の共通`AGENTS.md`変更による追加効果ではない。

Candidate60のA02はCandidate55比で`+200,201 total_tokens`（`+88.29%`）、`+77.128 elapsed_seconds`（`+94.20%`）、`+8 command`だった。Candidate60のN=5、採用、release、本体反映へ進めない。

## 条件

- evaluation set: `the-caption-operation-method-capsule-boundary-r1/r1`
- target: `THE-CAPTION` commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model: `gpt-5.6-sol`, reasoning `high`
- catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- iterations: `N=1`
- cases: F10 `r3-method-capsule-probe1`、A02 `r2-start-identity-method-capsule-probe1`
- Candidate55とCandidate60のprofile差: `profile_id`と`prompt_set_identity`だけ

この新TaskSpec revisionのresultは、旧C43 / C55 / C56 resultと互換KPI比較しない。本記録はroute診断であり、Layer 4 resultへ登録しない。

## 保存run

| prompt | case | run id | total tokens | elapsed seconds | command | outcome |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Candidate55 | F10 | `e555978d1b60499588d82eabefbe9a2d` | 73,775 | 73.049 | 11 | `monthly_main.py:25`のmajor finding、zero drift |
| Candidate60 | F10 | `8fdb5c3dc63641948624ead15b015f8f` | 72,476 | 53.468 | 11 | `monthly_main.py:25`のmajor finding、zero drift |
| Candidate55 | A02 | `a6db4b4c7f9f4e1c91af6ef4058d0f4a` | 226,746 | 81.871 | 18 | `run.sh` 1行修正、326 passed / 3 skipped、diff check成功 |
| Candidate60 | A02 | `1e400341557b498580816c7ac4bc4b8c` | 426,947 | 158.999 | 26 | `run.sh` 1行修正、326 passed / 3 skipped、diff check成功 |

## 境界の観測

F10は両promptとも、開始identity、固定read、終了statusの3 command phaseで完了した。指定methodは局所operationで利用された。

A02は両promptとも、最初の4つのidentity commandを一つの`start-identity` operationとして完了した。その後はterminal resultだけを説明し、canonical target探索を別operationとして開始した。先行method、tool grouping、invocation状態、raw outputの後続operationへの流用は観測しなかった。

## Candidate60で増えた実行

Candidate60では、TaskSpecが要求しない追加のauthority read、routing harness、wrapper起動確認が行われた。最初のrouting harnessはzshの引数分割により無効となり、再試行も発生した。これはstart-identity methodの漏出ではなく、後続operationで探索とvalidationを拡張した実行差である。

## 判定

今回の局所method isolationはTaskSpecだけで成立した。Candidate60の共通prompt変更は固有の制御効果を示さず、A02 costを増やした。次に試す場合は共通`AGENTS.md`を増やさず、TaskSpec capsuleだけを別の未知use caseでも検証する。
