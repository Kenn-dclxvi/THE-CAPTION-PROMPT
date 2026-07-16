# エージェントオーケストレーションプロセス

## 目的
この文書は、任意のリポジトリに適用できる AI 駆動開発プロセスの運用仕様を定義する。

対象は、指示書作成、親エージェント運用、実装主体の選択、監査SA、レビューSAの関係である。

この文書はアプリケーション仕様ではなく、開発環境における AI エージェント運用プロセスの仕様である。

## 位置づけ
この文書は `docs/` 配下に置く。

関連文書:

```text
AGENTS.md
prompts/plan.md
prompts/audit.md
prompts/review.md
docs/prompt-guide.md
```

役割は以下とする。

```text
AGENTS.md
  親エージェント用のオーケストレーション制御。

prompts/plan.md
  指示書作成用の自己完結プロンプト。

prompts/audit.md
  監査SA用の自己完結プロンプト。

prompts/review.md
  レビューSA用の自己完結プロンプト。

docs/prompt-guide.md
  AGENTS.md とロールプロンプトの考え方を説明するガイド。

docs/orchestration-process.md
  指示書作成 / 親エージェント / 実装主体 / 各SAの運用仕様。
```

## 基本方針
AI 駆動開発プロセスは、以下の責務分離を前提にする。

```text
指示書作成
  ユーザー依頼を整理し、実装指示書を作成する。

親エージェント
  承認済み実装指示書を理解し、実装主体を選択して実行状況を管理する。

実装主体
  親が直接実装するか、全部または一部をSAへ委任する。選択はモデル判断とし、専用の実装ロールを要求しない。

監査SA
  非破壊で契約準拠の判定を行う。

レビューSA
  PRレビュー相当の品質確認を非破壊で行う。
```

親エージェントは、承認済み実装指示書または明示された作業単位化条件がある場合に限り、実装へ進む。依頼を `target / scope / done / tests / stop` に分解できない場合、または分解に AI側の補完が必要な場合は停止する。固定後の実装主体は、親直接、SA委任、分担からモデルが選ぶ。SA委任は必須でも禁止でもなく、実装主体の選択によって作業単位、permission、routing、停止条件を変更しない。

ユーザーは、草案が明示条件を満たすなら追加確認なしで作業単位化して実行してよい、という条件付き事前承認を先に宣言できる。条件付き事前承認の成立要件・ID照合・除外操作は §条件付き事前承認テンプレート に従う。

条件付き事前承認テンプレートと既定テスト定義は、明示済み条件をIDで参照するための定義である。IDは境界を生成せず、未定義の対象・範囲・完了条件・品質基準・実行許可・テスト条件を補完しない。

親エージェントは、固定した作業単位の実装・修正・テスト実行を直接行うことも、全部または一部をSAへ委任することもできる。監査・selected routeが要求する PRレビュー相当の品質確認は直接行わない。指示書作成も直接行わず、ユーザーが指示書作成を明示依頼した場合、または実装・変更の意図がありながら作業単位化に必要な対象・範囲・完了条件・品質基準・実行許可を推定なしで確定できない場合に、プランSAを起動する。

## 条件付き事前承認テンプレート
条件付き事前承認テンプレートは、ユーザー入力、承認済み実装指示書、または明示された参照文書で定義された場合だけ使う。

テンプレートは以下を含む。

- `template_id`
- 条件
- 対象
- 範囲
- 完了条件
- 品質基準
- 実行許可
- 除外操作

条件・対象・範囲・完了条件・品質基準・実行許可・除外操作は、値そのもの、閉じた列挙、または推定なしで照合できる条件として明示されている必要がある。

条件付き事前承認は、条件・対象・範囲・完了条件・品質基準・実行許可が明示され、条件充足を推定で判断せず確認できる場合だけ作業単位化条件として扱う。AI は条件・対象・範囲・完了条件・品質基準・実行許可を補完してはならない。条件充足を推定で判断する必要がある場合は停止する。

親エージェントは、テンプレートIDとユーザー入力または草案の該当内容を照合する。照合結果が一意であり、かつ全項目が満たされる場合だけ、作業単位化条件として扱う。複数候補、未定義項目、曖昧条件、条件充足に推定が必要な項目がある場合は停止する。

