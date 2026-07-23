# THE-CAPTION execution control 修正指示書

作成日: 2026-07-23  
判定者: ChatGPT / Gemini 3.6 Thinking / Claude Opus 4.8 最大 / Grok（利用可能な「速い」モード）
監査状態: 3者独立レビューおよび争点再照会を反映済み

## 1. 結論

現行仕様の中核方針は維持する。

- requested outcome valueをcurrent value、option set、complement、test expectation、implementation convenienceから推測してbindしない。
- operationごとにproducerを一つ固定し、別producerやrootがresultを補完しない。
- result、constraint、terminalを別operationへ伝播させない。
- decision boundaryのない相互非依存invocationを不要に逐次化しない。
- validation成功後に根拠のない追加read・validationを行わない。

一方、現行仕様は次の点で実行可能な状態機械として閉じていない。

1. TaskSpec fieldごとの正当なauthorityが区別されていない。
2. invocationの実行状態とpredicateの真偽が混在している。
3. producerやartifactの変更後も旧resultを利用できる抜け道がある。
4. 依存関係のあるvalidationにも同時発行を強制する。
5. METHODとRECOVERYの終了条件および終了後の状態が不足している。
6. operationの分割規則とtask-wide constraintの適用規則が不足している。
7. 非producer rootが実行できるcontrol-plane処理の範囲が狭く読める。
8. invocationの終了、process exit、証拠取得成否が分離されていない。
9. operationの評価結果とpermissionによる停止理由を同時に保持できない。
10. validation dependencyのauthority、循環検査、実行時の未宣言依存の遷移が不足している。

以上を修正してから正式な実行制御仕様として採用する。

## 2. ChatGPTとしての独立見解

### 2.1 設計上優れている点

この仕様の価値は、単なる「慎重に実行する」指示ではなく、値・result・producerのprovenanceをoperation identityへ固定しようとしている点にある。特にOWNER_ROLEとROOTは、criterion ownerの自然言語表現をproducer選定へ流用する事故と、workerのresultをrootが再構成する事故を防ぐために有効である。

DECISION_BOUNDARYも妥当である。結果が後続invocationを変えないことが既知なら同一model stepで発行し、全result受領後に一度だけ判断するという規則は、不要な逐次化と中間resultによる判断汚染を同時に抑制する。

### 2.2 最も重大な欠陥

最大の欠陥は、`false / failed / unavailable / terminal`が異なる種類の状態であるにもかかわらず、同一のresult状態として扱われ得ることである。

- `false`: predicateを正常に評価した結果
- `failed`: invocationの実行状態
- `unavailable`:必要な実行または証跡を取得できない状態
- `terminal`: これ以上の状態遷移を行わないというlifecycle属性

これらを一軸にすると、コマンド失敗をrequested predicateの否定へ誤変換したり、再試行すべきinvocationをterminal化したりする。したがって状態の二軸化は文言改善ではなく必須の構造修正である。

### 2.3 4者の回答に対する裁定

4者の一致は参考にするが、多数決では決めない。原文に存在しない前提から作られた循環やデッドロックは不採用とする。

- Gemini初回の「spec_ready=falseがTaskSpec構築やclarificationまで禁止する」という指摘は不採用。禁止対象は列挙されており、準備処理は含まれない。
- Claude初回の「producer identityがTaskSpec値に含まれるためspec_readyと循環する」という指摘は不採用。producer identityはSPECの固定対象に列挙されていない。
- Claude初回の「delegated_result_ready=falseがworker起動を阻害する」という指摘は不採用。同gateが禁止するのはcriterionのpassed化である。
- `false / failed / unavailable`を一つのterminal enumへ並べるGemini・Claudeの初期案は不採用。状態を二軸化する。
- METHODの候補集合を静的有限と仮定するClaudeの初期案は不採用。実行時stop conditionとbudgetで閉じる。
- predicate 0件を自動的なvacuous successとする案は不採用。明示no-op以外はinvalid TaskSpecとする。

## 3. 4者判定の統合

