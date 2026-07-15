# Profiles

比較開始前にmodel、Agent、environment、実行policy、repetition、成功基準、停止条件を固定する。結果確認後の変更は新revisionとして扱う。

実行順は再現用provenanceとして保存するが、A / Bの実行環境を揃える補正には使わない。global queueでは処理時間短縮のために過去の所要時間が長いslotから投入し、空いたworkerへ次のslotを渡す。実測tokenと時間は環境補正せずKPIへ渡す。

最新の完了済みv2 profileは[`revision-2-expanded12-global-m24-n1-r1.json`](revision-2-expanded12-global-m24-n1-r1.json)である。12 case、A / B各1回、合計24 slotを`M=24`で実行し、[`result`](../results/revision-2-expanded12-global-m24-n1_2026-07-15.md)へ3 KPIと`B - A`差分を記録した。

直前の[`revision-2-core9-global-m4-r2.json`](revision-2-core9-global-m4-r2.json)はv1のwinnerによりN=1 screenからN=3 confirmationへ進む履歴profileであり、新しいv2 cycleへ再利用しない。

v2の新しい比較は、winnerやKPI優先順位を持たない新revisionを作り、実行前に`N`を固定する。

expanded profileにF09 r1とF10 review r1はexecution blockerのため含めない。
