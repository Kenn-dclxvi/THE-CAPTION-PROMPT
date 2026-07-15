# Prompt set KPI evidence workflow

## 目的

固定した評価セット上で2つのprompt setを同じ条件で実行し、判断材料となる比較情報を返す。

扱うKPIは次の3つだけとする。

- `quality_score`: 成果の品質。高いほど良い
- `total_tokens`: 使用したinput / output token。少ないほど良い
- `elapsed_seconds`: task開始から終了までの時間。短いほど良い

各反復の`total_tokens`と`elapsed_seconds`は全caseの合計とする。3 KPIの代表値には、それぞれ`N`回の中央値を使う。Layer 4はA / Bの値と数値差を固定するが、優先順位、閾値、`winner`、改善・悪化を出力しない。

このworkflowはpromptの作成、改善、採用、release判断を行わない。

## Layer

| Layer | 役割 | 出力 | 禁止 |
| --- | --- | --- | --- |
| 1. Evaluation set | 外部の評価セットとfixtureを固定する | 固定したEvaluation set capsule | 実行結果を見て同じcycle内のsetを変えること、prompt変更 |
| 2. Execution | prompt set AまたはBで実行する | 成果、token、時間 | 採点、優劣判定、prompt変更 |
| 3. Quality rating | 各成果をblindで採点する | 0〜4のscoreと短い事実根拠 | A / Bの比較、改善提案、artifact変更 |
| 4. KPI comparison | A / Bの3 KPIを集計する | A / Bの反復別値、中央値、`B - A`差分、除外attempt | score変更、優劣判定、改善提案、prompt変更 |

情報はLayer 1から4へ一方向に渡す。各Layerは自分の出力だけを作り、既存Layerの出力を上書きしない。評価基盤の責務はLayer 4の比較情報で終了する。

A / Bは比較条件を識別するlabelであり、順位や採用状態を表さない。比較情報をどう解釈し、次の作業へ何を優先するかは評価基盤の範囲外とする。

## Capsule boundary

workflowは個別のmodel、Agent、permission、task、executor parameterを持たない。変化する入力はEvaluation set capsuleまたはRun capsuleへ格納し、CLIにはcapsule pathだけを渡す。

基盤が解釈するのはcondition、prompt identity、case ID、repetitionなどLayer接続に必要な最小bindingだけとする。それ以外のpayloadとparametersはopaqueに扱い、入力parameterの追加をworkflow変更にしない。

tokenについて基盤が解釈するのは`total_tokens`だけとする。詳細分析用データはLayer 2の`extensions/<run_id>/<feature>/`へ分離する。評価基盤はその内容を読まず、分析schemaの追加や変更をworkflow変更にしない。

## `quality_score`

quality raterが各caseの成果全体を0から4で採点する。

```text
quality_score[r] = sum(case_score[r]) / (4 * case数) * 100
quality_score = median(quality_score[1], ..., quality_score[N])
```

採点基準は`evaluations/cases/README.md`に定義する。quality raterはscoreと短い事実根拠だけを作り、prompt identityとconditionを知らない状態で採点する。

## 反復回数`N`

`N`は任意の正の整数とし、固定値にしない。prompt set AとBを同じ`N`回だけ実行し、各回のKPIを保存する。

比較に使うcycleでは、AとBのcase、反復番号、評価条件を一致させる。外部要因を客観的証跡から自動検出したattemptはraw artifactを保持して除外し、同じslotを再実施する。不足または除外後の有効run数が不一致のcycleからLayer 4の比較情報を作らない。

除外attemptは3 KPIへ入力しない。ただし判断材料から外部要因の発生を隠さないため、`condition`、`case_id`、`repetition`、`category`、`reason_code`をLayer 4へ列挙する。

## KPI comparison

Layer 4はA / Bそれぞれについて次を保存する。

- prompt identity
- 反復ごとの3 KPI
- `N`回の中央値
- 中央値の`B - A`差分
- 外部要因により除外したattempt

`difference_b_minus_a`は単純な数値差であり、有利・不利を表す符号ではない。`quality_score`では正値がBの高値、`total_tokens`と`elapsed_seconds`では正値がBの多値を示す。評価基盤はこれらを単一の順位へ畳み込まない。

## 最小出力

```yaml
prompt_set_a: <prompt identity>
prompt_set_b: <prompt identity>
repetitions: <N>
median:
  quality_score: <a> vs <b>
  total_tokens: <a> vs <b>
  elapsed_seconds: <a> vs <b>
difference_b_minus_a:
  quality_score: <number>
  total_tokens: <number>
  elapsed_seconds: <number>
excluded_attempts: []
```

`winner`、改善・悪化、採用可否は出力しない。

## v1 artifactの扱い

2026-07-15までに作成したv1 cycle、result、profileには`winner`、`kpi_order`、`decision.json`が含まれる。これらは当時の契約による履歴であり、内容やidentityを遡及変更しない。

v2ではCLIを`decide`から`compare`へ、Layer 4 artifactを`decision.json`から`comparison.json`へ変更する。v1の`winner`をv2の現行判断として再利用せず、必要な場合は元の3 KPIと観測事項を判断材料として読む。
