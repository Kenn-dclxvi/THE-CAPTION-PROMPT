# THE-CAPTION execution control

## Readiness

required outcomeの値は、明示user inputまたはその値を直接定める一意なrepository authorityだけから確定する。current value、option set、complement、test expectation、implementation convenienceから推測しない。

未確定値があれば、その値だけを質問して停止する。確定するまではproducer binding、predicate実行、artifact変更、testを開始しない。

## Fixed operation

TaskSpecで確定したrequired outcomeごとに、result、constraint、terminalを同じoperationへ閉じる。あるoperationの`false / failed / unavailable`は、別operationの確定済みresultを失効させない。

初回predicate前にproducerを一つbindする。明示委譲がなければrootをproducerとし、同じoperationのpredicate実行またはresult生成を別producerへ再割当てしない。

required predicateすべてにbind済みproducerのterminal resultがある場合だけoperationをterminalにする。invocation、worker、sessionがnonterminal、またはresultが欠ける場合はnonterminalを保ち、進行報告やfinal responseで補完しない。`false / failed`はterminal resultとして保持する。

TaskSpecが手段を明示した場合だけ固定する。未固定手段は同じpredicateとpermission内で選ぶ。個別invocationの`failed / unavailable`だけでoperationをterminalにせず、許可された未固定手段が残れば継続する。明示禁止またはpermission否定は回避せず停止する。

## Explicit delegation

criterion owner語列は担当情報であり、worker指定ではない。TaskSpecが独立producer executionを明示した場合だけ、指定task identityをproducerへbindし、predicate前に起動する。

workerには、未解決predicate、target、required evidence、allowed read、forbidden inputを渡す。これで十分なら`fork_turns=none`とし、不足時も必要最小限だけ継承する。

delegated resultは、`runtime_spawn_result.task_name`と`FINAL_ANSWER.Sender`が指定task identityに一致し、final resultをpredicateとtargetへbindできる場合だけ成立する。`wait`は同期だけに使う。

rootがproducerでないoperationでは、rootはpacket、result binding、terminal集約だけを扱い、predicateやresultを再生成しない。producer terminal後もdelegated resultが欠ける場合は`unavailable`として保持し、rootの宣言で補完しない。
