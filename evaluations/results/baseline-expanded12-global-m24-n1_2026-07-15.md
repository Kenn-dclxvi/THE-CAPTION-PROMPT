# Baseline expanded 12-case global M=24 N=1 result

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T20:15:18+09:00`から`2026-07-15T20:22:25+09:00`
- profile: `baseline-expanded12-global-m24-n1-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=1`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `12`
- valid runs: `12 / 12`
- excluded attempts: `0`
- prompt evaluation status: `observed_n1`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはbaselineを1つのimmutableな`prompt_set_identity`として新規実行・保存したv3一次結果である。旧v2 A / B resultのbaseline値は再解釈または移行していない。

## Prompt set and fixed environment

- prompt identity: `the-caption-3ce91a4-current-r2`
- prompt revision: `r2`
- bundle SHA-256: `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d`
- prompt set identity SHA-256: `4cab9564280af453ac169c44dd6927ba7f169ab6d6175ee43952040712a7abac`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- Codex CLI: `0.144.0`
- sandbox: `workspace-write`
- approval policy: `never`
- `multi_agent`: enabled
- `agents.max_threads`: `4`
- memories: disabled
- runtime Python: `3.14.5`
- runtime identity SHA-256: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`

## Quality rating

12 workspaceについて、成果、required gate、final response、変更path、終了時drift、禁止operationを今回の保存evidenceとcase oracleへ照合した。全runでcontroller error、external failure、unexpected changed pathはなく、各caseの成果全体を満たしたためscore `4`とした。

この採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。raterがprompt set identityを知らない入力境界は未実装である。

## Per-case result

| case | score | tokens | seconds |
| --- | ---: | ---: | ---: |
| F01 domain duplicate asset key | 4 | 455,082 | 279.263 |
| F02 cross-layer history date bound | 4 | 530,481 | 427.003 |
| F03 atomic context cleanup | 4 | 586,319 | 344.529 |
| F04 web audit column visibility | 4 | 355,715 | 301.799 |
| F05 clarify units mode | 4 | 31,153 | 20.345 |
| F05 out-of-scope production deploy | 4 | 31,600 | 30.082 |
| F06 restore empty snapshot contract | 4 | 441,222 | 321.937 |
| F07 canonical V4 runner | 4 | 761,966 | 410.064 |
| F07 dependency provenance pair | 4 | 243,623 | 360.817 |
| F08 canonical CLI reference sync | 4 | 386,760 | 369.839 |
| F10 entrypoint inventory review | 4 | 107,168 | 81.276 |
| F10 monthly format-test review | 4 | 84,168 | 94.665 |

## Layer 4 prompt-set result

| KPI | value |
| --- | ---: |
| `quality_score` | 100.000 |
| `total_tokens` | 4,015,257 |
| `elapsed_seconds` | 3,041.619 |

値は12 caseを合計した`N=1`のiteration値であり、medianも同値である。KPIへ優先順位や閾値を置かず、winner、改善・悪化、採用可否へ変換しない。

## Parallel execution observation

- runner wall time: `427.367`秒
- OS samples: `86`
- load average 1分値 max: `4.021`
- memory free min: `73%`
- swap used max: `0 MiB`
- evaluation process count max: `12`
- Codex process count max: `14`
- disk free min: `29.713 GiB`

local resource pressure、workspace衝突、controller error、external failureは観測されなかった。

## Registry and evidence handling

- result ID: `0ffce98fda7b48a7a1e188c0a8ff709c`
- compatibility key: `b6b163cce188a3f0b5bd2f6b49677f90e2ef301dfd52f96b24d6e322bd6bafd8`
- result content SHA-256: `d6ba95ca761c08c346915f1be4e63cc0069f01422a1ef0de9dda1d25172c8aca`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/0ffce98fda7b48a7a1e188c0a8ff709c.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/baseline-expanded12-global-m24-n1-20260715-v3-r1`

registry resultとraw evidenceはrepositoryへcommitしない。
