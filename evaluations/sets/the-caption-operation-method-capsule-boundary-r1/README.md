# Operation method capsule boundary r1

## 結論

局所methodを一つのoperationだけへ提示し、同一task内の次operationへ非伝播にできるかを診断する2 case setである。

## 構成

| case | revision | capsule対象 | 後続境界 |
| --- | --- | --- | --- |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | `r3-method-capsule-probe1` | fixed-seed-diff-review | findingとcountだけをexport |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | `r2-start-identity-method-capsule-probe1` | start-identity | identity resultだけをexportし、canonical-target-resolutionのmethodは未指定 |

Candidate55とCandidate60へ同じsetを渡す。prompt identity以外の条件を変えない。旧case revisionのresultとは互換KPI比較せず、N=1 route診断として扱う。

実行profileは[`Candidate55`](../../profiles/candidate55-prebound-operation-graph-v10-operation-method-capsule-boundary-targeted2-global-m2-n1-catalog-fixed-r1.json)と[`Candidate60`](../../profiles/candidate60-operation-method-capsule-v10-operation-method-capsule-boundary-targeted2-global-m2-n1-catalog-fixed-r1.json)である。[結果](../../results/candidate55-candidate60-operation-method-capsule-boundary-probe_2026-07-21.md)では両promptが非伝播を満たし、Candidate60固有効果は観測しなかった。
