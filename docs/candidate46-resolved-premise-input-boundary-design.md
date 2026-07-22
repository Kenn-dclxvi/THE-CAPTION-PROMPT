# Candidate46 解決済み前提入力境界の設計記録

## 位置付け

Candidate46はCandidate45を直接sourceとし、後続operationが確定済みのauthority、scope、resultを再び未解決predicateとして探索しないための入力境界へ置換する候補である。

変更対象は`CONTEXT`と`ROOT`だけとする。Candidate45で導入した`PRODUCER`の判断成立責任境界は維持する。worker数、担当file、tool、読取り順、探索深度は固定しない。

Candidate46の作成、A06診断、採用、release、本体反映は別状態として扱う。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-judgment-authority-boundary-r1`（Candidate45）とする。最短正常経路は、producerが担当判断をrequired evidence付きのterminal resultとして成立させ、後続operationがそのresultと解決済み前提を入力として用い、未解決部分だけを判断する経路である。
2. 保存済みA06のCandidate45 strict traceでは、31 workerのうち16 workerが別workerから起動され、11件の起動が`agent thread limit reached`で失敗した。32 session中、`AGENTS.md`は32 session、`docs/reference`は30 session、`docs/adr`は29 session、`git status`は24 session、`rg --files`は30 sessionから参照された。新規対象の探索に必要な参照と、既に解決された共通前提の再取得が同じ経路へ流入した。
3. TaskSpec、repository authority、repository stateは正しい判断内容を制約するが、あるoperationで確定したauthority、scope、terminal resultを後続operationへどの状態で渡すかを定めない。そのため、同じrepository情報が後続operationごとにopen predicateへ戻ることを防げない。
4. 置換するpredicateは、後続operationの判断範囲を確定する解決済み前提とterminal resultを入力としてbindし、そのoperationのopen predicateへ戻さない境界である。
5. このpredicateは、後続operationごとのauthority再探索、scope再確定、同じresult根拠の再取得、およびroot admission前の無条件なsource再取得を消す。新しい対象範囲、失効、矛盾、またはevidence不足の探索は消さない。
6. 新たに必要になる判断は、受け取った前提が有効で十分か、それとも不足、失効、矛盾、scope extensionのいずれかかという区別である。新しいlabelは追加しない。TaskSpecが要求する独立確認は別operationとして維持する。
7. 成果はA06の最終監査について、適用authority、到達可能な不適合、重大な見落とし、既知false positive、現物適合性と製造履歴の分離、no-driftで確認する。Candidate43とCandidate45で確認された主要findingを基準にし、score `4`を維持できるかを別のquality ratingで判定する。単一runはdiagnosticであり、範囲外へ一般化しない。
8. 想定する実行変化は、実在する独立判断や新規対象探索のworkerを維持しつつ、共通前提の再取得を目的とするnested worker、同じauthorityの反復read、thread-limit到達、child input token、tool call、model stepが減ることである。worker数やtokenの減少だけを成功としない。
9. Candidate43またはCandidate45の主要findingを失った場合、quality scoreが低下した場合、必要な新規対象探索を抑止した場合、rootへ探索を集中させただけでall-agent tokenが減らない場合、または前提状態の判定が新たな再確認経路を増やした場合は、追加candidateへ進まず境界を再検討する。

## 変更単位

Candidate45のroot `AGENTS.md`だけを変更する。

- `CONTEXT`をpacket項目の列挙から、解決済み前提とterminal resultを後続operationの入力として扱う境界へ置換する。
- `ROOT`を、関連sourceを一律に再確認してからadmitまたはrejectする責任から、bind済みresult、required evidence、解決済み前提でadmissionできる場合は追加探索を条件にしない責任へ置換する。

二つの文面変更は、解決済み前提を後続operationの入力境界で閉じる一つのpredicateを表す。`SPEC`、`TERMINAL`、`PRODUCER`、`OWNER_ROLE`、`METHOD`、`RECOVERY`は変更しない。