| 論点 | ChatGPT | Gemini | Claude | Grok | 最終判定 |
|---|---|---|---|---|---|
| SPEC準備処理の自己阻害 | 原文上なし | 初回指摘を訂正 | 過剰循環を撤回 | 過剰循環あり | 不採用。誤読防止条文のみ追加 |
| worker起動の自己阻害 | なし | 問題視せず | 撤回 | 読み過ぎと認定 | 不採用 |
| field-specific authority | 必須 | High | 必須 | medium-high | 必須修正 |
| invocationとpredicateの状態分離 | 必須 | 必要 | Critical | High | 必須修正 |
| result version・epoch binding | 必須 | High | 必須 | High | 必須修正 |
| validation dependency wave | 必須 | 必要 | 必須 | Critical | 必須修正 |
| METHODのstop condition | 必須 | 必要 | 必須 | Medium | 必須修正 |
| RECOVERY上限後の遷移 | 必須 | 必要 | Critical | 必要 | 必須修正 |
| operation partition | 必須に近い | High | Medium | medium-high | 必須修正 |
| ROOT control-plane権限 | 推奨 | 必要 | Medium | Medium | 推奨修正 |
| CONTEXTのアクセス強制性 | 推奨 | 判定基準具体化 | 検証可能性を指摘 | 検証可能性を指摘 | 推奨修正 |
| 非zero exitと有効証拠の分離 | 必須 | Blocking | 支持 | 支持 | 必須修正 |
| operation outcomeとstop reasonの二軸化 | 必須 | 再照会で支持 | 再照会で支持 | 再照会で支持 | 必須修正 |
| validation DAGのauthority・acyclic検査 | 必須 | 支持 | Blocking | Blocking | 必須修正 |
| producer変更後の旧result再利用禁止 | 必須 | 再照会で支持 | 初回案を撤回し支持 | 再照会で支持 | 必須修正 |

## 4. 必須修正

### R-01: authorityをfieldごとに型分けする

対象: SPEC / METHOD / VALIDATION_CLOSURE / OWNER_ROLE

`TaskSpecへ固定する全値`を同一authorityへbindする定義を廃止し、次の型を導入する。

```text
outcome_authority:
  requested outcome valueは、明示user inputまたは当該valueを直接要求する
  一意なrepository authorityだけからbindする。

policy_authority:
  permission / constraintは、適用されるinstructionまたはpolicy authorityの
  優先順位に従ってbindする。

runtime_authority:
  operation / invocation / producer / worker task / Sender identityは、
  runtimeが発行したidentity evidenceへbindする。

method_authority:
  TaskSpecに明示されていないmethod / commandは、
  outcome・permission・constraintを変更しない範囲でexecutorが選択し、
  executor method choiceとしてbindする。

method_control_authority:
  method_stop_condition / method_budget / environment_recovery_maxは、
  明示TaskSpecまたは適用policyへbindする。
  どちらにも明示がなくpermissionが許す場合だけ、
  runtime policyの有限なdefaultへbindできる。

dependency_authority:
  validation dependency / shared-state classificationは、
  明示TaskSpecまたはそれらを直接要求する一意なrepository / policy authorityから、
  control-plane preparation中にbindする。
  dependency_rebuild_budgetは明示TaskSpecまたは適用policyへbindし、
  どちらにも定義がなければ未宣言依存の初回検出時にclarificationへ移る。
```

`spec_ready`は、すべてのfieldが同一authorityにbindされたかではなく、各fieldがその型に対応するauthorityへbindされたかで判定する。

上位permissionや明示禁止は、userまたはrepositoryが許可していても回避しない。

### R-02: control-plane preparationを定義する

対象: SPEC / ROOT

次をpredicate実行とは別のcontrol-plane処理として定義する。

```text
control_plane_preparation :=
  authority read
  + target / artifact state read
  + required outcome partition
  + operation identity generation
  + TaskSpec construction / versioning
  + clarification generation / binding
  + dependency graph construction
  + producer packet construction
```

`spec_ready=false`でもcontrol-plane preparationは実行できる。ただしproducer binding、predicate実行、artifact変更、testは開始しない。

clarification resultはpredicate resultではなくcontrol-plane resultとする。user回答を受領した場合は該当TaskSpec fieldへbindし、`TaskSpec_revision`を更新して`spec_ready`を再評価する。

### R-03: operation identityをlineageとexecutionへ分ける

対象: SPEC / PRODUCER / INDEPENDENCE / TERMINAL

次の二種類を区別する。

```text
operation_lineage_identity:
  同一required outcomeを追跡する論理identity。

operation_execution_identity:
  一つのproducer execution identityと、一つの互換なexecution contractで
  実行するidentity。

TaskSpec_revision:
  control-plane上のTaskSpec改訂ごとに更新するrevision。

predicate_contract_version:
  各predicateについて、criterion / pass condition / target version /
  適用permission・constraint / 明示method / dependency preconditionの
  有効性に影響するprojectionをversion化したもの。
```

producer変更時は同一`operation_execution_identity`へ別producerを再bindしない。新しいoperation execution identityを発行し、同じlineageへ関連づける。

