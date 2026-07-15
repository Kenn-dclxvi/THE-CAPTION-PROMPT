# TC-F04-WEB-AUDIT-COLUMN-VISIBILITY r1

## 目的

Audit Keyを持つfundが存在するときだけ列を表示するReact/TypeScriptの条件を復元する。Python以外のtoolchain、UI条件、生成物cleanupをcoverageへ追加する。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `36f594ae5d16f6ac930b0c5afe12335c7624c020`
- seeded fixture tree: `e578e8bbc6a8dc2fd0e2316e8279c7e87b21e3b9`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- trial input SHA-256: `f61f4a4baed8749e219543ed0f7ff73fc5d1dc23e8f9359b7370a8c71d8bff6e`
- seed patch SHA-256: `deb6d7633ac5bd4bafd6014d22513e6fabc9af42ac8f19f6088d57dae68846cd`

## Fixtureとqualification

`seed.patch`は`hasAuditKey`を常に`true`へ固定する。Node `v26.0.0`、npm `11.12.1`で`npm ci`、lint、buildが成功し、`node_modules`と`dist`を削除した後もtracked worktreeがcleanであることを確認した。通常gateがこの意味的なUI不具合を検出しないこともcase特性である。

statusは`fixture_qualified_prompt_not_evaluated`。画面操作による評価やA / B prompt実行はまだ行っていない。

## Visibility

workerへ渡すのは`trial-prompt-input.json`だけで、seed、oracle、grader、reference identityはmodel-invisibleである。
