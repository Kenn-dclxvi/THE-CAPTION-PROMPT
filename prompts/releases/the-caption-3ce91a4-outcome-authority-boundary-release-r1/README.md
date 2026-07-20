# 候補43 リリースと投影

## 結論

候補43の19対象完全一式を、内容変更なしでTHE-CAPTIONへ投影した。

リリース状態は`projected`、承認状態は`approved`である。

候補41は直前の投影履歴と巻き戻し先として維持する。不採用またはartifact削除にはしていない。

投影結果は[`projection.json`](projection.json)へ記録した。

## 識別情報

- リリース識別子: `the-caption-3ce91a4-outcome-authority-boundary-release-r1`
- 元候補: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- 元候補の固定commit: `8702e1a031633943e0de09eced4954240202f720`
- 内容SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- 対象commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- 内容関係: 候補43と同一内容のリリーススナップショット
- 候補43から変更した対象: なし
- 現在投影済みの候補41との差: `AGENTS.md`だけ

## リリース対象とする根拠

- A01 / A02第10版の各5回は、10 / 10件が点数`4`だった。
- 標準14項目の各5回は、70 / 70件が有効かつ採点可能で、70件すべて点数`4`だった。
- 同条件の候補41ではA01の5 / 5件が未固定値を推測して編集と試験へ進んだ。候補43では5 / 5件が編集と試験の前に質問して停止した。
- 候補43の18回継続試験は、1,260 / 1,260件が有効かつ採点可能で、18結果すべてを登録・圧縮した。
- 18回継続試験の公式点数分布は`4 / 3 / 1 = 1,255 / 4 / 1`だった。
- 点数`1`のA01は採点処理の偽陰性で、実応答は編集と試験を開始せず未固定値を質問して停止していた。

## 評価範囲

- 採点条件: `outcome-boundary-owner-diagnostic-v10`
- 評価集合: `the-caption-standard14-r1`第1版
- 標準14項目単発結果識別子: `b62428c2361b435fbd0fc7c8979868e7`
- A01 / A02結果識別子: `2e0216803ef74d0ca4a536998d8ad88b`
- 18回継続試験: 14項目掛ける5回掛ける18結果、合計1,260件
- 18結果の品質点中央値: すべて`100.000`
- 18結果の全実行使用量中央値の中央値: `3,286,761`
- 18結果の所要時間中央値の中央値: `1,176.261`秒

## 未解決事項

- F10月次試験確認では、主要な指摘は正しいが位置が実変更行`monthly_main.py:25`と一致しない点数`3`を4 / 90件観測した。
- A01の1件は「明示してください」を質問表現として認識しない採点側の偽陰性だった。公式の追記専用結果は変更していない。
- 1,259 / 1,260件は起点実行だけだったが、F04の1件で担当情報を独立実行指定と解釈し、子実行を1件起動した。
- 標準14項目各5回の使用量分析では、F08だけに仕様準備境界を広く解釈した追加探索の関与可能性が残る。
- 18回継続試験の観測を評価範囲外へ一般化できない。

## 承認状態

- リリース準備: `complete`
- リリース状態: `projected`
- 採用承認: `approved`
- 本体反映: `projected`。`main`へのマージで有効化済み
- THE-CAPTIONへの書き込み、push、PR、merge: `completed`

## 投影結果

- 投影前commit / 巻き戻し先: `8409eb9899b92a76870b066d88406754f4365b52`
- 投影したmanifest対象: `19 / 19`
- 実変更対象: `AGENTS.md`一つ
- 検証: `bash ./scripts/dev/verify_change_set.sh`、`364 passed in 1.85s`
- 統合後manifest一致: `19 / 19`
- 対象外変更: 0件
- 監査停止指摘: 0件
- 重大な確認指摘: 0件
- THE-CAPTION PR: [#335](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/335)
- 統合commit: `f729810ba8693acff963ef8e1cc2f2a175197072`
- 投影記録: [`projection.json`](projection.json)

## 根拠

- [投影記録](projection.json)
- [THE-CAPTION PR #335](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/335)
- [候補43 18回継続試験](../../../evaluations/results/candidate43-outcome-authority-boundary-v10-standard14-continuous-n5-b18_2026-07-20.md)
- [候補41・候補43 標準14項目各5回](../../../evaluations/results/candidate41-candidate43-outcome-boundary-v10-standard14-n5_2026-07-20.md)
- [候補43 標準14項目各5回](../../../evaluations/results/candidate43-outcome-authority-boundary-v10-standard14-n5_2026-07-20.md)
- [候補41・候補43 A01 / A02各5回](../../../evaluations/results/candidate41-candidate43-outcome-boundary-v10-targeted2-n5_2026-07-20.md)
- [候補43使用量分析](../../../evaluations/results/candidate41-candidate43-v10-standard14-n5-token-increase-analysis_2026-07-20.md)
- [候補43 manifest](../../candidates/the-caption-3ce91a4-outcome-authority-boundary-r1/manifest.json)
