# THE-CAPTION conditional exception transitions

この文書はroot `AGENTS.md`の`EXCEPTION_TRANSITION`が指定したheadingだけを、該当operationの例外遷移として適用する。通常経路では読まない。読んだ節もC71 coreを置換せず、triggerに関係するfield、result、transitionだけを精緻化する。

## AUTHORITY_AND_TASKSPEC

### R-01 field-specific authority

- `outcome_authority`: requested outcome valueは、明示user inputまたはそのvalueを直接要求する一意なrepository authorityだけへbindする。
- `policy_authority`: permission / constraintは適用instructionの優先順位へbindし、上位の禁止を下位authorityや別methodで回避しない。
- `runtime_authority`: operation / invocation / producer / worker task / Sender identityはruntimeのcanonical identity evidenceとbinding relationへbindする。
- `method_authority`: TaskSpec未指定のmethod / commandはoutcome、permission、constraintを変えないexecutor choiceとしてbindする。
- `method_control_authority`: `method_stop_condition / method_budget / environment_recovery_max`はTaskSpecまたはpolicyへbindする。permissionが許し両方に定義がない場合だけ有限runtime defaultを使い、authorityも有限defaultもなければ該当method実行を開始しない。
- `dependency_authority`: validation dependency / shared-state classificationは、それを直接要求するTaskSpecまたは一意なrepository / policy authorityへbindする。`dependency_rebuild_budget`も同様とし、未定義なら未宣言依存の初回検出時にclarificationへ移る。

`spec_ready`は各fieldがその型のauthorityへbind済みの場合だけ成立する。current value、option set、complement、test expectation、implementation convenienceをrequested outcome valueへbindしない。

### R-02 control-plane preparation

`control_plane_preparation := authority read + target / artifact state read + required outcome partition + operation identity generation + TaskSpec construction / versioning + clarification generation / binding + dependency graph construction + producer packet construction`。

`spec_ready=false`でもcontrol-plane preparationは行えるが、producer binding、predicate実行、artifact変更、testは開始しない。clarificationはcontrol-plane resultでありpredicate resultではない。回答は該当fieldへbindし、`TaskSpec_revision`を更新して`spec_ready`を再評価する。

### R-14 nullable criterion owner

pure machine predicateでnon-machine risk ownerが存在しない場合だけ、authorityから`criterion_owner=none`を明示固定できる。ownerが必要なcriterionの未固定状態を`none`へ推測しない。

## IDENTITY_AND_LINEAGE

### R-03 identity and revision

- `operation_lineage_identity`: 同一required outcomeの論理identity。
- `operation_execution_identity`: 一つのproducer execution identityと一つの互換execution contractによる実行identity。
- `TaskSpec_revision`: control-plane上のTaskSpec改訂revision。
- `predicate_contract_version`: criterion、pass condition、target version、permission、constraint、明示method、dependency preconditionに影響するpredicate別version。

producer変更時は旧executionへ再bindしない。TaskSpec revisionを更新し、新しいoperation execution identityとproducer bindingを同じlineageへ発行する。旧producer binding、未完了invocation、全predicate result、terminal候補は`invalidated`にし、独立predicateを含めcurrent resultへ再利用しない。

producer不変のcontrol-plane改訂は変更されたpredicate contractと下流resultだけをstaleにする。execution contractまたはproducer変更はnew executionとし、旧executionの全resultをstaleにする。TaskSpec revisionだけが変わりpredicate contractが不変なresultはrevision差だけでstaleにしない。

### R-04 operation partition

target identity / versionが異なる、独立producer executionが明示される、先行operationの最終result / artifact / decisionを独立要件で評価する、一方のresultが他方のtarget / permission / method / stop conditionを変え得る、または独立terminalが必要なrequired outcomeは別operationにする。同一operation内の過渡的artifact依存は別operationにせずvalidation waveで扱う。task-wide constraintは先行resultから伝播せず、元policy authorityから各operationへ個別materializeする。

### R-06 current result validity

`result_validity_key := operation_execution_identity ∧ predicate_contract_version ∧ predicate_identity ∧ target_identity ∧ target_or_artifact_version ∧ producer_execution_identity`。

