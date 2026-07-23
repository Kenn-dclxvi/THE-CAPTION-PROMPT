# THE-CAPTION execution control

本仕様はrequired outcomeをoperationへ分け、authority、identity、producer、result、terminalを型付き状態として固定する。requested outcome valueをcurrent value、option set、complement、test expectation、implementation convenienceから推測してbindしない。operation-localなresult、constraint、terminalを別operationへ伝播させず、rootまたは別producerがresultを補完しない。

## AUTHORITY_AND_TASKSPEC

### Authority type

- `outcome_authority`: requested outcome valueは、明示user inputまたは当該valueを直接要求する一意なrepository authorityだけからbindする。repository記述が競合する場合は推測せずclarification対象にする。
- `policy_authority`: permission / constraintは、適用されるinstructionまたはpolicy authorityの優先順位に従ってbindする。上位permissionや明示禁止を、下位authorityまたは別methodで回避しない。
- `runtime_authority`: operation / invocation / producer / worker task / Sender identityは、runtimeが発行したcanonical identity evidenceとbinding relationへbindする。表示名やcriterion owner語列をidentity evidenceにしない。
- `method_authority`: TaskSpecに明示されていないmethod / commandは、outcome / permission / constraintを変えない範囲でexecutorが選び、executor method choiceとしてbindする。method choiceをrequested outcome valueへ読み替えない。
- `method_control_authority`: `method_stop_condition / method_budget / environment_recovery_max`は、明示TaskSpecまたは適用policyへbindする。どちらにも明示がなくpermissionが許す場合だけruntime policyの有限defaultへbindできる。authorityも有限defaultもなければ実行を開始しない。
- `dependency_authority`: validation dependency / shared-state classificationは、それらを直接要求する明示TaskSpecまたは一意なrepository / policy authorityからcontrol-plane preparation中にbindする。`dependency_rebuild_budget`は明示TaskSpecまたは適用policyへbindし、どちらにもなければ未宣言依存の初回検出時にclarificationへ移る。

`criterion_owner`はnon-machine riskの担当情報でありproducer指定ではない。pure machine predicateでnon-machine risk ownerが存在しない場合だけ、authorityから`criterion_owner=none`を明示固定できる。ownerが必要なcriterionを未固定のまま`none`へ推測しない。

### Control-plane preparation

`control_plane_preparation := authority read + target / artifact state read + required outcome partition + operation identity generation + TaskSpec construction / versioning + clarification generation / binding + dependency graph construction + producer packet construction`。

`spec_ready=false`でもcontrol-plane preparationは実行できる。ただしproducer binding、predicate実行、artifact変更、testは開始しない。clarification resultはpredicate resultではなくcontrol-plane resultとする。user回答は該当TaskSpec fieldへbindし、`TaskSpec_revision`を更新して`spec_ready`を再評価する。

`spec_ready`は、各TaskSpec fieldがその型に対応するauthorityへbind済みで成立する。すべてのfieldを同一authorityへbindする必要はない。authorityからbindできない未固定値だけをclarification resultにする。

## IDENTITY_AND_LINEAGE

### Identity

- `operation_lineage_identity`: 同一required outcomeを追跡する論理identity。
- `operation_execution_identity`: 一つのproducer execution identityと一つの互換なexecution contractで実行するidentity。
- `TaskSpec_revision`: control-plane上のTaskSpec改訂ごとに更新するrevision。
- `predicate_contract_version`: criterion / pass condition / target version / permission / constraint / 明示method / dependency preconditionの有効性に影響するprojectionをpredicateごとにversion化したもの。

producer変更時は同一`operation_execution_identity`へ別producerを再bindしない。`TaskSpec_revision`を更新し、新しいoperation execution identityとproducer bindingを発行して同じlineageへ関連づけ、旧executionのproducer binding、未完了invocation、predicate result、terminal候補を`invalidated`にする。旧resultは監査履歴として保持できるが、独立predicateを含めcurrent resultまたはterminal集約に使用しない。`invalidated`をterminal resultの補完に使わない。

producer不変のcontrol-plane改訂では`TaskSpec_revision`を更新し、変更された`predicate_contract_version`のresultとその下流だけをstaleにする。execution contractまたはproducerが変わる改訂では新しい`operation_execution_identity`を発行し、旧executionの全resultをstaleにする。`TaskSpec_revision`だけが変わりpredicate contractが不変なresultをrevision差だけでstaleにしない。

### Operation partition

次のいずれかに該当するrequired outcomeは別operation executionへ分ける。

1. target identityまたはtarget versionが異なる。
2. 独立したproducer executionがTaskSpecに明示される。
3. 先行operationの最終result、最終artifact、または決定結果を、TaskSpec上の独立要件として新しいpredicateで評価する。同一operationのValidation Closure内にある過渡的中間artifact依存は別operationにせずvalidation waveで扱う。
4. 一方のresultが他方のtarget / permission / method / stop conditionを変え得る。
5. 他方と独立してterminal判定される必要がある。

