# Candidate2 expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T21:47:19+09:00`から`2026-07-15T21:58:17+09:00`
- profile: `candidate2-expanded12-global-m24-n5-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはcandidate2を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-3ce91a4-sa-routing-r1` / `r1`
- bundle SHA-256: `9f8fb5df21ec27296fefdae4aac0925735135b2163710b3fdfb98b4a56cd4f63`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 3,841,478 | 2,456.324 |
| 2 | 100.000 | 4,139,142 | 2,696.013 |
| 3 | 100.000 | 4,088,705 | 2,601.222 |
| 4 | 100.000 | 3,357,178 | 2,450.166 |
| 5 | 100.000 | 3,261,214 | 2,477.185 |
| median | 100.000 | 3,841,478 | 2,477.185 |

60 runはすべて所定成果、許可範囲、terminal dispositionを満たし、score `4`である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Unregistered precursor cycle

直前のcycle `candidate2-expanded12-global-m24-n5-20260715-v3-r1`はrunner summary上60 / 60 validだったが、F02 iteration 5のadapterがexit `2`、`total_tokens: null`、空JSONLで終了していた。Layer 2 bindingが`valid`になったため同slotを安全に再実行できず、このcycleを採点・result登録・比較へ使用していない。raw evidenceは変更せず保持し、同じ固定profileの新cycleを全60 slot実行した。

## Execution observation and storage

- runner wall time: `657.725`秒
- OS samples: `132`
- load average 1分値 max: `8.050`
- memory free min: `66%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- result ID: `0fe03069e84a4778a8b2cee90c327878`
- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/0fe03069e84a4778a8b2cee90c327878.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate2-expanded12-global-m24-n5-20260715-v3-r2`
- unregistered raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate2-expanded12-global-m24-n5-20260715-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。
