# C5 / C15 / 制御プロンプトなし2条件 expanded 12-case global M=24 N=5 comparison

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- Evaluation set: `the-caption-revision-2-expanded12-r1` / `r1`
- repetition: 各prompt set `N=5`、各60 run
- execution: `global_queue`、外側並列上限`M=24`
- valid runs: 各prompt set `60 / 60`
- excluded attempts: 各prompt set `0`
- prompt evaluation status: 両方とも`observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultは、root制御プロンプトを空にしたうえで、階層別repository instructionを持たない条件と持つ条件を、それぞれ独立したimmutableな`prompt_set_identity`として保存した一次結果を記録する。比較viewには互換なC5とC15も含める。winner、改善・悪化、採用判断は含めない。

## Prompt set and fixed environment

| condition | prompt identity | bundle SHA-256 | 空にしたtarget |
| --- | --- | --- | --- |
| repository固有指示なし | `the-caption-3ce91a4-control-free-generic-r1` | `e7aca7e2628eeeab90068a3b8e2138ea80d3addd483d9c333ff65ac0490d8d76` | root、`docs`、`scripts`、`src`、`tests`の`AGENTS.md` |
| repository固有指示あり | `the-caption-3ce91a4-control-free-repository-r1` | `999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d` | root `AGENTS.md`だけ |

両条件ともbaseline r2由来の19 path full bundleを使用した。target commit / tree、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iterationは同一である。

- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`

## Iteration KPI and median

### Repository固有指示なし

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 91.667 | 1,949,682 | 855.678 |
| 2 | 91.667 | 1,856,838 | 705.173 |
| 3 | 93.750 | 1,962,858 | 784.377 |
| 4 | 93.750 | 1,999,844 | 774.293 |
| 5 | 87.500 | 1,898,071 | 728.305 |
| median | 91.667 | 1,949,682 | 774.293 |

score内訳はscore `4`が52件、score `3`が2件、score `1`が6件である。

### Repository固有指示あり

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 2,066,113 | 873.457 |
| 2 | 100.000 | 2,128,060 | 827.544 |
| 3 | 100.000 | 2,048,545 | 844.564 |
| 4 | 97.917 | 2,015,266 | 818.295 |
| 5 | 100.000 | 2,051,791 | 858.843 |
| median | 100.000 | 2,051,791 | 844.564 |

score内訳はscore `4`が59件、score `3`が1件である。

## C5 / C15を含むKPI median comparison

| set | result ID | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | --- | ---: | ---: | ---: |
| C5 | `da8505348e4741a4a413618fbfa9aa1f` | 100.000 | 5,740,441 | 1,714.914秒 |
| C15 | `010b5b71f3154b6593590e9c6655ec1b` | 100.000 | 4,590,751 | 1,723.986秒 |
| repository固有指示なし | `ac7e83211d5442ceb222221d1d382751` | 91.667 | 1,949,682 | 774.293秒 |
| repository固有指示あり | `7cd596ed80064118a6833df0a81bf950` | 100.000 | 2,051,791 | 844.564秒 |

C5をsubtrahendとした4 result比較viewの中央値差は次のとおりである。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| C15 - C5 | 0.000 | -1,149,690 | +9.072秒 |
| repository固有指示なし - C5 | -8.333 | -3,790,759 | -940.621秒 |
| repository固有指示あり - C5 | 0.000 | -3,688,650 | -870.350秒 |

C15をsubtrahendとした制御プロンプトなし2条件の中央値差も併記する。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| repository固有指示なし - C15 | -8.333 | -2,641,069 | -949.693秒 |
| repository固有指示あり - C15 | 0.000 | -2,538,960 | -879.423秒 |

これらの数値差はKPIの優先順位、winner、改善・悪化を意味しない。

## Boundary observations

- repository固有指示なし条件はF10 entrypoint inventoryの5 / 5で、空のroot / `src/AGENTS.md`をauthority矛盾と解釈して停止した。zero driftは満たしたが、inventoryと独立確認は未実施のためscore 1とした。
- 同条件のF04は2 / 5で実装とNode validationを完了したが、cleanup command拒否後に`node_modules` / `dist`を残して停止しscore 3となった。
- 同条件のF10 monthly reviewは1 / 5で開始identityを誤認してreviewを実施せずscore 1となった。
- repository固有指示あり条件はF10 entrypoint inventoryを5 / 5で完了した。
- 同条件のF04は1 / 5で実装とNode validationを完了したが、cleanup未完了でscore 3となった。
- repository固有指示なし条件のF05 clarification 1件は、auditの英字marker検査では`fallback`不足として未分類になったが、final responseは日本語でdaily / strictの選択とstrict時のlive CSVフォールバック可否を一度に確認しzero driftだったためscore 4とした。残る59件は既存quality audit規則で採点した。

採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。この12 case、`N=5`の観測範囲を超えて一般化しない。

## Result identity and storage

| condition | runner wall time | result ID |
| --- | ---: | --- |
| repository固有指示なし | `190.757`秒 | `ac7e83211d5442ceb222221d1d382751` |
| repository固有指示あり | `219.898`秒 | `7cd596ed80064118a6833df0a81bf950` |

- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- 4 result comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate5-candidate15-control-free-expanded12-n5-20260716.json`
- 2 result comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/control-free-generic-repository-expanded12-n5-20260716.json`
- raw evidence root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/`

raw evidenceとregistry resultはrepositoryへcommitしない。両runはresult登録後にlossless archiveを検証し、Layer 2 / 3のlive evidenceを最終圧縮した。この結果は採用、release承認、THE-CAPTION本体へのruntime反映を意味しない。
