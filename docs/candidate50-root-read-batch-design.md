# Candidate50 root read batchの設計記録

## 位置付け

Candidate50はCandidate43を直接sourceとし、`spec_ready`後のroot-only operationで、順序依存のないread-only predicateを同一model stepの個別tool callとして実行する候補である。

Candidate49は明示委譲境界の診断candidateとして`draft / targeted_evaluated / stopped`のまま保持する。Candidate50はCandidate49をsourceにせず、委譲制御の圧縮を変更単位へ含めない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。最短正常経路は、TaskSpecが固定したread-only sourceと開始identityをrootが個別tool callのまま一つのmodel stepで確認し、結果をまとめて次の判断へ進める経路である。
2. 保存済みCandidate43 F10 N=5では、iteration 4 / 5が11個のshell executionを3つのtool batchへまとめ、最終responseを含むmodel callは各4回だった。一方、iteration 1 / 3は同じ11個を1回ずつ処理し、各12 model call、input tokenは`220,364 / 216,803`になった。iteration 4 / 5のinput tokenは`77,927 / 77,692`だった。
3. Candidate49 F10は5回中4回が12 model callとなり、Candidate43比でF10 input tokenが`+256,171`だった。command setとrequired evidenceは同じで、tool output文字数はCandidate49の方が小さかった。この観測はCandidate50のsource identityには使わず、直列model stepがcontext再送を増やす診断根拠としてだけ使う。
4. F10 TaskSpecはread可能path、開始identity、固定diff、終了時no-driftを定めるが、相互に依存しないread-only確認のmodel step数を固定しない。Candidate43の`METHOD`も手段選択をexecutorへ委ねるため、同じsourceを順次確認して毎回contextを再入力する経路を防がない。
5. 追加する一つのpredicateは、`spec_ready=true`かつrootがproducerであるoperationで、TaskSpecが順序を固定せず、先行resultを入力としないread-only predicateを、commandとexitを分離した同一model stepのtool batchとして実行する境界である。
6. このpredicateは、独立read間のmodel判断、固定済みTaskSpec・repository authority・既読sourceの再探索、各tool result受領ごとのcontext再送を消す。required command、read対象、evidence、最終判断は減らさない。
7. 新たに必要になる判断は、root producer、`spec_ready`、read-only、順序依存なし、先行result非依存の適用確認である。write、test、dependency操作、前段resultで対象またはcommandが変わる確認はbatch対象にしない。worker、owner、result identity、terminal stateは変更しない。
8. 成果品質はA01 / A02第10版とF05 / F10第9版を各N=5で確認する。score分布、変更path、required command evidence、no-driftを維持し、Layer 2 extensionでF10 / A02のmodel step、tool call、tool output、input tokenを比較する。
9. F10のmodel stepまたはinput tokenがCandidate43から減らない、A02の探索・tool outputが拡大したままtokenだけが移る、score `4`を失う、required commandをshell内へ結合して個別exit evidenceを失う、またはread-only以外をbatchした場合は停止する。別のprompt圧縮や委譲predicateを継ぎ足さない。

## 変更単位

Candidate43のroot `AGENTS.md`へ`ROOT_BATCH`を一つ追加する。

- Candidate43の`SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / METHOD / RECOVERY`はbyte identityを保つ。
- `ROOT_BATCH`は個別command identityとexitを維持したtool batchだけを扱う。
- prompt byte数の縮小、worker context、委譲条件、探索対象、required evidenceは変更しない。

## 評価順序

1. bundle identity、C43との差分1 target、未変更18 targetのbit identityを確認する。
2. A01 / A02第10版とF05 / F10第9版を各N=5で実行する。
3. 20件の成果品質と、F10 / A02のmodel step、tool call、tool output、input tokenをCandidate43の互換resultと比較する。
4. 停止条件に該当しない場合だけ、次の評価範囲を別判断として検討する。

## 評価結果

互換条件を揃えたA01 / A02とF05 / F10を各`N=5`で実行した。Candidate50は20 / 20件がscore `4`で、全runがroot-onlyだった。

F05 / F10では10 run token合計が`1,050,768 → 629,619`、F10 model stepが`37 → 22`となり、固定read集合の逐次context再送は減った。一方、A01 / A02では10 run token合計が`2,171,599 → 2,512,469`、A02 commandが`38 → 84`、model stepが`48 → 54`となった。

20 run合計は`-2.49%`だが、root promptは`+12.01%`であり、F項目の減少がA項目の増加を相殺している。事前停止条件の「A02の探索が拡大したままtokenが増える」に該当するため、Candidate50は`draft / targeted_evaluated / stopped`とする。A03 / F07、標準14項目、A06へ進めず、別predicateを継ぎ足さない。

詳細は[`Candidate43 / Candidate50 root read batch 対象試験 N=5`](../evaluations/results/candidate43-candidate50-root-read-batch-targeted-n5_2026-07-21.md)に記録する。

Candidate50の作成、評価、採用、release、本体反映は別状態として扱う。採用、release、本体反映は未判断・未実施である。
