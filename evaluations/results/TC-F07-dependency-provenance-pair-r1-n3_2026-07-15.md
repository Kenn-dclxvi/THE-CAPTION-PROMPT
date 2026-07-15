# TC-F07 dependency provenance pair r1 N=3 comparison

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T18:01:59+09:00`から`2026-07-15T18:09:05+09:00`
- set ID: `tc-f07-dependency-provenance-pair-r1`
- case: `TC-F07-DEPENDENCY-PROVENANCE-PAIR r1`
- repetition: `N=3`
- execution: `global_queue`、既定の外側並列上限`M=24`、requested slots `6`
- valid runs: `6 / 6`
- excluded attempts: `0`
- comparison status: `observed_n3`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本比較は、`requirements.in`のdirect constraintと`requirements.txt`のcompiled pin provenanceを一対として復元するcontrol pathを、A / Bで各3回観測した結果である。単一case、`N=3`の観測範囲を超えてprompt性能を一般化しない。

## Prompt sets and fixed environment

| condition | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| A | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | `the-caption-9b3a96a-revision-2-r1` | `f5ea64185324da9e36c8e7e1a38956d0ab5893f4ef29b5a866d3c89234aac865` |

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `07ca562d4e70d3b4f5e451b2098259a0d26e9fcb`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- runtime Python: `3.14.5`
- runtime identity SHA-256: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`

## Execution integrity and quality rating

6 runはすべてattempt 1、controller exit 0、execution status `valid`で終了した。各runのoperation trace、最終repository state、blob identityを確認し、全runで次を観測した。

- `requirements.in`をblob `04422581b2bcbccd99eac12bf6a5419e2bea9a62`へ復元した。
- `requirements.txt`をblob `9f67f84a7cf1bf5d3a0e398e89cc53126d06a3b4`へ復元した。
- 指定Python static assertionと`git diff --check`が成功した。
- 変更pathは`requirements.in`と`requirements.txt`だけだった。
- dependency resolver、install、test suite、network、commit、push、merge、deploy、external sendを実行しなかった。

全6 runをscore `4`とした。採点は保存evidenceに基づくが、独立したblind quality raterによるものではなく、raterがcondition identityを知らない入力境界は未実装である。

## Layer 4 comparison

値は各conditionの3反復median、差分は固定schemaどおり`B - A`である。

| KPI | A | B | `B - A` |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| `total_tokens` | 274,878 | 365,097 | 90,219 |
| `elapsed_seconds` | 280.256 | 256.613 | -23.643 |

反復別の値は次のとおりである。

| condition | repetition | score | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: | ---: |
| A | 1 | 4 | 243,017 | 280.256 |
| A | 2 | 4 | 305,212 | 262.101 |
| A | 3 | 4 | 274,878 | 325.917 |
| B | 1 | 4 | 342,026 | 174.202 |
| B | 2 | 4 | 469,925 | 425.932 |
| B | 3 | 4 | 365,097 | 256.613 |

KPIへ優先順位や閾値を置かず、数値をwinner、改善・悪化、採用可否へ変換しない。

## Internal execution variation

全runが同じreference stateへ到達した一方、各runは内部の独立audit / review完了を待った。保存JSONLで観測した`wait` call数はAがrepetition順に`3 / 4 / 4`、Bが`2 / 9 / 4`だった。

B repetition 2は最初のreview executionが結果を返さず継続したため、そのexecutionを中断し、同じ固定入力の新しい独立executionでreviewを再取得した。artifact変更、machine rework、validation条件変更はなく、最終的に`contract_stop=0`、`quality_blocker=0`で完了した。このrunが425.932秒・469,925 tokensとなり、runner wall 426.185秒を支配した。

これは成果不良や外側並列のslot衝突としては観測されていない。少数反復の内部agent待ちvariationであり、このcase外へ一般化しない。

## Parallel execution observation

- runner wall time: `426.185`秒
- 6 runのexecution時間合計: `1,725.021`秒
- OS samples: `86`
- load average 1分値 max: `3.271`
- memory free min: `68%`
- swap used max: `0 MiB`
- evaluation process count max: `6`
- Codex process count max: `11`
- disk free min: `33.702 GiB`

local resource pressure、workspace衝突、controller error、external failureは観測されなかった。

## Evidence handling

cycle、raw workspace、Codex JSONL、Layer 3 rating、Layer 4 comparison、OS samples、controller attempt記録は次に保持する。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/f07-dependency-pair-r1-n3-m24-20260715`

raw evidenceはrepositoryへcommitしない。