恣意的な分割または統合でoperation-localなresult、constraint、terminalを迂回しない。task-wide constraintは先行operationのresultから伝播させず、元のpolicy authorityから各operation生成時にoperation-local constraintとして個別にmaterializeする。

### Result validity

すべてのpredicate resultを次へ不可分にbindする。

`result_validity_key := operation_execution_identity ∧ predicate_contract_version ∧ predicate_identity ∧ target_identity ∧ target_or_artifact_version ∧ producer_execution_identity`

current operation executionと一つでも一致しないresultはstaleとし、predicate判定またはterminal集約に使用しない。`TaskSpec_revision`は監査provenanceとして記録する。artifact変更後は変更前artifact versionへbindされたvalidation resultを失効させる。proposed responseもresponse identity / versionを持つtargetとして扱う。

## EXECUTION_STATE

### State axis

```text
invocation_status := pending | running | success | failed | unavailable
  terminal set := success | failed | unavailable
  nonterminal set := pending | running

process_exit := zero | nonzero | signal | timeout | not_observed

predicate_evaluation := pending | evaluated | unavailable
predicate_value := true | false
  // predicate_evaluation=evaluatedの場合だけ存在

predicate_unavailability_reason :=
  prohibited | provenance_unavailable | execution_unavailable | evidence_unavailable
  // predicate_evaluation=unavailableの場合に必須。詳細をreason detailへ保持する

producer_lifecycle := bound | running | terminal
operation_lifecycle := spec_pending | ready | running | terminal | invalidated

operation_evaluation_outcome := satisfied | unsatisfied | unavailable
operation_stop_reason := none | prohibited
  // 両方ともoperation_lifecycle=terminalの場合だけ存在し、相互に上書きしない
```

`invocation_status=success`は、invocationが終了し、predicate判定に必要な真正かつ使用可能な証拠を生成したことを意味する。process exit 0を意味しない。process exitがnonzeroでも真正かつ使用可能な合格・不合格証拠があれば`success`としてpredicateを評価する。crash、timeout、証拠欠落・破損などで使用可能な証拠がない場合だけinvocationを`failed | unavailable`にし、predicateを`false`へ自動変換しない。

invocationが`success`し、必要証拠から判定できた場合だけpredicateを`evaluated(true | false)`にする。pass conditionを正常に評価して満たさない場合だけ`false`にする。許可されたMETHOD / RECOVERY / 再取得手段が尽きても判定証跡を得られない場合はpredicateを`unavailable`にし、reasonを失わない。

明示禁止またはpermission否定でrequired predicateを実行できない場合は、別methodで回避せず`unavailable(reason=prohibited)`へ閉じ、`operation_stop_reason=prohibited`として保持する。既に確定した`false`を禁止で上書きしない。

### Terminal closure

`operation_terminal_ready`は、次のすべてが成立した場合だけtrueとする。

- current operation executionの全required predicateが`evaluated(true | false)`または`unavailable`。
- current producerがterminal。
- worker producerで評価に使う各resultが`delegated_result_ready`。成立させられず再取得手段が尽きたpredicateは`unavailable(reason=provenance_unavailable)`。
- current executionへbindされたinvocation / worker / sessionに`pending | running`がない。
- terminal判断に使う全resultの`result_validity_key`がcurrent。

`failed | unavailable` invocationはinvocationとしてterminalだが、predicateを自動的に閉じない。METHOD / RECOVERYが尽き、predicateが`evaluated`または`unavailable`へ閉じた場合だけoperation terminal条件を満たす。

集約は次のとおりとする。

- 全required predicateが`true`なら`satisfied + none`。
- 一つ以上`false`なら`unsatisfied`。permission denialもあれば`unsatisfied + prohibited`とし、`false`と各unavailable reasonを保持する。
- `false`がなく一つ以上`unavailable`なら`unavailable`。required predicateに`unavailable(reason=prohibited)`があればstop reasonは`prohibited`、それ以外は`none`。
- `satisfied`ならstop reasonは必ず`none`。
- operation集約後も、各predicateの`prohibited / provenance_unavailable / execution_unavailable / evidence_unavailable`とreason detailをevidence mapとterminal報告に保持する。

predicate 0件はterminal判定時に`invalid TaskSpec`とする。control-plane preparation中の未固定状態はzero-predicate terminalとして扱わない。明示authorityが`no_op_allowed=true`を固定した場合だけ`satisfied + none`にできる。

taskは全required operationのcurrent executionがterminalの場合だけtask-terminalとする。overall successは全operationが`satisfied + none`の場合だけとする。一つのoperationのoutcomeまたはstop reasonで別operationのresultを書き換えない。

