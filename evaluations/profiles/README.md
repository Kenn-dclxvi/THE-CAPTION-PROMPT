# Profiles

比較開始前にmodel、Agent、environment、実行policy、repetition、成功基準、停止条件を固定する。結果確認後の変更は新revisionとして扱う。

実行順は再現用provenanceとして保存するが、A / Bの実行環境を揃える補正には使わない。global queueでは処理時間短縮のために過去の所要時間が長いslotから投入し、空いたworkerへ次のslotを渡す。実測tokenと時間は環境補正せずKPIへ渡す。

現在のstaged comparisonは[`revision-2-core9-global-m4-r2.json`](revision-2-core9-global-m4-r2.json)で固定する。F09を除く9 caseを対象に、`M=4`、N=1 screen、必要時N=3 confirmationを行う。
