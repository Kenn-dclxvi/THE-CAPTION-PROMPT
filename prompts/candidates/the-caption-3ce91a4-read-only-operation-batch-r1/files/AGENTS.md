# THE-CAPTION execution control

- READINESS: required outcomeの値は、明示user inputまたはその値を直接定める一意なrepository authorityだけから確定する。current value、option set、complement、test expectation、implementation convenienceから推測しない。未確定値があればその値だけを質問して停止し、producer binding、predicate実行、artifact変更、testを開始しない。
- OPERATION: 初回predicate前に、TaskSpecで確定済みの`required outcome / predicate / permission / constraint`を同一operationへbindする。`result / constraint / terminal`はそのoperation内だけへbindし、別operationまたはtask全体へ伝播させない。
- FIXED_READ: operation全体がedit=false、test=false、dependency=falseで、実行前TaskSpecが許可read path / commandとread-only validationを有限列挙した場合だけ、rootは列挙済みreadを個別tool callとexitを保って同一model stepで取得する。一条件でも未明示なら非適用とし、repository authority / stateから補完・拡張しない。
- PRODUCER: 初回predicate前にrootを一つのproducerとしてbindする。同じoperationのpredicate実行またはresult生成を別producerへ再割当てしない。TaskSpecが独立producer executionを明示した場合だけ、その指定identityへbindする。
- TERMINAL: required predicateすべてにbind済みproducerのterminal resultがある場合だけoperationをterminalにする。invocation、worker、sessionがnonterminal、またはresultが欠ける場合はnonterminalを保ち、進行報告やfinal responseで補完しない。`false / failed / unavailable`はそのoperationのterminal resultとして保持し、別operationの確定済みresultを失効させない。
- METHOD: TaskSpecが手段を明示した場合だけ固定する。未固定手段は同じpredicateとpermission内で選ぶ。個別invocationの`failed / unavailable`だけでoperationをterminalにせず、許可された未固定手段が残れば継続する。明示禁止またはpermission否定は回避せず停止する。
- DELEGATION: criterion owner語列は担当情報であり、worker指定ではない。TaskSpecが独立producer executionを明示した場合だけ、指定task identityをproducerへbindし、predicate前に起動する。
- CONTEXT: workerには`未解決predicate / target / required evidence / allowed read / forbidden input`を渡す。これで十分なら`fork_turns=none`とし、不足時も必要最小限だけ継承する。
- DELEGATED_RESULT: `runtime_spawn_result.task_name`と`FINAL_ANSWER.Sender`が指定task identityに一致し、final resultをpredicateとtargetへbindできる場合だけ成立する。`wait`は同期だけに使う。rootがproducerでないoperationではpacket、result binding、terminal集約だけを行い、predicateやresultを再生成しない。producer terminal後もresultが欠ける場合は`unavailable`とし、rootの宣言で補完しない。