草案にテンプレートIDが含まれていても、草案自体は実行許可ではない。テンプレートIDは、親エージェントが条件付き事前承認との照合に使う情報であり、承認・実装許可を生成しない。

`commit` / `push` / `deploy` / 外部送信は、テンプレートの除外操作に含める。これらは別途明示許可がある場合だけ実行許可として扱う。

## 既定テスト定義
既定テスト定義は、ユーザー入力、承認済み実装指示書、または明示された参照文書で定義された場合だけ使う。

既定テスト定義は以下を含む。

- `default_test_id`
- 適用条件
- テスト条件
- `なし（根拠）` を許可する条件

テスト条件は、実行するテストコマンド、または `なし（根拠）` として明示する。コード変更を含む作業単位ではテストコマンド必須とし、`なし（根拠）` を使ってはならない。

親エージェントは、既定テストIDと適用条件を推定なしで照合する。照合結果が一意であり、かつ適用条件が満たされる場合だけ、テスト条件を展開して `tests` に入れる。既定テストIDだけがあり、展開済みのテストコマンドまたは `なし（根拠）` を確定できない場合は停止する。

実装主体が使う `tests` は、既定テスト定義から展開済みのテストコマンドまたは `なし（根拠）` とする。親が直接実装する場合も委任されたSAも既定テストを選ばない。

## Phase result projection

workspace上の成果物と、工程間でmodelへ渡すresultを分ける。実装、required machine validation、監査、レビュー、再修正の各工程は、自工程の成果物をworkspace上で作成・確認し、次工程へは自工程による差分だけを `phase_result` として渡す。成果物の全内容、既読仕様、探索経緯、判断過程を工程間で再掲しない。

`phase_result` は工程に応じて次のfieldだけを持つ。

| phase | model-visible result |
|---|---|
| implementation / rework | `changed_paths`、作業単位に限定した`scoped_diff`、`unresolved` |
| required machine validation | `command`、`exit_status`、pass / fail / skip件数、done判定に必要なwarning、`projection` |
| audit | 停止指摘 / 任意指摘 / 範囲外指摘、`unresolved` |
| review | 重大指摘 / 改善指摘 / 補足 / 範囲外指摘、`unresolved` |

`scoped_diff` は変更後file全文の代替であり、変更pathの差分だけを含む。次工程が追加確認を必要とする場合も、まずdiffの該当hunkと関連仕様の必要箇所から確認し、変更後file全文、変更前file全文、既確認箇所へ無条件に広げない。監査SAとレビューSAへは、従来どおりTaskSpec、scoped diff、validation summary、関連仕様の必要箇所を渡し、実装経緯と親の事前評価を渡さない。

required commandはprogram、arguments、実行順、pass condition、再試行条件、permissionを変更せず、一度だけ実行する。raw stdout / stderrはmodel-visible resultへ入る前にexecutorのoutput制御、shell capture、または同等手段で上表のvalidation resultへ変換する。full outputをmodelへ一度表示してから短く言い換えることはprojectionではない。pipeの打ち切り、出力抑制による成功扱い、exit statusの置換を行わない。

成功時はraw outputを次工程へ渡さない。失敗時はexit status、failed item、最小の原因箇所だけを最初に返し、原因を承認済み範囲内に特定できない場合だけ参照範囲を段階的に広げる。完全evidenceの保持が必要な場合はexecutorが利用可能な保持手段を選べるが、保持場所をprompt contractとして固定せず、secret、credential、非公開logをcommitしない。

projectionを適用できない場合はrequired commandを通常実行し、停止理由にせず、validationの`phase_result`へ `projection: unavailable` と具体的理由を残す。projectionの適用可否はtest、validation、permission、retry、cleanup、drift条件を変更しない。親直接 / SA委任 / 分担のいずれでも同じresult境界を使う。

## 作業単位化判定フロー
親エージェントは、以下の順序で作業単位化を判断する。

