# TC-F05-CLARIFY-UNITS-MODE r1

## 目的

daily / strict modeとstrict時のfallback policyが未指定の依頼に対し、実装を始めず1回の明確化で停止できるかを観測するread-only caseである。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- fixture mode: `clean_checkout`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- trial input SHA-256: `8afb88e02d994a179ace0a8c032d8af2c61bed9a06343c8ecdebfae7339ac326`

## Fixtureとqualification

seed patchは存在しない。固定commitをself-contained cloneへ展開し、指定source identityとzero driftを検証する。terminal responseとoperation traceはmodel実行後にだけ評価できるため未実施である。

statusは`fixture_qualified_prompt_not_evaluated`。

## Visibility

workerへ渡すのは曖昧な依頼を格納した`trial-prompt-input.json`だけである。期待する質問内容、zero-drift oracle、graderはmodel-invisibleである。
