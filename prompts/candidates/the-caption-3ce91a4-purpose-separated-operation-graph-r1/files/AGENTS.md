# THE-CAPTION execution control

## Outcome readiness

- READINESS: `spec_ready := 全required outcome valueが、明示user inputまたはそのvalueを直接要求する一意なrepository authorityからTaskSpecへ固定済み`。current value / option set / complement / test expectation / implementation convenienceは根拠にしない。`spec_ready=false`ならproducer binding / predicate実行 / artifact変更 / testを開始せず、未固定値だけを質問して停止する。

## Fixed operation

- OPERATION: trueならrequired outcomeをoperation identityへ分け、各identityへ`predicate / criterion owner / permission / constraint`を固定する。`result / constraint / terminal`は同一identity内だけへbindし、別operation / task全体へ伝播させない。
- PRODUCER: 初回predicate前に各operationへ一つbindする。`DELEGATION`がなければrootとする。同一operationを他producerへ順次・並行に再割当て・再生成しない。変更は旧bindingを失効し、新identityのTaskSpecで行う。
- COMPLETION: 全predicateにbind済みproducerのterminal resultがある場合だけterminalにする。invocation / worker / sessionがnonterminal、またはresult欠落ならoperationもnonterminalとし、進行報告 / 集約結果 / final responseで補完しない。
- INDEPENDENCE: 先行result / artifactを対象とする別operationは、固有predicate / owner / producerを実行前に固定する。同一predicateを別producerへ再割当てしない。
- METHOD: TaskSpec明示手段だけを固定し、他は同じpredicate / permission内でexecutorが選ぶ。invocationのfailed / unavailableをpermission否定 / terminalにせず、未固定手段があれば継続する。明示禁止 / permission否定は停止し、回避しない。
- RECOVERY: 同一operationの`environment recovery := environment-only repair + same required command rerun`。組の開始時だけ`environment_recovery_max`を消費し、未固定手段の選択は数えない。

## Explicit delegation

- DELEGATION: criterion owner語列は担当情報でありworker指定ではない。TaskSpecが独立producer executionを明示した場合だけ、指定identityをtask identityとproducerへbindし、predicate前にworkerを起動する。
- CONTEXT: packetへ`criterion / owner / pass condition / TaskSpec範囲 / target identity / scoped diffまたはresult / required evidence / allowed read / forbidden input`を固定する。packetとallowed readで十分なら`fork_turns=none`、不足時も必要最小turnだけを継承する。利便性や無関係なtool outputを全履歴継承の理由にしない。
- RESULT: `delegated_result_ready := spawnのtask_nameとFINAL_ANSWER.Senderがtask identityに一致 ∧ final resultをcriterion / target artifactまたはproposed responseへbind可能`。`wait`は同期専用とする。falseの間はpassedにせず、producer terminal後もfalseなら`unavailable`にする。bind済み`false / failed`は当該operationのterminal resultとし、別operationを失効させない。root宣言 / 進行記述 / 異Sender message / root再構成で補完しない。
- ROOT: rootがproducerでないoperationではpacket構築 / result binding / terminal集約だけを行い、predicate実行 / result再生成をしない。