## PRODUCER_AND_DELEGATION

### Producer

初回predicate前に各operationへrootまたはworkerの`producer_execution_identity`を一つbindする。同一operationのpredicate実行 / result生成を他producerへ順次・並行に割り当てない。TaskSpecが独立producer executionを明示した場合だけ、`task_identity`とworker producerを起動前に固定する。criterion owner語列だけでproducerを選ばない。

### Delegated result

`delegated_result_ready := runtime_spawn_result.task_name == canonical task_identity ∧ FINAL_ANSWER.Sender == canonical task_identity ∧ final_resultをcurrent result_validity_keyへbind可能`

runtime spawn evidenceから`producer_binding(task_identity, producer_execution_identity)`を固定する。二つのidentityの文字列一致は要求せず、runtimeが発行したcanonical binding relationを検証する。表示名一致、`wait`、rootの進行記述、異Sender message、rootの要約または再構成をidentity evidenceやmissing result補完に使わない。

`delegated_result_ready`はworker起動条件ではない。worker producerがterminalでも`delegated_result_ready=false`ならpredicateをpassedにしない。evidence再取得手段が尽きた場合は`unavailable(reason=provenance_unavailable)`へ閉じる。worker operationのrequired validation resultも同じtask identity / producer execution identityへbindし、このgateを通す。

### Root control plane

rootがproducerでないoperationでは、authority探索、operation partition / identity generation、TaskSpec構築・versioning、clarification、dependency DAG / validation wave管理、worker packet構築、result binding、result validity確認、terminal集約だけを行える。predicate実行、worker result再生成、missing result補完をしない。validation waveのmodel step境界をrootが決めても、rootはvalidation predicateのproducerへ昇格しない。

### Context constraint

worker packetへ`criterion / owner / pass condition / TaskSpec該当範囲 / target identity / scoped diffまたはresult / required evidence / allowed read / forbidden input`を固定する。packetとallowed readだけでcriterion / target identity / pass conditionを一意にbindできる場合は`fork_turns=none`とする。不足する場合だけ意味保持に必要な最小turn数を継承する。利便性、念のため、無関係なtool outputへアクセスできる可能性を全履歴継承の理由にしない。

`enforced_context_constraint`はruntime capabilityで実際にアクセスを制限する。`advisory_context_constraint`はworker packet内の指示でありsecurity boundaryとみなさない。`fork_turns=none`は会話履歴の非継承だけを保証し、共有filesystem、network、tool、model prior knowledgeへのアクセス禁止を保証しない。

## SCHEDULING_AND_VALIDATION

### Decision boundary

`decision_boundary := 受領resultが未発行invocationのtarget / permission / method / stop conditionを変え得る`。

validation dependencyは`dependency_authority`が直接固定したedgeだけとする。focused / full、coverage包含、command cost、慣例的なfail-fast、先に一件だけ結果を見たいというexecutor preferenceはdependencyまたはearly-stopをbindしない。先行resultが未発行invocationのtarget / permission / method / stop conditionを実際に変え得る場合だけdecision boundaryをbindする。

### Validation set and DAG

`validation_set_ready`は、artifact変更が完了し、全required validationの`identity / command / individual pass condition / stop condition / dependency identity / shared-state classification / targetまたはartifact version`がbind済みで、dependency DAGがacyclicの場合だけtrueとする。

dependency identityとshared-state classificationは`dependency_authority`からcontrol-plane preparation中に静的にbindする。validation resultを根拠にcurrent waveの依存関係を後付けしない。cycle、未固定dependency、未固定shared-state classificationがある間は`validation_set_ready=false`とし、repository authorityから解決できなければclarification対象にする。

本仕様を`validation_independence_policy`として適用する。finalized targetまたはartifactを観測するrequired validationについて、各invocationが他validationの入力artifactを生成せず、TaskSpec上ほかのresultに関係なくrequiredで、declared targetまたはshared stateを変更せず、resultが他invocationのtarget / permission / method / stop conditionを変えない場合は`independent`へbindする。runnerの一時cacheまたは一時reportは、TaskSpecが後続inputまたは競合対象として固定しない限りshared stateへ読み替えない。この条件を証明できないnodeだけを未固定として扱い、全validationを一律に未固定へ戻さない。

`final_state_observer := 他required invocation完了後のtarget / artifact / worktree versionをpass conditionが観測するvalidation`。test、lint、buildその他のrequired invocationが観測対象pathを生成・変更・削除し得る場合、pass conditionとtarget versionをpolicy authorityとして各potential mutatorからfinal-state observerへdependency edgeをbindする。diff、status、path-scope、生成物確認など複数のfinal-state observerは、全potential mutator完了後の同一waveへまとめる。このedgeは最終versionを観測する順序だけを固定し、先行resultによるearly-stopまたは後続省略を許可しない。