旧executionに属するproducer binding、未完了invocation、predicate result、terminal候補は`invalidated`とし、新executionへ伝播させない。旧resultはlineage上の監査履歴として保持できるが、current resultまたはterminal集約には使用しない。これは独立predicateの完了resultにも適用する。`invalidated`はterminal resultの補完ではない。

producerを変えず、control-planeだけでTaskSpecを改訂する場合は`TaskSpec_revision`を更新する。各predicateの`predicate_contract_version`を再計算し、変更されたpredicateとその下流依存resultだけを失効させる。execution contractまたはproducerが変わる改訂では新しい`operation_execution_identity`を発行し、旧executionの全resultを失効させる。

### R-04: operation partition規則を追加する

対象: SPEC / INDEPENDENCE

次のいずれかに該当するrequired outcomeは別operation executionとして分ける。

1. target identityまたはtarget versionが異なる。
2. 独立したproducer executionがTaskSpecに明示される。
3. 先行operationの最終result、最終artifact、または決定結果を、TaskSpec上の独立要件として新しいpredicateで評価する。同一operationのValidation Closure内にある過渡的中間artifactの依存はR-09のvalidation waveで扱い、この条件だけではoperationを分けない。
4. 一方のresultが他方のtarget、permission、method、stop conditionを変え得る。
5. 他方と独立してterminal判定される必要がある。

恣意的な分割・統合によってresult、constraint、terminalのoperation-local規則を迂回してはならない。

task-wide constraintは、あるoperationのresultとして他operationへ伝播させない。元のpolicy authorityから、各operation生成時にoperation-local constraintとして個別にmaterializeする。

### R-05: invocationとpredicateの状態を分離する

対象: TERMINAL / OWNER_ROLE / METHOD / RECOVERY / VALIDATION_CLOSURE

次の状態モデルを採用する。

```text
invocation_status :=
  pending | running | success | failed | unavailable
  terminal set := success | failed | unavailable
  nonterminal set := pending | running

process_exit :=
  zero | nonzero | signal | timeout | not_observed
  // invocation_statusとは別のruntime evidence

predicate_evaluation :=
  pending | evaluated | unavailable

predicate_value :=
  true | false
  // predicate_evaluation=evaluatedの場合だけ存在

predicate_unavailability_reason :=
  prohibited
  | provenance_unavailable
  | execution_unavailable
  | evidence_unavailable
  // predicate_evaluation=unavailableの場合に必須。
  // method / recoveryの枯渇などの詳細はreason detailへ保持する。

producer_lifecycle :=
  bound | running | terminal

operation_lifecycle :=
  spec_pending | ready | running | terminal | invalidated

operation_evaluation_outcome :=
  satisfied | unsatisfied | unavailable
  // operation_lifecycle=terminalの場合だけ存在

operation_stop_reason :=
  none | prohibited
  // operation_lifecycle=terminalの場合だけ存在し、
  // operation_evaluation_outcomeを上書きしない
```

変換規則:

- `invocation_status=success`は「invocationが終了し、predicate判定に必要な真正かつ使用可能な証拠を生成した」ことを意味する。process exit code 0を意味しない。
- process exitがnonzeroでも、仕様で要求された証拠が真正かつ使用可能なら`invocation_status=success`とし、predicateを評価する。crash、timeout、証拠欠落・破損などで使用可能な証拠がない場合だけ`failed`または`unavailable`とする。
- invocationが`success`し、必要証拠から判定できた場合だけpredicateを`evaluated`にする。
- predicateを正常に評価してpass conditionを満たさない場合だけ`predicate_value=false`にする。
- invocationの`failed`をpredicateの`false`へ自動変換しない。
- recovery・代替method・許可された再取得手段が尽きても判定証跡を得られない場合、predicateを`unavailable`にする。
- 明示禁止またはpermission否定によりrequired predicateが実行不能になった場合、そのpredicateを`unavailable(reason=prohibited)`へ閉じ、`operation_stop_reason=prohibited`として保持する。既に確定した`false`を上書きせず、別手段で禁止を回避しない。

### R-06: result validityをversion付きで固定する

対象: TERMINAL / OWNER_ROLE / PRODUCER / INDEPENDENCE / VALIDATION_CLOSURE

すべてのpredicate resultを次の組へ不可分にbindする。

```text
result_validity_key :=
  operation_execution_identity
  ∧ predicate_contract_version
  ∧ predicate_identity
  ∧ target_identity
  ∧ target_or_artifact_version
  ∧ producer_execution_identity
```

