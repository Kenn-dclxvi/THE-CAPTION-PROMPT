# Candidate61 atomic SPEC operation gate設計記録

## 結論

Candidate61はCandidate55を直接sourceとし、C55で分割した`READINESS`と`OPERATION`を、Candidate43の`SPEC`一文へ完全一致で戻す。

新しいmethod、batch、case分類、TaskSpec fieldは追加しない。検証するのは、Candidate43が一つのgateで行っていた「全TaskSpec値の確定、operation binding、実行開始」の原子性だけである。

## Candidate作成前gate

1. 基準prompt setはCandidate55である。最短正常経路は、TaskSpecへ固定する全値を一つの`spec_ready` gateで確定し、required outcomeをoperation identityへ分け、predicate実行前にowner、permission、constraintまでbindしてから開始する経路である。
2. 保存済み誤経路はCandidate55 route gate r2のF10である。固定済みの同じ11 shell commandを4 / 5 runで11 top-level tool callへ分け、Candidate43比でF10が`48 -> 52 model step`、`43 -> 47 tool call`、`848,388 -> 909,468 tokens`となった。
3. F10 TaskSpec、repository authority、repository stateは成果、対象read、permissionを固定するが、C55の`READINESS`完了と`OPERATION` bindingを一つの開始判定として扱うことまでは固定しない。C55はoutcome値の確定後にpredicate、permission、constraintを別labelでbindし、Candidate43が同じ`SPEC`内へ含めたcriterion ownerも外している。
4. 置換する一つのpredicateはCandidate43の`SPEC`一文そのものである。Candidate55の`READINESS`と`OPERATION`を削除し、同じ位置へ完全一致で置く。
5. この置換が消す判断点は、outcome readiness成立後にoperationのpredicate、owner、permission、constraint、result scopeを別々に再評価してよいかという中間判断である。
6. 新しい判断点、label、例外は増えない。labelは2個から1個へ減り、Candidate43で既に評価済みの関係だけを復元する。Candidate55のproducer、terminal、method、delegation、context、delegated resultは変更しない。
7. 成果品質はcatalog固定済みF05 / F10各`N=5`で確認する。10 / 10 score `4`、root-only、zero drift、scope維持を必須とする。
8. F10のmodel step、tool call、shell command、all-agent token、elapsedをCandidate43およびCandidate55 route gate r2と比較する。少なくともCandidate43の`48 step / 43 tool call / 55 command / 848,388 tokens`以下を通過条件とする。
9. F10のmodel step、tool call、token合計のいずれかがCandidate43を超える、品質を失う、探索範囲が広がる、または短経路がC55 r2より増えない場合は停止する。通過した場合だけ同じcatalog固定A01 / A02各`N=5`へ進む。

九項目を定義済みであるため、Candidate61 bundleとF05 / F10 profileを作成できる。

## A系境界の追加診断

F10の既知のレビュー位置ずれは、現行TaskSpecだけでは防げず、atomic `SPEC`の復元効果を判定する事象ではない。この事象はF系品質記録へ残すが、A系境界の診断を止める理由には用いない。

Candidate61がC43から保持したA01の未固定値停止とA02のrepository解決を確認しなければ、C55で分割したgateの復元効果を判定できない。このため、F系gateを通過したとは読み替えず、別のcatalog固定A01 / A02 profileで各`N=5`を追加実行する。

## 変更する関係

```text
Candidate55
  READINESS -> OPERATION -> PRODUCER -> TERMINAL

Candidate61
  SPEC(all values ready + operation binding) -> PRODUCER -> TERMINAL
```

Candidate61の作成、対象試験、採用、release、本体反映は別状態である。

## 実行結果

catalog固定F05 / F10各`N=5`とA01 / A02各`N=5`を完了した。A01 / A02は10 / 10 score `4`だったが、F10は5 / 5が11 tool call経路となり、Candidate43比で`43 -> 55 tool call`、`848,388 -> 1,048,829 tokens`となった。

atomic `SPEC`の復元だけではC43のF10短経路を復元しなかった。結果は[`Candidate43 / Candidate55 / Candidate61 catalog固定対象試験`](../evaluations/results/candidate43-candidate55-candidate61-atomic-spec-operation-gate-catalog-fixed-targeted-n5_2026-07-21.md)へ記録し、Candidate61を停止する。