current executionと一要素でも異なるresultはstaleであり、predicate判定やterminal集約に使わない。artifact変更後は変更前versionのvalidation resultを失効させ、proposed responseにもresponse identity / versionを持たせる。履歴保存とcurrent validityを分ける。

## EXECUTION_STATE

### R-05 orthogonal state axes

```text
invocation_status := pending | running | success | failed | unavailable
  terminal := success | failed | unavailable
  nonterminal := pending | running
process_exit := zero | nonzero | signal | timeout | not_observed
predicate_evaluation := pending | evaluated | unavailable
predicate_value := true | false  # evaluatedだけに存在
predicate_unavailability_reason := prohibited | provenance_unavailable | execution_unavailable | evidence_unavailable
producer_lifecycle := bound | running | terminal
operation_lifecycle := spec_pending | ready | running | terminal | invalidated
operation_evaluation_outcome := satisfied | unsatisfied | unavailable
operation_stop_reason := none | prohibited
```

`invocation_status=success`はpredicate判定に真正で使用可能な証拠を生成した終了を表し、exit 0とは限らない。nonzeroでも有効な合格・不合格証拠があればsuccessとしてpredicateを`evaluated(true | false)`にする。crash、timeout、証拠欠落・破損は`failed | unavailable`であり、predicateを`false`へ自動変換しない。許可されたmethod / recovery / 再取得が尽きても証拠がなければpredicateをreason付き`unavailable`へ閉じる。permission否定または明示禁止は回避せず`unavailable(reason=prohibited)`と`operation_stop_reason=prohibited`を保持する。

### R-08 terminal closure

`operation_terminal_ready`は、current executionの全required predicateが`evaluated(true | false)`または`unavailable`、producerがterminal、worker resultがdelegated-result gate済み、current executionにpending / running invocation・worker・sessionなし、使用resultがcurrent validity keyの場合だけ成立する。failed / unavailable invocationはinvocationとしてterminalだがpredicateを自動的に閉じない。

全predicate trueは`satisfied + none`、一つ以上falseは`unsatisfied`、falseなしでunavailableありは`unavailable`とする。禁止が併存すればstop reasonを`prohibited`にし、`unsatisfied + prohibited`を保持する。各unavailability reasonを集約で失わない。predicate 0件は、authorityが`no_op_allowed=true`を明示した場合を除きterminal時にinvalid TaskSpecとする。taskは全required operationがterminalの場合だけterminalで、overall successは全operationが`satisfied + none`の場合だけとする。

## PRODUCER_AND_DELEGATION

### R-07 delegated result identity

`delegated_result_ready := runtime_spawn_result.task_name == canonical task_identity ∧ FINAL_ANSWER.Sender == canonical task_identity ∧ final_resultをcurrent result_validity_keyへbind可能`。

TaskSpecが独立producer executionを明示した場合だけ起動前にtask identityを固定する。runtimeのcanonical `producer_binding(task_identity, producer_execution_identity)`を使い、文字列一致、表示名、criterion owner、`wait`、root進行記述、異Sender message、root要約で補完しない。このgateはworker起動条件ではない。worker terminal後もgate不能なら再取得枯渇後に`unavailable(reason=provenance_unavailable)`へ閉じる。worker validationも同じproducer identityへbindする。

### R-12 nonproducer root control plane

nonproducer rootはauthority探索、operation partition / identity generation、TaskSpec構築 / versioning、clarification、dependency DAG / wave管理、worker packet構築、result binding / validity確認、terminal集約だけを行える。worker predicate実行、result再生成、missing result補完を行わない。wave schedulingをproducer roleへ読み替えない。

### R-13 context strength

`enforced_context_constraint`はruntime capabilityによる実制限、`advisory_context_constraint`はpacket指示でありsecurity boundaryではない。`fork_turns=none`は会話履歴だけを遮断し、filesystem、network、tool、prior knowledgeを遮断しない。packetとallowed readだけでcriterion、target identity、pass conditionをbindできる場合はnoneとし、不足時だけ意味保持に必要な最小turnを継承する。

## SCHEDULING_AND_VALIDATION

### R-09 dependency wave

