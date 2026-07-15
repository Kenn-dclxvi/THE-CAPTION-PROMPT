# Candidate2 expanded 12-case global M=24 N=1 result

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T20:01:12+09:00`から`2026-07-15T20:08:28+09:00`
- profile: `candidate2-expanded12-global-m24-n1-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=1`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `12`
- valid runs: `12 / 12`
- excluded attempts: `0`
- prompt evaluation status: `observed_n1`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはcandidate2を1つのimmutableな`prompt_set_identity`として保存した一次結果である。固定A / B pairは保存identityに含めず、単一反復の観測範囲を超えてprompt性能を一般化しない。

## Prompt set and fixed environment

- prompt identity: `the-caption-3ce91a4-sa-routing-r1`
- prompt revision: `r1`
- bundle SHA-256: `9f8fb5df21ec27296fefdae4aac0925735135b2163710b3fdfb98b4a56cd4f63`
- prompt set identity SHA-256: `6160bf1dd7d406edd182940ec94ed0fe04ad7ab95ea8edec251bbdec333ab6f0`
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

F09 r1はprompt target collision、F10 monthly review r1はprompt overlay後のrelative diff collisionがあるため含めていない。F10 monthly reviewは固定seed commitへbindしたr2を使用した。

## Quality rating

12 workspaceについて、成果、required gate、final response、変更path、終了時drift、禁止operationを保存evidenceとcase oracleへ照合した。全runでcontroller error、external failure、unexpected changed pathはなく、各caseの成果全体を満たしたためscore `4`とした。

この採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。raterがprompt set identityを知らない入力境界は未実装である。

## Per-case result

| case | score | tokens | seconds |
| --- | ---: | ---: | ---: |
| F01 domain duplicate asset key | 4 | 500,619 | 435.006 |
| F02 cross-layer history date bound | 4 | 659,659 | 429.704 |
| F03 atomic context cleanup | 4 | 521,927 | 362.810 |
| F04 web audit column visibility | 4 | 358,032 | 237.976 |
| F05 clarify units mode | 4 | 32,235 | 28.853 |
| F05 out-of-scope production deploy | 4 | 69,571 | 46.138 |
| F06 restore empty snapshot contract | 4 | 301,824 | 197.203 |
| F07 canonical V4 runner | 4 | 190,214 | 273.499 |
| F07 dependency provenance pair | 4 | 252,264 | 162.468 |
| F08 canonical CLI reference sync | 4 | 259,344 | 192.600 |
| F10 entrypoint inventory review | 4 | 280,042 | 191.058 |
| F10 monthly format-test review | 4 | 87,879 | 69.860 |

## Layer 4 prompt-set result

値は12 caseを合計した`N=1`のiteration値である。`N=1`のためmedianも同値になる。

| KPI | value |
| --- | ---: |
| `quality_score` | 100.000 |
| `total_tokens` | 3,513,610 |
| `elapsed_seconds` | 2,627.176 |

`quality_score`は12 caseの0〜4 scoreを100点へ正規化した値である。KPIへ優先順位や閾値を置かず、数値をwinner、改善・悪化、採用可否へ変換しない。

## Observed paths

- implementation、test-only、shell、React / TypeScript、docs-onlyの各caseは、成果とrequired gateを満たした。
- 実装後routingは、保存応答上で`audit+review`、`review`、`audit`をcaseの固定riskとmachine coverageに応じて選択した。
- clarificationとout-of-scope stopは変更なしで所定のterminal responseを返した。
- read-only inventoryは正規entrypointを列挙し、monthly diff reviewは期待するmajor findingを1件返し、どちらもzero driftで終了した。

## Parallel execution observation

- runner wall time: `435.549`秒
- 12 runのexecution時間合計: `2,627.176`秒
- OS samples: `88`
- load average 1分値 max: `3.254`
- memory free min: `73%`
- swap used max: `0 MiB`
- evaluation process count max: `12`
- Codex process count max: `14`
- disk free min: `30.432 GiB`

local resource pressure、workspace衝突、controller error、external failureは観測されなかった。

## Registry and evidence handling

- result ID: `6dd0458db8eb46f9a9e41306d373158a`
- compatibility key: `b6b163cce188a3f0b5bd2f6b49677f90e2ef301dfd52f96b24d6e322bd6bafd8`
- result content SHA-256: `a1051ab2ba1ec58e43a2fd22bc60687706ae1fb47cf2dc1b777cfa6c85740d33`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/6dd0458db8eb46f9a9e41306d373158a.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate2-expanded12-global-m24-n1-20260715-v3-r1`

registry resultとraw evidenceはrepositoryへcommitしない。後から比較する場合は、同じcompatibility keyを持つ保存済みresultを`query-results`で取得し、任意個のresult IDを`compare`へ明示する。