現在のoperation executionと一つでも一致しないresultは`stale`として失効させ、predicate判定またはterminal集約に使用しない。`TaskSpec_revision`は監査provenanceとしてresultへ記録するが、control-planeだけの改訂で`predicate_contract_version`が不変なresultまで一律に失効させるためには使用しない。

producer変更前に別producerが評価を完了したresultも、`producer_execution_identity`または`operation_execution_identity`がcurrent executionと不一致ならstaleとする。過去resultの履歴保存とcurrent resultとしての有効性を区別する。

artifact変更後は、変更前artifact versionへbindされたvalidation resultを失効させる。proposed responseをtargetとする場合もresponse identity/versionを使用する。

### R-07: delegated resultのidentity証跡を維持する

対象: OWNER_ROLE

現行`delegated_result_ready`の中核は維持する。

```text
delegated_result_ready :=
  runtime_spawn_result.task_name == task_identity
  ∧ FINAL_ANSWER.Sender == task_identity
  ∧ final_resultをcurrent result_validity_keyへbind可能
```

追加要件:

- `task_identity`はTaskSpecが独立producer executionを明示した場合だけ、起動前に固定する。
- runtimeが返したcanonical task identityと比較する。表示名やcriterion owner語列を使用しない。
- `producer_binding(task_identity, producer_execution_identity)`をruntime spawn evidenceから固定する。両identityの文字列一致は要求せず、canonicalなbinding relationを検証する。
- `wait`、rootの進行記述、異Sender messageはidentity evidenceにしない。
- worker producerがterminalであっても`delegated_result_ready=false`ならpredicateをpassedにしない。
- evidenceを取得できず、再取得手段が尽きた場合はpredicateを`unavailable`にする。

### R-08: terminal closureを定義する

対象: TERMINAL / ROOT

operationをterminalにできる条件を次に限定する。

```text
operation_terminal_ready :=
  current operation executionに属する全required predicateが
    evaluated(true | false)またはunavailable
  ∧ current producerがterminal
  ∧ worker producerの場合、
      evaluatedに使用する各resultがdelegated_result_ready
      ∧ delegated_result_readyを成立させられないpredicateは
        再取得手段の枯渇後にunavailable(reason=provenance_unavailable)
  ∧ current executionへbindされたinvocation / worker / sessionにnonterminalがない
  ∧ 使用する全resultのresult_validity_keyがcurrent
```

ここでinvocationのnonterminalはR-05の`pending | running`だけを指す。`failed | unavailable`はinvocationとしてterminalだが、predicateを自動的にterminalへはしない。許可されたMETHOD / RECOVERYが尽き、predicateが`evaluated`または`unavailable`へ閉じた場合だけoperation terminal条件を満たせる。

集約規則:

- 全required predicateが`true`なら`operation_evaluation_outcome=satisfied`。
- 一つ以上`false`なら`operation_evaluation_outcome=unsatisfied`。他の`unavailable`状態も個別証跡として保持する。
- `false`がなく、一つ以上`unavailable`なら`operation_evaluation_outcome=unavailable`。
- permission否定または明示禁止で停止した場合は`operation_stop_reason=prohibited`。評価結果を上書きしないため、`false`と禁止が共存する場合は`unsatisfied + prohibited`として保持する。
- 禁止によってrequired predicateが未評価のまま残る場合、そのpredicateを`unavailable(reason=prohibited)`へ閉じてからterminalを判定する。
- `operation_evaluation_outcome=satisfied`なら`operation_stop_reason=none`でなければならない。
- `operation_evaluation_outcome=unavailable`へ集約しても、寄与した各predicateの`predicate_unavailability_reason`とreason detailをoperation evidence mapへ保持し、terminal報告でreason別に列挙する。集約によって`provenance_unavailable`、`execution_unavailable`、`evidence_unavailable`、`prohibited`を相互変換または消去しない。
- required predicateに`unavailable(reason=prohibited)`が一つでもあれば`operation_stop_reason=prohibited`、それ以外は`none`とする。

predicateが0件のoperationを`invalid TaskSpec`とする規則はterminal判定時に適用する。control-plane preparation中の未固定状態は対象外とする。明示authorityが`no_op_allowed=true`を固定した場合だけ`satisfied + none`にできる。

taskは全required operationのcurrent executionがterminalの場合だけtask-terminalとする。overall successは全operationが`operation_evaluation_outcome=satisfied ∧ operation_stop_reason=none`の場合だけとし、それ以外はoperationごとの両軸を失わずに報告する。あるoperationのfailureやunavailableによって、別operationのresultを書き換えない。

