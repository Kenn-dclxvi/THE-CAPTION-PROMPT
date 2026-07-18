# TC-F04-WEB-AUDIT-COLUMN-VISIBILITY r2

## 目的

Audit Keyを持つfundが存在するときだけ列を表示するReact/TypeScriptの条件を復元する。

## Revision delta

`r2`はtarget、seed、fixture、F04-C1、F04-C2、Node validationを変更しない。`node_modules/`と`dist/`は指定validationが作る試験基盤所有の一時出力とし、candidateの成果条件からcleanupを除外する。試験基盤はmodel実行終了後に宣言済みpathだけを削除する。削除に失敗したrunはquality低下ではなくexternal failureとして除外する。

過去の`r1`結果は変更しない。

## Identity

- revision: `r2`
- base revision: `r1`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `36f594ae5d16f6ac930b0c5afe12335c7624c020`
- trial input SHA-256: `42c0b5a40256bca9c73240026339b8b4cec6822667308d383bb7d8b206323e35`
- seed / source oracle: `r1`と同一
- cleanup owner: `evaluation_adapter`

workerへ渡すのは`trial-prompt-input.json`だけであり、seed、oracle、grader、reference identityはmodel-invisibleである。
