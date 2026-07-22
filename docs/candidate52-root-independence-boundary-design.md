# Candidate52 root independence境界の設計記録

## 位置付け

Candidate52はCandidate51を直接sourceとし、Candidate43からCandidate49への意味圧縮で消え、Candidate51でも未復元だった`INDEPENDENCE`を一文だけ復元する診断candidateである。

Candidate51で復元済みのroot producer bindingと全predicate completionは変更しない。worker packet、runtime Sender照合、result projection、tool API、code mode、command結合、read順序は追加しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-root-operation-completion-boundary-r1`（Candidate51）とする。最短正常経路は、rootをproducerとする固定済みoperationで、先行依存のないpredicateを同じ実行局面で取得し、全predicate resultが揃った時点でterminalにする経路である。
2. capability catalog固定済みF10 `N=5`では、Candidate51は5 / 5 runを`12 model step / 11 tool call`へ分割した。Candidate43には開始確認5 commandを1 call、authority / diff / source 5 readを1 callへまとめるrunがあり、F10全体は`48 model step / 43 tool call`だった。
3. TaskSpecはrequired outcome、対象commit、必要なread、permissionを固定するが、先行resultへ依存する別operationと、同じoperation内で互いに依存しないpredicateの境界をCandidate51では固定しない。repository authorityとstateだけでは、各readを新しい逐次判断として再開する経路を防げない。
4. 追加する一つのpredicateは、Candidate43の`INDEPENDENCE: 先行result / artifactを対象とする別operationへ固有predicate / owner / producerを実行前に固定する。同一predicateを別producerへ再割当てしない。`をCandidate51へそのまま復元することである。
5. このpredicateは、先行resultを必要としない同一operation内のreadまで別operationとして逐次再開する判断点を消す。後続依存operationだけを分け、同一predicateの再割当てを防ぐ。
6. 新たに増える判断は、後続処理が先行result / artifactを対象とする別operationかの判定一つである。tool call数、同一model step、batch、並列数は判断条件へ追加しない。
7. 成果品質はF05 clarificationとF10 monthly reviewを各`N=5`、第9版採点で確認する。Candidate52の10 runでscore `4`、root-only、required outcome、zero driftを維持する。
8. capability catalogを固定し、F10のmodel step、tool call、input tokenがCandidate51からC43方向へ戻るか確認する。同じtool call経路ではprompt追加costも確認する。
9. F10のmodel stepまたはtool callがCandidate51から減らない、token合計が減らない、F05で逐次分割が増える、score `4`を失う、不要なworkerを起動する、またはcommand / evidenceを省略した場合は停止する。別のC43要素をCandidate52へ継ぎ足さない。

## 変更単位

Candidate51のroot `AGENTS.md`へCandidate43の`INDEPENDENCE`一文だけを追加する。

- `SPEC / DELEGATION / CONTEXT / COMPLETION / METHOD / RECOVERY`はCandidate51とbyte identityを保つ。
- 残り18 targetはCandidate51とbit identityを保つ。
- `PRODUCER / TERMINAL / OWNER_ROLE / ROOT`は追加しない。
- tool batching方法は指定しない。

## 評価順序

1. bundle identity、Candidate51との差分1 target、未変更18 targetのbit identityを確認する。
2. apps、plugins、plugin sharingを無効化し、model-visible capability catalog SHA-256一致を開始gateにする。
3. F05 / F10第9版を各`N=5`で実行する。
4. Candidate43 / Candidate51のcatalog-fixed resultとscore、token、elapsed、tool call、model step、input tokenを比較する。
5. 狙ったrouting変化と品質維持を確認できた場合だけ、A系への影響確認を別判断として行う。

Candidate52の作成、評価、採用、release、本体反映は別状態として扱う。

## 対象試験結果

2026-07-21にcapability catalog固定済みF05 / F10第9版を各`N=5`で実行した。10 / 10がscore `4`、root-only、protocol違反0、zero driftだった。

Candidate52のF05はCandidate51比でmodel step `22 -> 19`、token `-13.36%`だった。一方、F10はmodel step `60 -> 61`、tool call `55 -> 56`、token `+6.76%`だった。10 run token合計も`+2.01%`となった。

Candidate52のF10は4 tool callへまとめるrunを1件作ったが、16 / 14 tool callへ追加探索するrunも2件作った。`INDEPENDENCE`一文はC43のroutingを安定して復元しなかった。

作成前gateの停止条件に従い、Candidate52へ別のC43要素を追加しない。Candidate52は`targeted_evaluated / stopped`として保持する。詳細は[`Candidate43 / Candidate51 / Candidate52対象試験`](../evaluations/results/candidate43-candidate51-candidate52-root-independence-catalog-fixed-targeted-n5_2026-07-21.md)に記録する。

## Evidence

- [`Candidate43 / Candidate51 capability catalog固定対象試験`](../evaluations/results/candidate43-candidate51-catalog-fixed-targeted-n5_2026-07-21.md)
- [`Candidate51設計記録`](candidate51-root-operation-completion-boundary-design.md)
- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
