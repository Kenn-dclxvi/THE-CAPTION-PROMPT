# Candidate57 task-enumerated read boundary設計記録

## 結論

Candidate57はCandidate56を直接sourceとし、root `AGENTS.md`一枚だけを変更する。

新しいpredicateは追加しない。Candidate56の`FIXED_READ`一文を、実行開始前のTaskSpecがread pathまたはcommandを有限列挙している場合だけへ狭める。repository authority / stateの取得結果からmodelがread集合を決めるoperationは、readiness解決後でも対象外とする。

## Candidate作成前gate

1. control-freeな最短正常経路は、F10 TaskSpecが開始identity、固定diff、authority、2 source、終了statusを列挙し、rootがread-only reviewを3 top-level tool callで完了する経路である。
2. 保存済みの誤経路はCandidate56 A02 iteration 4である。開始identity後の`rg --files`結果からmodelが6種類のreadを選び、authority探索中に同一model stepへまとめた。
3. Candidate56 A02はmodel step / tool callがCandidate43と同じ`51 / 46`のまま、shell commandが`47 -> 70`へ増えた。1 runは必須の`git diff --check`を欠きscore `3`となった。
4. Candidate56の「TaskSpecが入力を確定済み」は、TaskSpec自身の列挙と、modelがrepository stateから確定した集合を区別できなかった。既存のTaskSpec readiness、repository authority、repository stateだけではmethod適用を防げない。
5. 置換後の適用条件は、`実行前TaskSpecがread path / commandを有限列挙 ∧ root producer ∧ 相互非依存 ∧ read-only`である。取得結果による列挙の補完、authority / stateからの対象決定、先行result依存、write、test、dependencyには適用しない。
6. 消す判断点は、TaskSpec列挙済みreadを一つ受け取るたびの残りread再決定とcontext再送だけである。探索対象、validation、completion、evidenceは削らない。
7. 増える判断は、TaskSpec自身にpathまたはcommandの有限列挙が存在するかの一回判定だけである。modelが後から作ったlistを適用根拠にしない。
8. A01 / A02各`N=5`で10 / 10 score `4`、root-only、zero unexpected driftを必須とする。A02はshell command、model step、tool call、token合計、elapsed中央値をCandidate43以下とし、repository探索readを同一model stepへまとめたtraceが1件でもあれば停止する。
9. A系gateを通過した場合だけF05 / F10各`N=5`を実行する。F10は10 / 10ではなくcase内5 / 5 score `4`、各run5 tool call以下、合計25以下、token合計Candidate43以下を必須とする。

九項目を定義済みであるため、Candidate57 bundleとA / F profileの作成を許可する。

## 変更するgraph

```text
TaskSpec before execution
  explicit finite read paths / commands
    + root producer + independent + read-only
      -> same model step; preserve individual tool identity / exit

  repository authority / state decides read targets
      -> FIXED_READ not applicable
      -> ordinary A exploration and completion
```

## 評価順序

1. Candidate56から`FIXED_READ`一文だけを置換する。
2. catalog固定A01 / A02各`N=5`で非適用境界を先に確認する。
3. A系gate通過時だけcatalog固定F05 / F10各`N=5`でF系効果を確認する。
4. 両gate通過後にstandard14を別判断として検討する。

candidate作成、対象試験、採用、release、本体反映は別状態である。
