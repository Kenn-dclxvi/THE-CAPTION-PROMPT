# Candidate4 expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T23:41:54+09:00`から`2026-07-15T23:49:24+09:00`
- profile: `candidate4-expanded12-global-m24-n5-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはcandidate4を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-3ce91a4-executor-discretion-r1` / `r1`
- bundle SHA-256: `f8cdd2802653bed0511776a99bb0f7282234425d37d8bfe8cc5c8910f8f923e2`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 6,125,378 | 1,884.515 |
| 2 | 100.000 | 4,306,758 | 1,676.820 |
| 3 | 91.667 | 4,579,476 | 1,644.877 |
| 4 | 93.750 | 5,170,122 | 1,868.563 |
| 5 | 100.000 | 3,938,158 | 1,544.938 |
| median | 100.000 | 4,579,476 | 1,676.820 |

57 runは所定成果、required validation、許可範囲、terminal dispositionを満たしたためscore `4`とした。

- F04 iteration 3は所定実装とNode validationを満たしたが、cleanup command拒否後に未完了停止し、reviewとfinal drift確認を行わなかったためscore `3`とした。
- F10 monthly format-test review iteration 3 / 4は開始identityを誤認してreviewを実施せず、zero driftと禁止操作回避だけを満たしたためscore `1`とした。

採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Execution observation and storage

- 40 implementation runの実装主体申告: 親直接 `40`、SA委任 `0`、分担 `0`
- selected route: `none` 25、`audit` 20、`review` 10、`audit+review` 5
- actual independent worker launch: audit 25、review 14。F04 iteration 3のreview 1件はcleanup未完了のため未起動
- runner wall time: `449.760`秒
- OS samples: `91`
- load average 1分値 max: `6.724`
- memory free min: `69%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- result ID: `24874ca754284603a79b5144137e5c81`
- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/24874ca754284603a79b5144137e5c81.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate4-expanded12-global-m24-n5-20260715-v3-r1`

実装主体とworker launchの集計はLayer 4のKPIではなく、保存済み実行evidenceの明示内容から数えた補助観測である。raw evidenceとregistry resultはrepositoryへcommitしない。