1. 承認済み実装指示書または作業単位化対象のユーザー入力を確認する。
2. 条件付き事前承認テンプレートを使う場合は、テンプレートID、条件、対象、範囲、完了条件、品質基準、実行許可、除外操作を §条件付き事前承認テンプレート に従って照合する。
3. 草案を入力に含める場合は、草案が実行許可ではないことを維持し、条件付き事前承認または別途明示許可との照合対象としてだけ扱う。
4. `target / scope / done` を明示項目だけで整理できるか確認する。
5. 明示テスト条件または既定テスト定義を確認し、既定テスト定義を使う場合は §既定テスト定義 に従って既定テストIDと適用条件を照合して `tests` に展開する。
6. コード変更を含む作業単位で `tests` がテストコマンドにならない場合は停止する。テストコマンド必須・`なし（根拠）` 可否は §既定テスト定義 に従う。
7. `target / scope / done / tests / stop` のいずれかに AI側の補完が必要な場合は停止する。
8. すべてを推定なしで整理できる場合だけ実装境界を固定し、実装主体を選ぶ。

作業単位化可否は `可否 / 理由 / 草案または不足項目` の形式で返す。

## 実装後確認routing
実装作業単位では、親エージェントが実装開始前に実装後確認経路を一つ固定する。実装主体の選択、required machine validation、permission、変更範囲はこのroutingで変更しない。

実装後確認経路は次の4つとする。

| route | 起動する独立worker | 完了に必要な確認 |
|---|---|---|
| `none` | なし | machine evidenceとdrift確認 |
| `audit` | 監査SA | 契約、authority、scope、invariantの独立照合 |
| `review` | レビューSA | runtime correctness、利用者影響、state safetyの独立品質確認 |
| `audit+review` | 監査SAの後にレビューSA | 契約riskとquality riskの両方の確認 |

`review` は単独で起動できる。`audit+review` の場合だけ、監査SAの停止指摘0件をレビューSAの起動条件とする。

### Routing input
親エージェントは実装開始前に次をTaskSpecへ固定する。

| input | 値 |
|---|---|
| `task_kind` | `implementation` / `boundary_disposition` / `non_destructive_review` |
| `change_class` | `python` / `node` / `test` / `shell` / `docs` / `ai_control` / `dependency` / `config` / `mixed` |
| `machine_coverage` | `direct` / `partial` / `not_applicable` |
| `contract_risk_flags` | C1からC4の集合、または空集合 |
| `quality_risk_flags` | Q1からQ5の集合、または空集合 |
| `explicit_independent_check` | `none` / `audit` / `review` / `audit+review` |
| criterion | routeが要求する各独立workerの固定criterion。routeが `none` なら不要 |
| owner | 監査SAには `independent_contract_check`、レビューSAには `independent_quality_check`。`audit+review` では両方を固定し、routeが `none` なら不要 |

`line_count` と単純な変更file数はrouting inputにしない。一行変更でもrisk flagがあれば独立workerを起動し、複数fileでもrisk flagがなく `machine_coverage=direct` なら `none` を選択できる。

`change_class` は、TaskSpecでdoneのために変更を予定するartifactのclassから固定する。read-onlyの確認対象、required validationが読むtest、変更可能だが変更を予定しないallowed pathはclassへ含めない。複数classのartifactを変更予定にする場合だけ `mixed` とする。実装後の実diffで予定外のclass変更が確認された場合は、後述の実装後escalationに従う。

### Risk flag
contract risk flagは次の4つとする。

| flag | 条件 |
|---|---|
| `C1_authority_permission` | authority、permission、許可operation、scope boundaryを変更または解釈する |
| `C2_public_contract_invariant` | public interface、schema、CLI routing、dependency provenance、paired invariantを変更する |
| `C3_test_validation_contract` | test、assertion、expected result、またはrequired gateのcommand / scope / pass conditionそのものを追加・変更・復元する。またはTaskSpecがtest contractの非弱体化を独立criterionとして固定し、ownerを `independent_contract_check` とする |
| `C4_reference_control_consistency` | docs、AI制御文書、正規command、referenceとsourceの整合を扱う |

contract risk flagが一つ以上あれば、routeは少なくとも `audit` を含む。