### R-09: validationをdependency waveで発行する

対象: VALIDATION_CLOSURE / DECISION_BOUNDARY

`validation_set_ready`へ次を追加する。

```text
validation_set_ready :=
  artifact変更完了
  ∧ 全required validationのidentity
  ∧ command
  ∧ individual pass condition
  ∧ stop condition
  ∧ dependency identity
  ∧ shared-state classification
  ∧ target/artifact version
  がbind済み
```

`dependency identity`と`shared-state classification`はR-01の`dependency_authority`からcontrol-plane preparation中に静的にbindする。validation実行resultを根拠に、current waveの依存関係を後付けしない。

validation dependency graphは発行前にacyclicであることを検証する。cycle、未固定dependency、未固定shared-state classificationがある間は`validation_set_ready=false`とし、repository authorityから解決できなければclarification対象にする。

発行規則:

1. required validationを依存DAGへ分ける。
2. 現在発行可能な相互非依存nodeを一つのwaveとする。
3. 同一waveの全invocationを同一model stepから発行する。
4. wave内の全resultを一度だけmodelへ返す。
5. 全result受領後に一度だけ次waveまたはterminalを判断する。
6. 先行resultが後続validationのtarget、permission、method、stop conditionを変え得る場合はdecision boundaryとしてwaveを分ける。

全validationを無条件で一つのwaveへ入れてはならない。共有状態を変更するvalidation、先行validationの生成物へ依存するvalidation、early-stop関係を持つvalidationは同一waveへ入れない。

rootがnonproducerである場合、rootはwaveの構築・発行スケジューリング・result bindingだけを行う。各validation invocationのpredicate実行とresult生成は、当該operationへbind済みのproducerが行う。worker producerのoperationではvalidation resultも同じ`task_identity`と`producer_execution_identity`へbindし、R-07の`delegated_result_ready`を通す。

waveのmodel step境界は発行スケジューリングを担うrootが確定し、bound producerはその一つのwave scheduleに従ってinvocationを実行する。model step境界を決めることはpredicate実行またはproducer roleの取得ではない。

rootまたは別executionがvalidation predicateを直接実行する必要がある場合は、既存worker operationのresultとして扱わない。R-04に従って独立operationへ分け、実行前に固有predicate / owner / producerを固定する。wave scheduling authorityをproducer roleへ読み替えてはならない。

実行時に未宣言依存または共有状態競合が判明した場合、predicateの`false`やoperationの`unsatisfied`へ変換しない。`unexpected state`としてoperationをnonterminalに戻し、current waveの未完了invocationを停止条件に従って閉じ、control-planeでTaskSpecを再構築する。`predicate_contract_version`またはresult validity keyが変わるaffected resultとその下流だけをstaleにし、整合するresultは保持する。再構築不能または`dependency_rebuild_budget`到達時は、authorityからbindできない値だけをclarification resultにする。

全required validationについて`invocation_status=success ∧ predicate_evaluation=evaluated ∧ predicate_value=true`のcurrent resultがbind済みなら、TaskSpec追加要求またはresult失効がない限り追加read・validationを行わずterminalを判断する。

### R-10: METHODのstop conditionを追加する

対象: METHOD / VALIDATION_CLOSURE

TaskSpecにmethodが明示された場合だけそのmethodを固定する。未指定の場合、executorはpermission内でmethodを選択できる。

```text
method_search_ready :=
  predicate_identity
  ∧ permission
  ∧ method_stop_condition
  ∧ method_budget
  がbind済み

method_stop_condition :=
  permitted candidate exhaustion
  | method budget exhaustion
  | explicit prohibition
  | permission denial
```

`method_stop_condition`と`method_budget`はR-01の`method_control_authority`へbindする。executorが無制限budgetを推測してはならない。

method選択はrequested outcome valueのbindではない。current valueやtest expectationをoutcomeとして採用してはならないが、permission内の実行手段選択には使用できる。

invocationのfailedまたはunavailableだけでpermission否定と解釈しない。別の許可されたmethodが残る間は同一predicateへ向けて継続する。stop condition成立後もpredicate証跡が得られなければpredicateを`unavailable`にする。

### R-11: RECOVERYを閉じる

対象: RECOVERY / METHOD / TERMINAL

次を固定する。

```text
environment_recovery_attempt :=
  一回のenvironment-only repair適用
  + その直後のsame required command identityの一回のrerun

environment_recovery_max:
  最初のenvironment recovery開始前にpolicy authorityまたはTaskSpecへbindする。
```

