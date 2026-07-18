# Prompt制御見直し 引き継ぎ

## 目的

次の作業では、Candidate35からCandidate40までの制御を追加修正する前に、ControlFreeRepositoryで成立していた基本挙動へ戻って制御graphを見直す。

目的は、条件を増やすことではない。成果品質を維持しながら、制御の読解・確認costより多くの探索、context継承、再読、再試行、手戻りを消す最小制御を特定する。

この見直しが完了するまで、次candidate、評価profile、追加runを作成しない。

## 作業状態

- repository: `/Users/kenn/repos/THE-CAPTION-PROMPT`
- branch: `codex/c35-evaluation-corrections`
- handoff作成時HEAD: `a92a4ce`
- working tree: C35以降の試験修正、candidate、profile、result、制御原則を含む未commit差分がある
- 既存差分はこの作業の入力である。reset、checkout、破棄、別worktreeへの分離をしない
- publish、commit、push、PR、mergeは未依頼であり、実施しない

## 必ず先に読む文書

1. [`AGENTS.md`](../AGENTS.md)
2. [`prompt-control-design-principles.md`](prompt-control-design-principles.md)
3. [`Control-free repository N=5`](../evaluations/results/control-free-generic-repository-expanded12-global-m24-n5_2026-07-16.md)
4. [`Candidate11 worker context sufficiency N=5`](../evaluations/results/candidate11-sa-context-boundary-expanded12-global-m24-n5_2026-07-16.md)
5. [`ControlFreeRepository / Candidate23 operation boundary N=5`](../evaluations/results/control-free-repository-candidate23-operation-boundary-expanded12-global-m24-n5_2026-07-17.md)
6. [`Candidate35 / Candidate38 v9 targeted N=5`](../evaluations/results/candidate35-candidate38-outcome-quality-owner-diagnostic-v9-targeted2-n5_2026-07-19.md)
7. [`Candidate35 / Candidate38 token trace analysis`](../evaluations/results/candidate35-candidate38-v9-targeted2-n5-token-trace-analysis_2026-07-19.md)
8. [`Candidate40 targeted N=5`](../evaluations/results/candidate40-operation-result-projection-boundary-v9-targeted2-n5_2026-07-19.md)

あわせて、次のroot prompt本文を直接比較する。

- `prompts/candidates/the-caption-3ce91a4-control-free-repository-r1/files/AGENTS.md`
- `prompts/candidates/the-caption-3ce91a4-control-free-operation-boundary-r1/files/AGENTS.md`
- `prompts/candidates/the-caption-3ce91a4-root-control-only-r1/files/AGENTS.md`
- `prompts/candidates/the-caption-3ce91a4-result-unit-evidence-binding-r1/files/AGENTS.md`
- `prompts/candidates/the-caption-3ce91a4-operation-result-projection-boundary-r1/files/AGENTS.md`

## 確認済みの事実

### ControlFreeRepository

- root `AGENTS.md`だけが0-byteである。`src/AGENTS.md`などのpath-scoped repository authorityは残る。
- 実行はTaskSpec、path-scoped repository authority、source・test・diff・repository stateの三層で制御される。
- expanded 12 case N=5ではscore `4 / 3 = 59 / 1`、quality中央値`100.000`だった。
- F10 entrypoint inventoryは5 / 5がscore `4`だった。各runはroot sessionだけで完了し、childを必要としなかった。
- ambiguity 5 caseでは、未指定policyの推測、authority conflict、permission conflict、validation completionに不足があった。

### 有効な制御例

- Candidate11は、worker packetとallowed readで十分な場合に`fork_turns=none`とした。
- workerの要否や数を固定せず、不要な親context流入だけを実行前に遮断した。
- F07では必要な2 workerを維持したまま10 spawnすべてが`none`となり、C10比のcase token中央値は`-1,009,985`だった。
- Candidate11全体は60 / 60がscore `4`だった。

### C35からC40

- C35 v9 targeted N=5は10 / 10がscore `4`、10 run token合計`2,073,880`だった。
- C38 v9 targeted N=5も10 / 10がscore `4`だったが、C35比の10 run token合計は`+255,767`だった。
- C38とC35のtoken差の99.34%はinput tokenで、90.50%はF10に集中した。F10はC38で`exec +8`、`wait +3`、model step `+10`だった。
- C40はresult unitをoperation terminal resultのprojectionへ限定したが、F10のtool call、model step、token合計をC38から減らさなかった。F10 token合計はC38比`+49,106`だった。
- C40のscore分布は`4 / 1 = 9 / 1`だった。score `1`ではchildの正しいfindingをrootがowner identity不一致と解釈して省略した。
- したがって、C38からC40の境界明確化は、狙った実行経路削減を実現していない。

