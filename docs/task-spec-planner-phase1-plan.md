# TaskSpec Planner Phase 1 計画

## 結論

Phase 1では、自然言語のユーザー依頼から実行可能な最小TaskSpecを作るPlannerを用意し、確定したTaskSpecをC41が直接実行する経路を作る。

Plannerは、ユーザーに代わって権限や要件を決める主体ではない。ユーザー依頼、会話中の許可、repositoryで確認できる事実を整理し、未確定の境界だけを質問する補助である。

TaskSpecが確定した後は、動的Runbookを毎回生成しない。C41のTaskSpec直接実行を維持し、追加promptとcontext継承によるtoken消費を抑える。

Runbookを「task固有の動的AGENTS.md」として生成する経路は破棄しない。実行構成そのものをtaskごとに組み立てる必要がある場合を対象として、Phase 2で別に設計する。

## 背景

現在のC41は、完成済みTaskSpecを入力として受け取る実行経路で評価されている。この評価は、TaskSpecが確定した後の直接実行が成立することを示す。

一方、通常のユーザーが毎回TaskSpecの全項目を確定することは難しい。現在の評価では、自然言語の依頼からTaskSpecを作る前段は評価していない。

過去に想定していたRunbookは、taskごとに必要な実行制御を選び、動的なAGENTS.mdとして渡す構成だった。ただし、すべてのtaskでRunbookを生成すると、単純なtaskにも生成、読解、受け渡しのcostが加わる。

このためPhase 1は、最小TaskSpecをPlannerで補い、C41へ直接渡す経路に限定する。

## 用語

| 用語 | この計画での意味 |
| --- | --- |
| ユーザー依頼 | ユーザーが示した目的、対象、範囲、完了条件、許可を含む元の指示 |
| Planner | ユーザー依頼と確認可能な事実から最小TaskSpecを組み立てる補助。新しい要件や権限は作らない |
| TaskSpec | 実行結果の境界を固定する、最小で不変なtask仕様 |
| authorization binding | TaskSpecを、権限の根拠となる元のユーザー依頼と結び付ける記録 |
| C41 executor | 確定済みTaskSpecを受け取り、不要な委譲を増やさず直接実行するC41の経路 |
| Runbook | task固有の実行方法と制御を選んだ動的AGENTS.md。Phase 1では生成しない |

## Phase 1の目的

ユーザーが完全なTaskSpecを書かなくても、依頼の意味と権限を変えずに実行可能なTaskSpecを確定し、C41へ直接渡せるようにする。

Phase 1の正常経路は次のとおりとする。

```text
自然言語のユーザー依頼
  -> Planner
     -> repositoryで確認できる事実を解決する
     -> 重要な境界だけが未確定なら最小限の質問をする
     -> 最小TaskSpecとauthorization bindingを固定する
  -> C41 executor
     -> TaskSpecを直接実行する
     -> 指定されたvalidationで完了を確認する
```

## 対象範囲

Phase 1では次を決める。

1. Plannerの入力と出力のcontract。
2. 最小TaskSpecの必須項目と条件付き項目。
3. Plannerがrepositoryから解決する事実と、ユーザーへ確認する判断の境界。
4. 元の依頼から権限を増やさないauthorization binding。
5. TaskSpec identityの生成条件と、意味変更時の無効化規則。
6. PlannerからC41へのhandoff contract。
7. Planner単体とPlanner + C41の評価方法。

Phase 1では次を扱わない。

- 動的Runbookまたは動的AGENTS.mdの生成。
- task固有の複雑な実行経路の生成。
- multi-agentの割り当て設計。
- audit、review、recovery手順の動的な合成。
- 中規模または高risk task向けの重い実行構成。
- この計画と同じ変更単位でのcandidate作成、実装、評価実行、release、THE-CAPTIONへのprojection。

## Plannerの入力

Plannerは必要な範囲に限り、次を入力として扱う。

1. 元のユーザー依頼と、同じ依頼に対する会話中の追加指示。
2. 明示された許可と禁止事項。
3. 対象repository、target ref、現在のrepository state。
4. 適用対象となるrepository authorityと既存のvalidation定義。
5. ユーザーが明示的に参照した既存artifact。