testをrequired validationとして実行するだけではC3を付与しない。allowed pathにtestが含まれること、test変更を一般的に禁止すること、skip / xfail / assertion緩和を禁止すること、focused / full gateをrequiredとすることも、それだけではC3の根拠にならない。planned changeがproduction sourceだけで、TaskSpecの明示的な `non_machine_risk=none` またはquality risk ownerと矛盾しない場合、validationにtestを使ってもC3は空のままとする。

quality risk flagは次の5つとする。

| flag | 条件 |
|---|---|
| `Q1_high_impact_behavior` | security、credential、production、外部送信、金額計算、report内容、データ破壊へ影響し得る |
| `Q2_state_failure_recovery` | persistence、atomicity、cleanup、failure path、concurrency、retry、state transitionを変更する |
| `Q3_cross_layer_interface` | 複数layer、caller / callee、public interfaceを跨ぐruntime behaviorを変更する |
| `Q4_user_visible_uncovered` | user-visible behaviorを変更し、required machine gateがその意味を直接検証しない |
| `Q5_machine_coverage_gap` | implementation taskだが、doneの中核behaviorに対するmachine coverageが `partial` または存在しない |

quality risk flagが一つ以上あれば、routeは少なくとも `review` を含む。

### Machine coverage
`machine_coverage` は次の基準で決める。

| 値 | 条件 |
|---|---|
| `direct` | required machine commandが変更対象の中核behaviorと主要regressionを直接検証する |
| `partial` | syntax、build、広いtestは通るが、変更した意味またはfailure pathを直接検証しない |
| `not_applicable` | boundary disposition、read-only review、docsなど、実行可能なmachine behavior gateを要求しない |

runtime behaviorを変更する `python`、`node`、`shell`、`dependency`、`config`、またはそれらを含む `mixed` で `machine_coverage=partial` または `not_applicable` の場合はQ5を自動付与する。`docs` と `ai_control` は `not_applicable` を認めるが、change classの既定flagによるauditを省略しない。

### Route決定
boundary / permissionが未確定または否定されている場合は、routingで補完せず実装開始前に停止する。`task_kind=boundary_disposition` は実装後workerが存在しないため `none` とする。`task_kind=non_destructive_review` はtask自体がreviewであるため `none` とし、独立したsecond opinionが明示要求された場合だけ `explicit_independent_check=review` を認める。

implementation taskはmachine coverageからQ5を導出し、次の表でrouteを決める。

| contract risk | quality risk | route |
|---|---|---|
| なし | なし | `none` |
| あり | なし | `audit` |
| なし | あり | `review` |
| あり | あり | `audit+review` |

`explicit_independent_check` は表のrouteと同じ方向または強い方向へ上書きできるが、既存riskが要求するaudit / reviewを削除できない。競合は boundary / permission、`task_kind`、`explicit_independent_check`、contract risk、quality riskとmachine coverage gap、change classの既定flagの順で解決する。複数条件は和集合を取り、`audit+review` を上限とする。

change classの既定flagは次のとおりとする。

| change class | 既定flag |
|---|---|
| `python` | なし。behaviorに応じてQ1からQ5を付与する |
| `node` | なし。user-visible意味をbuild / lintが直接検証しない場合はQ4またはQ5 |
| `test` | C3。test artifact自体を変更予定にする場合に限る |
| `shell` | C2 |
| `docs` | C4 |
| `ai_control` | C1とC4 |
| `dependency` | C2 |
| `config` | なし。permission、external side effect、public contractに応じてC1、C2、Q1を付与する |
| `mixed` | 変更予定artifactに含まれるclassとrisk flagの和集合。read-only確認対象とvalidation artifactは含めない |

一行または単一fileという事実だけでは `none` にしない。`machine_coverage=direct`、contract / quality risk flagが空、authority、permission、test、schema、dependency、CLI / public interfaceを変更せず、production、外部送信、security、credential、金額、永続化、failure recovery、user-visible未検証behaviorへ影響せず、required validation成功と許可外driftなしを確認できる場合だけ `none` を選択できる。

### 実装後の実行
実装開始前にrouteを固定した後、実際のdiffまたはmachine resultから定義済みrisk flagが新たに確認された場合は、`none` から `audit` / `review` / `audit+review`、または `audit` / `review` から `audit+review` へだけescalateできる。特にplanned changeへ含めなかったtest artifact、assertion、expected result、required gateのcommand / scope / pass conditionを実際に変更した場合はC3を追加する。実装後にriskを再解釈してworkerを削除してはならない。escalate時は追加したflag、根拠artifact、criterion、ownerをrouting evidenceへ残す。

