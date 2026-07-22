# Candidate55 prebound operation graph設計記録

## 結論

Candidate55はCandidate43を直接sourceとし、root `AGENTS.md`一枚だけを変更する。

A系readiness、F系fixed operation、D系explicit delegationの目的分別は分析上維持する。runtime promptでは三つを実行phaseとして並べず、一つの条件付きoperation graphへ戻す。

変更predicateは一つである。TaskSpecで確定済みの`predicate / permission / constraint`を、初回predicate前にrequired outcomeと同じoperationへbindする。tool API、read順序、command結合は指定しない。

## Candidate作成前gate

1. 基準はCandidate43である。control-freeな最短正常経路は、TaskSpecがrequired outcomeと必要なreadを確定している場合、rootが一つのproducerとして固定済み入力を取得し、required predicateを判定し、全terminal resultが揃った時点で完了する経路である。
2. 保存済みの誤経路はCandidate54のF10 iteration 2である。開始確認後、authority 2 read、固定diff、2 source、追加`git grep`を別tool callへ分け、各read後に残りのread要否を再判断した。Candidate43の同iterationはauthority、固定diff、2 sourceを一つのtool callで取得した。
3. F10 TaskSpecはread対象を`AGENTS.md`、`src/AGENTS.md`、固定diff、changed file、`monthly_engine.py`へ最初から限定している。しかしCandidate54はrequired outcomeだけをoperationへ閉じ、固定済みpredicate、permission、constraintを初回predicate前に同じoperationへbindする関係を省いた。TaskSpecに入力が列挙されていることだけでは、保存trace上の段階的な再判断を防げなかった。
4. 置換するpredicateは、`初回predicate前にTaskSpecで確定済みのrequired outcome / predicate / permission / constraintを同一operationへbindする`である。これはCandidate43の`SPEC`先頭で成立していた関係の復元であり、新しい方法規則ではない。
5. このpredicateが消す判断点は、固定済みauthority、diff、sourceを一つ取得するたびに、残りを同じoperationで読む必要があるか再判定することである。
6. 新たに増える判断は実行前の一回のoperation bindingだけである。新label、例外条件、owner探索、evidence再取得、tool batch指定は増やさない。A / F / Dは別sectionにしない。
7. 成果品質はcatalog固定済みF05 / F10各`N=5`で判定する。10 / 10 score `4`、root-only、zero driftを必須とする。
8. 経路効果はF10のmodel step、tool call、shell command、token合計で確認する。Candidate43の`48 step / 43 tool call / 55 shell command / 848,388 tokens`以下を通過条件とする。F05もCandidate43の品質を維持する。
9. F10のmodel step、tool call、token合計のいずれかがCandidate43を超えた場合は停止する。Candidate55へ説明文を足さず、同じ候補でA01 / A02、standard14、A06へ進めない。

このgateは九項目すべて定義済みであるため、Candidate55のbundleとcatalog固定対象profileの作成を許可する。

## 変更するgraph

```text
TaskSpec
  |
  +-- unresolved outcome value -> clarification result -> stop
  |
  +-- resolved outcome
        |
        +-- before first predicate:
        |     bind predicate / permission / constraint to one operation
        |
        +-- one producer -> all required terminal results -> terminal
        |                      |
        |                      +-- missing result -> nonterminal
        |
        +-- explicit producer only -> delegation packet -> runtime provenance
```

readinessは開始可否を決める。fixed operationは、開始後に何を同じoperationとして完了させるかを決める。explicit delegationはTaskSpecが独立producerを要求した場合だけfixed operationへ接続する。三領域を順番に再評価するphaseにはしない。

## Candidate54からの修正点

| 対象 | Candidate54 | Candidate55 |
| --- | --- | --- |
| operation input | required outcomeだけを明示 | outcomeと固定済みpredicate / permission / constraintを初回predicate前にbind |
| runtime構造 | `Readiness`、`Fixed operation`、`Explicit delegation`の三section | 一つの条件付きgraphを短い不変条件で表現 |
| tool方法 | 指定なし | 指定なし |
| D系 | 明示委譲時だけ | 同じ |
| R系 | 常時coreから除外 | 同じ |

Candidate54の全体を親として継ぎ足さない。Candidate43を直接sourceとし、必要性を確認できたA / F / Dの関係と、今回特定した事前bindingだけでroot promptを再構成する。

## 評価順序

1. bundle identity、root一枚だけの差分、事前binding、条件付きdelegation、R系除外を構造testで確認する。
2. Candidate43と同じcatalog固定F05 / F10 profileからprompt identityだけを替える。
3. 各`N=5`を実行し、事前gateの品質とF10経路条件を判定する。
4. 通過した場合だけA01 / A02用profileの作成を別変更として検討する。

candidate作成、対象試験、採用、release、本体反映は別状態である。

## 対象試験結果

2026-07-21にcatalog固定済みF05 / F10を各`N=5`で実行した。Candidate55は10 / 10でscore `4`、root-only、zero driftだった。

Candidate43比でF10はmodel step `48 -> 38`、tool call `43 -> 33`、token合計`-19.31%`だった。一方、shell commandは`55 -> 61`となり、事前gateのCandidate43以下を満たさなかった。

結果後にgateを変更せず、Candidate55は`catalog_fixed_targeted_n5 / stopped`とする。A01 / A02、standard14、A06、採用、release、本体反映へ進めない。詳細は[`Candidate43 / Candidate55対象試験`](../evaluations/results/candidate43-candidate55-prebound-operation-graph-catalog-fixed-targeted-n5_2026-07-21.md)に記録する。

停止基準を変更した[`route gate r2`](candidate55-route-efficiency-gate-r2.md)では、同じpromptと互換条件で新しい`N=5`を実行した。F10はmodel step `52`、tool call `47`、token合計`909,468`となり、Candidate43上限を超えた。初回resultの短経路は反復間で安定しなかったため、Candidate55は停止を継続する。
