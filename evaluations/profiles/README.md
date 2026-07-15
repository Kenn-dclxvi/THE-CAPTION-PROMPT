# Profiles

比較開始前にmodel、Agent、environment、実行policy、repetition、成功基準、停止条件を固定する。結果確認後の変更は新revisionとして扱う。

実行順は再現用provenanceとして保存するが、A / Bの実行環境を揃える補正には使わない。global queueでは処理時間短縮のために過去の所要時間が長いslotから投入し、空いたworkerへ次のslotを渡す。実測tokenと時間は環境補正せずKPIへ渡す。

最新の完了済みprofileは[`revision-2-core9-global-m4-r2.json`](revision-2-core9-global-m4-r2.json)である。これはv1のwinnerによりN=1 screenからN=3 confirmationへ進む履歴profileであり、新しいv2 cycleへ再利用しない。

v2の新しい比較は、winnerやKPI優先順位を持たない新revisionを作り、実行前に`N`を固定する。