## 現在の解釈

制御は、規則を増やすものではなく、将来の不要な判断を先に消す圧縮情報である。

C38以降は、result unit、producer terminal result、owner identity、evidence、invalidationの関係を増やした。これにより、誤経路を減らす以上に、label間の関係を解釈し確認する判断点を増やした可能性がある。

ControlFreeRepositoryでは、TaskSpecとrepository evidenceから成果へ直接到達できたcaseがある。これらへroot controlで同じ意味を再定義すると、最短経路を阻害する可能性がある。

次に必要なのは新しい境界文言ではない。既存制御のうち、基本挙動に対して何を追加し、どの誤経路を消し、どの判断点を増やしたかの棚卸しである。

## 次タスクで行う見直し

### 1. 基本の最短正常経路を記述する

F05 clarificationとF10 monthly reviewについて、ControlFreeRepository相当のTaskSpec、repository authority、repository evidenceだけで成立する最短正常経路を記述する。

各経路は、入力、必要なread、判断、terminal outputだけに限定する。既存root promptのlabelを前提にしない。

### 2. 制御graphを棚卸しする

C35、C38、C40の各predicateについて、次を表にする。

| 項目 | 内容 |
| --- | --- |
| label / predicate | prompt上の規則 |
| 入力となる状態 | 何を判定材料にするか |
| 消そうとした誤経路 | 保存traceで確認した具体的な問題 |
| 追加した判断点 | identity、binding、evidence、失効など |
| 基本三層との重複 | TaskSpec、repository authority、repository evidenceで既に決まるか |
| 実測結果 | quality、token、tool call、model stepへの観測 |
| 判定 | 維持、置換、統合、削除の候補 |

必要に応じてCandidate23、Candidate31、Candidate34を由来確認に使う。ただしcandidate番号順を親子関係とみなさず、manifestのdirect sourceを確認する。

### 3. 制御を分類する

各predicateを次のいずれかへ分類する。

- repository / TaskSpecで既に成立するためrootで重複している
- 観測済みの誤経路を一つ消すため必要である
- 成果後の確認だけを増やし、実行前の分岐を減らしていない
- 複数labelを結合し、解釈のブレまたは最短経路の阻害を生んでいる
- 効果を判断する証拠が不足している

### 4. 次の変更predicateを一つだけ提案する

提案は追加を前提にしない。削除、既存predicateへの統合、直接記述への置換を優先する。

提案には次を含める。

- 残す最短正常経路
- 消す一つの誤経路
- 削除または追加される判断点
- 期待するquality不変条件
- 期待するcase別token、tool call、model stepの変化
- targeted試験のcaseと停止条件

この提案をユーザーへ説明し、合意を得るまでcandidate bundleを作らない。

## やらないこと

- 棚卸し前にC41相当のcandidateを作らない
- 「一回だけ読む」「tool callをN回にする」など、必要性を示さない方法指定を追加しない
- C40の低token中央値だけを成功と解釈しない
- quality中央値だけでscore分布の低下を隠さない
- prompt byte数の減少を実行token削減と読み替えない
- prompt変更と評価条件変更を同じ比較単位へ混ぜない
- 評価基盤v3の固定点を追加分析のために変更しない
- THE-CAPTION本体への反映、release判断、commit、push、PR、mergeを行わない

## 検証状態

- C40 bundle identity検証済み
- C40 campaignは10 / 10 valid・rateable、retry / excluded 0、Layer 4 registration、lossless archive、compact完了
- `python3 -m unittest discover -s tests -q`: 108 tests、OK
- `git diff --check`: pass
- 引き継ぎ作成後の変更は文書とroot `AGENTS.md`参照だけであり、コード試験は再実行していない

## 次タスクの最初の完了条件

最初の完了単位は、candidate作成ではなく、F05 / F10の最短正常経路とC35 / C38 / C40の制御graph棚卸しを、事実・推論・提案に分けて提示することである。

棚卸しから一つの変更predicateを導けない場合は、無理にcandidateを作らず、証拠不足または制御不要として報告する。
