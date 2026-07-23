# Candidate71 control abstraction分析

## 結論

Candidate71のKPI差から確認できる因果は、11 label全体ではなく、Candidate69へ追加した`VALIDATION_CLOSURE`一行の効果に限定される。

その効果は「細かい試験手順」ではなく、変更後に行動集合が確定したら、全validationを一度に発行し、全result受領後の状態遷移を一度でterminalへ閉じる制御として抽象化できる。

ただしCandidate72とCandidate73は、抽象名だけを残すことと、tool実行だけを閉じることでは不十分だと示した。保持が必要なのは、入口の完全性、同時発行、result有効性、成功後のtool closure、成功後のresponse closureである。Candidate71の全単語が必要だとは確認していない。

`OWNER_ROLE`の監査では削除可能な未根拠句を確認できなかった。`VALIDATION_CLOSURE`と`OWNER_ROLE`を変更せず、次に`SPEC`を監査する。まだCandidate74は作らない。

## 事実

Candidate71のroot `AGENTS.md`は4,987 byte、11 labelである。

| label | byte | root全体比 | 主な内容 |
| --- | ---: | ---: | --- |
| `OWNER_ROLE` | 1,010 | 20.3% | owner解釈、worker起動条件、runtime identity、result binding、失敗伝播、補完禁止 |
| `SPEC` | 781 | 15.7% | outcome authority、実行開始gate、clarification、operation間の非伝播 |
| `VALIDATION_CLOSURE` | 695 | 13.9% | validation入口、同時発行、result判定、terminal closure、非適用域 |
| `PRODUCER` | 505 | 10.1% | producer一意性と変更時失効 |
| `CONTEXT` | 452 | 9.1% | workerへ渡す最小十分context |
| その他6 label | 1,544 | 31.0% | terminal、operation独立性、decision、method、recovery |

上位3 labelだけで2,486 byte、root全体の49.9%を占める。

Candidate69とCandidate71のroot差は`VALIDATION_CLOSURE`一行だけである。同一互換条件のB18ではCandidate71のall-agent token合計、elapsed合計、top-level tool call、model stepがCandidate69より小さかった。一方、意味確認ではCandidate71にA02のrequired validation欠落3件と、A01の未確認実装1件があり、Candidate71は停止済みである。

Candidate72は`VALIDATION_CLOSURE`を短いOPEN / CLOSED表現へ置換した。品質は維持したが、F06の編集後model再入中央値とtoken中央値が増えた。

Candidate73は入口、同時発行、成功後追加read禁止、失敗時nonterminalを残した。成功後の追加read / validationは0件だったが、F06の編集後model再入中央値は`2 -> 3`となった。tool closureだけでresponse closureを再現できなかった。

## 五つの制御機能

11 labelは、表現ではなく次の五機能へまとめて読める。

