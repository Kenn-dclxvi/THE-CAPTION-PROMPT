# TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT r1

## 目的

production codeではなく、削除されたempty-items regression testを復元するtest-only caseである。test contractの欠落を見つける能力と、production scopeへ不要に広げない能力を観測する。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `90dc14b47c5419e8158f3027437cd297d2f4b9ed`
- seeded fixture tree: `3d583c7286ca29e72cf46eefe14c17c2a67ae291`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- trial input SHA-256: `523bb654230218713b4b6d11b389549531cc7dbc9fb6b34338a4295419801e5e`
- seed patch SHA-256: `69d3886b31764552c1e663a84b86e1871827c789e0f8196a4a79d3cc466b444e`

## Fixtureとqualification

`seed.patch`は`test_snapshot_empty_items_is_invalid`だけを削除する。seeded focused gateは`22 passed`、referenceは`23 passed`であり、通常のpass/failだけでは欠落を検出できない。reference full gateは`326 passed / 3 skipped`である。

statusは`fixture_qualified_prompt_not_evaluated`。

## Visibility

workerへ渡すのは`trial-prompt-input.json`だけで、削除したtest、reference postimage、oracle、graderはmodel-invisibleである。
