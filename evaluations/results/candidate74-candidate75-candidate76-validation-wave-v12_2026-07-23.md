# Candidate74 / Candidate75 / Candidate76 validation wave 第12版評価

## 結論

Candidate75はCandidate74の型付き状態構造を維持したまま、F06のfocused / full test同時発行を`0 / 5`から`5 / 5`へ回復した。ただしpost-test final stateを観測するdiff / path確認まで4 / 5でtest waveへ入れたため、target version dependencyを保持できず停止した。

Candidate76はfinal-state observerを後続waveへ固定した。F06 targeted N=5では、focused / full同時発行`5 / 5`、final-state observerのpost-test wave`5 / 5`、全required validation後の追加read / validation`0 / 5`、score `4 = 5`を満たした。

標準14項目N=5ではCandidate76の70 / 70 runがvalidかつrateableだったが、score分布は`4 = 69 / 3 = 1`だった。A02 iteration 2で`git diff --check`の成功証拠が欠落したため、Candidate76を`stopped`とする。採用、release、THE-CAPTION本体反映へ進めない。

## 変更境界

| Candidate | direct source | 変更 | 維持 |
| --- | --- | --- | --- |
| Candidate75 | Candidate74 | authority-bound independent validation fast path | C74のauthority、identity、state axis、producer、DAG、METHOD / RECOVERY |
| Candidate76 | Candidate75 | potential mutatorからfinal-state observerへのtarget-version dependency | C75までの全構造とindependent fast path |

## F06 targeted N=5

固定条件はF06 revision `r2`、第12版採点、model `gpt-5.6-sol`、global queue `M=5`、各`N=5`、all-agent token accounting `v1`である。3 resultのcompatibility keyは`dad6b2d2fea74c17b7976420eb225769dd524a8bb089016a0ab6359bf7ebe1e0`で一致する。

| Prompt | score分布 | token中央値 | elapsed中央値 | 5 run token合計 |
| --- | ---: | ---: | ---: | ---: |
| Candidate74 | `4 = 5` | 362,370 | 111.048秒 | 1,770,571 |
| Candidate75 | `4 = 5` | 296,605 | 114.827秒 | 1,341,797 |
| Candidate76 | `4 = 5` | 206,100 | 83.856秒 | 1,102,759 |

Candidate74比でCandidate76のtoken中央値は`-156,270`（`-43.12%`）、elapsed中央値は`-27.192秒`（`-24.49%`）、token合計は`-667,812`（`-37.72%`）だった。

### behavior trace

| Prompt | focused / full同一wave | final-state確認がpost-test wave | 成功後追加readなし |
| --- | ---: | ---: | ---: |
| Candidate74 | `0 / 5` | `5 / 5` | `5 / 5` |
| Candidate75 | `5 / 5` | `1 / 5` | `5 / 5` |
| Candidate76 | `5 / 5` | `5 / 5` | `5 / 5` |

Candidate75 iteration 4のtraceは、testがreport等を生成し得るためdiff / path確認はtest後の最終worktreeを対象にすべきだと明示した。この観測により「全required validationを1 wave」という初期gateを棄却し、Candidate76で独立test waveとfinal-state observer waveを分離した。

### 保存result

- Candidate74: `cec0c99d9be447c6b3911091bcd0f60c`
- Candidate75: `3773c086021648b791297a387df8fb17`
- Candidate76: `1709082cf43a49f9a2eea43950450800`
- comparison view: `candidate76-final-state-validation-wave-v12-validation-fast-path-f06-global-m5-n5-20260723-r1/comparison-c74-c75-c76.json`

## Candidate76標準14項目N=5

固定条件は`the-caption-standard14-r1`、第12版採点、model `gpt-5.6-sol`、global queue `M=24`、14 case × `N=5`、all-agent token accounting `v1`である。Candidate74 resultとのcompatibility keyは`d975daefc55ae9914230e5d0fbf03f2f5325ab9f30e3d79f30a4239c7f7b0c78`で一致する。

| Prompt | score分布 | quality中央値 | token中央値 | elapsed中央値 | 70 run token合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Candidate74 | `4 = 70` | 100.000 | 3,366,548 | 1,140.329秒 | 16,812,026 |
| Candidate76 | `4 = 69 / 3 = 1` | 100.000 | 2,901,382 | 1,098.945秒 | 14,477,086 |

Candidate76 - Candidate74の中央値差はquality `0.000`、token `-465,166`（`-13.82%`）、elapsed `-41.383秒`（`-3.63%`）だった。70 run token合計差は`-2,334,940`（`-13.89%`）である。quality中央値が同じでもscore分布は一致せず、品質維持とは判定しない。

### quality failure

- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING`
- iteration: `2`
- run id: `24e4a8ac5de14b9e95674e038c7a5f11`
- failure: `a02_missing_successful_command:diff_check`
- trace: `bash -n run.sh`とtests全体は成功し、最終`git diff -- run.sh`と`git status --short`も実行したが、`git diff --check`を実行しなかった。

この欠落をCandidate76の評価後に採点基準へ合わせてin-place修正しない。新しい制御根拠なしに`git diff --check`という特定commandをroot promptへ追加すると、方法制約の試験対策になるためである。

### 保存result

- Candidate74 reference: `a5c74ebb0e9640b89bff11aaeb903a59`
- Candidate76: `6200b15874f94900b6d0fc373c363e08`
- comparison view: `candidate76-final-state-validation-wave-v12-standard14-global-m24-n5-20260723-r1/comparison-c74-c76.json`

## 判定境界

Candidate76はF06の狙ったwave topologyと標準14のtoken / elapsed低下を観測した。しかし標準14でrequired evidence欠落が1件あるため、品質gateは不合格である。KPI低下を採用またはrelease根拠へ読み替えない。

Candidate75とCandidate76は履歴として保持する。次candidateを作る場合は、A02の欠落が同じ一般predicateから再現することを保存traceで確認し、特定case / command名をroot promptへ書かずに消せる判断点が定義できた場合だけ作成する。
