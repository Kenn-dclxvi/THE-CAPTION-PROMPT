# Baseline, candidate1, and candidate2 expanded 12-case N=1 comparison view

## Compared results

| role | prompt set identity | result ID |
| --- | --- | --- |
| reference | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `0ffce98fda7b48a7a1e188c0a8ff709c` |
| minuend | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `4584e31f75374cedbdda3fa81c8e2edf` |
| minuend | `the-caption-3ce91a4-sa-routing-r1` / `r1` / `9f8fb5…4f63` | `6dd0458db8eb46f9a9e41306d373158a` |

- compatibility key: `b6b163cce188a3f0b5bd2f6b49677f90e2ef301dfd52f96b24d6e322bd6bafd8`
- set: `the-caption-revision-2-expanded12-r1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / effort: `gpt-5.6-sol` / `high`
- repetition: `N=1`
- execution: `global_queue`、`M=24`
- valid runs: 各prompt set `12 / 12`
- excluded attempts: 各prompt set `0`

evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件は3 resultで一致している。referenceは差分方向を固定するためだけの指定であり、採用状態や順位を表さない。

## Three KPI view

差分は各candidateからbaselineを引いた値である。

| prompt set | `quality_score` | quality diff | `total_tokens` | token diff | `elapsed_seconds` | seconds diff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 100.000 | — | 4,015,257 | — | 3,041.619 | — |
| candidate1 | 100.000 | 0.000 | 3,782,381 | -232,876 | 1,699.304 | -1,342.315 |
| candidate2 | 100.000 | 0.000 | 3,513,610 | -501,647 | 2,627.176 | -414.443 |

KPIへ優先順位や閾値を設定せず、差分をwinner、改善・悪化、採用可否へ変換しない。

## Per-case numeric view

全caseで3 prompt setのquality scoreはすべて`4`である。

| case | baseline tokens | candidate1 tokens | candidate2 tokens | baseline sec | candidate1 sec | candidate2 sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 domain duplicate asset key | 455,082 | 226,999 | 500,619 | 279.263 | 86.343 | 435.006 |
| F02 cross-layer history date bound | 530,481 | 471,534 | 659,659 | 427.003 | 123.606 | 429.704 |
| F03 atomic context cleanup | 586,319 | 184,663 | 521,927 | 344.529 | 98.260 | 362.810 |
| F04 web audit column visibility | 355,715 | 283,107 | 358,032 | 301.799 | 112.543 | 237.976 |
| F05 clarify units mode | 31,153 | 34,253 | 32,235 | 20.345 | 22.827 | 28.853 |
| F05 out-of-scope production deploy | 31,600 | 34,055 | 69,571 | 30.082 | 25.668 | 46.138 |
| F06 restore empty snapshot contract | 441,222 | 806,941 | 301,824 | 321.937 | 325.453 | 197.203 |
| F07 canonical V4 runner | 761,966 | 863,925 | 190,214 | 410.064 | 321.410 | 273.499 |
| F07 dependency provenance pair | 243,623 | 312,115 | 252,264 | 360.817 | 246.592 | 162.468 |
| F08 canonical CLI reference sync | 386,760 | 392,434 | 259,344 | 369.839 | 223.476 | 192.600 |
| F10 entrypoint inventory review | 107,168 | 96,838 | 280,042 | 81.276 | 65.698 | 191.058 |
| F10 monthly format-test review | 84,168 | 75,517 | 87,879 | 94.665 | 47.430 | 69.860 |

## Observed scope

- 3 prompt setともimplementation、test-only、shell、React / TypeScript、docs-only、clarification、out-of-scope stop、read-only inventory、monthly diff reviewの所定成果を満たした。
- candidate1のmonthly diff reviewは今回、期待するmajor findingを返した。旧v2の早期停止履歴は別resultとして保持する。
- candidate2で観測した条件付き実装後routingと、各KPI値の因果関係は`N=1`から確定しない。

case別の値をこのevaluation setと反復条件の外へ一般化しない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate2-expanded12-n1-20260715.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v1`
- generated at: `2026-07-15T20:34:59+09:00`

採点は各runの保存evidenceに基づくが、独立したblind quality raterによるものではない。prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。
