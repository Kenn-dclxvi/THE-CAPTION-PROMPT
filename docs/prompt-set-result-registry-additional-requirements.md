# Prompt set別試験結果台帳の追加要件

## Status

- artifact: `additional_requirement`
- scope: 評価基盤v3へ反映済みの要件記録
- implementation: `implemented_as_evaluation_foundation_v3`
- schema / workflow変更: 新revisionとして実施
- existing result migration: 対象外、未実施
- current work boundary: `candidate2`構築とは分離

## 背景

prompt setが`baseline`、`candidate1`、`candidate2`と増える場合、固定したA / Bの組を一次的な試験結果として保存すると、別の組合せや3つ以上のprompt setを確認するたびに比較単位を作り直す必要がある。

必要なのはA / B比較そのものの保存ではなく、どのprompt setを固定条件で試験した結果かを独立して保持し、後から互換条件を満たす結果を任意個取得できることである。

## 追加要件

1. 試験結果の一次単位を、1つのprompt setを固定条件で実行した結果とする。
2. 各結果はprompt set名だけでなく、revisionまたはbundle hashを含むimmutableな`prompt_set_identity`へ結び付ける。
3. 各結果から、少なくともevaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件を特定できるようにする。
4. 各prompt setの結果は他のprompt setとの比較から独立して保存し、既存結果を別の比較のために書き換えない。
5. 固定的なA / B condition labelを、保存結果のidentityまたは評価対象の概念として要求しない。
6. `baseline`、`candidate1`、`candidate2`を含む任意個のprompt setについて、互換条件を満たす結果を後から取得できるようにする。取得数を2つに限定しない。
7. 比較可能な集合には、prompt identity以外の固定条件が一致する結果だけを含める。条件が一致しない結果を同一比較へ暗黙に混ぜない。
8. `quality_score`、`total_tokens`、`elapsed_seconds`はprompt setごとの結果として保持する。
9. 複数prompt setの一覧、中央値、数値差などは保存済み結果から生成するviewとし、一次結果を変更しない。
10. 数値差を表示する場合は、どのprompt setからどのprompt setを引いた値かをview側で明示する。固定的な`B - A`を前提にしない。
11. 過去のprompt revisionとその結果を引き続き取得できるよう、結果はappend-onlyで保持し、現行revisionへ読み替えない。

## 境界

このartifactは追加要件と実装statusだけを記録する。v3実装でも次は対象外とする。

- 既存A / B resultのmigrationまたは再解釈
- KPI、Layer、quality rating責務の追加
- prompt setの優劣、採用、release判断
- `candidate2`のprompt設計または評価条件との混在

具体設計とinterfaceは`docs/prompt-comparison-workflow.md`と`docs/evaluation-loop-manual.md`を正本とする。v1 / v2 artifactは履歴として保持し、v3へ読み替えない。
