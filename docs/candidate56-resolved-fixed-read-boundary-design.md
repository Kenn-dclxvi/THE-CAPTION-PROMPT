# Candidate56 resolved fixed read boundary設計記録

## 結論

Candidate56はCandidate55を直接sourceとし、root `AGENTS.md`一枚だけを変更する。

追加するpredicateはF系の`FIXED_READ`一つである。readiness解決後、rootがproducerで、TaskSpecが有限の相互非依存read-only入力を確定済みの場合だけ、個別tool callとexitを保ったまま同一model stepで取得する。

authorityを探索中のA系、先行resultで次のtargetが決まるread、write、test、dependency操作には適用しない。Candidate50の全域batchを戻さず、C55 r2で観測したF10の逐次context再送だけを対象にする。

## Candidate作成前gate

1. 基準prompt setはCandidate55である。最短正常経路は、readinessが解決済みのF10で、開始identityを一つのtool call、TaskSpecが固定したauthority・diff・2 sourceを一つのtool call、終了statusを一つのtool callとして取得し、findingを返す3-call経路である。
2. 保存済みの誤経路はCandidate55 route gate r2のF10である。5 run中4 runが同じ11 shell commandを11 top-level tool callへ分け、経路は`3 / 11 / 11 / 11 / 11`、合計47 callとなった。
3. F10 TaskSpecはread対象を固定し、Candidate55はpredicate・permission・constraintをoperationへ事前bindする。それでも同じpromptのr1 / r2でtool call合計が`33 / 47`へ変動した。意味上のoperation bindingだけでは、独立readを逐次model stepへ分ける経路を防げない。
4. Candidate50の`ROOT_BATCH`はF05 / F10のmodel stepを`59 -> 32`、token合計を`-40.08%`とした。一方、read集合が未確定のA01 / A02にも適用され、A02 command `38 -> 84`、token合計`+13.38%`となった。batch方法のF系効果とA系探索拡大を分離する必要がある。
5. 追加するpredicateは、`readiness解決後 ∧ root producer ∧ TaskSpecが有限の入力集合を確定済み ∧ 各readが相互非依存 ∧ read-only`の場合だけ、個別tool callとexitを維持して同一model stepで取得する境界である。
6. このpredicateが消す判断点は、固定済みreadを一つ受け取るたびに残りのread実行を再決定することと、その都度のcontext再送である。required read、command、evidence、最終判断は削らない。
7. 新たに増える判断は一回の適用判定である。readiness未解決、入力集合未確定、先行result依存、write、test、dependency操作なら非適用とする。非適用時にread集合を探索または拡張する権限は与えない。
8. 成果品質はcatalog固定F05 / F10各`N=5`で10 / 10 score `4`、root-only、zero driftを必須とする。F10は各run5 tool call以下、合計25以下、token合計Candidate43の`848,388`以下とする。F05はCandidate43のmodel step `22`、tool call `17`、token合計`330,657`を超えない。
9. F系gateを通過した場合だけcatalog固定A01 / A02へ進む。A01のauthority探索中に`FIXED_READ`を適用する、A02のread集合を広げる、A01 / A02のmodel step・tool call・token合計がCandidate43を超える、またはscore `4`を失う場合は停止する。別predicateをCandidate56へ継ぎ足さない。

九項目を定義済みであるため、Candidate56 bundleとF05 / F10 profileの作成を許可する。

## 変更するgraph

```text
A readiness
  unresolved -> clarification -> stop
  resolved
     |
     v
F operation input fixed before first predicate
     |
     +-- finite + independent + read-only + root producer
     |      -> same model step, separate tool identity / exit
     |
     +-- otherwise
            -> normal execution; no read-set expansion authority
```

`FIXED_READ`はF系methodであり、A系readinessを確定するための探索方法ではない。D系explicit delegationにも適用しない。

## Prompt変更

Candidate55の`OPERATION`直後へ`FIXED_READ`を一つ追加する。他のA / F / D、terminal、method predicateは変更しない。残り18 targetはCandidate55とbit identityを保つ。

## 評価順序

1. bundle identity、1 target差分、`FIXED_READ`の適用条件と非適用条件を構造testで確認する。
2. Candidate43と同じcatalog固定F05 / F10条件で各`N=5`を実行する。旧catalogと実行時catalogが不一致なら、そのrunは外部計測失敗として除外し、観測したcatalogを別profile revisionへ固定してCandidate43 / Candidate56を同条件で取り直す。
3. F系gateを通過した場合だけ、Candidate43 / Candidate56のcatalog固定A01 / A02 profileを新しい別revisionとして作る。
4. A系非適用境界を通過した場合だけstandard14を別判断として検討する。

candidate作成、対象試験、採用、release、本体反映は別状態である。

## 評価後状態

F05 / F10各`N=5`ではF10が5 / 5 runとも3 tool callへ収束し、token合計はCandidate43比`-56.17%`だった。F系gateは通過した。

A01 / A02各`N=5`ではA02 commandが`47 -> 70`へ増え、1 runで必須`git diff --check`を欠いてscore `3`となった。A系非適用gateで停止した。詳細は[`Candidate43 / Candidate56 result`](../evaluations/results/candidate43-candidate56-resolved-fixed-read-boundary-catalog-fixed-targeted-n5_2026-07-21.md)へ分離する。
