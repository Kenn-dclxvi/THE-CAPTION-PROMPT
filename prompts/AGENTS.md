# prompts instructions

`prompts/`の指示は、baseline、candidate、route、releaseのartifact lifecycleを扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。prompt制御の設計原則は`docs/prompt-control-design-principles.md`を正本とする。

## 共通

- baseline、candidate、route、releaseを別pathで管理する。
- prompt identity、source identity、bundle hash、変更targetを固定する。
- 既存bundleをin-placeで改訂しない。
- 変更時は新しいrevisionまたはidentityを作る。
- prompt変更と評価条件変更を同じ比較単位へ混ぜない。
- artifactの存在を評価済みまたは採用済みの根拠にしない。

## Baseline

- baselineは取得元repository、commitまたはtree、source path、content SHA-256へbindする。
- 取得後のbaseline本文とmanifestを変更しない。
- baselineの評価状態はbaseline artifactではなく、独立したevaluation resultで表す。

## Candidate

新しいcandidateの作成前に、次を固定する。

1. 基準prompt set
2. 基準状態での最短正常経路
3. 保存済みtraceで確認した一つの誤経路
4. 既存TaskSpec、repository authority、repository stateだけでは防げない理由
5. 追加、置換、削除する一つのpredicate
6. そのpredicateが消す具体的な判断点またはcontext伝播
7. 新たに増える判断点、参照、例外
8. 品質維持を確認するcaseとscore分布
9. 期待と逆の結果になった場合の停止条件

加えて、次を守る。

- 一つのcandidateでは一つのpredicateまたは一つの変更軸だけを扱う。
- 解く問題、baseline identity、変更理由、非目標、評価状態を記録する。
- prompt短縮、label削減、構造変更だけを効率改善と判断しない。
- targeted評価で成果品質と狙った経路変化を確認する前に、expandedまたはcontinuous評価へ進めない。
- 保存済みtraceにない将来不安だけを理由として制御を追加しない。
- 新しいpredicateの追加より、既存predicateの置換、統合、削除を優先する。

## Route

- routeは共通全文sourceへ実行前に合成する最小差分として扱う。
- route固有の差分を共通promptの新しい正本へ読み替えない。
- 適用条件、source identity、差分identity、合成後identityを固定する。
- routeでのみ成立する結果を、共通prompt全体の一般的効果として扱わない。

## Release

- release作成だけでは採用承認またはTHE-CAPTION本体への反映を意味しない。
- source candidate、評価範囲、未解決risk、release status、approval、projection、rollback identityを分離して記録する。
- 評価上の`stopped`と、別判断による`approved`または`projected`を混ぜない。
- THE-CAPTIONへの反映はrelease作成とは別operationとする。
- projection後も、元の評価状態と未解決riskを削除しない。