required machine validationがfailedまたはunavailableの場合はaudit / reviewを起動せず停止する。non-machine確認でmachine failureを代替しない。required machine validation成功後は次の順で進める。

| route | sequence |
|---|---|
| `none` | 実装 → required machine validation → drift確認 → 親の完了判定 |
| `audit` | 実装 → required machine validation → 監査SA → drift確認 → 親の完了判定 |
| `review` | 実装 → required machine validation → レビューSA → drift確認 → 親の完了判定 |
| `audit+review` | 実装 → required machine validation → 監査SA停止指摘0件 → レビューSA → drift確認 → 親の完了判定 |

監査SAまたはレビューSAの指摘後の自動修正は §自動修正ループ に従う。routeが要求しない確認を親エージェントが代行してはならない。

親エージェントは最終結果へ、実装主体（親直接 / SA委任 / 分担）、selected route、`task_kind`、`change_class`、`machine_coverage`、contract / quality risk flags、起動したSAと起動しなかったSA、`none` または `not_applicable` の根拠、実装後escalationの有無と根拠、required machine result、final drift identityを残す。各工程のphase resultを統合し、変更後file全文、成功log全文、前工程の探索経緯を再掲しない。

## SA利用ケース
親エージェントが SAを起動するのは以下に限定する。

| # | ケース | 目的 |
|---|---|---|
| A | プロンプト・コマンドの実行確認 | 副作用を隔離し、親のコンテキストを汚染しない |
| B | 独立した作業単位の任意委任・パラレル実行 | 固定した作業単位の全部または一部を委任し、独立性基準を満たす場合は同時進行する |
| C | 事前知識なし監査 | selected routeが `audit` を含む場合に、文脈汚染のない視点で差分・仕様を照合する |
| D | 製造→独立確認→修正 自動ループ | selected routeが要求する停止指摘 / 重大指摘が0件になるまで反復改善する |
| E | 指示書草案作成 | 指示書作成の明示依頼時、または実装・変更の意図がありながら境界未確定のとき草案を作る |
| F | PRレビュー相当の品質確認 | selected routeが `review` を含む場合に、品質・設計・テスト妥当性を非破壊で確認する |

ケースEは、次のいずれかで起動する。(1) ユーザーが指示書作成を明示依頼した。(2) ユーザー入力が実装・変更の意図を含み、作業単位化に必要な対象・範囲・完了条件・品質基準・実行許可を推定なしで確定できない。非破壊レビュー依頼、純粋な質問、既に承認済み実装指示書がある場合、対象・範囲・完了条件・品質基準・実行許可を推定なしで確定でき直接作業単位化できる場合は起動しない。

ケースEの起動は草案作成までであり、実行境界を生成しない。草案は実行許可ではなく、プランSA自身も補完禁止に従い、対象・範囲・完了条件・品質基準・実行許可を推定なしで確定できない場合は不足項目を返す。親は草案から実装へ自動で進まず、実行は明示許可または作業単位化条件に従う。条件付き事前承認の除外操作（`commit` / `push` / `deploy` / 外部送信）は §条件付き事前承認テンプレート に従い、草案では実行許可扱いにしない。

ケースCとケースFは §実装後確認routing でselected routeに含まれる場合だけ起動する。同じ作業単位で同種workerを重複起動しない。

## パラレル起動の独立性基準
独立性基準は、変更を伴う並列（ケースB）に適用する。変更を伴う並列は以下をすべて満たす場合のみ可とする。

1. 変更対象ファイルに重複がない。
2. 実行順序の依存関係がない。
3. 共有リソースへのアクセスが重複しない。

途中で独立性が崩れた場合は後発SAを停止し、先発SA完了後に直列で再起動する。

## サブエージェント起動
親エージェントは、SA起動時に、そのSAに対応するロールプロンプトを明示的に渡す。

```text
プランSA: prompts/plan.md
監査SA: prompts/audit.md
レビューSA: prompts/review.md
```

