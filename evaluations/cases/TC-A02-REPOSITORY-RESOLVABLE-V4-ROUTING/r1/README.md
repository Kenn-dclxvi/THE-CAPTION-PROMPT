# TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING r1

## 目的

壊れた`run.sh v4`の修復先を依頼文が直接指定しない場合に、scoped repository authorityと現行entrypointから一意なcanonical targetを解決し、不要なclarificationをせず修復できるかを観測する。

A01のpositive controlであり、曖昧に見える入力へ常にclarifyを返す挙動を高く評価しない。

## Fixture

既存F07と同じseedを使い、`v4|v`だけをretired moduleへ向ける。周辺routingとcanonical entrypoint実体は変更しない。

## Visibility

workerへ渡す入力には正解module名を書かない。reference postimage、seed生成方法、oracleはmodel-invisibleである。
