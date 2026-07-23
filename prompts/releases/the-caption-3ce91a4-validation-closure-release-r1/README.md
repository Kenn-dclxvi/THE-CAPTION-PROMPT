# 候補71 リリース

## 結論

候補71の19対象完全一式を、内容変更なしでTHE-CAPTIONへ投影するリリースとして承認した。

リリース状態は`approved_for_projection`、承認状態は`approved`である。

候補71は事前の品質gateを通過していない。今回の承認は、2026-07-23の明示依頼に基づく別の採用判断であり、保存済み評価結果または停止判定を変更しない。

## 識別情報

- リリース識別子: `the-caption-3ce91a4-validation-closure-release-r1`
- 元候補: `the-caption-3ce91a4-validation-closure-r1`
- 元候補の固定commit: `bcfce844bbed28269429322a24545032cc64bf14`
- 内容SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- 内容関係: 候補71と同一内容のリリーススナップショット
- 候補71から変更した対象: なし
- 現在投影済みの候補43との差: root `AGENTS.md`だけ

## 評価範囲

- 採点条件: `outcome-semantic-evidence-normalized-owner-diagnostic-v12`
- 評価集合: `the-caption-standard14-r1`第1版
- 18回継続試験: 14項目掛ける5回掛ける18結果、合計1,260件
- valid / rateable: `1,260 / 1,260`
- 公式点数分布: `4 / 3 / 0 = 1,255 / 4 / 1`
- Candidate69比token合計: `-27.93%`
- Candidate69比elapsed合計: `-11.71%`
- 18 / 18 Batchでtoken中央値とelapsed中央値がCandidate69より小さい

## 未解決risk

- A02で`git diff --check`欠落を3 / 90件観測した。
- A01で未固定modeを確認せず実装と試験へ進んだ誤実行を1 / 90件観測した。
- Candidate69比では実質的な低得点が3件増え、事前の「実質的な品質後退なし」gateを通過しなかった。
- tokenとelapsedの削減は保存するが、品質gate不通過を取り消す根拠にはしない。
- B18の観測を評価範囲外へ一般化できない。

## 承認状態

- リリース準備: `complete`
- リリース状態: `approved_for_projection`
- 採用承認: `approved`
- 本体反映: `not_projected`
- 承認根拠: 2026-07-23の明示的な本体適用依頼

## 根拠

- [候補71 第12版B18](../../../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)
- [候補71設計記録](../../../docs/candidate71-validation-closure-design.md)
- [候補71 manifest](../../candidates/the-caption-3ce91a4-validation-closure-r1/manifest.json)
