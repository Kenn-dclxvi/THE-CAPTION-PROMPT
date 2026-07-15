# TC-F01-DOMAIN-DUPLICATE-ASSET-KEY r3

## 目的

CSV境界で重複した`asset_key`を拒否するsingle-source Python implementation caseである。

## Revision delta

`r3`は`r2`のtarget identity、seed patch、fixture commit、oracle、F01-C1からF01-C3を変更しない。N=3比較で、成果とrequired gateを満たしたrunが許可path外の既存caller riskを理由に未完了停止したため、scope外の既存riskは報告してよいがcriterion達成後の停止理由にしないと明記した。

これは観測後の要件変更なので、新しいcase revisionとして扱う。過去の`r2`結果は変更しない。

## Identity

- revision: `r3`
- base revision: `r2`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `4e6910d08f49b0825beff08837178f5106cbd0f2`
- trial input SHA-256: `a349a3d9415c4ab163352b654d8dd6ddf1fb74307dd9347d10ed49ff1ad35ae6`
- seed / oracle: `r2`と同一

workerへ渡すのは`trial-prompt-input.json`だけである。private data、seed、oracle、graderはmodel-invisibleとする。

作成時qualification receiptは`fixture_qualified_prompt_not_evaluated`である。その後、[`core9 r2 global M=4 staged N=3`](../../../results/revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)でprompt比較を実施した。比較済みであることは採用、release、本体反映を意味しない。
