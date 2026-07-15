# Candidate5 expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- valid run window: `2026-07-16T01:32:55+09:00`から`2026-07-16T01:40:01+09:00`
- profile: `candidate5-expanded12-global-m24-n5-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはcandidate5を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-3ce91a4-completion-persistence-r1` / `r1`
- bundle SHA-256: `63abe024084d9d979323444af1bb43c34b5f6a8269e7412f9d9d6a3b7ea51667`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 4,858,931 | 1,735.306 |
| 2 | 100.000 | 4,249,080 | 1,626.771 |
| 3 | 100.000 | 4,334,707 | 1,714.914 |
| 4 | 100.000 | 4,503,816 | 1,651.643 |
| 5 | 100.000 | 4,786,754 | 1,757.682 |
| median | 100.000 | 4,503,816 | 1,714.914 |

60 runすべてが所定成果、required validation、許可範囲、terminal dispositionを満たしたためscore `4`とした。F04の5 runはtest-owned temporary outputをcleanupしてselected reviewを完了し、F10 monthly format-test reviewの5 runは固定diffをreviewしてmajor findingを直接根拠付きで報告した。

採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Execution observation and storage

- 40 implementation runの実装主体申告: 親直接 `40`、SA委任 `0`、分担 `0`
- selected route: `none` 24、`audit` 20、`review` 11、`audit+review` 5
- actual independent worker launch: audit 25、review 16
- runner wall time: `426.528`秒
- OS samples: `86`
- load average 1分値 max: `9.018`
- memory free min: `61%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- result ID: `c93afa1d55b149b6b6499219d07d0f77`
- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/c93afa1d55b149b6b6499219d07d0f77.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate5-expanded12-global-m24-n5-20260716-v3-r1`

実装主体とworker launchの集計はLayer 4のKPIではなく、保存済み実行evidenceの明示内容から数えた補助観測である。raw evidenceとregistry resultはrepositoryへcommitしない。
