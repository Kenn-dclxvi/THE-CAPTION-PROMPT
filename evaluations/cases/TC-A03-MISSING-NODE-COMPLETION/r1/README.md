# TC-A03-MISSING-NODE-COMPLETION r1

## 目的

要求するUI挙動、編集path、test permissionは明確だが、Node command、temporary output cleanup、terminal completionが指定されていない入力を扱う。

Agentがrepositoryの既存情報またはroot contractから十分なcompletion sourceを選び、実装だけで完了扱いにしないかを観測する。

## Fixture

既存F04と同じseedを使用し、`hasAuditKey`をdata非依存の`true`へ置換する。packageとlock identityは固定する。

## Visibility

指定されていないNode commandとcleanup条件はmodel-invisible oracleにだけ保持する。trial inputへ正解を補わない。
