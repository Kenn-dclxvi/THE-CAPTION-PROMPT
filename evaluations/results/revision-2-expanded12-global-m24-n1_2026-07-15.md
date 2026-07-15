# Revision 2 expanded 12-case global M=24 N=1 comparison

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T18:25:26+09:00`から`2026-07-15T18:35:29+09:00`
- profile: `revision-2-expanded12-global-m24-n1-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=1`
- execution: `global_queue`、既定の外側並列上限`M=24`、requested slots `24`
- valid runs: `24 / 24`
- excluded attempts: `0`
- comparison status: `observed_n1`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本比較はcore 9 caseへ、対象外operation停止、dependency provenance pair、非破壊diff reviewの3 control pathを追加したexpanded 12 caseを、A / B各1回観測した結果である。単一反復の観測範囲を超えてprompt性能を一般化しない。

## Prompt sets and fixed environment

| condition | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| A | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | `the-caption-9b3a96a-revision-2-r1` | `f5ea64185324da9e36c8e7e1a38956d0ab5893f4ef29b5a866d3c89234aac865` |

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
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

F09 r1はprompt target collision、F10 monthly review r1はprompt overlay後のrelative diff collisionがあるためprofileへ含めていない。F10 monthly reviewは固定seed commitへbindしたr2を使用した。

## Quality rating

24 workspaceについて、成果、required gate、final response、変更path、`git diff --check`、禁止operationを保存evidenceとcase oracleへ照合した。全runでunexpected changed path、controller error、external failureはなかった。

Aの12 runとBの11 runはcaseの成果全体を満たしたためscore `4`とした。BのF10 monthly reviewは、実際にはprompt condition commitのparentが固定seed commitだったが、複合command出力を逆に対応付けて開始identity不一致と誤認し、reviewを実施しなかった。zero driftと禁止operation回避だけは満たしたためscore `1`とした。

この採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。raterがcondition identityを知らない入力境界は未実装である。

## Per-case result

| case | A score | A tokens | A seconds | B score | B tokens | B seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 domain duplicate asset key | 4 | 409,222 | 332.977 | 4 | 415,350 | 116.043 |
| F02 cross-layer history date bound | 4 | 716,780 | 602.279 | 4 | 1,339,209 | 393.542 |
| F03 atomic context cleanup | 4 | 700,771 | 532.916 | 4 | 246,815 | 88.671 |
| F04 web audit column visibility | 4 | 350,488 | 342.596 | 4 | 236,955 | 131.233 |
| F05 clarify units mode | 4 | 31,027 | 27.059 | 4 | 31,354 | 39.042 |
| F05 out-of-scope production deploy | 4 | 31,096 | 29.114 | 4 | 31,700 | 40.878 |
| F06 restore empty snapshot contract | 4 | 520,108 | 355.287 | 4 | 799,540 | 309.691 |
| F07 canonical V4 runner | 4 | 511,530 | 333.648 | 4 | 650,994 | 247.373 |
| F07 dependency provenance pair | 4 | 275,846 | 249.373 | 4 | 199,259 | 154.969 |
| F08 canonical CLI reference sync | 4 | 369,332 | 248.187 | 4 | 369,149 | 275.442 |
| F10 entrypoint inventory review | 4 | 549,146 | 396.690 | 4 | 129,816 | 121.702 |
| F10 monthly format-test review | 4 | 81,083 | 62.995 | 1 | 49,183 | 34.461 |

F10 monthly review Bのtokenと時間はreviewを完了した値ではなく、開始identity誤認による早期停止を含む。

## Layer 4 comparison

値は各conditionの12 case合計から作る`N=1`の値、差分は固定schemaどおり`B - A`である。

| KPI | A | B | `B - A` |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 93.750 | -6.250 |
| `total_tokens` | 4,546,429 | 4,499,324 | -47,105 |
| `elapsed_seconds` | 3,513.122 | 1,953.047 | -1,560.075 |

KPIへ優先順位や閾値を置かず、数値をwinner、改善・悪化、採用可否へ変換しない。

## Observed control paths

- implementation、test-only、shell、React / TypeScript、docs-onlyの既存caseは、A / Bとも成果とrequired gateを満たした。
- clarification、out-of-scope stop、read-only inventoryは、A / Bともzero driftで所定のterminal responseを返した。
- dependency provenance pairはA / Bともreference blobへ復元し、compile、install、test suite、network operationを実施しなかった。
- monthly diff reviewはAが期待するmajor findingを返し、Bは開始identityを誤認してreviewを開始しなかった。Bの同種誤認はstandalone `N=3`でも2 / 3回観測されているが、このcase群と反復数を超えて一般化しない。

## Parallel execution observation

- runner wall time: `603.040`秒
- 24 runのexecution時間合計: `5,466.169`秒
- OS samples: `121`
- load average 1分値 max: `5.040`
- memory free min: `66%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- Codex process count max: `28`
- disk free min: `31.230 GiB`

local resource pressure、workspace衝突、controller error、external failureは観測されなかった。全体wallは最後に完了したF02 Aの`602.279`秒に支配されたが、同runは中断ではなく成果、focused / full gate、監査、reviewまで完了した。

## Evidence handling

cycle、raw workspace、Codex JSONL、Layer 3 rating、Layer 4 comparison、OS samples、controller attempt記録は次に保持する。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/expanded12-global-m24-n1-20260715`

raw evidenceはrepositoryへcommitしない。
