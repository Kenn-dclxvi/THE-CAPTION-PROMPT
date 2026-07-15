# Revision 2 core 9-case N=1 comparison

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-14T21:46:49Z`から`2026-07-14T23:00:52Z`
- set ID: `the-caption-revision-2-core9-r1`
- repetition: `N=1`
- execution: 直列、caseごとにA / B先行順を交互化
- valid runs: `18 / 18`
- external failure: `1`件を除外し、同じ反復を自動補充
- Layer 4: `winner: b`
- comparison status: `preliminary_n1`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本比較はF09を除外した9 caseについて、固定条件下でbaselineとcandidateを各1回実行した初回比較である。単一反復のため、この観測範囲を超えてprompt性能を一般化しない。

## Prompt sets

| condition | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| A | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | `the-caption-9b3a96a-revision-2-r1` | `f5ea64185324da9e36c8e7e1a38956d0ab5893f4ef29b5a866d3c89234aac865` |

## Cases

対象はF01、F02、F03、F04、F05、F06、F07、F08、F10である。F09はfixture condition pathの`tests/AGENTS.md`と両prompt bundleのtargetが衝突するため、実行前に除外した。これは実行時の外部失敗ではなく、現行file bundle方式では同じ条件を作れないcase設計上の除外である。

## Fixed execution environment

- model: `gpt-5.6-sol`
- reasoning effort: `high`
- Codex CLI: `codex-cli 0.144.0`
- sandbox: `workspace-write`
- approval policy: `never`
- session mode: `persisted`
- `multi_agent`: enabled
- `agents.max_threads`: `4`
- memories: disabled
- shared Python: `3.14.5`
- runtime materialization: `venv_shim`
- runtime identity SHA-256: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`

各fixtureは独立workspaceで、中央の固定Python package setをlocal `.venv` shimから参照した。Node dependencyはF04のworkspace内だけへ作成し、終了前に削除した。

## Environment correction before the final cycle

最初のcycleでは、isolated fixtureにGit-ignoredな`logs/` directoryが存在しなかった。Python testのexit code自体は0だったが、loggerが`logs/test.log`を開けずlogging errorを発生させた。Aはそのまま完了扱いにするrunがあり、Bは環境failureとして停止したため、このcycleをprompt比較へ使わなかった。

fixture生成時に空の`logs/`をmaterializeするよう修正し、9 fixtureすべてで存在を確認した新しいcycleを最初から実行した。最終cycleでは各Python workspaceに`logs/test.log`が生成され、logging errorは再発していない。

また、最終cycleのF03 A初回attemptは約12分後にCodex JSONLで`Selected model is at capacity`を返した。adapterが`error` / `turn.failed` eventから`codex_model_at_capacity`を自動検知し、runを`excluded`としてraw evidenceとともに保存した。同じcase、condition、repetitionを自動再実施し、有効回数をA / Bで揃えた。除外attemptのtokenと時間はKPIへ入れていない。

## Quality rating

保存workspace、reference postimage、final drift、command結果、terminal responseを照合した。18有効runすべてで`logs/`存在、`git diff --check`成功、unexpected changed path 0を確認した。

F01 AとF03 Aは、期待された成果とrequired validationを満たした一方、TaskSpecで定義されていない周辺境界を監査またはレビューが停止指摘にし、terminal outcomeが未完了となったためscore `3`とした。それ以外はcaseの成果全体とrequired evidenceが揃ったためscore `4`とした。

この採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。raterがcondition identityを知らない入力境界は未実装であり、正式なblind qualificationではない。

## Per-case result

| case | A score | A tokens | A seconds | A terminal | B score | B tokens | B seconds | B terminal |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| F01 | 3 | 502,928 | 379.4 | TaskSpec外の呼出し元riskを重大指摘として停止 | 4 | 257,672 | 68.6 | complete |
| F02 | 4 | 577,632 | 360.4 | complete | 4 | 518,649 | 138.9 | complete |
| F03 | 3 | 442,131 | 238.7 | 未定義のunlink恒久失敗を停止指摘として停止 | 4 | 280,855 | 99.3 | complete |
| F04 | 4 | 376,377 | 368.9 | complete | 4 | 304,747 | 129.2 | complete |
| F05 | 4 | 31,669 | 38.8 | clarification | 4 | 31,880 | 20.4 | clarification |
| F06 | 4 | 577,341 | 473.5 | complete | 4 | 577,852 | 216.2 | complete |
| F07 | 4 | 276,220 | 279.3 | complete | 4 | 1,020,401 | 311.0 | complete |
| F08 | 4 | 343,638 | 269.1 | complete | 4 | 273,207 | 172.7 | complete |
| F10 | 4 | 88,462 | 74.7 | read-only complete | 4 | 125,462 | 83.1 | read-only complete |

F01とF03のA / Bはそれぞれ同じ正解成果を作っており、quality差は成果物の意味差ではなく、AがTaskSpec外の境界指摘を停止理由として扱ったterminal dispositionの差である。

## Layer 4 result

| KPI | A | B | difference |
| --- | ---: | ---: | ---: |
| `quality_score` | 94.444 | 100.000 | Bが5.556 point高い |
| `total_tokens` | 3,216,398 | 3,390,725 | Bが174,327多い（A比5.4%） |
| `elapsed_seconds` | 2,482.859 | 1,239.273 | Bが1,243.585秒短い（A比50.1%） |

固定判定規則はquality、token、時間の順で比較する。qualityでBが上回ったため、tokenと時間で逆転させず`winner: b`となった。この9 case、`N=1`の観測範囲ではBをAに対する改善として扱う。

Bの合計tokenはAより多い。特にF07 Bの`1,020,401` tokensが全体を押し上げている。一方、合計時間はBが約20.7分、Aが約41.4分だった。既存のbit-identical bundle N=10 null calibrationではSA待機pollingによりtokenと時間が大きく揺れたため、本比較のperformance値を単一反復から一般化しない。今回のwinnerはperformanceではなくquality差で確定している。

## Judgement

最終cycleは、fixture環境欠陥を除去した後に18有効runを揃え、外部capacity failureを自動除外して不足回数を補充できた。したがって、case variationとexecution経路の初回end-to-end確認は成立した。

ただし、`N=1`、F09除外、非blind採点、既知のperformance calibration未成立という制約がある。この結果だけでrelease、adoption、THE-CAPTION本体反映を判断しない。

## Evidence handling

最終cycleは次に保持する。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/revision-2-core9-n1-20260715/cycle-logs-fixed`

raw workspace、Codex JSONL、stdout / stderr、除外attemptはlocal evidenceであり、repositoryへcommitしない。比較前に破棄したcycleもfixture欠陥と検知修正の調査根拠として同じrun rootに保持する。
