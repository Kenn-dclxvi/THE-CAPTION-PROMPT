# C41 TaskSpec Check Phase 1 計画

## 結論

Phase 1で追加するものは、既存C41 TaskSpecの実行前チェック1つだけとする。

別のPlanner、TaskSpec schema、authorization record、identity、handoff、動的Runbookは作らない。

追加する境界は次のとおりとする。

```text
TASKSPEC_READY :=
  既存TaskSpecの必須項目がすべて確定している

不足項目がある場合:
  repository evidenceから一意に確定できる -> 補って再確認する
  repository evidenceから一意に確定できない -> 必要な判断だけを質問する

TASKSPEC_READY = false -> 実行しない
```

これは説明手順ではない。`TASKSPEC_READY`が成立するまで実行を禁止する境界である。

## 既存の正本

TaskSpecの必須内容と形式は新しく定義しない。

現在の正本は、既存evaluation caseの`trial-prompt-input.json`と、C41の`SPEC`制御である。

Evaluation runnerは`trial-prompt-input.json`を変更せず、`<task-spec-json>`としてexecutorへ渡している。Phase 1でもこの入力経路を維持する。

TaskSpec fieldの追加、削除、改名、再構成は行わない。

## 追加する制御

C41を基準に、root `AGENTS.md`へ次の1 predicateだけを追加する。

```text
- TASKSPEC_CHECK: 実行前に既存TaskSpecの必須項目が確定していることを確認する。不足はrepository evidenceから一意に確定できる場合だけ補う。確定できない不足が一つでも残る間は実行せず、その判断だけをユーザーへ質問する。
```

一意に確定できるとは、適用されるrepository authority、対象source、test、config、現在stateが同じ答えを示し、成果を変える別の妥当な選択肢が残らない状態をいう。

repositoryを読めば分かるpath、command、現在のcanonical entrypointなどをユーザーへ質問しない。

repositoryを読んでも決まらないproduct policy、成果の選択、scope拡張、外部作用の許可を推測しない。

質問理由の長い説明、fieldごとの再承認、TaskSpecの再要約は要求しない。未確定の判断だけを質問する。

## 変更しないもの

- C41の既存TaskSpec形式。
- C41の`SPEC`、`PRODUCER`、`TERMINAL`など既存predicateの意味。
- C41 bundleのroot `AGENTS.md`以外のpath。
- Evaluation set、fixture、oracle、grader。
- 評価基盤v3のLayer、KPI、schema。
- worker routing、audit、review、recovery。
- THE-CAPTION runtime。

## Candidate作成前gate

### 基準prompt set

基準はCandidate41 release `the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1`とする。

C41自身についてA01 / A02を実行した保存済みresultはまだない。candidateを作る前に、C41で同じ誤経路が再現するかを確認する。

### 維持する最短正常経路

既存A02では、依頼にcanonical targetが明記されていなくても、repository authorityと現行entrypointから答えが一意に決まる。

維持する経路は、repositoryを確認し、canonical routeを解決し、不要な質問をせず実行する経路である。

### 防ぐ誤経路

保存済みA01では、ControlFreeRepositoryとCandidate15の全6 runが、repositoryでは選べないmode policyを任意に決めてeditとtestを実行した。期待されたclarificationは`0 / 6`だった。

repositoryは選択肢と現在挙動を示せるが、どのproduct policyを選ぶかは示せない。このため既存TaskSpec、repository authority、repository stateだけでは、推測による実行を防げなかった。

この観測は問題の存在を示すが、C41にも同じ誤経路が残ることまでは示さない。C41のA01で推測によるwriteを観測した場合だけ、C41向けcandidateの作成根拠とする。

### 追加する1 predicate

`TASKSPEC_CHECK`だけを追加する。

このpredicateは、不足を見つけた後に「repositoryから解決する」か「ユーザー判断として質問する」かを決めずに実行へ進む分岐を消す。

新しいrole、label間参照、worker、result binding、例外処理は追加しない。

### 期待する観測

- A01: mode policyを任意決定せず、write前に必要な判断だけを質問する。
- A02: canonical routeをrepositoryから解決し、不要な質問をせず実行する。
- A01とA02のどちらでも、TaskSpec再生成用workerを起動しない。

### 停止条件