一つのattempt開始時にだけ`environment_recovery_max`を消費する。同じattempt内のrepairとrerunを別々に数えない。異なるrepairを続けて適用する場合は、それぞれ別attemptとして消費する。未固定methodの選択はenvironment recoveryとして数えない。

`environment-only`の変更範囲を明示し、target artifactやrequested deliverableを変更するrepairはenvironment recoveryとして扱わない。

上限到達後:

- commandが実行され、predicateを評価できる証跡が得られた場合は`true / false`を固定する。
- commandを実行できない、または必要証跡を取得できない場合はpredicateを`unavailable`にする。
- command failureだけをpredicate`false`へ変換しない。

## 5. 推奨修正

### R-12: 非producer rootのcontrol-plane権限を補足する

対象: ROOT

非producer rootは次だけを行えるとする。

```text
authority探索
operation partition / identity generation
TaskSpec構築・versioning
clarification処理
dependency DAG / validation wave管理
worker packet構築
result binding
result validity確認
terminal集約
```

predicate実行、worker result再生成、missing result補完は禁止のままとする。

### R-13: CONTEXTの制約強度を区別する

対象: CONTEXT

`allowed read / forbidden input`がランタイムで強制可能かを区別する。

```text
enforced_context_constraint:
  runtime capabilityで実際にアクセスを制限する。

advisory_context_constraint:
  worker packet内の指示に留まり、security boundaryとはみなさない。
```

`fork_turns=none`は会話履歴の非継承を保証するが、共有filesystem、network、tool、model prior knowledgeへのアクセス禁止までは保証しない。

「意味保持に必要な最小turn数」は、packetとallowed readだけではcriterion、target identity、pass conditionのいずれかを一意にbindできない場合に限る。無関係なtool outputへアクセスできる可能性を理由に継承しない。

### R-14: criterion ownerのnullable性を定義する

対象: SPEC / OWNER_ROLE

pure machine predicateでnon-machine risk ownerが存在しない場合、`criterion_owner=none`を明示的に固定できるようにする。ownerが必要なcriterionで未固定のまま`none`へ推測してはならない。

## 6. 既存節の再編指示

重複と将来の乖離を防ぐため、次の共通定義節を新設し、既存節は参照だけにする。

1. `AUTHORITY_AND_TASKSPEC`
   - R-01、R-02、clarification flow
2. `IDENTITY_AND_LINEAGE`
   - R-03、R-04、R-06
3. `EXECUTION_STATE`
   - R-05、R-08
4. `PRODUCER_AND_DELEGATION`
   - PRODUCER、OWNER_ROLE、ROOT
5. `SCHEDULING_AND_VALIDATION`
   - DECISION_BOUNDARY、R-09
6. `METHOD_AND_RECOVERY`
   - R-10、R-11

既存の中核禁止規則は削除せず、共通定義への参照に置き換える。

## 7. 不採用とする変更

次の変更は行わない。

1. spec_ready=false時にTaskSpec構築、authority read、clarificationまで禁止する。
2. producer identityをspec_readyのTaskSpec fieldへ追加する。
3. delegated_result_readyをworker起動条件にする。
4. rootが異Sender resultを再構成してdelegated_result_readyを成立させる。
5. invocation failureをpredicate falseへ自動変換する。
6. false、failed、unavailableを同一状態enumへ統合する。
7. 未固定method集合が静的有限であると仮定する。
8. 全validationを依存関係にかかわらず同時発行する。
9. task-wide constraintを先行operationのresultとして別operationへ伝播させる。
10. predicate 0件を無条件でsuccessにする。
11. task全体のfailureを理由に、成功済みの別operation resultをfailedへ書き換える。

## 8. 受入条件

修正版は最低限、次のシナリオを一意に判定できなければならない。

### A. outcome authority

- current repository valueしか存在しない場合、requested outcome valueへbindしない。
- 一意なrepository authorityが新しい値を直接要求する場合だけbindする。
- repository記述が競合する場合、推測せずclarification対象にする。

### B. producer変更

- producer Aのresult生成後にproducer Bへ変更する。
- AのresultがBのexecutionでterminal判断に使用されない。
- Bは新operation execution identity、新TaskSpec revision、新producer bindingを持つ。

### C. worker result provenance

- task name不一致、Sender不一致、target version不一致の各ケースで`delegated_result_ready=false`になる。
- rootの要約や進行報告でtrueへ補完できない。
- worker operationのrequired validation resultも同じworker producer identityへbindされ、`delegated_result_ready`を通る。
- nonproducer rootがvalidation waveを管理しても、validation predicateのproducerへ昇格しない。

