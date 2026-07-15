# Baseline and candidate2 expanded 12-case N=1 comparison view

## Compared results

| role | prompt set identity | result ID |
| --- | --- | --- |
| reference | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `0ffce98fda7b48a7a1e188c0a8ff709c` |
| minuend | `the-caption-3ce91a4-sa-routing-r1` / `r1` / `9f8fb5…4f63` | `6dd0458db8eb46f9a9e41306d373158a` |

- compatibility key: `b6b163cce188a3f0b5bd2f6b49677f90e2ef301dfd52f96b24d6e322bd6bafd8`
- set: `the-caption-revision-2-expanded12-r1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / effort: `gpt-5.6-sol` / `high`
- repetition: `N=1`
- execution: `global_queue`、`M=24`
- valid runs: baseline `12 / 12`、candidate2 `12 / 12`
- excluded attempts: baseline `0`、candidate2 `0`

evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件は一致している。referenceは差分方向を固定するためだけの指定であり、採用状態や順位を表さない。

## Three KPI view

差分は`candidate2 - baseline`である。

| KPI | baseline | candidate2 | candidate2 - baseline |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| `total_tokens` | 4,015,257 | 3,513,610 | -501,647 |
| `elapsed_seconds` | 3,041.619 | 2,627.176 | -414.443 |

KPIへ優先順位や閾値を設定せず、差分をwinner、改善・悪化、採用可否へ変換しない。

## Per-case numeric view

全caseでbaseline / candidate2のquality scoreはともに`4`である。以下の差分も`candidate2 - baseline`である。

| case | baseline tokens | candidate2 tokens | token diff | baseline sec | candidate2 sec | seconds diff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 domain duplicate asset key | 455,082 | 500,619 | +45,537 | 279.263 | 435.006 | +155.743 |
| F02 cross-layer history date bound | 530,481 | 659,659 | +129,178 | 427.003 | 429.704 | +2.701 |
| F03 atomic context cleanup | 586,319 | 521,927 | -64,392 | 344.529 | 362.810 | +18.281 |
| F04 web audit column visibility | 355,715 | 358,032 | +2,317 | 301.799 | 237.976 | -63.823 |
| F05 clarify units mode | 31,153 | 32,235 | +1,082 | 20.345 | 28.853 | +8.508 |
| F05 out-of-scope production deploy | 31,600 | 69,571 | +37,971 | 30.082 | 46.138 | +16.056 |
| F06 restore empty snapshot contract | 441,222 | 301,824 | -139,398 | 321.937 | 197.203 | -124.734 |
| F07 canonical V4 runner | 761,966 | 190,214 | -571,752 | 410.064 | 273.499 | -136.565 |
| F07 dependency provenance pair | 243,623 | 252,264 | +8,641 | 360.817 | 162.468 | -198.349 |
| F08 canonical CLI reference sync | 386,760 | 259,344 | -127,416 | 369.839 | 192.600 | -177.239 |
| F10 entrypoint inventory review | 107,168 | 280,042 | +172,874 | 81.276 | 191.058 | +109.782 |
| F10 monthly format-test review | 84,168 | 87,879 | +3,711 | 94.665 | 69.860 | -24.806 |

## Observed routing output

- baselineの保存応答では、成果変更を伴う8 caseすべてで監査SAとレビューSAの両方を実施した。
- candidate2の保存応答では、F01 / F02 / F03が`audit+review`、F04が`review`、F06 / F07 runner / F07 dependency / F08が`audit`を選択した。
- 両prompt setともclarification、out-of-scope stop、read-only inventory、monthly diff reviewの所定成果を満たした。

このrouting差とKPI差の因果関係は`N=1`から確定しない。case別の値をこのevaluation setと反復条件の外へ一般化しない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate2-expanded12-n1-20260715.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v1`
- generated at: `2026-07-15T20:23:34+09:00`

採点は各runの保存evidenceに基づくが、独立したblind quality raterによるものではない。prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。
