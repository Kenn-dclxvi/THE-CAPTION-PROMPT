# Revision 2 core 9-case global M=4 staged N=3 comparison

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T12:32:38+09:00`から`2026-07-15T13:54:34+09:00`
- profile: `revision-2-core9-global-m4-r2`
- set ID: `the-caption-revision-2-core9-r2`
- execution: barrierなしの`global_queue`、外側並列`M=4`、estimated duration降順
- staged repetition: N=1 screenの`winner: b`を受けて同じcycleへrepetition 2 / 3を追加
- final repetition: `N=3`
- valid runs: `54 / 54`
- external failure / retry: `0 / 0`
- Layer 4: `winner: a`
- comparison status: `observed_n3`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本比較はF09を除外した9 caseについて、固定条件下でbaselineとcandidateを各3回実行した結果である。`N=3`の観測範囲を超えてprompt性能を一般化しない。

## Prompt sets

| condition | role | prompt identity | bundle SHA-256 |
| --- | --- | --- | --- |
| A | baseline | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | candidate | `the-caption-9b3a96a-revision-2-r1` | `f5ea64185324da9e36c8e7e1a38956d0ab5893f4ef29b5a866d3c89234aac865` |

## Cases and fixed environment

対象revisionはF01 r3、F02 r1、F03 r2、F04 r1、F05 r1、F06 r2、F07 r2、F08 r1、F10 r1である。F01 / F03 / F06 / F07は、前回結果でTaskSpec外の周辺riskやrequired gate重複を未完了理由にした揺れを減らすため、新しいcase contract revisionを使用した。F09はprompt target collisionのため除外した。

- model: `gpt-5.6-sol`
- reasoning effort: `high`
- Codex CLI: `codex-cli 0.144.0`
- sandbox: `workspace-write`
- approval policy: `never`
- `multi_agent`: enabled
- `agents.max_threads`: `4`
- memories: disabled
- shared Python: `3.14.5`
- runtime identity SHA-256: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`

外側並列`M=4`は、直前のF01 r3 / F04 r1 identical-baseline `N=2` qualificationで8 / 8 valid、retry 0、workspace衝突0、swap 0を確認してから使用した。

## Staged screen

repetition 1だけを採点した時点ではqualityが同点で、tokenの少ないBがscreenを通過した。main cycleへLayer 4 decisionは書き込まず、同じfrozen setとprompt identityへrepetition 2 / 3を追加した。

| KPI | A baseline | B candidate |
| --- | ---: | ---: |
| `quality_score` | 97.222 | 97.222 |
| `total_tokens` | 3,790,333 | 3,399,430 |
| `elapsed_seconds` | 2,938.942 | 1,778.404 |

N=1 screenは`winner: b`だったが、final judgementではなく追加反復を開始する条件としてだけ使用した。

## Execution integrity

54 slotはすべてattempt 1、controller exit 0、execution status `valid`で終了した。外部要因として除外されたattemptはなく、再実施もなかった。

54 workspaceのtracked差分を確認し、各caseの許可pathと一致した。F05 / F10はzero driftで、他caseも許可外changed pathは0件だった。case、condition、repetitionごとに独立workspaceを使い、runの混在やworkspace衝突はなかった。

## Quality rating

成果物、required gate、drift、terminal dispositionをrunごとに照合した。51 runをscore `4`、3 runをscore `3`とした。

score `3`は成果と主要validationを満たした一方、terminal outcomeを未完了として返したrunである。

- A: F04 repetition 1。Node validation後のtemporary output cleanup commandが実行policyに拒否された。
- B: F06 repetition 1。対象testと全体pytestを満たしたが、required gate重複の契約解釈で停止した。
- B: F04 repetition 3。Node validation後のtemporary output cleanup commandが実行policyに拒否された。

F01 r3、F03 r2、F07 r2は全6 runがscore `4`で、改訂対象だった周辺risk、未定義のcleanup恒久失敗、既存default routingを未完了理由にしなかった。F06 r2もrepetition 2 / 3ではA / Bとも完了したが、B repetition 1の停止が残り、terminal dispositionの揺れを完全には除去できていない。

この採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。raterがcondition identityを知らない入力境界は未実装である。