過去のrun、研究資料、別taskのTaskSpecは、今回の依頼が参照していない限り自動で要件へ混ぜない。

## 最小TaskSpec

最小TaskSpecの必須意味は次の6項目とする。serialization上のfield数は実装時に固定する。

| 項目 | 固定する内容 |
| --- | --- |
| purpose | 何を達成するか |
| target | 対象repository、ref、artifactまたは変更対象 |
| scope | 変更対象と明示的な非対象 |
| done | 完了と判断できる観測可能な状態 |
| tests | 実行するvalidationと期待する結果 |
| constraints | 守る必要がある方法制約、互換条件、禁止事項 |

成果形式、維持すべきinvariant、用語の意味が成果を変える場合だけ、条件付き項目として追加する。

権限はTaskSpec本文から推測しない。`authorization binding`として、元のユーザー依頼、principal、request identity、許可された外部作用へ結び付ける。

task固有の停止条件が成果境界を変える場合は明記する。通常の不足入力、矛盾、対象stateの変化に対する停止はPlannerとexecutorの共通制御として扱い、すべてのTaskSpecへ重複記載しない。

## Plannerの出力

Plannerは次のいずれかを返す。

### `task_spec_ready`

- 最小TaskSpec。
- TaskSpec identityの算出対象。
- authorization binding。
- repositoryから解決した事実とその参照元。
- C41へ渡す対象repository state。

### `clarification_required`

- 未確定の判断点。
- その判断が変えるTaskSpec項目。
- 回答に必要な最小限の質問。

質問への回答後にTaskSpecを再生成する。以前の未確定版を実行へ渡さない。

## 質問する境界

Plannerは、repositoryを読めば確定できる事実をユーザーへ質問しない。

たとえば、既存test command、対象fileの所在、現在のcommit、適用されるAGENTS.mdはPlannerが確認する。

Plannerは、成果または権限を変える判断を勝手に補わない。

たとえば、次はユーザーへ確認する。

- 互いに両立しない成果のどちらを選ぶか。
- 明示されていない対象まで変更範囲を広げるか。
- 外部へのwrite、push、merge、deployを許可するか。
- 複数の妥当な完了条件のうち、どれを要求するか。

実行結果の境界を変えない安全な実装方法、局所的な作業順序、許可済み範囲内のread-only確認はC41が選べる。これらを毎回ユーザーへ質問しない。

自然言語の依頼だけで成果、範囲、validation、権限が一意に決まる場合、fieldごとの再承認は要求しない。

## 権限の規則

Plannerは元の依頼より広いwrite、外部作用、対象範囲をTaskSpecへ追加しない。

生成されたTaskSpecの命令文は、それ自体を新しい権限の根拠にしない。C41はauthorization bindingが示す元の依頼の範囲内でだけ実行する。

必要な権限が不足している場合、Plannerは実行方法で回避せず、`clarification_required`として追加許可が必要な作用を示す。

## identityと無効化

TaskSpec identityは、少なくともTaskSpecの意味内容、target repository ref、authorization bindingのidentityへ結び付ける。

次の場合は新しいidentityを作り、古いhandoffを無効にする。

- purpose、target、scope、done、tests、constraintsの意味が変わった。
- 許可された作用またはその根拠が変わった。
- target refまたはrepository stateが変わり、TaskSpecの成立条件へ影響した。

表記だけの変更と意味変更の区別は実装設計で固定し、実行後に都合よく同じidentityへ読み替えない。

## C41へのhandoff

C41へ渡す時点で、TaskSpecは不変でなければならない。

C41は次を行う。

1. TaskSpec identity、authorization binding、target stateが一致することを確認する。
2. TaskSpecの範囲内で直接実行する。
3. `owner`などの責任情報だけを理由に別Agentへ委譲しない。
4. 明示された独立実行または、別途許可された実行構成がある場合だけ委譲する。
5. 指定されたtestsを実行し、doneを観測する。

実行中に成果境界を変える不足や矛盾が判明した場合、C41はTaskSpecを書き換えない。Plannerへ差し戻し、新しいidentityを作る。

## 評価計画

### 1. Planner単体

少なくとも次のcaseを、実装前に固定する。

