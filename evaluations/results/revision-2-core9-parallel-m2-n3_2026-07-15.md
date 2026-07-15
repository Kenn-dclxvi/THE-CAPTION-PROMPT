# Revision 2 core 9-case parallel M=2 N=3 comparison

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T09:32:16+09:00`から`2026-07-15T11:42:58+09:00`
- set ID: `the-caption-revision-2-core9-r1`
- repetition: `N=3`
- execution: 外側並列`M=2`、同一case・反復のA / Bを同じwaveへ配置
- valid runs: `54 / 54`
- external failure / retry: `0 / 0`
- Layer 4: `winner: b`
- comparison status: `observed_n3`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本比較はF09を除外した9 caseについて、固定条件下でbaselineとcandidateを各3回実行した結果である。`N=3`の観測範囲を超えてprompt性能を一般化しない。

## Prompt sets

| condition | role | prompt identity | bundle SHA-256 |
| --- | --- | --- | --- |
| A | baseline | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | candidate | `the-caption-9b3a96a-revision-2-r1` | `f5ea64185324da9e36c8e7e1a38956d0ab5893f4ef29b5a866d3c89234aac865` |

## Cases and fixed environment

対象はF01、F02、F03、F04、F05、F06、F07、F08、F10である。F09はfixture condition pathの`tests/AGENTS.md`と両prompt bundleのtargetが衝突するため、既存判断どおり除外した。

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

外側並列`M=2`は、直前のTC-F01 r2 identical-bundle `N=3` qualificationでworkspace衝突、resource saturation、controller failureがないことを確認してから使用した。

## Execution integrity

27 wave、54 slotがすべて有効終了した。external failureとして除外されたattemptはなく、controller errorもなかった。

54 workspaceについてexecution status、exit code、token、terminal response、tracked drift、oracle postimageを照合した。全runがexit 0で、許可外changed pathは0件だった。132個のreference postimage fileを照合し、113個はblob一致、19個は非exclusive oracle内の意味的に同等な実装またはtest強化だった。後者はF03のcleanup表現、F04のtruthy判定表現、F02 / F06のcontract assertion追加であり、禁止されたtest弱体化ではない。

## Quality rating

成果物、required gate、drift、terminal dispositionをrunごとに照合した。48 runをscore `4`、6 runをscore `3`とした。

score `3`は、期待成果とrequired validationを満たした一方でterminal outcomeを未完了として返したrunである。

- A: F01 repetition 1、F07 repetition 1、F03 repetition 2
- B: F03 repetition 3、F06 repetition 3、F07 repetition 3

停止理由はTaskSpec外の周辺risk、未定義の恒久filesystem failure、またはfocused / full gate重複の契約解釈だった。成果物の意味差だけでなく、与えられた作業単位を完了として閉じる能力を成果全体へ含めている。

この採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。raterがcondition identityを知らない入力境界は未実装である。

## Per-case result

tokenと時間は3反復のcase内median、scoreは反復順に示す。

| case | A scores r1/r2/r3 | A median tokens | A median sec | B scores r1/r2/r3 | B median tokens | B median sec |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| F01 | 3/4/4 | 427,939 | 262.5 | 4/4/4 | 256,507 | 81.5 |
| F02 | 4/4/4 | 548,864 | 389.5 | 4/4/4 | 514,707 | 198.2 |
| F03 | 4/3/4 | 453,149 | 329.3 | 4/4/3 | 318,331 | 108.2 |
| F04 | 4/4/4 | 442,936 | 346.7 | 4/4/4 | 290,655 | 121.0 |
| F05 | 4/4/4 | 31,805 | 22.5 | 4/4/4 | 31,169 | 13.4 |
| F06 | 4/4/4 | 382,517 | 321.3 | 4/4/3 | 521,270 | 235.7 |
| F07 | 3/4/4 | 553,408 | 275.9 | 4/4/3 | 871,984 | 271.4 |
| F08 | 4/4/4 | 374,920 | 270.6 | 4/4/4 | 320,346 | 177.9 |
| F10 | 4/4/4 | 339,638 | 291.5 | 4/4/4 | 89,154 | 72.7 |

## Layer 4 result

固定規則どおり、各反復で9 caseを集計し、その3反復のmedianを比較した。

| KPI | A baseline | B candidate | difference |
| --- | ---: | ---: | ---: |
| `quality_score` | 97.222 | 100.000 | Bが2.778 point高い |
| `total_tokens` | 3,482,836 | 3,357,482 | Bが125,354少ない（A比3.6%） |
| `elapsed_seconds` | 2,450.456 | 1,404.102 | Bが1,046.354秒短い（A比42.7%） |

反復別qualityはAが`94.444 / 97.222 / 100.000`、Bが`100.000 / 100.000 / 91.667`だった。quality medianでBが上回ったため、tokenと時間で逆転させず`winner: b`となった。この9 case、`N=3`の観測範囲ではBをAに対する改善として扱う。

Bもrepetition 3では3件を未完了停止しており、全反復で一様に優位ではない。terminal dispositionの揺れは未解決事項として残す。

## Parallel and OS observation

- runner wall time: `7,842.376`秒（2時間10分42秒）
- 54 runの実測時間を逐次合計した値: `11,740.690`秒（3時間15分41秒）
- observed speedup: `1.497x`
- wall time reduction: `33.2%`
- wave max合計との差: `0.034`秒
- OS samples: `522`
- load average 1分値: median `1.913`、max `3.711`
- memory free: median `80%`、min `67%`
- swap used max: `0 MiB`
- disk free min: `28.609 GiB`
- monitor sample error: `0`

外側runnerのoverheadは小さく、local resource saturationも観測されなかった。`1.497x`に留まった主因は、同一wave内のA / B実行時間差と、長い側を待って次waveへ進むbarrierである。より大きい`M`の適格性はこの結果から判断しない。

## Judgement

`M=2`の並列実行は、固定case・反復を欠落や混在なく実行し、OS余力を保ったまま直列相当時間を短縮できた。並列実行extensionはLayer 2に限定され、rating、KPI comparison、release判断へ越境していない。

prompt比較は固定規則で`winner: b`となった。ただし`N=3`、F09除外、非blind採点、terminal dispositionの反復揺れがある。この結果だけでrelease、adoption、THE-CAPTION本体反映を判断しない。

## Evidence handling

cycle、raw workspace、Codex JSONL、Layer 3 rating、Layer 4 decision、OS samples、controller attempt記録は次に保持する。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/revision-2-core9-parallel-m2-n3-20260715`

raw evidenceはrepositoryへcommitしない。
