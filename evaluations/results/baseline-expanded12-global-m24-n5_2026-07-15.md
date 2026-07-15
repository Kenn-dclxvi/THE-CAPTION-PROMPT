# Baseline expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T21:12:50+09:00`から`2026-07-15T21:25:04+09:00`
- profile: `baseline-expanded12-global-m24-n5-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはbaselineを1つのimmutableな`prompt_set_identity`として保存した一次結果である。固定A / B pair、winner、KPI優先順位、採用判断は保存identityと出力へ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-3ce91a4-current-r2` / `r2`
- bundle SHA-256: `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 97.917 | 3,171,210 | 2,785.312 |
| 2 | 97.917 | 4,426,813 | 3,255.848 |
| 3 | 100.000 | 4,114,672 | 2,764.735 |
| 4 | 100.000 | 3,798,066 | 2,975.869 |
| 5 | 100.000 | 3,888,115 | 2,828.032 |
| median | 100.000 | 3,888,115 | 2,828.032 |

F04 iteration 1 / 2は所定実装とNode validationを満たしたが、cleanup command拒否後に別commandへ切り替え、terminal outcomeを未完了停止としたためscore `3`である。残る58 runはscore `4`である。

採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Execution observation and storage

- runner wall time: `733.867`秒
- OS samples: `147`
- load average 1分値 max: `9.297`
- memory free min: `66%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- result ID: `7748386da9cf4cc8a5fc35025f5972f2`
- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/7748386da9cf4cc8a5fc35025f5972f2.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/baseline-expanded12-global-m24-n5-20260715-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。