`validation_set_ready`はartifact変更完了後、全required validationのidentity、command、individual pass condition、stop condition、dependency identity、shared-state classification、target / artifact versionがbind済みで、dependency DAGがacyclicの場合だけ成立する。dependencyとshared stateは`dependency_authority`から実行前にbindし、resultからcurrent waveへ後付けしない。cycleや未固定値があれば発行せず、authorityで解決不能ならclarificationへ移る。

明示dependencyがない相互非依存validationは一つのwaveとして同一model stepから発行し、全resultを一度だけ返す。依存nodeはDAGの現在発行可能な単位ごとにwave化する。wave内の一部resultだけを見て次waveを発行しない。focused / full、coverage包含、command cost、慣例的fail-fastだけではdependencyを作らない。

`final_state_observer := 他required invocation完了後のtarget / artifact / worktree versionをpass conditionが観測するvalidation`。test、lint、build等が観測対象を生成・変更・削除し得る場合だけpotential mutatorからobserverへedgeをbindし、複数observerは全mutator完了後の同一waveへまとめる。このedgeでearly-stopや後続省略を許可しない。

runtimeで未宣言依存や共有状態競合を検出した場合はpredicate falseへ変換せず`unexpected state`としてnonterminalへ戻す。current waveをstop conditionに従って閉じ、TaskSpecを再構築し、affected resultと下流だけをstaleにする。再構築不能またはbudget到達時は未固定値だけをclarificationにする。全required validationのcurrentなsuccess / evaluated / true resultが揃えば、追加要求や失効がない限りstatus再確認、line再読、根拠再取得を追加せずterminalとfinal responseを確定する。

## METHOD_AND_RECOVERY

### R-10 finite method search

TaskSpecがmethodを明示した場合だけ固定し、未指定methodはpermission内のexecutor choiceとする。`method_search_ready := predicate_identity ∧ permission ∧ method_stop_condition ∧ method_budget`。`method_stop_condition := permitted candidate exhaustion | method budget exhaustion | explicit prohibition | permission denial`。stop conditionとbudgetは`method_control_authority`へbindし、無制限を推測しない。failed / unavailableだけをpermission denialとせず、許可された別methodが残る間は同一predicateへ向けて継続する。枯渇後も証拠がなければreason付きunavailableへ閉じる。

### R-11 bounded recovery

`environment_recovery_attempt := 一回のenvironment-only repair + 直後のsame required command identityの一回rerun`。`environment_recovery_max`を最初のrecovery前にTaskSpecまたはpolicyへbindする。一attempt開始時に一回だけbudgetを消費し、別repairは別attempt、未固定method選択はrecoveryに数えない。target artifactやdeliverableを変えるrepairをenvironment-onlyとして扱わない。上限後、有効証拠があればevaluated true / false、実行不能または証拠なしならreason付きunavailableへ閉じ、command failureだけをpredicate falseへ変換しない。

## Acceptance mapping

| Scenario | 適用節 |
| --- | --- |
| A outcome authority | `AUTHORITY_AND_TASKSPEC` |
| B producer変更 | `IDENTITY_AND_LINEAGE` |
| C worker provenance | `PRODUCER_AND_DELEGATION` |
| D invocation failure | `EXECUTION_STATE` |
| E validation dependency | `SCHEDULING_AND_VALIDATION` |
| F recovery exhaustion | `METHOD_AND_RECOVERY` |
| G task-wide constraint | `IDENTITY_AND_LINEAGE` |
| H stale result | `IDENTITY_AND_LINEAGE` |
| I root非producer | `PRODUCER_AND_DELEGATION` |
| J zero predicate | `EXECUTION_STATE` |
| K policy / runtime / method authority | `AUTHORITY_AND_TASKSPEC` |
| L outcome / stop reason | `EXECUTION_STATE` |
| M operation / wave境界 | `SCHEDULING_AND_VALIDATION` |
| N producer変更とsingle producer | `IDENTITY_AND_LINEAGE` |
| O control-plane改訂 | `IDENTITY_AND_LINEAGE` |
| P delegated producer binding | `PRODUCER_AND_DELEGATION` |
| Q task集約 | `EXECUTION_STATE` |
