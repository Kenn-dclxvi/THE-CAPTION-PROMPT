# Repository instructions

## Scope

このリポジトリはTHE-CAPTION向けプロンプトの構築、比較、評価、release準備を扱う。THE-CAPTION本体のruntime変更は、このリポジトリの通常作業範囲に含めない。

## Working rules

- 文書は原則として日本語で記述する。schema名、path、status、commandは再現性のため英語表記を使ってよい。
- artifactが存在することと、評価済み、採用済み、本体反映済みであることを混同しない。
- baseline、candidate、releaseを別pathで管理し、in-placeで上書きしない。
- 比較ではtarget repository ref、prompt identity、model、Agent環境、TaskSpec、permission、fixture、反復条件を固定する。
- model-visible入力とoracle、grader、expected resultなどのmodel-invisible情報を分離する。
- 単一caseや少数反復の結果を一般化しない。観測範囲と未解決事項を明記する。
- THE-CAPTION本体への書き込み、push、PR、merge、runtime有効化は、明示的に依頼された別作業として扱う。
- secret、credential、非公開の生run log、一時worktreeをcommitしない。

## Evaluation foundation v2

- 評価基盤の目的は、固定条件下で2つのprompt setを比較し、判断材料となる情報を提供することに限定する。promptの作成、改善方法の提案、優劣判定、採用、release判断、本体反映を評価基盤へ持ち込まない。
- A / Bは比較条件のlabelであり、順位、baseline / candidateの固定的な役割、採用状態を表さない。
- 評価基盤が扱うKPIは`quality_score`、`total_tokens`、`elapsed_seconds`の3つだけとする。A / Bそれぞれの値と`B - A`差分を出力するが、KPIへ優先順位や閾値を設定せず、`winner`、改善・悪化を出力しない。
- `quality_score`はcaseごとの成果全体を0〜4で採点して算出する。細かな観点分解、重み付け、機械的な合否判定を標準化しない。quality raterはscoreと短い事実根拠だけを返し、A / Bの選択や改善提案を行わない。
- 反復回数`N`は任意の正の整数とし、AとBで同じcaseと`1..N`を揃える。単一caseや少数反復の結果を評価範囲外へ一般化しない。
- Layerは`Evaluation set`、`Execution`、`Quality rating`、`KPI comparison`の4つに限定する。各Layerは自分の出力だけを作り、前段のartifactを変更せず、後段の責務へ越境しない。評価基盤はA / Bの反復別KPI、中央値、数値差、除外attemptの比較情報で終了する。
- 可変のtask、model、Agent、permission、executor parameterはEvaluation set capsuleまたはRun capsuleへ格納する。基盤はLayer接続に必要な最小binding以外をopaqueに扱い、parameter追加をworkflow変更にしない。
- tokenについて評価基盤が扱う値は`total_tokens`だけとする。内訳や詳細分析は`layer2/extensions/<run_id>/<feature>/`配下の独立機能として実装し、quality ratingやKPI comparisonへ入力しない。
- v1の`winner`、`kpi_order`、`decision.json`を含む既存result、profile、cycleは履歴として保持し、v2の現行出力へ読み替えたりin-placeで変更したりしない。
- `docs/prompt-comparison-workflow.md`、`docs/evaluation-loop-manual.md`、`scripts/evaluation_loop.py`を評価基盤v2の固定点とする。再現できる不具合または明示的な要件変更がない限り変更しない。詳細化や追加分析は、まず配下機能で実現し、基盤のLayer、KPI、出力schemaを拡張しない。

## Change discipline

- 1つの変更では1つの判断またはartifact単位を扱う。
- prompt変更と評価条件変更を同じ比較単位へ混ぜない。
- 結果を見た後に評価基準を変更する場合は、新しいprofile revisionとして扱う。
- release候補には由来、対象identity、評価結果、未解決risk、承認状態を含める。
