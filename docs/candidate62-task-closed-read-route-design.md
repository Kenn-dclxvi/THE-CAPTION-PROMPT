# Candidate62 task-closed read route設計記録

## 結論

Candidate62はCandidate43を直接sourceとし、C56でF10を5 / 5の3 tool callへ収束させた固定read方法を、task全体がread-onlyで対象集合が探索前に閉じている場合だけへ限定する。

C59のようにoperation単位で適用可否を判定しない。変更・testを最終成果に含むA02の開始確認だけをread-only operationとして切り出し、固定read方法を適用する抜け道を閉じる。

## Candidate作成前gate

1. 基準prompt setはCandidate43である。A02の最短正常経路は、repository authorityからcanonical targetを解決し、`run.sh`だけを修正して構文、全test、diff checkを完了する経路である。F10の最短正常経路は、固定済みidentity、authority、diff、sourceを取得し、zero driftのreview resultを返す経路である。
2. 保存済み誤経路はCandidate56のA02である。task全体は変更とtestを要求していたが、開始identity後のrepository探索readへC56の同一model step取得が流入した。shell commandはCandidate43の`47`から`70`へ増え、1 runで必須`git diff --check`を欠いた。
3. A02のTaskSpec、repository authority、repository stateは最終成果が変更とtestを含むことを固定している。それでもC56とC59は、task内の開始確認またはauthority探索を別のread-only operationとして扱った。operation単位の非適用条件ではこの再分割を防げない。
4. 追加する一つのpredicateは`TASK_CLOSED_READ`である。required outcome全体がread-onlyで、実行前に明示user inputまたはrequested target identityを直接定める一意なrepository authorityから有限の相互非依存read target集合が閉じているtaskだけ、C56の同一model step取得を許可する。
5. このpredicateが消す判断点は、変更・test・dependency操作を含むtaskの一部を別のread-only operationへ切り出し、C56方法を適用してよいかという判断である。答えを常にfalseへ固定する。
6. 新しい判断点はtask開始時の`TASK_CLOSED_READ`一つである。case label、command列挙、TaskSpec field、A系の実行方法は追加しない。read結果によるtarget追加、taskの一部operationへの適用、read集合の補完・拡張を認めない。
7. 最初にcatalog固定A02 `N=1`を実行する。canonical `run.sh`、必要な三検証、score `4`を必須とする。開始確認またはauthority探索へC56型のmulti-read methodが流入した場合は、成果が正しくても停止する。
8. A02を通過した場合だけcatalog固定F10 `N=5`を実行する。semanticなreview成果、root-only、zero drift、55 shell commandを維持し、5 runすべてを3 top-level tool callへ収束させる。既知のfinding locationずれはroute predicateで防げないため、記録するがroute停止条件にしない。token合計はCandidate43 `848,388`とCandidate55 r2 `909,468`を下回ることを必須とする。
9. A02へmethodが流入する、F10が1 runでも3 tool callを超える、read集合が広がる、必要な成果または検証を失う場合は停止する。別predicateを継ぎ足さず、standard14、A06、採用、release、本体反映へ進めない。

九項目を定義済みであるため、Candidate62 bundleとA02 / F10 profileを作成できる。

## 変更する関係

```text
Candidate43 common control
  ├─ task outcomeまたはtarget集合が未解決
  │    └─ Candidate43通常経路
  └─ task全体がread-only AND target集合が探索前にclosed
       └─ C56 fixed-read method
```

Candidate62の作成、対象試験、採用、release、本体反映は別状態である。

## 対象gate通過後のA系反復確認

A02 `N=1`はcanonical成果、三つの検証、C43型の通常経路を満たした。続くF05 / F10各`N=5`も10 / 10 score `4`で、F10は全runが3 top-level tool call以下となった。

単発A02だけでは非適用境界を一般化できないため、既存gateを通過した後の別profileとして、C43 catalog固定A01 / A02条件からprompt identityだけをCandidate62へ変更した各`N=5`を実行する。これはA02 `N=1`の判定基準を変更せず、反復範囲を追加する診断である。

## 実行結果

F05 / F10は10 / 10 score `4`で、F10 routeは`2 / 3 / 3 / 1 / 1 tool call`、F系token合計はCandidate43比`-61.32%`だった。

一方、A02 `N=5`では4 / 5 runにC56型の並行取得が流入した。F05でも2 / 5 runがsource readを追加した。成果品質はA01 / A02の10 / 10でscore `4`だったが、事前gateのmethod非流入とread集合非拡張を満たさない。

結果は[`Candidate43 / Candidate56 / Candidate62 catalog固定試験`](../evaluations/results/candidate43-candidate56-candidate62-task-closed-read-route-catalog-fixed_2026-07-22.md)へ記録し、Candidate62を停止する。