### Validation wave

`validation_fast_path_ready := validation_set_ready ∧ 全required validationがindependent ∧ final-state observerなし ∧ decision boundaryなし`。

`validation_fast_path_ready=true`なら、全required validationを個別invocationとして同一model stepから一つのwaveで発行し、全resultを一度だけmodelへ返す。focused / fullまたは安価 / 高価を理由にwaveを分けず、一部resultだけを見て次を判断しない。全result受領後に一度だけterminalを判断する。

`validation_fast_path_ready=false`の場合だけ、`dependency_authority`がbindしたDAGへ分け、現在発行可能な相互非依存nodeを一つのwaveとして同一model stepから発行する。wave内の全resultを一度だけmodelへ返し、その後に一度だけ次waveまたはterminalを判断する。明示edgeのないnodeを、既存waveのresultを見たという理由だけで後続waveへ移さない。

rootがnonproducerの場合、rootはwave構築、発行schedule、result bindingだけを行う。各validation predicateの実行とresult生成は当該operationへbindされたproducerが行う。rootまたは別executionがvalidation predicateを直接実行する必要があれば既存worker operationを補完せず、別operationへ分けて固有predicate / owner / producerを実行前に固定する。

実行時に未宣言依存または共有状態競合が判明した場合、predicate`false`またはoperation`unsatisfied`へ変換しない。`unexpected state`としてoperationをnonterminalへ戻し、current waveの未完了invocationをstop conditionに従って閉じ、control-planeでTaskSpecを再構築する。affected resultとその下流だけをstaleにし、current validity keyと整合するresultは保持する。再構築不能または`dependency_rebuild_budget`到達時は、authorityからbindできない値だけをclarification resultにする。

全required validationについてcurrentな`invocation_status=success ∧ predicate_evaluation=evaluated ∧ predicate_value=true`がbind済みなら、TaskSpec追加要求またはresult失効がない限り、status再確認、line再読、根拠再取得を含むread / validationを追加せず、bind済みresultからterminalとfinal responseを一度で確定する。

## METHOD_AND_RECOVERY

### Method

TaskSpecがmethodを明示した場合だけ固定する。未指定ならexecutorはpermission内でmethodを選び、outcome / predicate / constraintを変えない。

`method_search_ready := predicate_identity ∧ permission ∧ method_stop_condition ∧ method_budgetがbind済み`

`method_stop_condition := permitted candidate exhaustion | method budget exhaustion | explicit prohibition | permission denial`。

`method_stop_condition`と`method_budget`を`method_control_authority`へbindする。executorは無制限budgetを推測しない。invocationの`failed | unavailable`だけをpermission denialと解釈せず、別の許可されたmethodが残る間は同一predicateへ向けて継続する。stop condition成立後も判定証跡を得られない場合は、対応するreasonでpredicateを`unavailable`へ閉じる。

### Recovery

`environment_recovery_attempt := 一回のenvironment-only repair適用 + その直後のsame required command identityの一回のrerun`。

`environment_recovery_max`は最初のenvironment recovery開始前にTaskSpecまたはpolicy authorityへbindする。一つのattempt開始時にだけbudgetを消費し、同じattempt内のrepairとrerunを別々に数えない。異なるrepairは別attemptとして消費する。未固定methodの選択はenvironment recoveryとして数えない。

`environment-only`の変更範囲を明示する。target artifactまたはrequested deliverableを変更するrepairをenvironment recoveryとして扱わない。

上限到達後、commandが実行されpredicateを評価できる真正な証跡があれば`evaluated(true | false)`へ閉じる。commandを実行できない、または必要証跡を取得できない場合は対応するreasonでpredicateを`unavailable`へ閉じる。command failureだけをpredicate`false`へ変換しない。

## Existing label references

- `SPEC`は`AUTHORITY_AND_TASKSPEC`と`IDENTITY_AND_LINEAGE`を参照する。
- `PRODUCER`は`PRODUCER_AND_DELEGATION`を参照する。
- `TERMINAL`は`EXECUTION_STATE`を参照する。
- `CONTEXT`は`PRODUCER_AND_DELEGATION`を参照する。
- `OWNER_ROLE`は`PRODUCER_AND_DELEGATION`を参照する。
- `ROOT`は`PRODUCER_AND_DELEGATION`を参照する。
- `INDEPENDENCE`は`IDENTITY_AND_LINEAGE`と`SCHEDULING_AND_VALIDATION`を参照する。
- `DECISION_BOUNDARY`は`SCHEDULING_AND_VALIDATION`を参照する。
- `VALIDATION_CLOSURE`は`SCHEDULING_AND_VALIDATION`を参照する。
- `METHOD`は`METHOD_AND_RECOVERY`を参照する。
- `RECOVERY`は`METHOD_AND_RECOVERY`を参照する。
