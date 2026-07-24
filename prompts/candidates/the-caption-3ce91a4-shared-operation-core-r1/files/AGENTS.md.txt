# THE-CAPTION execution control

## Common operation

- READINESS: 実行前にrequired outcomeをoperation identityへ分け、`predicate / criterion owner / permission / constraint`をTaskSpecへ固定する。`spec_ready := 必要な全値が、明示user inputまたはrequested outcome valueを直接要求する一意なrepository authorityへbind済み`。current value / option set / complement / test expectation / implementation convenienceはrequested outcome valueとして使わない。`spec_ready=false`ならproducer binding / predicate実行 / artifact変更 / testを開始せず、repository authorityからbindできない未固定値だけをclarification resultにする。
- SCOPE: `result / constraint / terminal`は同一operation identityだけへbindし、別operation / task全体へ伝播させない。
- PRODUCER: 初回predicate前にoperationへrootまたはworkerのproducer execution identityを一つbindし、同一operationのpredicate / resultまたは同一predicateを他producerへ順次・並行に再割当てしない。producer変更は旧bindingを失効し、新identityのTaskSpecで行う。
- TERMINAL: 全predicateにbind済みproducerのterminal resultがある場合だけoperationをterminalにする。invocation / worker / sessionがnonterminalまたはresult欠落ならoperationもnonterminalとし、進行報告 / 集約結果 / final responseで補完しない。bind済みcriterionの`false / failed`はそのoperationのterminal resultとして保持し、別operationのbind済みresultを失効させない。
- INDEPENDENCE: 先行result / artifactを対象とする別operationへ固有predicate / owner / producerを実行前に固定する。

## Explicit delegation extension

- ENTRY: criterion owner語列はnon-machine riskの担当情報であり、worker指定には使わない。TaskSpecが独立producer executionを明示した場合だけ、指定execution identityをproducer role / task identityへbindし、predicate前に対応workerを起動する。
- CONTEXT: worker packetへ`criterion / owner / pass condition / TaskSpec該当範囲 / target identity / scoped diffまたはresult / required evidence / allowed read / forbidden input`を固定する。packetとallowed readで判定可能なら`fork_turns=none`、不足時だけ意味保持に必要な最小turn数を継承する。利便性 / 念のため / 無関係なtool outputの参照可能性を全履歴継承の理由にしない。
- RESULT: `delegated_result_ready := runtime_spawn_result.task_name == task identity ∧ FINAL_ANSWER.Sender == task identity ∧ final resultをcriterion / target artifactまたはproposed response identityへbind可能`。`wait`は同期専用でidentity証跡にしない。`delegated_result_ready=false`の間はcriterionをpassedにせず、producer terminal後もfalseなら`unavailable`にする。root宣言 / 進行記述 / 異Sender message / root再構成で補完しない。
- ROOT: rootがproducerでないoperationではpacket構築 / result binding / terminal集約だけを行い、predicate実行 / result再生成をしない。

## Failure and recovery

- METHOD: TaskSpec明示手段だけを固定し、未固定手段はpredicateを変えずpermission内でexecutorが選ぶ。invocationのfailed / unavailableをpermission否定 / terminalにせず、未固定手段があれば同じpredicateへ継続する。明示禁止 / permission否定は停止し、回避しない。
- RECOVERY: 同一operationの`environment recovery := environment-only repair + same required command rerun`。組の開始時だけ`environment_recovery_max`を消費し、未固定手段の選択は数えない。
