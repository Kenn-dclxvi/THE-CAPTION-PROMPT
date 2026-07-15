# Baseline and candidate1-5 expanded 12-case N=5 comparison view

## Compared results

| label | prompt set identity | result ID |
| --- | --- | --- |
| Base | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `7748386da9cf4cc8a5fc35025f5972f2` |
| C1 | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `7105fa9353824d3187ad299c1f3542f3` |
| C2 | `the-caption-3ce91a4-sa-routing-r1` / `r1` / `9f8fb5…4f63` | `0fe03069e84a4778a8b2cee90c327878` |
| C3 | `the-caption-3ce91a4-sa-routing-test-boundary-r1` / `r1` / `c77581…2dbc` | `35650f74c9034c959d6806350ec9a5dd` |
| C4 | `the-caption-3ce91a4-executor-discretion-r1` / `r1` / `f8cdd2…23e2` | `24874ca754284603a79b5144137e5c81` |
| C5 | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `c93afa1d55b149b6b6499219d07d0f77` |

- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- set: `the-caption-revision-2-expanded12-r1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / effort: `gpt-5.6-sol` / `high`
- repetition: `N=5`
- execution: `global_queue`、`M=24`
- registered valid runs: 各prompt set `60 / 60`
- excluded attempts: 各prompt set `0`

evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件は6 resultで一致している。Baseのreference指定は差分方向だけを固定し、採用状態や順位を表さない。

## KPI median comparison

差分は各candidateからBaseを引いた値である。

| set | `quality_score` | Base差 | `total_tokens` | Base差 | `elapsed_seconds` | Base差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Base | 100.000 | — | 3,888,115 | — | 2,828.032 | — |
| C1 | 97.917 | -2.083 | 4,338,633 | +450,518 | 1,932.971 | -895.062 |
| C2 | 100.000 | 0.000 | 3,841,478 | -46,637 | 2,477.185 | -350.848 |
| C3 | 100.000 | 0.000 | 3,112,542 | -775,573 | 2,465.865 | -362.167 |
| C4 | 100.000 | 0.000 | 4,579,476 | +691,361 | 1,676.820 | -1,151.213 |
| C5 | 100.000 | 0.000 | 4,503,816 | +615,701 | 1,714.914 | -1,113.118 |

KPIへ優先順位や閾値を設定せず、差分をwinner、改善・悪化、採用可否へ変換しない。

## Quality distribution and runner wall time

| set | iteration quality | score 1 | score 3 | score 4 | runner wall time |
| --- | --- | ---: | ---: | ---: | ---: |
| Base | `97.917 / 97.917 / 100 / 100 / 100` | 0 | 2 | 58 | 733.867秒 |
| C1 | `100 / 100 / 97.917 / 97.917 / 97.917` | 0 | 3 | 57 | 635.451秒 |
| C2 | `100 / 100 / 100 / 100 / 100` | 0 | 0 | 60 | 657.725秒 |
| C3 | `100 / 100 / 100 / 100 / 100` | 0 | 0 | 60 | 583.449秒 |
| C4 | `100 / 100 / 91.667 / 93.750 / 100` | 2 | 1 | 57 | 449.760秒 |
| C5 | `100 / 100 / 100 / 100 / 100` | 0 | 0 | 60 | 426.528秒 |

採点は各resultの保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Prompt execution design

| set | 実装主体の制御 | Audit / Review制御 | 停止制御 |
| --- | --- | --- | --- |
| Base | 専用実装SAへ委任 | 実装後に監査SAとレビューSAを要求 | Base既定 |
| C1 | active executorに委ね、専用実装SA roleを持たない | TaskSpec predicateによるconditional audit / review | C1既定 |
| C2 | 専用実装SAへ必須委任 | riskとmachine coverageによる4 route | C2既定 |
| C3 | C2と同じ | C2の4 routeを維持し、test contract risk境界を限定 | C2と同じ |
| C4 | 親直接 / SA委任 / 分担をモデル判断 | C3の4 routeを維持 | C3と同じ |
| C5 | C4と同じ | C4と同じ | 実行開始後の停止を明示済み条件と観測事実へ限定 |

C5の保存evidenceでは40 implementation runすべてが親直接を選び、実装目的のSA委任は0件だった。

## SA routing observation

同じ4 route schemaを持つC2からC5のselected routeと実際の独立worker起動数を示す。これはLayer 4のKPIではなく、保存済み実行evidenceから数えた補助観測である。

| set | `none` | `audit` | `review` | `audit+review` | audit SA | review SA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C2 | 19 | 24 | 6 | 11 | 35 | 17 |
| C3 | 24 | 21 | 10 | 5 | 26 | 15 |
| C4 | 25 | 20 | 10 | 5 | 25 | 14 |
| C5 | 24 | 20 | 11 | 5 | 25 | 16 |

C5ではF01 iteration 5が`Q2_state_failure_recovery`を付与して`review`を選択したため、C4より`none`が1件少なく`review`が1件多い。selected routeが要求した独立workerはすべて起動された。

## C5 and C4 numeric difference

差分はC5からC4を引いた値である。

| `quality_score` | `total_tokens` | `elapsed_seconds` | runner wall time |
| ---: | ---: | ---: | ---: |
| 0.000 | -75,660 | +38.094 | -23.232秒 |

C4のscore 1が2件、score 3が1件だったのに対し、C5は60件すべてscore 4だった。これはこの12 case、`N=5`でのquality distributionの観測であり、KPI中央値の差ではない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate2-candidate3-candidate4-candidate5-expanded12-n5-20260716.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v1`
- generated at: `2026-07-16T01:42:24+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。この12 case、`N=5`の観測範囲を超えて一般化しない。
