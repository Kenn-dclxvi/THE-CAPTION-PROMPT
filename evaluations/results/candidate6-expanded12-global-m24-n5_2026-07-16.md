# Candidate6 expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- valid run window: `2026-07-16T02:11:37+09:00`から`2026-07-16T02:19:33+09:00`
- profile: `candidate6-expanded12-global-m24-n5-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはcandidate6を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-3ce91a4-context-efficiency-r1` / `r1`
- bundle SHA-256: `ffd54c1715b3ccdac1db72e52be71ddce6894616a3fb340d2e5c4c997873b907`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 4,692,041 | 1,755.140 |
| 2 | 100.000 | 4,980,426 | 1,715.486 |
| 3 | 93.750 | 3,842,747 | 1,534.541 |
| 4 | 97.917 | 3,955,268 | 1,677.297 |
| 5 | 100.000 | 4,698,116 | 1,941.314 |
| median | 100.000 | 4,692,041 | 1,715.486 |

58 runはscore `4`である。F04 iteration 4は所定実装とNode validationを満たしたが、test-owned outputのcleanupを完了せずreview前に停止したためscore `3`とした。F10 monthly review iteration 3は開始identityを誤認して固定diffのreviewを実施せず、zero driftと禁止操作回避だけを満たしたためscore `1`とした。

採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Execution observation and storage

- runner wall time: `476.489`秒
- OS samples: `96`
- load average 1分値 max: `12.509`
- memory free min: `60%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- result ID: `db405b73e3ca4ed5aa367bed3fa1e5ce`
- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/db405b73e3ca4ed5aa367bed3fa1e5ce.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate6-expanded12-global-m24-n5-20260716-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。