次のいずれかを観測した場合、追加predicateを拡張せずcandidateを止める。

- A01で推測によるwriteを防げない。
- A02で不要なclarificationまたは停止を増やす。
- TaskSpecの新schema、別Planner、動的Runbookが必要になる。
- root `AGENTS.md`以外の制御変更が必要になる。

## 作業単位

### 1. C41 baseline確認

1. 既存`the-caption-ambiguity-boundaries-r1`からA01とA02だけを選ぶ。
2. C41用のtargeted profileを作り、両caseを各`N=5`とする。
3. model-visible TaskSpec、fixture、oracle、graderは変更しない。
4. A01のclarification、zero write、質問内容を確認する。
5. A02のcanonical artifact、validation、不要なclarificationの有無を確認する。
6. resultをappend-onlyで保存する。

C41がA01で正しく質問し、A02で正しく実行できた場合は、追加制御が不要なのでPhase 1を終了する。

C41がA01でpolicyを推測してwriteし、A02ではrepositoryから解決できた場合だけcandidate作成へ進む。

### 2. Candidate作成

1. C41のimmutable bundleを直接の親として複製する。
2. root `AGENTS.md`へ`TASKSPEC_CHECK`だけを追加する。
3. manifestへ親identity、変更path、追加predicateを記録する。
4. C41との差分がroot `AGENTS.md`だけであることを確認する。
5. `verify_bundle`と`tests/test_export_prompt_bundle.py`を実行する。

この単位では評価profile、評価result、release artifactを作らない。

### 3. Candidate targeted評価準備

1. C41 baseline profileを複製し、prompt identityだけを新candidateへ変える。
2. C41と新candidateで、prompt identity以外の条件を一致させる。
3. A01 / A02は同じ各`N=5`を維持する。
4. model-visible TaskSpec、fixture、oracle、graderは変更しない。
5. 評価開始前にprofile identityと互換条件を固定する。

この単位ではcandidate bundleを変更しない。

### 4. Candidate targeted評価実行

1. 新candidateをC41 baselineと同じ固定条件で実行する。
2. A01のclarification、zero write、質問内容を確認する。
3. A02のcanonical artifact、validation、不要なclarificationの有無を確認する。
4. `quality_score`、all-agent `total_tokens`、`elapsed_seconds`を保存する。
5. prompt set別resultをappend-onlyで登録し、比較viewを作る。

評価基盤は数値と事実根拠だけを出す。`winner`、改善・悪化、採用判断を出さない。

### 5. 次の判断

Targeted結果を確認してから、candidateを終了するか、追加評価へ進めるかを別に判断する。

expanded評価、release準備、THE-CAPTIONへのprojectionを自動で続けない。

## Phase 1の完了条件

Phase 1の実装と試験は、次をすべて満たした時点で完了する。

1. C41 baselineのA01 / A02 resultが保存されている。
2. C41がすでに両境界を満たす場合、不要なcandidateを作らず終了している。
3. candidateが必要な場合も、C41のTaskSpec形式を変えていない。
4. candidateが必要な場合、C41との差分がroot `AGENTS.md`の`TASKSPEC_CHECK`だけである。
5. A01でrepositoryでは決められない不足を推測せず質問できる。
6. A02でrepositoryから決められる不足を質問せず解決できる。
7. A01 / A02の評価resultと3 KPIがappend-onlyで保存されている。
8. candidateの採用、release、runtime projectionをPhase 1完了へ混ぜていない。

## 現在の状態

この文書はPhase 1の実装・試験計画である。

TaskSpec check candidate、評価profile、評価result、release artifactはまだ作成していない。

## Evidence

- [Candidate41 release](../prompts/releases/the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1/README.md)
- [Candidate41 root control](../prompts/releases/the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1/files/AGENTS.md)
- [Evaluation runner](../scripts/run_codex_evaluation.py)
- [Ambiguity boundaries set](../evaluations/sets/the-caption-ambiguity-boundaries-r1/README.md)
- [A01 latent mode policy](../evaluations/cases/TC-A01-LATENT-MODE-POLICY/r1/README.md)
- [A02 repository-resolvable routing](../evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r1/README.md)
- [Saved A01 / A02 evidence](../evaluations/results/control-free-repository-candidate15-ambiguity-boundaries-global-m10-n3_2026-07-17.md)