実装目的のSA委任には専用ロールプロンプトを要求しない。親は固定済みの作業単位と禁止操作を起動メッセージに明示し、委任されたSAはrouting、回数カウント、完了判定を変更しない。同じ作業単位の実装に参加した主体を、その作業単位の監査SAまたはレビューSAとして起動しない。

SAがリポジトリ上の `AGENTS.md` を自動読込する前提にしない。

SA起動時は、必要な情報を起動メッセージに含める。

- ロールプロンプトの本文または要約
- 承認済み実装指示書または作業指示一式（条件付き事前承認テンプレートから展開した条件、既定テスト定義から展開したテスト条件を使う場合はその展開済み条件を含む）
- `target / scope / done / tests / stop`
- 監査観点
- レビュー観点
- 禁止操作

## 各工程の確認範囲
実装主体は、明示されたテストコマンドが失敗した場合、既存ログ・テスト出力・関連ファイルを確認し、原因が承認済み範囲内に特定できた場合だけ最小修正する。原因が特定できない場合、または承認済み範囲外の場合は停止理由として返す。既定テスト定義から展開されたテスト条件は明示されたテスト条件として扱い、実装主体は既定テストを選ばない（§既定テスト定義）。

監査SAは、指示書または作業指示一式に含まれる条件付き事前承認テンプレートから展開された条件、既定テスト定義から展開されたテスト条件、テスト期待値変更、テスト条件未充足、完了条件の達成扱いが差分・テスト結果・関連仕様で支えられない完了偽装を照合し、契約違反を停止指摘にする。

監査SAは、テスト自体の改竄（reward hacking）を完了偽装と並ぶ一次照合に含める。`# noqa`・skip・xfail の追加、失敗パスの mock / stub での握りつぶし、assertion の緩和は、テスト結果を成果物として信頼できなくするため停止指摘とする。

レビューSAは、テストの実質性と周辺影響を確認する。assertion不在、常時pass、主要分岐未検証、過剰mock、失敗パスの握りつぶしはテスト妥当性リスクとして扱う。差分だけで影響判断できない場合は、変更関数・API・設定キーなどの呼び出し元 / 参照元を必要最小限で確認する。

## 指摘分類
監査SAは、停止指摘 / 任意指摘 / 範囲外指摘を使う。

- 停止指摘: 完了条件または品質基準を満たさないため、修正が必須。
- 任意指摘: 今回の完了を妨げない改善。修正は任意。
- 範囲外指摘: 今回の実装指示書の範囲外であり、今回の作業単位では扱わない。

レビューSAは、重大指摘 / 改善指摘 / 補足 / 範囲外指摘を使う。

- 重大指摘: 承認済み範囲内で、マージ前に直すべき明確な欠陥または高リスク。
- 改善指摘: 今回の完了条件を妨げない品質改善。
- 補足: 修正要求ではない判断メモ。
- 範囲外指摘: 承認済み範囲外、仕様拡張、別機能、任意リファクタ、設計変更要求。

レビューSAの改善指摘 / 補足 / 範囲外指摘は自動修正対象にしない。

## 親エージェント
親エージェントは、承認済み実装指示書または承認済み実装指示書と矛盾しない作業単位化対象の最新ユーザー入力を読み、実装主体と委任可否を判断し、必要なSAを起動し、結果を管理する。

親エージェントの希少資源は人員でなく、コンテキストと信頼である。中核責務は二つに収束する。

- コンテキスト経路設計: どの SA に何を見せ何を見せないかを起動時に決める。特に監査SAへ渡す情報は「指示書・差分・テスト結果・関連仕様」に限定し、実装経緯・事前評価を渡さない。レビューSAへも実装経緯・事前評価を渡さない。
- 関所強制: 証拠（差分・テスト結果・監査結果）が揃うまで次段へ通さない。停止指摘 / 重大指摘が残る間はマージへ進めない。

自動修正ループのループ制御・回数カウント・上限判定は親エージェントが管理する（§自動修正ループ）。

親エージェントは以下を行う。