1. 十分な依頼から、質問なしで正しいTaskSpecを作る。
2. repositoryで解決できる事実を、不必要に質問しない。
3. 成果を変える境界が不足する場合だけ、最小限の質問を返す。
4. 元の依頼よりscopeを広げない。
5. 元の依頼にないwrite、push、merge、deploy権限を追加しない。
6. 意味変更時にTaskSpec identityを更新する。

### 2. Planner + C41

同じ互換条件で次を確認する。

1. Plannerが生成したTaskSpecをC41が追加Runbookなしで実行できる。
2. 成果、範囲、validationが元の依頼と一致する。
3. 不要なAgent起動、重複read、同じ事実の再確認を増やさない。
4. TaskSpecの不足をC41が推測で補わない。
5. `quality_score`とall-agent `total_tokens`を保存する。

現在のTaskSpec注入済みC41結果は、executor経路の既存証拠として保持する。Planner経路の品質を示す証拠には読み替えない。

比較は、evaluation set revision、target repository ref、model、Agent環境、permission、fixture、executor parameter、反復条件、token accounting revisionが一致する結果に限定する。

## Phase 1の完了条件

Phase 1の設計完了は次の状態とする。

1. Plannerの入出力contractが固定されている。
2. 最小TaskSpecとauthorization bindingのschema案が固定されている。
3. repository解決とユーザー確認の境界が例付きで固定されている。
4. C41へのhandoffとidentity無効化規則が固定されている。
5. Planner単体とPlanner + C41の評価caseが、結果を見る前に固定されている。
6. Phase 2のRunbook要件がPhase 1へ混入していない。

この完了は、candidateの実装、評価成功、release承認、THE-CAPTIONへの反映を意味しない。それぞれ別の変更単位と判断gateで扱う。

## 停止条件

次の場合はPhase 1の実装へ進まず、計画を見直す。

- 元の依頼と生成TaskSpecの間で、権限の由来を追跡できない。
- Plannerがscopeまたはdoneを推測で作らなければTaskSpecを完成できない。
- 対象caseを実行するために動的Runbookが必須である。
- Plannerの正しさとC41の実行結果を分離して評価できない。
- 評価基盤v3の固定Layer、KPI、出力schemaを変更しなければ評価できない。

## Phase 2へ送る事項

Phase 2では、TaskSpecだけでは実行構成を固定できないtaskに限り、Runbookを動的AGENTS.mdとして生成する経路を検討する。

RunbookはTaskSpecを言い換える文書にしない。worker routing、独立audit、review、recovery、tool policyなど、そのtaskで追加が必要な実行制御の差分だけを持たせる。

Phase 2は、必要条件、生成責務、authority、評価costを別に定義し、独立した設計承認を受ける。

## 根拠となる既存資料

この計画は、次の既存資料の区別を維持する。

- `ai-development-research: docs/deliverable.md` — TaskSpecは最小で曖昧さのない意味を固定し、外部作用の権限を別に扱う。
- `ai-development-research: records/archive/judgements/EXTERNAL-005_minimum_execution_configuration_skeleton_2026-07-08.md` — canonical rulebook、Agent固有summary、tool policyを分離する初期構想。
- `ai-development-research: records/archive/judgements/EXTERNAL-007_canonical_rulebook_to_runbook_generation_rule_judgement_2026-07-08.md` — TaskSpecの6つのcore意味、条件付き情報、routing、停止、test選択の候補。
- `ai-development-research: records/archive/design_prep/small_implementation_execution_configuration_candidate.md` — authorizationを別のmodel-visible recordへ結び付ける案。
- `ai-development-research: records/archive/execution-configurations/runbook_generation_prompt_candidate.md` — 完成済みTaskSpecからRunbookを生成する案。自然言語からTaskSpecを作るPlannerではない。
- [`Candidate41 release`](../prompts/releases/the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1/README.md) — 現在のC41 release identityと制御内容。
- [`Evaluation runner`](../scripts/run_codex_evaluation.py) — 現在の評価がTaskSpecを事前注入する経路であることの実装上の根拠。

## 現在の状態

この文書はPhase 1の計画である。

Plannerの実装、candidate identity、評価profile、評価実行、release判断、THE-CAPTIONへのprojectionはまだ行わない。
