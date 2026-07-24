# Repository instructions

## Scope

このリポジトリはTHE-CAPTION向けプロンプトの構築、比較、評価、release準備を扱う。THE-CAPTION本体のruntime変更は、このリポジトリの通常作業範囲に含めない。

## Working rules

- 文書は原則として日本語で記述する。schema名、path、status、commandは再現性のため英語表記を使ってよい。専門用語、短縮語は注釈付きで許可。
- artifactが存在することと、評価済み、採用済み、本体反映済みであることを混同しない。
- baseline、candidate、releaseを別pathで管理し、in-placeで上書きしない。
- 比較ではtarget repository ref、prompt identity、model、Agent環境、TaskSpec、permission、fixture、反復条件を固定する。
- model-visible入力とoracle、grader、expected resultなどのmodel-invisible情報を分離する。
- 単一caseや少数反復の結果を一般化しない。観測範囲と未解決事項を明記する。
- THE-CAPTION本体への書き込み、push、PR、merge、runtime有効化は、明示的に依頼された別作業として扱う。
- secret、credential、非公開の生run log、一時worktreeをcommitしない。

## Agent execution discipline

このリポジトリで作業するagentは、Candidate71（`the-caption-3ce91a4-validation-closure`）で本体へ採用されたvalidation-closure制御をrepository内作業へ適用し、次の規律で動く。制御原文は`prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/files/AGENTS.md`を正本とする。

### 実行権限と情報取得

- ユーザーの依頼（TaskSpec）を唯一のauthorityとして受け取り、成果の生成、検証、報告に責任を持つ。
- 判断に必要な情報はJITで取得し、必要になった時点で関連文書と一次資料を参照する。憶測で補完しない。

### 委譲

- 単一のoperationで完了する作業は、agent自身で実行する。
- 依頼が独立した別作業を明示的に指定した場合だけ、そのoperationを委譲する。委譲した場合も、最終成果の受領、検証、報告はagentが担う。

### Validation closure

- 文書、評価成果物、bundle、codeを変更した後は、依頼と適用されるrepository規則が要求する検証（tests、リンクと数値の実測確認、schema検証など）の全体集合を一度に発行する。
- 全ての検証結果を受領してから、一度だけ成否を判断する。
- 成否が確定した後は、根拠のない追加の読み取りや再確認を行わない。
- 検証していない結果を、完了または成功として報告しない。tool callの適用可否は実際の結果で確認し、結果を予測で語らない。

### 禁止

- 依頼が要求しない成果物の変更や、既存artifactと周辺経路の破壊を行わない。
- 確定していない前提を推測で埋めない。件数、状態、数値などrepositoryから確定できる事実は実測し、確定できない値は一度確認して停止する。

## Evaluation foundation v3

- 評価基盤の目的は、1つのprompt setを固定条件で実行した結果を独立して保存し、互換条件を満たす任意個の保存結果から判断材料となる比較viewを作ることに限定する。promptの作成、改善方法の提案、優劣判定、採用、release判断、本体反映を評価基盤へ持ち込まない。
- 一次結果は、prompt set名に加えてrevisionまたはbundle hashを含むimmutableな`prompt_set_identity`へ結び付ける。固定A / B pairやcondition labelを保存identityとして要求しない。
- 比較可能な結果は、evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件が一致するものに限定する。異なる条件を暗黙に混ぜない。
- 評価基盤が扱うKPIは`quality_score`、`total_tokens`、`elapsed_seconds`の3つだけとする。`total_tokens`はroot agentと、そのrunから起動された全SA sessionの最終token usageを合算したall-agent値とする。prompt setごとの値、中央値、明示した2 result間の数値差を出力できるが、KPIへ優先順位や閾値を設定せず、`winner`、改善・悪化を出力しない。
- `quality_score`はcaseごとの成果全体を0〜4で採点して算出する。細かな観点分解、重み付け、機械的な合否判定を標準化しない。quality raterはscoreと短い事実根拠だけを返し、prompt setの選択や改善提案を行わない。
- 反復回数`N`は任意の正の整数とし、各prompt set resultで同じcaseと`1..N`を揃える。単一caseや少数反復の結果を評価範囲外へ一般化しない。
- Layerは`Evaluation set`、`Execution`、`Quality rating`、`KPI comparison`の4つに限定する。各Layerは自分の出力だけを作り、前段のartifactを変更せず、後段の責務へ越境しない。Layer 4はprompt set別のappend-only resultと、保存済みresultから生成する比較viewで終了する。
- 可変のtask、model、Agent、permission、executor parameterはEvaluation set capsuleまたはRun capsuleへ格納する。基盤はLayer接続に必要な最小binding以外をopaqueに扱い、parameter追加をworkflow変更にしない。
- tokenについて評価基盤が扱う値はall-agentの`total_tokens`だけとする。root / SA別内訳やsession情報は`layer2/extensions/<run_id>/<feature>/`へ保存し、quality ratingやKPI comparisonへ入力しない。全sessionの最終usageを完全に取得できないrunはtoken値を推定せず、外部計測失敗として除外する。token accounting revisionが異なるresultを互換比較へ混ぜない。
- v1の`winner`、`kpi_order`、`decision.json`とv2の固定A / B `comparison.json`を含む既存result、profile、cycleは履歴として保持し、v3の現行出力へ読み替えたりin-placeで変更したりしない。
- v3でroot agentだけを`total_tokens`として保存した`prompt-set-result/v1`も履歴として保持する。all-agentへ再集計した結果は`prompt-set-result/v2`としてappend-onlyで追加し、元resultとの由来とtoken accounting revisionを明示する。
- `docs/prompt-comparison-workflow.md`、`docs/evaluation-loop-manual.md`、`scripts/evaluation_loop.py`を評価基盤v3の固定点とする。再現できる不具合または明示的な要件変更がない限り変更しない。詳細化や追加分析は、まず配下機能で実現し、基盤のLayer、KPI、出力schemaを拡張しない。

## Prompt control design

- prompt制御の追加、置換、削除では、`docs/prompt-control-design-principles.md`を検討原則の正本とする。
- 新しいcandidateを作る前に、control-freeなrepository条件で成立する最短正常経路、保存済みtraceで確認した一つの誤経路、既存のTaskSpec・repository authority・repository stateだけでは防げない理由を記録する。
- 制御は、追加する読解・判断・確認costより多くの探索、context継承、再読、再試行、手戻りを消す場合に追加する。消す具体的な判断点またはcontext伝播を示せないpredicateは追加しない。
- 一つのlabelには一つの不変条件だけを持たせる。既存labelへの条件追加より、重複predicateの置換、統合、削除を優先する。
- 正しい成果が既に存在する最短経路を、追加のowner探索、evidence再取得、identity照合で阻害しない。境界制御、terminal state、context流入、方法制約を別の変更軸として扱う。
- 効果は同一互換条件の成果品質、score分布、all-agent `total_tokens`、case別token、tool call、model step、worker routingで確認する。中央値の低下やprompt byte数の縮小だけを効率化と判断しない。
- `docs/prompt-control-design-principles.md`のcandidate作成前gateが未定義なら、candidate bundleと評価profileを先に作らない。

## Change discipline

- 1つの変更では1つの判断またはartifact単位を扱う。
- prompt変更と評価条件変更を同じ比較単位へ混ぜない。
- 結果を見た後に評価基準を変更する場合は、新しいprofile revisionとして扱う。
- release候補には由来、対象identity、評価結果、未解決risk、承認状態を含める。
