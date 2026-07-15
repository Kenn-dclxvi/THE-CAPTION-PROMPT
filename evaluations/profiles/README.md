# Profiles

比較開始前にmodel、Agent、environment、実行policy、repetition、成功基準、停止条件を固定する。結果確認後の変更は新revisionとして扱う。

実行順は再現用provenanceとして保存するが、A / Bの実行環境を揃える補正には使わない。global queueでは処理時間短縮のために過去の所要時間が長いslotから投入し、空いたworkerへ次のslotを渡す。実測tokenと時間は環境補正せずKPIへ渡す。

最新のv3 profileは[`baseline N=5`](baseline-expanded12-global-m24-n5-r1.json)、[`candidate1 N=5`](candidate1-expanded12-global-m24-n5-r1.json)、[`candidate2 N=5`](candidate2-expanded12-global-m24-n5-r1.json)、[`candidate3 N=5`](candidate3-expanded12-global-m24-n5-r1.json)、[`candidate4 N=5`](candidate4-expanded12-global-m24-n5-r1.json)、[`candidate5 N=5`](candidate5-expanded12-global-m24-n5-r1.json)である。各prompt setをexpanded 12 case、`1..5`、`M=24`の同一互換条件へ固定し、単独resultとして登録した。既存`N=1` profileとresultは変更していない。

最初のv3 standalone profileは[`candidate2-expanded12-global-m24-n1-r1.json`](candidate2-expanded12-global-m24-n1-r1.json)である。candidate2の12 caseを`N=1`、`M=24`で実行し、[`result`](../results/candidate2-expanded12-global-m24-n1_2026-07-15.md)へ単一prompt setの3 KPIを記録した。

比較用baselineも固定A / B profileへ戻さず、[`baseline-expanded12-global-m24-n1-r1.json`](baseline-expanded12-global-m24-n1-r1.json)として単独実行した。candidate2 profileとの互換条件key一致を確認し、保存済み2 resultから比較viewを生成した。

candidate1も[`candidate1-expanded12-global-m24-n1-r1.json`](candidate1-expanded12-global-m24-n1-r1.json)として単独実行し、同じcompatibility keyを持つ3つの保存resultから比較viewを生成した。

最新の完了済みv2 profileは[`revision-2-expanded12-global-m24-n1-r1.json`](revision-2-expanded12-global-m24-n1-r1.json)である。12 case、A / B各1回、合計24 slotを`M=24`で実行し、[`result`](../results/revision-2-expanded12-global-m24-n1_2026-07-15.md)へ3 KPIと`B - A`差分を記録した。

直前の[`revision-2-core9-global-m4-r2.json`](revision-2-core9-global-m4-r2.json)はv1のwinnerによりN=1 screenからN=3 confirmationへ進む履歴profileであり、新しいv2 cycleへ再利用しない。

v2の新しい比較は、winnerやKPI優先順位を持たない新revisionを作り、実行前に`N`を固定する。v3ではA / B pairをprofile identityにせず、1 prompt set単位でprofileを固定する。

expanded profileにF09 r1とF10 review r1はexecution blockerのため含めない。