### D. invocation failureとpredicate false

- process exitがnonzeroという理由だけでinvocationを`failed`、predicateを`false`または`unavailable`へ自動変換しない。
- nonzero exitでも真正かつ使用可能な不合格証拠があれば`invocation_status=success`、`predicate_evaluation=evaluated`、`predicate_value=false`になる。
- crash、timeout、証拠欠落などで使用可能な証拠がない場合はinvocationを`failed | unavailable`とし、predicateを`false`へ変換しない。

### E. validation dependency

- validation BがAの生成物へ依存する場合、同一waveで発行されない。
- AとBが相互非依存なら同一model stepで発行される。
- wave内の一部resultだけを見て次waveを発行しない。
- dependency graphにcycleがある場合はvalidationを発行せず、`validation_set_ready=false`になる。
- runtimeで未宣言依存が判明した場合は`unsatisfied`ではなくunexpected stateとしてnonterminalになり、TaskSpec再構築後はaffected resultだけがstaleになる。

### F. recovery exhaustion

- recovery上限前はnonterminalを維持する。
- 上限後、証跡なしならunavailableへ閉じる。
- 上限後、評価証跡がある場合はtrue/falseへ閉じる。
- `failed | unavailable` invocationはterminal集合に属し、predicateがunavailableへ閉じた後にnonterminal invocationとしてoperationを阻害しない。
- 一回のrepairと直後の一回rerunだけが一attemptであり、次のrepairは別attemptとしてbudgetを消費する。

### G. task-wide constraint

- task-wide禁止が元authorityから各operationへ個別materializeされる。
- 一つのoperation resultから別operationへ伝播したものとして扱わない。

### H. stale result

- artifact version、predicate contract version、operation execution identity、producer identityのいずれかが変わった場合、旧resultをterminal集約に使用しない。
- `TaskSpec_revision`だけが変わりpredicate contractが不変なresultは、revision差だけを理由にstaleにしない。
- producer変更時は、旧resultを履歴として保持しても新executionのcurrent resultには使用しない。独立predicateも例外にしない。
- producer不変のcontrol-plane改訂では、`predicate_contract_version`が変わったresultとその下流だけをstaleにする。

### I. root非producer

- rootはTaskSpec構築とDAG管理を行える。
- rootはworker predicateを再実行・再生成できない。

### J. zero predicate

- `no_op_allowed`がauthorityへbindされていなければinvalid TaskSpecとなる。
- 明示no-opの場合だけterminal satisfiedにできる。
- preparation中のpredicate未固定状態をzero-predicate terminalと誤判定しない。

### K. policy / runtime / method authority

- competing instruction間でpermissionが衝突する場合は`policy_authority`の優先順位で解決し、requested outcome valueへ推測bindしない。
- runtime canonical identityと表示名が異なる場合、canonical identityとruntimeが発行したbinding relationだけを採用する。
- TaskSpec未指定methodをexecutorが選んだ場合は`method_authority`へbindし、requested outcome valueへはbindしない。
- `method_stop_condition`、`method_budget`、`environment_recovery_max`にauthorityも有限defaultもなければ実行を開始しない。

### L. operation outcomeとstop reason

- 全predicateがtrueなら`satisfied + none`。
- 一つfalseなら`unsatisfied`。同時にpermission denialがあれば`unsatisfied + prohibited`として両方を保持する。
- falseがなく一つunavailableなら`unavailable`。
- permission denialでrequired predicateが実行不能なら`unavailable(reason=prohibited)`へ閉じ、`operation_stop_reason=prohibited`とする。
- 明示禁止をinvocation failureと取り違えて別methodで回避しない。

### M. operation partitionとvalidation waveの境界

- 先行operationの最終artifactを独立要件で評価する場合は別operationになる。
- 同一operationのValidation Closure内にある中間artifact依存は別operationへ分割せず、R-09の別waveになる。
- どちらの場合もresult、constraint、terminalのoperation-local scopeを迂回しない。

### N. producer変更と単一producer provenance

- producer AがP1をtrueへ評価した後producer Bへ変更した場合、artifactが不変でもAのP1 resultはBのterminal集約へ使用しない。
- Aのresultはlineage上の監査履歴としては保持できる。
- Bのcurrent resultはすべてBのproducer bindingとcurrent executionへbindされる。

### O. TaskSpec control-plane改訂