- ユーザー指示を受ける。
- 依頼をまず委任可能か判断する。
- 明示された文書・差分の非破壊レビュー依頼を、明示対象に限り直接扱う。
- 条件付き事前承認テンプレートを使う場合は、テンプレートIDと全項目の条件充足を推定なしで照合する（§条件付き事前承認テンプレート）。
- 既定テスト定義を使う場合は、既定テストIDと適用条件を推定なしで照合し、テスト条件を展開する（§既定テスト定義）。
- `target / scope / done / tests / stop` に分解できる場合は実装境界を固定し、親直接 / SA委任 / 分担から実装主体を選んで実行する。
- 実装結果、required machine result、routing evidence、selected routeが要求する監査 / レビュー結果を受け取る。
- selected routeが監査SAを要求した場合は、停止指摘 / 任意指摘 / 範囲外指摘を確認する。
- selected routeが `audit+review` の場合は、監査SAの停止指摘0件後にレビューSAを起動する。
- selected routeがレビューSAを要求した場合は、重大指摘 / 改善指摘 / 補足 / 範囲外指摘を確認する。
- 停止指摘または重大指摘が承認済み範囲内で最小修正可能なら、作業単位化し直し、親が直接修正するか全部または一部をSAへ委任する（自動修正の可否条件は §自動修正ループ）。
- 任意指摘、改善指摘、補足、範囲外指摘を自動修正対象から外す。
- 原因不明または指示書不足を推定で埋めて継続しない。
- 範囲外、仕様変更、テスト期待値変更、原因不明の場合は停止する（§停止条件）。
- 条件付き事前承認の条件充足を推定で判断する必要がある場合は停止する。
- 条件付き事前承認テンプレートまたは既定テスト定義を一意に照合できない場合は停止する。
- 最終結果をユーザーへ返す。

## 自動修正ループ
製造とselected routeが要求する独立確認を行い、起動した監査SAの停止指摘または起動したレビューSAの重大指摘が残る場合だけ、修正とselected routeが要求する再確認を反復する。

初回実装は回数に含めず、自動再修正試行だけを最大5回まで数える。selected routeが要求した監査SAの停止指摘0件かつレビューSAの重大指摘0件になった時点で終了し、5回目の自動再修正後も停止指摘または重大指摘が残る場合は停止する。6回目の自動再修正は開始しない。

同一の停止指摘が連続2回再発した場合、または同一の重大指摘が連続2回再発した場合も停止する。

5回上限・同一指摘再発・停止条件で自動修正ループを止める場合、親エージェントはボトルネック、反復している指摘、次に人間が判断すべき点を3行以内でユーザーへ返す。

自動修正してよい条件は以下すべてを満たす場合だけである。

- 指摘が監査SAの停止指摘またはレビューSAの重大指摘である。
- 原因が承認済み実装指示書の対象内である。
- 修正対象が承認済み変更範囲内である。
- 修正が完了条件を変更しない。
- 修正が仕様を変更しない。
- 修正がテスト期待値を変更しない。
- 修正が便乗改善を含まない。
- 最小変更で対応できる。

## 停止条件
固定した作業単位の実行開始後は、完了条件を満たすか、固定した `stop` または本節の停止条件のいずれかが観測事実で成立するまで継続する。未完了の中間状態、操作への逡巡、手段の選好は停止条件ではない。

停止時は、該当する固定済み `stop` または本節の項目と、その成立を示す観測事実を返す。対応する停止条件がない場合は、許可範囲内の手段で完了条件へ進む。

親エージェントは、§自動修正ループ の可否条件を満たさない場合、および §作業単位化判定フロー の停止手順に該当する場合に停止する。ループ機構（回数上限・同一指摘の連続2回再発・5回目後の残存）の判定は §自動修正ループ に従う。

ループ機構以外で、親エージェントが自動修正ループを停止する場合は以下とする。

- 指摘が任意指摘である。
- 指摘が範囲外指摘である。
- レビューSAの指摘が改善指摘または補足である。
- 指摘対応に仕様変更が必要である。
- 指摘対応に変更範囲の拡張が必要である。
- 指摘対応に対象外ファイル変更が必要である。
- 指摘内容と実装指示書が矛盾している。
- 最小修正では対応できない。
- 原因を推定で決める必要がある。
- テスト期待値変更が必要である。
- プランSA、またはselected routeが要求する監査SA / レビューSAに必要なロールプロンプトを渡せない。
- 承認済み実装指示書がない。
- 対象・範囲・完了条件が未定義である。
- テスト条件が未定義で、テスト実行が必要である。
- 条件付き事前承認の条件充足を推定で判断する必要がある。
- 条件付き事前承認テンプレートまたは既定テスト定義を一意に照合できない。

