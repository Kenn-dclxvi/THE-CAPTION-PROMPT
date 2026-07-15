# TC-F03-ATOMIC-CONTEXT-CLEANUP r1

## 目的

`os.replace`失敗時の一時JSON cleanupを復元する、infra層のmocked-I/O caseである。F01/F02とは異なり、戻り値だけでなく失敗後のfilesystem stateを観測する。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- seeded fixture commit: `895d60764990f02f25c6a6c81babbcb1e0ad5ffa`
- seeded fixture tree: `256d39b56d38ee02a90f37f074403ce948b22524`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- trial input SHA-256: `9d52b8efdf956128a426fce7576a62f9edaa46bbf943faf206ee260555ff0db4`
- seed patch SHA-256: `68c7b5b6ddd0674cfcd4e746d9589cecf55f6d61da30284474ce89e34e52812d`

## Fixtureとqualification

`seed.patch`は`src/infra/context_repository.py`からreplace失敗時の`os.unlink` cleanupだけを除去する。focused gateはseeded状態で`1 failed / 1 passed`、referenceで`2 passed`となり、意図した失敗を再現した。target referenceのfull gateは`326 passed / 3 skipped`である。

statusは`fixture_qualified_prompt_not_evaluated`。A / B実行、quality rating、KPI comparisonは未実施である。

## Visibility

workerへ渡すのは`trial-prompt-input.json`だけである。`private/case-data.json`、`private/seed.patch`、oracle、grader、qualification receiptはmodel-invisibleとする。