| 制御機能 | 対応label | 不変条件 |
| --- | --- | --- |
| Authority closure | `SPEC`、`INDEPENDENCE` | outcomeとoperation境界が確定するまで変更を始めない |
| Producer uniqueness | `PRODUCER`、`OWNER_ROLE`、`ROOT` | 一つのoperation resultを一つの実行identityだけが生成する |
| Context boundary | `CONTEXT` | producerへ必要十分なcontextだけを渡す |
| Decision / terminal closure | `DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`TERMINAL` | 独立resultをまとめ、欠落を補完せず、一度の状態遷移で閉じる |
| Failure semantics | `METHOD`、`RECOVERY` | method失敗、permission否定、environment recoveryを混同しない |

この五機能が構造であり、11個のlabel名や現在の文章量は実装表面である。

## どこが試験対策に見えるか

### 事実

`OWNER_ROLE`は`runtime_spawn_result.task_name`、`FINAL_ANSWER.Sender`、`wait`など、特定runtimeの観測fieldを直接参照する。

`SPEC`は一つのlabel内で、authority、開始gate、clarification、operation間伝播という複数の独立判断を扱う。

`VALIDATION_CLOSURE`はvalidation commandの発行model stepまで指定するため、境界制御だけでなく方法制約を含む。

### 推測

`OWNER_ROLE`は、一般的な「producer identityを一意にする」という不変条件より、評価traceでidentityを証明する方法までroot promptへ持ち込んでいる可能性が高い。これは11 label中で最も試験対策的に見える部分である。

`SPEC`も過積載だが、A01の未固定mode誤実装に直接関係するため、先に短縮するとStrict制御を弱める可能性がある。

`VALIDATION_CLOSURE`の方法制約は一般原則だけなら細かい。しかしCandidate72 / 73で、現在のruntimeではtool closureとresponse closureを自然には同時に保証できないことを観測した。現時点では単なる試験対策とは切り分ける。

## `OWNER_ROLE`の監査順序

1. `OWNER_ROLE`の各節を、保存済みtraceで実際に防いだ誤経路へ対応付ける。
2. 対応する誤経路がないruntime証跡手順を、構造的不変条件から分離する。
3. 一つの削除または置換predicateが定まった場合だけCandidate74の作成前gateを書く。
4. targeted試験でproducer誤帰属、worker欠落、root補完、tokenとmodel stepを確認する。
5. targetedで機能を保持した場合だけ、標準14項目またはB18を検討する。

`SPEC`と`VALIDATION_CLOSURE`はこの段階で変更しない。

## `OWNER_ROLE`監査結果

### 結論

`OWNER_ROLE`は試験case固有ではない。Codex runtimeの委譲protocolへ強く依存した条件である。

root-only taskへ常時読ませる配置は細かいが、句をそのまま削除できる証拠はない。既に同じ問題へ広い圧縮を行ったCandidate49は品質を維持した一方、20 run token合計を13.21%増やして停止している。Candidate74は作らない。

| `OWNER_ROLE`の機能 | 保存済み根拠 | 判定 |
| --- | --- | --- |
| criterion owner語列だけでworkerを起動しない | Candidate41はF05 / F10の不要workerを10 / 10で0にし、score `4`を維持した | 保持 |
| TaskSpecが独立producer executionを明示した場合だけ委譲する | Candidate41の変更predicate。Candidate67ではこのgateを`OWNER_ROLE`一か所へ残してD01の指定workerを5 / 5で維持した | 保持 |
| spawn `task_name`、`FINAL_ANSWER.Sender`、final result bindingでprovenanceを確認する | Candidate29はruntimeに存在しないfieldを要求した。Candidate30は実fieldへ直し、targeted 25、expanded 60、continuous 300 runでowner証跡不成立0だった | 明示委譲時だけ保持 |
| `wait`をidentity証跡にせず、result欠落をpassedへ補完しない | Candidate20 / 22ではchild sessionとfinal resultがないままrootが独立判定の受領を自己申告した | 明示委譲時だけ保持 |
| `false / failed`を同operationのterminal resultとして保持し、別operationを失効させない | Candidate33の必須response欠落に対しCandidate34が状態を分離し、targeted 10 / 10とexpanded 60 / 60を登録した | 意味は保持。ただし所属は`TERMINAL`側が自然 |
| root宣言、異Sender、root再構成でresultを補完しない | child resultなしの受領自己申告と、別producer resultのroot差替えを直接禁止する | 上記provenance / terminal条件の否定例として保持 |

### 推測の訂正

`runtime_spawn_result.task_name`や`FINAL_ANSWER.Sender`が書かれているため試験対策的に見える、という最初の推測は半分だけ正しい。

特定caseの正答を誘導する文ではない。実runtimeが返すfieldと、過去に実際に起きた偽のresult受領を対応付けたprotocolである。この意味では構造的である。

問題は、明示委譲がないroot-only taskでも1,010 byteの条件がroot promptに常在することである。ただしCandidate49の広い分離は実行tokenを減らさなかったため、「委譲時だけ別blockにする」と再提案するだけでは新しい検証仮説にならない。

### 次の対象

`OWNER_ROLE`は変更せず、次は`SPEC`を同じ方法で監査する。`SPEC`は781 byteの中にauthority、開始gate、clarification、operation間非伝播を持ち、`OWNER_ROLE`よりも一label一不変条件の原則へ明確に反している。

## 現在の判定

Candidate71のKPI改善は、制御全体が優れている証拠ではない。`VALIDATION_CLOSURE`によるmodel再入削減の証拠である。

同時に、Candidate72 / 73の結果は現在の詳細文を逐語的に正当化しない。抽象化で保持すべき機能境界を示しただけである。

したがって、全体を一括短縮するのではなく、KPI差に寄与していない大きなlabelから一つずつ、誤経路との対応を監査する。

## `SPEC`監査結果

### 結論

`SPEC`の六句はすべて保存済み誤経路へ対応し、削除または他labelへの置換で判断点を消せる句は一つもない。Candidate74は作らない。次は`CONTEXT`の9-field packet列挙を同じ方法で監査する。

### identity確認

- prompt identity `the-caption-3ce91a4-validation-closure-r1`、bundle SHA-256 `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`を`verify_bundle`で検証済み。
- 監査対象の`SPEC`一行はroot `AGENTS.md`の正本と一致。live HEADは`2113ed247a0060f4b68846ced2188a420ff17ea8`。
- 六句は[`Candidate43 control element分類`](candidate43-control-element-classification.md)の原子要素へ次のとおり対応する。`S1=F1`、`S2=A1`、`S3=A2`、`S4=A3`、`S5=A4`、`S6=F2`。`S2..S5`はauthority readiness(A系)、`S1 / S6`はfixed operation(F系)である。

### 六句の証拠対応表

事実列と判定列を分け、推測・提案は本表に混ぜない。

| 句 | 防ぐ誤経路(保存trace) | TaskSpec等で防げない理由 | 増やす判断点 | 観測結果 | 判定 |
| --- | --- | --- | --- | --- | --- |
| `S1` operation identity分割 + predicate / criterion owner / permission / constraint固定 | C54でoutcome単位だけへ縮めるとF10の段階的再判断が増えた | TaskSpecはoutcome / read / permissionを固定するが、初回predicate前に一つのoperationへpredicate / permission / constraintをbindする原子開始単位を固定しない | operation identity分割、初回predicate前binding | C61で原子`SPEC`を復元しA01 / A02は10 / 10 score `4`。ただしF10短経路は復元せず(model step `48 -> 60`) | `retain`(意味)。効率効果は未確定 |
| `S2` `spec_ready`を明示input / outcome値を直接要求する一意authorityへbind済みで成立 | C42 A01 5 / 5でcurrent value `daily`と選択肢`daily / strict`から`strict`を推測し、質問前に編集・試験へ進んだ | TaskSpecはrequired outcomeを列挙するが、値をbindする根拠の適格性(authorityの一意性と直接要求)を限定せず、repository stateがbind候補として残る | authority適格性のbinding判定 | C43 A01 5 / 5で編集・試験前に質問、A02 5 / 5でcanonical routeを解決 | `retain` |
| `S3` current value / option set / complement / test expectation / implementation convenienceをbindしない | C42の補集合推測(`strict = not daily`)を直接閉じたnegative boundary | repository stateはauthorityに見えるため、positive規則(`S2`)だけでは補集合推測を排除しない | negative list照合 | C43でA01の補集合推測が5 / 5で消失 | `retain`(`S2`と一体) |
| `S4` `spec_ready=false`の間はproducer binding / predicate実行 / artifact変更 / testを開始しない | C41 A01 5 / 5で未固定policyを推測して実行。C42で開始禁止を追加。C71 B18 A01では1件が未固定modeを確認せず実装・testへ進行 | TaskSpec / authority / stateはreadinessの真偽を計算できても、falseでの実行開始を抑止する状態遷移を持たない | readiness gateによる実行抑止 | C43 A01 5 / 5で停止。C71に残存失敗1件があり、gateは強化対象で削除対象でない | `retain`(強化側) |
| `S5` authorityからbindできない未固定値だけをclarification resultにする | C42は質問せず推測(過小)、対称にrepository解決可能な値まで質問する過剰もありうる | TaskSpecは質問対象集合を定義せず、全部質問と全部推測の両誤りが起こりうる | clarification範囲の限定 | C43 A01 5 / 5で未固定値だけ質問、A02 5 / 5で解決可能routeを質問しなかった | `retain` |
| `S6` result / constraint / terminalを同一operation identity内だけへbindし別operation / task全体へ伝播させない | C33で別operationの成立済みresponse失効と必須response欠落。C34が状態を分離 | TaskSpec / stateは各resultを保持するが、あるoperationの`false / failed`を別operationへ伝播させない境界を定めない | operation間の失効非伝播 | C34 targeted 10 / 10、expanded 58 / 60がscore `4`、C31比token中央値`-12.57%` | `retain`。ただしOWNER_ROLE `F8`と非伝播方向で重複 |

### Strict制御と実行効率の分離

- `S2..S5`のStrict境界はA01 / A02で成立を確認済みだが、C71 B18で`S4`の残存失敗(A01の未固定mode誤実装1件)が観測された。これは`VALIDATION_CLOSURE`の非適用域である仕様確定前へ検証が流入した事例で、`S4`を弱めれば悪化する。A01の未確認実装をtoken削減と相殺せず、`S4`は削除・短縮対象にしない。
- `S1`の効率効果は未確定である。C61は原子`SPEC`をC55へ完全一致で戻したが、F10短経路は復元せず(`43 -> 55 tool call`、`848,388 -> 1,048,829 tokens`)。短経路はpredicate成立ではなくsampling変動に依存する。したがって`S1`の分割・統合でtoken削減を主張できず、C61 runtime不通過を`S1 / S6`の意味が不要という証拠へ読み替えない。

### 重複・移動候補の検討

handoffが挙げた四関係を確認した。いずれも判断点を消さない。

- `S1`と`PRODUCER`: `S1`はoperation identityとspec値の確定、`PRODUCER`はそのoperationへproducer execution identityを一つbind(`F3`)。`S1`は`PRODUCER`の前提条件であり、同一predicateの重複ではない。削除候補にならない。
- `S6`とTERMINAL / OWNER_ROLE: `S6`(`F2`)は一般の失効非伝播、OWNER_ROLEの`false / failed`保持(`F8`)は同じ非伝播を特定状態へ適用したものである。分類表でも`F2 / F8`統合が候補だが、OWNER_ROLE監査は既にOWNER_ROLEを変更しないと結論済みで、`S6`は一般形として常時読むcoreに必要である。統合は常時読むcore内の再配置で、判断点を消さない。
- `S2 + S3`統合: 分類は`A2`を`A1`へmergeと分類するが、これは一文への表面圧縮であり意味削減ではない。negative list(`S3`)はC42の補集合推測を排除する動作本体で、positive規則だけへ縮めると境界を失う。表面圧縮はC65 / C66で短経路を安定再現しなかったため、新しい検証仮説にならない。
- criterion ownerの`SPEC`常時固定: criterion ownerはOWNER_ROLE `D1`でも常時「担当情報でありworker指定でない」と記述され、常時読むcoreに既に存在する。`S1`から外してもcoreから消えず、明示委譲時だけ別blockにする再提案はCandidate49で実行tokenを減らさなかった。移動して同じ判断を別labelで読むだけであり、削減候補にしない。

### 構造と表現過積載の切り分け

- 構造: `S2 / S3`(authority適格性 + negative boundary)、`S4`(readiness gate)、`S5`(clarification範囲)、`S6`(失効非伝播)は、それぞれC42 / C43 / C34の異なる保存済み誤経路へ一対一で対応する独立不変条件である。
- 表現上の過積載に見える点: `SPEC`は一labelにA系(readiness)とF系(operation scope)を同居させ、一label一不変条件の原則へ反する。しかし句単位では重複predicateがなく、分割はlabel参照を一つ増やすだけで判断点を消さない。過積載はlabel名の粒度の問題であって、削除可能な句の存在を意味しない。

### Candidate74の判断

`作成根拠なし`。

削除または置換する一つのpredicateを導けない。六句すべてが保存済み誤経路へ対応し、既存の重複(`S6 / F8`、`S2 / S3`、criterion owner)はいずれも常時読むcore内の再配置または表面圧縮で、消す判断点・context伝播を示せない。handoffのCandidate74作成前gate九項目のうち、項目5(削除・置換predicate)と項目6(消す判断点)を定義できないため、bundle / profile / evaluation setを作らない。

### 次に監査するlabel

`CONTEXT`(452 byte)。分類`D6`で9-field packet列挙の単独効果が未分離で、field列挙の多くがTaskSpec / allowed read / required evidenceと重複するという具体的な縮小仮説がある。`SPEC`と`OWNER_ROLE`はこの段階で変更しない。
