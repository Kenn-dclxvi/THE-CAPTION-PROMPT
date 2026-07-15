# Candidate1 expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T21:25:38+09:00`から`2026-07-15T21:36:13+09:00`
- profile: `candidate1-expanded12-global-m24-n5-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはcandidate1を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-revision-2-r1` / `r1`
- bundle SHA-256: `f5ea64185324da9e36c8e7e1a38956d0ab5893f4ef29b5a866d3c89234aac865`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 4,372,892 | 1,932.971 |
| 2 | 100.000 | 4,338,633 | 1,735.112 |
| 3 | 97.917 | 3,244,970 | 1,513.648 |
| 4 | 97.917 | 4,767,521 | 2,221.309 |
| 5 | 97.917 | 4,133,955 | 2,022.353 |
| median | 97.917 | 4,338,633 | 1,932.971 |

F03 iteration 4とF06 iteration 3 / 5は成果と主要validationを満たしたが、authority conflictを理由にterminal outcomeを未完了停止としたためscore `3`である。残る57 runはscore `4`である。

採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Execution observation and storage

- runner wall time: `635.451`秒
- OS samples: `127`
- load average 1分値 max: `9.823`
- memory free min: `67%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- result ID: `7105fa9353824d3187ad299c1f3542f3`
- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/7105fa9353824d3187ad299c1f3542f3.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate1-expanded12-global-m24-n5-20260715-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。
