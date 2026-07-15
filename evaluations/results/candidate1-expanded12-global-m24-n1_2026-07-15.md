# Candidate1 expanded 12-case global M=24 N=1 result

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T20:28:50+09:00`から`2026-07-15T20:34:16+09:00`
- profile: `candidate1-expanded12-global-m24-n1-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=1`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `12`
- valid runs: `12 / 12`
- excluded attempts: `0`
- prompt evaluation status: `observed_n1`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはcandidate1を1つのimmutableな`prompt_set_identity`として新規実行・保存したv3一次結果である。旧v2 A / B resultのcandidate1値は再解釈または移行していない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-revision-2-r1`
- prompt revision: `r1`
- bundle SHA-256: `f5ea64185324da9e36c8e7e1a38956d0ab5893f4ef29b5a866d3c89234aac865`
- prompt set identity SHA-256: `993a5e032e057bb73d548b5d620300e81b33d2871e5df87db72a0242181daed4`
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
| F01 domain duplicate asset key | 4 | 226,999 | 86.343 |
| F02 cross-layer history date bound | 4 | 471,534 | 123.606 |
| F03 atomic context cleanup | 4 | 184,663 | 98.260 |
| F04 web audit column visibility | 4 | 283,107 | 112.543 |
| F05 clarify units mode | 4 | 34,253 | 22.827 |
| F05 out-of-scope production deploy | 4 | 34,055 | 25.668 |
| F06 restore empty snapshot contract | 4 | 806,941 | 325.453 |
| F07 canonical V4 runner | 4 | 863,925 | 321.410 |
| F07 dependency provenance pair | 4 | 312,115 | 246.592 |
| F08 canonical CLI reference sync | 4 | 392,434 | 223.476 |
| F10 entrypoint inventory review | 4 | 96,838 | 65.698 |
| F10 monthly format-test review | 4 | 75,517 | 47.430 |

## Layer 4 prompt-set result

| KPI | value |
| --- | ---: |
| `quality_score` | 100.000 |
| `total_tokens` | 3,782,381 |
| `elapsed_seconds` | 1,699.304 |

値は12 caseを合計した`N=1`のiteration値であり、medianも同値である。KPIへ優先順位や閾値を置かず、winner、改善・悪化、採用可否へ変換しない。

F10 monthly format-test reviewは今回、期待するmajor findingを1件返した。旧v2 resultにある同caseの早期停止履歴は変更せず、この`N=1`観測へ読み替えない。

## Parallel execution observation

- runner wall time: `325.846`秒
- OS samples: `66`
- load average 1分値 max: `3.452`
- memory free min: `72%`
- swap used max: `0 MiB`
- evaluation process count max: `12`
- Codex process count max: `14`
- disk free min: `28.973 GiB`

local resource pressure、workspace衝突、controller error、external failureは観測されなかった。

## Registry and evidence handling

- result ID: `4584e31f75374cedbdda3fa81c8e2edf`
- compatibility key: `b6b163cce188a3f0b5bd2f6b49677f90e2ef301dfd52f96b24d6e322bd6bafd8`
- result content SHA-256: `fb90ffc684eeef4d82c89393252f612a05a806bca191fa994a151861acc16bca`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/4584e31f75374cedbdda3fa81c8e2edf.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate1-expanded12-global-m24-n1-20260715-v3-r1`

registry resultとraw evidenceはrepositoryへcommitしない。
