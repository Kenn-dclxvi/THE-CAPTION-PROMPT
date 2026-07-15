# Baseline, candidate1, and candidate2 expanded 12-case N=5 comparison view

## Compared results

| role | prompt set identity | result ID |
| --- | --- | --- |
| reference | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `7748386da9cf4cc8a5fc35025f5972f2` |
| minuend | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `7105fa9353824d3187ad299c1f3542f3` |
| minuend | `the-caption-3ce91a4-sa-routing-r1` / `r1` / `9f8fb5…4f63` | `0fe03069e84a4778a8b2cee90c327878` |

- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- set: `the-caption-revision-2-expanded12-r1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / effort: `gpt-5.6-sol` / `high`
- repetition: `N=5`
- execution: `global_queue`、`M=24`
- registered valid runs: 各prompt set `60 / 60`
- excluded attempts: 各prompt set `0`

evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件は3 resultで一致している。reference指定は差分方向だけを固定し、採用状態や順位を表さない。

## Three KPI median view

差分は各candidateからbaselineを引いた値である。

| prompt set | `quality_score` | quality diff | `total_tokens` | token diff | `elapsed_seconds` | seconds diff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 100.000 | — | 3,888,115 | — | 2,828.032 | — |
| candidate1 | 97.917 | -2.083 | 4,338,633 | +450,518 | 1,932.971 | -895.062 |
| candidate2 | 100.000 | 0.000 | 3,841,478 | -46,637 | 2,477.185 | -350.848 |

KPIへ優先順位や閾値を設定せず、差分をwinner、改善・悪化、採用可否へ変換しない。

## Quality observation

| prompt set | iteration quality | score 3 runs | score 4 runs |
| --- | --- | ---: | ---: |
| baseline | `97.917 / 97.917 / 100 / 100 / 100` | 2 | 58 |
| candidate1 | `100 / 100 / 97.917 / 97.917 / 97.917` | 3 | 57 |
| candidate2 | `100 / 100 / 100 / 100 / 100` | 0 | 60 |

baselineの2件はF04 cleanup手順後の未完了停止、candidate1の3件はF03 / F06のauthority conflict解釈による未完了停止である。いずれもartifactと主要validationを満たした上でterminal outcomeをscoreへ反映した。

採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。candidate2の未登録precursor cycleは比較対象に含めていない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate2-expanded12-n5-20260715.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v1`
- generated at: `2026-07-15T21:59:03+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。この12 case、`N=5`の観測範囲を超えて一般化しない。