## Per-case result

tokenと時間は3反復のcase内median、scoreは反復順に示す。

| case | A scores r1/r2/r3 | A median tokens | A median sec | B scores r1/r2/r3 | B median tokens | B median sec |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| F01 | 4/4/4 | 539,808 | 352.985 | 4/4/4 | 268,082 | 84.497 |
| F02 | 4/4/4 | 655,231 | 464.113 | 4/4/4 | 776,579 | 383.777 |
| F03 | 4/4/4 | 634,078 | 477.651 | 4/4/4 | 297,369 | 188.433 |
| F04 | 3/4/4 | 405,123 | 442.087 | 4/4/3 | 234,993 | 226.448 |
| F05 | 4/4/4 | 31,029 | 19.050 | 4/4/4 | 49,096 | 37.405 |
| F06 | 4/4/4 | 591,279 | 329.782 | 3/4/4 | 648,180 | 280.506 |
| F07 | 4/4/4 | 835,485 | 747.328 | 4/4/4 | 785,929 | 429.647 |
| F08 | 4/4/4 | 338,621 | 362.367 | 4/4/4 | 574,286 | 745.454 |
| F10 | 4/4/4 | 88,848 | 110.205 | 4/4/4 | 128,418 | 104.371 |

## Layer 4 result

固定規則どおり、各反復で9 caseを集計し、その3反復のmedianを比較した。

| KPI | A baseline | B candidate | difference |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 97.222 | Aが2.778 point高い |
| `total_tokens` | 4,160,915 | 3,399,430 | Bが761,485少ない（A比18.3%） |
| `elapsed_seconds` | 3,527.482 | 2,136.693 | Bが1,390.789秒短い（A比39.4%） |

反復別qualityはAが`97.222 / 100.000 / 100.000`、Bが`97.222 / 100.000 / 97.222`だった。quality medianでAが上回ったため、tokenと時間で逆転させず`winner: a`となった。この9 case、`N=3`の観測範囲ではBをAに対する改善として扱わない。

N=1ではB、N=3ではAとなった。N=3での差も、3件の未完了terminal outcomeの反復位置によって生じている。単一screen結果の採用判断への使用と、少数反復の過度な一般化は避ける。

## Global queue and OS observation

- active runner wall time: `4,851.510`秒（1時間20分52秒）
- 54 runのexecution時間を逐次合計した値: `18,878.298`秒（5時間14分38秒）
- observed speedup: `3.891x`
- wall time reduction: `74.3%`
- OS samples: `323`
- load average 1分値: median `2.477`、max `7.405`
- memory free: median `76%`、min `73%`
- swap used max: `0 MiB`
- disk free min: `25.191 GiB`
- evaluation process count max: `4`
- monitor sample error: `0`

queueは過去のcase・condition別median所要時間が長い順にslotを投入し、workerが空き次第次のslotを開始した。A / Bの実行環境を揃えるqueue操作、時間補正、token補正は行っていない。

case barrierを外したことで長い1本を待たず他workerが次へ進み、active runner wallは逐次実行時間の25.7%になった。一方、最長runはF06 baseline repetition 3の`1,783`秒で、local resource saturationなしでも単一run内部の待機が長いtailとして残った。`M=4`はこのtailを消さず、他slotへの波及を抑える。

## Judgement

barrierなしglobal queueと`M=4`は、54 runを欠落や混在なく実行し、local resource余力を保ったままwall timeを短縮した。parallel execution extensionはLayer 2に限定され、rating、KPI comparison、release判断へ越境していない。

prompt比較は固定規則で`winner: a`となった。したがってcandidate Bは今回のevaluation setと`N=3`では改善ではない。これはrelease不採用やTHE-CAPTION本体への反映判断そのものではなく、評価基盤の比較出力である。

## Evidence handling

cycle、raw workspace、Codex JSONL、Layer 3 rating、Layer 4 decision、OS samples、controller attempt記録は次に保持する。

`/Users/kenn/repos/THE-CAPTION-prompt-ab-measurement/runs/revision-2-core9-r2-global-m4-staged-20260715`

raw evidenceはrepositoryへcommitしない。
