# Candidate65 shared operation core設計記録

## 結論

Candidate65はCandidate43を直接sourceとし、32 atomic clauseの意味を、重複なしの`Common operation`、`Explicit delegation extension`、`Failure and recovery`へ短文化する。

Candidate64のようにroot / delegatedへF coreを複製しない。新しいpath選択、適用条件、tool methodも追加しない。Candidate43内で重複する明示委譲gateとproducer再割当て禁止だけを一つの表現へ統合する。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。最短正常経路は、requested outcome valueが未固定なら変更・test前にその値だけを質問して終了し、固定済みならoperationごとに一つのproducerが全predicateのterminal resultを作る経路である。独立producer executionが明示されないoperationはrootが実行し、明示されたoperationだけを指定workerが実行する。
2. 保存済みCandidate64 `N=5`では32 / 32 clauseと25 / 25 score `4`を保持した一方、root / delegatedへF coreを複製すると、F10はCandidate43比でtool call `43 -> 54`、model step `48 -> 59`、token合計`+28.90%`だった。A / F / D各scopeのtoken合計も12〜14%増えた。
3. TaskSpec、repository authority、repository stateは実行成果を固定するが、常時可視root promptの重複表現と、その反復input costは除去しない。したがって、重複削除はroot prompt側の変更として扱う。
4. 置換する一つのpresentation relationは、`compact clause := 一つ以上のCandidate43 atomic clauseと同じpredicateを一度だけ表す`である。重複するsource clauseは一つのcompact clauseへ統合できるが、source predicateを削除または別条件へ変更しない。
5. 消す判断点は二つである。第一に、TaskSpecが独立producer executionを明示したかを`PRODUCER`と`OWNER_ROLE`で二度読む経路を一つの`ENTRY`へ統合する。第二に、同一predicateの別producer再割当て禁止を`PRODUCER`と`INDEPENDENCE`で二度読む経路を一つの`PRODUCER`へ統合する。
6. 新たに増えるのは三つの目的見出しだけである。新しいpredicate、例外、path selector、permission、tool、read順序、SA起動条件は増やさない。
7. 静的保持は32 source clauseすべてが対応表へ一度以上現れ、compact側の各predicateへ説明可能に対応することで判定する。behavioral確認はA01 / A02、F05 / F10、D01をCandidate43と同じ互換条件で各`N=5`実行し、Candidate65の25 / 25 score `4`を必須とする。
8. root `AGENTS.md`はCandidate43の`3,980 bytes`未満を必須とする。root-only F10はCandidate43のtool call `43`、model step `48`、token合計`848,388`を超えないことを次段へ進む条件とする。A / Fはworkerを起動せず、D01は指定workerを一つ起動し、result provenanceを受信してrootがreviewを再実行しないことを確認する。
9. source predicate欠落、静的bytes非減少、A / Fでのworker起動、D01の指定worker欠落またはroot再実行、score `4`喪失、F10のtool call・model step・token増加があれば停止する。Candidate65へ補助predicateを追加しない。

九項目を定義済みであるため、Candidate65の構造bundleを作成できる。構造testに合格した場合だけ評価profileを作る。

## Source predicate対応

| Candidate43 source clause | Candidate65 compact label | 処置 |
| --- | --- | --- |
| `SPEC1..5` | `READINESS` | negative binding例と開始禁止を保持して短文化 |
| `SPEC6` | `SCOPE` | 単独保持 |
| `PRODUCER1 / 2 / 5`、`INDEPENDENCE2` | `PRODUCER` | producer exclusivityと再割当て禁止を統合 |
| `TERMINAL1 / 2`、`OWNER_ROLE6` | `TERMINAL` | terminal成立、欠落、`false / failed`を一か所へ配置 |
| `INDEPENDENCE1` | `INDEPENDENCE` | 単独保持 |
| `PRODUCER3 / 4`、`OWNER_ROLE1 / 2` | `ENTRY` | 明示委譲gateとowner metadata境界を統合 |
| `CONTEXT1..3` | `CONTEXT` | packet、context sufficiency、全履歴禁止を保持 |
| `OWNER_ROLE3..5 / 7` | `RESULT` | runtime provenance、wait、未取得state、補完禁止を保持 |
| `ROOT1` | `ROOT` | 単独保持 |
| `METHOD1..4` | `METHOD` | 単独保持 |
| `RECOVERY1 / 2` | `RECOVERY` | 単独保持 |

同じsource clauseをroot / delegatedへ複製しない。対応表は意味保持の静的根拠であり、behavioral成立の代わりにはしない。

## 圧縮境界

削らない要素は次のとおりである。

- A01を止める`current value / option set / complement / test expectation / implementation convenience`
- `spec_ready=false`中のproducer、predicate、artifact変更、test開始禁止
- operation scope、single producer、terminal result、`false / failed`保持
- worker packet 9 field、`fork_turns=none`と必要最小turn継承
- `runtime_spawn_result.task_name`、`FINAL_ANSWER.Sender`、result bindingのAND predicate
- root非再実行、permission否定時の停止、recovery counter

短くするのは重複gate、重複した再割当て禁止、同じ主語の反復、説明上の接続語だけである。

Candidate31からCandidate34の同条件`N=5`では、predicateを保持した圧縮後も60 / 60 score `4`を維持し、all-agent token中央値が`-15.98%`だった。一方、Candidate32ではroot bytes `-32.6%`でもruntime tokenが`+6.45%`だった。したがって、Candidate65も静的bytesではなく同条件behavioral KPIで判定する。

Candidate65の構築、構造確認、behavioral評価、採用、release、本体反映は別状態とする。

## 構築結果

Candidate43を直接sourceとし、root `AGENTS.md`だけを変更したbundleを構築した。

- prompt identity: `the-caption-3ce91a4-shared-operation-core-r1`
- bundle SHA-256: `2f3da313b82f0e2085e23b6d040a64bee892870a221e3b4158a612dfb8ec4eff`
- root bytes: `3,980 -> 3,701`、`-279`、`-7.01%`
- compact label: `READINESS / SCOPE / PRODUCER / TERMINAL / INDEPENDENCE / ENTRY / CONTEXT / RESULT / ROOT / METHOD / RECOVERY`
- source clause mapping: 32 / 32
- 追加predicate、path selector、tool method: 0

構造testとbundle verificationは合格した。manifestの構築時`not_evaluated`状態はprovenanceとして変更せず、評価状態は独立resultへ記録する。

## F系評価結果

catalog固定F05 / F10各`N=5`は10 / 10 score `4`、root-only、excluded attempt 0だった。一方、停止対象F10はCandidate43比でtool call `43 -> 49`、model step `48 -> 54`、all-agent token合計`848,388 -> 969,284`となり、事前上限をすべて超えた。

Candidate65は`targeted_evaluated / stopped`とする。A01 / A02とD01のprofileは作成済みだが、gateに従い実行していない。Candidate65へ補助predicateを追加せず、standard14、採用、release、本体反映へ進めない。

詳細は[`Candidate43 / Candidate65 catalog固定F系N=5`](../evaluations/results/candidate43-candidate65-shared-operation-core-catalog-fixed-f-n5_2026-07-22.md)へ固定する。
