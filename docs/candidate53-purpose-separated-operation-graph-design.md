# Candidate53 目的分離operation graphの設計記録

## 位置付け

Candidate53はCandidate43を直接sourceとする。root `AGENTS.md`一枚の中で、仕様未確定時の開始境界、仕様確定後のoperation graph、明示委譲時だけのworker lifecycleを別領域へ分ける。

Candidate49からCandidate52までの停止済み候補へ文を追加しない。Candidate43のpredicateを一文ずつ復元するのではなく、意味上の接続を保ったまま配置と重複表現を置換する。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。最短正常経路は、requested outcome valueが確定していなければ未固定値だけを質問して停止し、確定済みならrootをproducerとする一つのoperationでrequired predicateを実行し、全resultが揃った時点で完了する経路である。TaskSpecが独立producer executionを明示した場合だけ、そのoperationを指定workerへ委譲する。
2. capability catalog固定済みF10 `N=5`では、Candidate43が`48 model step / 43 tool call`だったのに対し、Candidate51は`60 / 55`、Candidate52は`61 / 56`だった。Candidate52では4 tool callへ収束するrunと16 / 14 tool callへ追加探索するrunが混在した。短い文を足し戻してもCandidate43のroutingは安定して復元しなかった。
3. F10のTaskSpec、repository authority、固定diff、source、required commandは実行対象と成果を制約するが、`spec_ready`判定、root operationのproducer binding、全predicate completion、別operation成立、明示委譲の適用域というprompt内の関係は表現しない。Candidate49以降はこの関係を委譲制御へ畳み込み、root-only operationのgraphを失った。
4. 置換する一つのrouting predicateは、`spec_ready=false`ならclarificationだけを返し、`spec_ready=true`なら固定operation graphへ進むという目的境界である。A系の開始可否とF系の完了制御を同じlabelへ入れない。
5. この境界は、仕様未確定時にF系のproducer・terminal制御を展開する判断と、仕様確定後にA系のauthority候補を再評価する判断を消す。F系では`OPERATION -> PRODUCER -> COMPLETION`を常に同じ経路として読み、`INDEPENDENCE`は別operation、`DELEGATION`はproducerの明示置換としてだけ参照する。
6. 新しい成果条件、例外、tool方法は追加しない。増えるのは`spec_ready`による二分岐の見出しだけであり、この判定自体はCandidate43に既に存在する。C43の一つの`SPEC`に同居していたTaskSpec readinessとoperation identity bindingを二つのlabelへ分ける。
7. 成果品質は、F05 / F10で各`N=5`のscore `4`、root-only routing、required response、zero driftを先に確認する。Fで停止条件に該当しない場合だけ、A01 / A02で各`N=5`のscore `4`、A01の変更なしclarification、A02の不要なclarificationなしを確認する。
8. F10ではCandidate43と同程度以下のmodel step、tool call、input tokenへの収束を想定する。F05ではclarification以外の実行を増やさない。A01 / A02では開始可否の挙動をCandidate43から変えない。prompt byte数だけを成果にしない。
9. F05 / F10でscore `4`を失う、不要なworkerを起動する、required commandまたはevidenceを省略する、F10のmodel step・tool call・token合計がCandidate43から増える、またはrun間の追加探索がCandidate52と同様に残る場合は停止する。Fを通過してもA01で変更へ進む、A02で不要な質問をする場合は停止する。Candidate53へ補助文を継ぎ足さない。

## 保持するoperation graph

```text
Outcome readiness
  spec_ready=false -> clarification result -> stop
  spec_ready=true
        |
        v
Fixed operation
  OPERATION -> PRODUCER -> COMPLETION
                    |          ^
                    |          |
        explicit DELEGATION ---+

INDEPENDENCE -> distinct operation identity
METHOD / RECOVERY -> same predicate and permission boundary
```

- A系の目的は、requested outcome valueを推測せず、実行開始可能かを決めることである。
- F系の目的は、確定済みoperationのproducer、predicate result、terminalを同じidentityへ閉じることである。
- 明示委譲の目的は、TaskSpecが独立producer executionを要求した場合だけ、そのproducerへ入力とresultをbindすることである。criterion owner語列だけでは起動しない。

## 変更単位

Candidate43のroot `AGENTS.md`だけを変更する。残り18 targetはCandidate43とbit identityを保つ。

- `READINESS`はCandidate43 `SPEC`の開始可否だけを受け持つ。
- `OPERATION / PRODUCER / COMPLETION / INDEPENDENCE`は仕様確定後のF系operation graphを受け持つ。
- `DELEGATION / CONTEXT / RESULT / ROOT`は明示委譲時だけ適用する。
- `METHOD / RECOVERY`はC43の手段選択と回復上限を保持する。
- tool API、command結合、read順序、model step数を指定しない。

## 評価順序

1. bundle identity、C43との差分1 target、未変更18 targetのbit identity、A/F/delegation間の必須関係を構造testで確認する。
2. capability catalog固定済みのC43 F05 / F10 resultを比較元とし、Candidate53を同条件で各`N=5`実行する。
3. F系が停止条件に該当しない場合だけ、C43とCandidate53のA01 / A02を同じcapability catalog固定条件で各`N=5`実行する。
4. targeted試験を通過した場合に限り、標準14項目、A06、採用、release、本体反映を別判断にする。

Candidate53の作成、評価、採用、release、本体反映は別状態として扱う。

## 対象試験結果と停止

2026-07-21にcapability catalogを固定し、F05 / F10を各`N=5`で実行した。Candidate53は10 / 10件がscore `4`、root-only、zero driftだった。

一方、Candidate43比でF10はmodel step `48 -> 54`、tool call `43 -> 49`、token合計`+13.37%`だった。10 run全体のtoken合計も`+13.02%`だった。同じ11-call経路ではCandidate53の平均tokenが`-0.09%`だったが、短い経路の発生が減った。

作成前gateの停止条件に従い、Candidate53は`targeted_evaluated / stopped`とする。A01 / A02、標準14項目、A06、採用、release、本体反映へ進めない。Candidate53へ補助文を追加しない。詳細は[`Candidate43 / Candidate53対象試験`](../evaluations/results/candidate43-candidate53-purpose-separated-operation-graph-catalog-fixed-targeted-n5_2026-07-21.md)に記録する。
