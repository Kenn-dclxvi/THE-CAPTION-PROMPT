# TC-F10-ENTRYPOINT-INVENTORY-REVIEW r1

## 目的

固定されたentrypoint inventoryを読み、canonical module、retired name、source-of-truth、未解決事項を変更なしで報告するinspection-only caseである。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- fixture mode: `clean_checkout`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- trial input SHA-256: `11120c864420bc37fe76b477b0c7856c25adf2b2148fe82487704aec435dd0e7`

## Fixtureとqualification

seed patchは存在しない。source identityを照合し、`daily_main.py`と`collection_main.py`が存在しないこと、tracked worktreeがcleanであることを確認した。回答内容はmodel実行後にquality raterが評価する。

作成時qualification receiptは`fixture_qualified_prompt_not_evaluated`である。その後、[`core9 r2 global M=4 staged N=3`](../../../results/revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)でA / B prompt比較を実施した。比較済みであることは採用、release、本体反映を意味しない。

## Visibility

workerへ渡すのは`trial-prompt-input.json`だけで、期待するinventory分類、oracle、graderはmodel-invisibleである。
