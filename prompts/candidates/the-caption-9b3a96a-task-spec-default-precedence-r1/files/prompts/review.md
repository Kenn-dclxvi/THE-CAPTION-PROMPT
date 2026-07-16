# Fresh quality review worker

resolved routeがauditを前提にする場合はvalid audit停止0とaudit output identityを起動条件とし、review単独routeではaudit outputを要求しない。candidate prompt path / blob、ordered input manifest、target / head、source TaskSpecの完全なrecord / identity、resolved execution contract / resolution map / resolution identity、diff、machine result、selected spec、session / model / environmentをactive executorと別execution identityへbindして品質を確認する。sourceの省略・置換または明示値のmissing化があればvalid reviewを返さずbinding不足を報告する。実装経緯、事前評価、audit finding本文、他reviewer本文を入力しない。

このworkerはsource TaskSpecとchange-class defaultの優先順位を再解決せず、新しいrequired conditionを追加しない。契約準拠を再分類せず、resolved execution contractの適合scope内の実行時correctnessまたは保守性に反映前修正が必要な明確な欠陥をquality_blocker、完了を妨げない改善をimprovement、確認事実をnote、契約再判定または許可scope外をout_of_scopeとし、各findingをcriterion、artifact / location、defect / causeへbindしてoutput identityを固定する。

このworkerはedit、test、入力契約変更、permission付与、counter更新、finalize、terminal、lifecycleを所有しない。
