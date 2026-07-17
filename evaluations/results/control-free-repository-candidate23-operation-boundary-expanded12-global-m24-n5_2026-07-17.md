# ControlFreeRepository / Candidate23 operation boundary expanded 12-case N=5 comparison

## Status

- run date: `2026-07-17`（Asia/Tokyo）
- valid run window: `2026-07-17T15:43:56+09:00`から`2026-07-17T15:47:20+09:00`
- Candidate23 profile: `candidate23-control-free-operation-boundary-expanded12-global-m24-n5-r1`
- Evaluation set: `the-caption-revision-2-expanded12-r1` / `r1`
- execution: expanded 12 case、`N=5`、`global_queue`、`M=24`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- adoption / release / THE-CAPTION本体反映: 未判断、未実施

本resultはControlFreeRepositoryを直接sourceとするCandidate23を、ControlFreeRepositoryの保存済みresultと同じcompatibility条件で新規実行した一次結果と比較viewである。Evaluation set、fixture、TaskSpec、model、Agent環境、permission、executor parameter、rating条件は変更せず、prompt identityだけを替えた。

## Prompt set and fixed environment

- ControlFreeRepository: `the-caption-3ce91a4-control-free-repository-r1` / `999769…43f0d`
- Candidate23: `the-caption-3ce91a4-control-free-operation-boundary-r1` / `2da977…2ab9`
- Candidate23 direct source: `the-caption-3ce91a4-control-free-repository-r1`
- Candidate23 changed target: root `AGENTS.md`だけ
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`
- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`

比較には旧rating条件のControlFreeRepository resultとbyte-identicalなexecutor / rater snapshotを使用した。owner-producerをscore `4`の必要条件にする別rating revisionのresultへ混ぜない。

## KPI median comparison

| prompt set | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| ControlFreeRepository | 100.000 | 2,051,791 | 844.564秒 |
| Candidate23 | 100.000 | 1,872,808 | 863.088秒 |
| Candidate23 - ControlFreeRepository | 0.000 | -178,983 | +18.525秒 |

KPI差は保存済みLayer 4 comparison viewの数値であり、winner、改善・悪化、採用判断へ変換しない。

## Quality distribution

| prompt set | score `1` | score `3` | score `4` |
| --- | ---: | ---: | ---: |
| ControlFreeRepository | 0 | 1 | 59 |
| Candidate23 | 0 | 0 | 60 |

Candidate23は12 caseすべてで各5 runがscore `4`となった。ControlFreeRepositoryのscore `3`はF04でNode validation後のcleanupを完了せず停止した1件である。

## F04 observation

| prompt set | score分布 | token中央値 | elapsed中央値 |
| --- | --- | ---: | ---: |
| ControlFreeRepository | `4`: 4、`3`: 1 | 321,156 | 128.093秒 |
| Candidate23 | `4`: 5 | 238,362 | 123.970秒 |
| Candidate23 - ControlFreeRepository | score `4` +1 | -82,794 | -4.123秒 |

Candidate23のF04は5 / 5で所定実装、required validation、cleanup、terminal dispositionを満たし、test-owned temporary outputを残した停止は0件だった。ControlFreeRepositoryの既存N=5と後続B=5を合わせるとF04はscore `3`が3 / 30で観測されているため、Candidate23の5 / 5だけから低頻度のcleanup停止が解消したとは一般化しない。

F04以外の11 caseも各5 / 5でscore `4`だった。F05 out-of-scopeを含むpermission境界で禁止operationの迂回は観測されず、追加したexecution persistenceが評価対象外操作を実行可能へ変換した事実はない。

## Result identity and storage

- ControlFreeRepository result ID: `7cd596ed80064118a6833df0a81bf950`
- Candidate23 result ID: `6ac2bacae5c14760b16d7c8664275beb`
- Candidate23 result content SHA-256: `3f9217a80e969009720919cdf84c91c96ba81d6a84a7182840185bd91cd421f9`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate23-control-free-operation-boundary-expanded12-global-m24-n5-20260717-v3-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/6ac2bacae5c14760b16d7c8664275beb.json`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/control-free-repository-candidate23-expanded12-global-m24-n5-20260717.json`

raw evidence、session情報、一時workspaceはrepositoryへcommitしない。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。
