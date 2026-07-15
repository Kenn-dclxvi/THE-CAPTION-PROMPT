# Candidate3 expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T22:41:19+09:00`から`2026-07-15T22:51:03+09:00`
- profile: `candidate3-expanded12-global-m24-n5-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはcandidate3を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-3ce91a4-sa-routing-test-boundary-r1` / `r1`
- bundle SHA-256: `c77581feb35a42a7b52c8d035366db9051c7e1d8cd000f8a9540e97c4fee2dbc`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 3,071,248 | 2,465.865 |
| 2 | 100.000 | 3,210,183 | 2,509.195 |
| 3 | 100.000 | 3,335,508 | 2,458.368 |
| 4 | 100.000 | 3,112,542 | 2,783.587 |
| 5 | 100.000 | 2,529,905 | 2,294.647 |
| median | 100.000 | 3,112,542 | 2,465.865 |

60 runはすべて所定成果、許可範囲、terminal dispositionを満たし、score `4`である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Execution observation and storage

- runner wall time: `583.449`秒
- OS samples: `117`
- load average 1分値 max: `8.606`
- memory free min: `65%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- result ID: `35650f74c9034c959d6806350ec9a5dd`
- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/35650f74c9034c959d6806350ec9a5dd.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate3-expanded12-global-m24-n5-20260715-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。