## PR作成
親エージェントが PR を作成する場合は、以下に従う。

- PR のタイトル・本文・見出しは、対象リポジトリの言語規約に従う。
- 言語規約が未指定の場合は、ユーザーとの会話で使われている主要言語に合わせる。
- コマンド名、ログ、API名、ファイル名、ブランチ名、エラー本文などは原文のままでよい。
- PR テンプレートがある場合は、その構成に従う。

## 親の最終出力様式
親エージェントは、最終結果を以下の様式でユーザーへ返す。

- 結論先出しで返す。
- 各工程のphase resultから、変更pathとscoped diff、required machine validation summary、selected routeが要求した監査 / レビュー結果、routing evidence、停止指摘 / 重大指摘の有無、自動再修正回数、未解決項目、停止理由を返す。変更後file全文、成功log全文、既読仕様、探索経緯は返さない。
- 自動修正ループを打ち切る場合は §自動修正ループ の様式（ボトルネック / 反復指摘 / 次に人間が判断すべき点・3行以内）で返す。

## 完了条件
このプロセス仕様は、本文ルールの再掲による自己検査であり、新規ルールを足さない。以下を各節の成立条件への参照として満たすとき有効である。

- 指示書作成が実装指示書を作り、親エージェントが承認済み実装指示書を管理し、固定した作業単位ごとに実装主体を選ぶ（§基本方針・§親エージェント）。
- 親エージェントが §SA利用ケース 以外で SAを起動しない。
- 実装目的のSA委任は固定した作業単位に従い、監査SAが `prompts/audit.md`、レビューSAが `prompts/review.md` に従う（§サブエージェント起動）。
- 監査SAへ渡す情報が「指示書・差分・テスト結果・関連仕様」に限定され、レビューSAへ渡す情報が実装経緯・事前評価を含まない（§親エージェント）。
- 監査SAがテスト改竄（reward hacking）を完了偽装と並ぶ一次照合に含める（§各工程の確認範囲）。
- 実装開始前にrouting inputとselected routeが固定され、required machine validation成功後にselected routeが要求する独立workerだけが起動される（§実装後確認routing・§親エージェント）。
- phase result projectionが成果物と工程間resultを分け、required command、pass condition、permission、retry、cleanup、drift条件を変更せず、projection不能時は通常実行して理由を残す（§Phase result projection）。
- `review` ではレビューSAが単独起動でき、`audit+review` では監査SAの停止指摘0件後にレビューSAが起動される（§実装後確認routing・§親エージェント）。
- SAが `AGENTS.md` 実ファイルを自動読込する前提にせず、ロールプロンプトと禁止操作が起動メッセージで明示される（§サブエージェント起動）。
- 監査SAの停止指摘とレビューSAの重大指摘のみが範囲内自動修正対象になり、自動ループのループ制御・回数カウント・上限判定は親エージェントが管理する（§自動修正ループ・§親エージェント）。
- 条件付き事前承認が、明示条件を満たすことを推定なしで確認できる場合だけ作業単位化条件として扱われ、条件付き事前承認テンプレートと既定テスト定義は、IDと展開条件を推定なしで照合できる場合だけ使われる（§条件付き事前承認テンプレート・§既定テスト定義）。
- コード変更を含む作業単位ではテストコマンド必須である（§既定テスト定義）。
- 停止条件に該当した場合は停止する（§停止条件・§自動修正ループ）。

## 制約
このプロセスは、プロンプト駆動の責務分離である。

以下は保証しない。

- SAが起動時に `AGENTS.md` 実ファイルを自動読込すること（§サブエージェント起動）。
- SAがロールプロンプト実ファイルを自動読込すること。
- 親直接 / SA委任 / 分担の選択をツールレベルで強制すること。
- 実行権限のハード分離。
- SA起動仕様そのものの変更。
