# TC-F07-CANONICAL-V4-RUNNER r1

## 目的

root launcherの`v4|v` aliasをcanonical moduleへ戻すshell-script caseである。syntax gateが通るが実行先だけが壊れている条件を観測する。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `5b17df6fc5c86be5614c37e0883277d52045c0cd`
- seeded fixture tree: `c5a5adb90e0667bab3caed99623bf64359d51ccd`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- trial input SHA-256: `cc75e8fe5735186bfb83cf2db7deff55cfd65cb4019532d2dcaca3cd884156bd`
- seed patch SHA-256: `4fc234a69e0592337c2e4e59b7929feff306c9660312f310a3b028c87e129ee9`

## Fixtureとqualification

`seed.patch`はV4 aliasを存在しないretired module `src.app.entrypoints.daily_main`へ向ける。seeded状態でも`bash -n`とfull gateは成功し、`326 passed / 3 skipped`だった。したがってmodule inventoryを読んだ意味的修正が必要なcaseである。

statusは`fixture_qualified_prompt_not_evaluated`。

## Visibility

workerへ渡すのは`trial-prompt-input.json`だけで、canonical postimageとgrader contractはmodel-invisibleである。