- producerを変えずdependency宣言だけを修正した場合、`TaskSpec_revision`は更新される。
- predicate contractが変わったpredicateとその下流resultだけがstaleになる。
- producerまたはexecution contractを変える改訂では新executionを発行し、旧executionの全resultをstaleにする。

### P. delegated producer binding

- canonical `task_identity`と`producer_execution_identity`のruntime binding relationが存在すれば、文字列が異なってもidentity証跡として扱える。
- 表示名一致だけ、`wait`、rootの要約、異Sender messageではbinding relationを補完できない。

### Q. task集約

- `satisfied + none`のoperationだけで構成されるtaskだけをoverall successにする。
- `unsatisfied + prohibited`と`unavailable + prohibited`を区別して報告する。
- `unavailable + none`でも、predicateごとのprovenance / execution / evidence reasonを保持して区別する。
- 一つのoperationのstop reasonやevaluation outcomeで別operationのresultを書き換えない。

## 9. 完了判定

修正完了は次の全条件を満たした場合とする。

- R-01からR-11が仕様本文へ反映されている。
- R-12からR-14について採用または不採用理由が記録されている。
- 第8節の全受入シナリオについて期待状態が一意である。
- invocation statusのterminal / nonterminal集合とprocess exitの意味が一意である。
- 既存のrequested outcome value推測禁止が弱められていない。
- producerとcriterion ownerの分離が維持されている。
- producer変更前のresultが新executionのcurrent resultへ再利用されない。
- operation-local resultを別operationへ伝播する抜け道がない。
- rootまたは別producerによるresult補完が許可されていない。
- validationの相互非依存性が確認されない限り同時発行されない。
- validation DAGのauthority、acyclic性、未宣言依存時のnonterminal遷移が閉じている。
- operationのevaluation outcomeとstop reasonが別軸で保持される。
- predicate unavailability reasonがoperation集約とterminal報告で失われない。
- nonproducer rootのvalidation wave管理がproducer実行やresult生成へ拡張されない。
- terminal判断に使用する全resultがcurrent result validity keyへbindされている。

## 10. Gemini / Grok / Claudeレビューの反映記録

### 採用した指摘

1. invocationのterminal集合を`success | failed | unavailable`、nonterminal集合を`pending | running`として明記した。
2. process exitと使用可能なpredicate evidenceを分離し、nonzero exitでも有効証拠があれば正常評価できるようにした。
3. `operation_evaluation_outcome`と`operation_stop_reason`を二軸化し、`unsatisfied + prohibited`を保持できるようにした。
4. operation partitionと同一operation内validation waveの境界を明記した。
5. validation dependencyのauthority、static bind、DAG acyclic検査、未宣言依存時のunexpected-state遷移を追加した。
6. method stop condition / budget、recovery attempt単位、zero-predicate規則の適用時点を明記した。
7. authority型、prohibited、三分岐集約、producer変更、DAG cycleを受入条件へ追加した。
8. predicate unavailability reasonを集約後も保持し、worker operationのvalidation provenanceをbound producerへ固定した。

### 再照会後に採用した裁定

1. producer変更前のresultは監査履歴として保存できるが、新executionのcurrent resultまたはterminal集約には使用しない。初回Claudeが提案した独立predicate resultの再利用は、単一producer provenanceに反するため不採用とした。
2. prohibitionを単一outcomeの優先順位で表現する案は、既存の`false`を隠すため不採用とした。評価結果と停止理由を直交する二軸で保持する。
3. runtimeで判明した未宣言validation依存を`unsatisfied`へ変換する案は、TaskSpec不備をpredicate falseへ誤変換するため不採用とした。unexpected stateとしてnonterminalに戻す。

### 採用しなかった指摘

1. `result_validity_key`へlineage identityを追加しない。current validityは一意な`operation_execution_identity`で閉じ、lineageは監査履歴の関連づけにだけ使う。lineage全体を失効させると別executionの履歴まで誤って使用不能にする。
2. workerの`task_identity`と`producer_execution_identity`の文字列一致を要求しない。runtimeが発行したcanonical binding relationを要求する。
3. validation未宣言依存を自動的な`unsatisfied`へしない。

### 最終blocking監査

- Gemini: blocking contradictionなし。旧producer result失効、二軸化、未宣言依存のnonterminal化を整合と判定。
- Grok: `READY — blockingなし`。
- Claude: 初回最終監査でunavailability reasonの集約保持とworker validation provenanceの2点を指摘。両点を追加修正後、`READY — blockingなし`。
- ChatGPT: 上記指摘を本文、受入条件、完了判定へ反映し、旧語彙と矛盾する参照が残っていないことを確認。
