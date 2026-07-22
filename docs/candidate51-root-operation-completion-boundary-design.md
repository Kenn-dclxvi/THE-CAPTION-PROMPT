# Candidate51 root operation completion境界の設計記録

## 位置付け

Candidate51はCandidate49を直接sourceとし、Candidate49の意味圧縮で明示委譲時だけへ狭まったoperation completionを、root-only operationにも復元する診断candidateである。

Candidate50はCandidate43へread batch方法を追加した別診断として`draft / targeted_evaluated / stopped`のまま保持する。Candidate51はCandidate50をsourceにせず、tool batch、read順序、model step数をpromptで指定しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-explicit-delegation-control-boundary-r1`（Candidate49）とする。最短正常経路は、明示委譲がなければrootがoperationの単一producerとなり、TaskSpecに固定済みの全predicate resultを揃えてからoperationを完了する経路である。
2. 保存済みCandidate49 F10 N=5では、Candidate43と同じ50 command、同じauthority、固定diff、2 source fileを使い、全runがroot-onlyかつscore `4`だった。一方、F10 token合計は`702,320 -> 960,823`、input tokenは`689,536 -> 945,707`となった。Candidate49は5回中4回が12 model callで、固定済み確認を逐次model stepへ分割した。
3. Candidate49はC43の`PRODUCER / TERMINAL / INDEPENDENCE`をworker固有制御と一括分類し、`DELEGATION / COMPLETION`を明示委譲時だけへ限定した。TaskSpecはrequired outcomeとpredicateを固定するが、root-only operationのproducerと全predicate completionをCandidate49では固定しない。
4. 置換する一つのpredicateは、明示委譲がなければrootをoperationのproducerとし、開始済みoperationは全predicateのbind済みproducer terminal resultが揃うまで完了にしない境界である。
5. このpredicateは、root-only operationの各predicateを別々の未関連な判断として再開する経路と、全predicate resultが揃う前にoperation completionを再判断する経路を消す。tool batch、command結合、read順序、探索対象は固定しない。
6. 新たに増える判断は、明示委譲の有無によるproducer選択と、全predicate terminal resultが揃ったかの確認である。Candidate43の`INDEPENDENCE`、worker packet field、runtime Sender照合、result projectionは復元しない。
7. 成果品質はF05 clarificationとF10 monthly reviewを各`N=5`、第9版採点で確認する。全10 runのscore `4`、root-only、required command、no-driftを維持する。
8. F10ではcommand数とread対象をCandidate49と同程度に保ち、model step、tool call、input tokenがCandidate43方向へ戻るかを確認する。prompt byte数だけを成果にしない。
9. F10のmodel stepまたはinput tokenがCandidate49から減らない、commandまたは探索対象が増える、score `4`を失う、不要なworkerを起動する、またはmethod制御なしにoperation closureの復元を判定できない場合は停止する。`INDEPENDENCE`復元はCandidate51へ継ぎ足さず、別candidateとして扱う。

## 変更単位

Candidate49のroot `AGENTS.md`にある`DELEGATION`と`COMPLETION`だけを、全operationに共通する一つのcompletion不変条件へ合わせて置換する。

- 明示委譲がある場合は指定producer、ない場合はrootを一つのproducerとしてbindする。
- 開始済みoperationは全predicateのbind済みproducer terminal resultが揃うまで完了にしない。
- `SPEC / CONTEXT / METHOD / RECOVERY`はCandidate49とbyte identityを保つ。
- `INDEPENDENCE`と`ROOT_BATCH`は追加しない。

## 評価順序

1. bundle identity、Candidate49との差分1 target、未変更18 targetのbit identityを確認する。
2. F05 / F10第9版を各`N=5`で実行する。
3. Candidate43 / Candidate49の互換resultとscore、token、command、tool call、model step、input tokenを比較する。
4. root operation completionの復元効果を確認できた場合だけ、A01 / A02への影響確認を別判断として行う。

Candidate51の作成、評価、採用、release、本体反映は別状態として扱う。

## 対象試験結果

2026-07-21にF05 / F10第9版を各`N=5`で実行した。10 / 10がscore `4`、root-only、protocol違反0、zero driftだった。

Candidate51のF10はCandidate49比でmodel step `52 -> 38`、input token `945,707 -> 737,406`、token合計`960,823 -> 750,869`となった。Candidate43比ではmodel step `37 -> 38`、input token `689,536 -> 737,406`、token合計`702,320 -> 750,869`である。

C49で増えた逐次分割は数値上C43とほぼ同じ分布へ戻った。ただし登録後に、Candidate43 / Candidate49とCandidate51でmodel-visible skill / plugin catalogが一致していないことを確認した。現行compatibility keyはこの差を検出しないため、prompt効果として確定しない。Candidate51へ追加predicateを継ぎ足さず、model-visible Agent環境identityを固定するまでA01 / A02と`INDEPENDENCE`復元へ進まない。

詳細は[`Candidate43 / Candidate49 / Candidate51 対象試験`](../evaluations/results/candidate43-candidate49-candidate51-root-operation-completion-boundary-targeted-n5_2026-07-21.md)に記録する。
token増加要素は[`F10 token増加分析`](../evaluations/results/candidate43-candidate51-f10-token-increase-analysis_2026-07-21.md)に分離する。

## Capability catalog固定再試験

apps、plugins、plugin sharingを無効化し、20 / 20 runのmodel-visible catalog SHA-256一致をgateにした[`Candidate43 / Candidate51固定再試験`](../evaluations/results/candidate43-candidate51-catalog-fixed-targeted-n5_2026-07-21.md)を追加した。C49は再実行していない。

固定再試験ではCandidate51のF05はCandidate43比`-2.61%`、F10は`+22.70%`だった。F10 model stepは`48 -> 60`で、Candidate51は5 / 5 runを11 tool callへ分けた。同じ11 tool call経路ではCandidate51のinput tokenが`-1.54%`である。

root producerとcompletionの復元だけでは、固定済みの独立readを同一model stepへまとめる経路は復元しなかった。次candidateを検討する場合は、worker制御全体を戻さず、Candidate51で未復元のroot predicate間の依存境界だけを別変更単位とする。
