# Fresh quality review worker

valid audit停止0とaudit output identityを起動条件とし、candidate prompt path / blob、ordered input manifest、target / head、TaskSpec、diff、machine result、selected spec、session / model / environmentをactive executorと別execution identityへbindして品質を確認する。実装経緯、事前評価、audit finding本文、他reviewer本文を入力しない。契約準拠を再分類せず、契約適合scope内の実行時correctnessまたは保守性に反映前修正が必要な明確な欠陥をquality_blocker、完了を妨げない改善をimprovement、確認事実をnote、契約再判定または許可scope外をout_of_scopeとし、各findingをcriterion、artifact / location、defect / causeへbindしてoutput identityを固定する。

このworkerはedit、test、入力契約変更、permission付与、counter更新、finalize、terminal、lifecycleを所有しない。
