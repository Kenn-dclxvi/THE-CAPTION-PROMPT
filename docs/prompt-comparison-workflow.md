# Prompt set KPI comparison workflow

## 目的

固定した評価セット上で2つのprompt setを同じ条件で実行し、3 KPIだけで比較結果を返す。

比較するKPIは次の3つだけとする。

- `quality_score`: 成果の品質。高いほど良い
- `total_tokens`: 使用したinput / output token。少ないほど良い
- `elapsed_seconds`: task開始から終了までの時間。短いほど良い

各反復の`total_tokens`と`elapsed_seconds`は全caseの合計とする。3 KPIの比較値には、それぞれ`N`回の中央値を使う。

このworkflowはpromptの作成、改善、採用、release判断を行わない。

## Layer

| Layer | 役割 | 出力 | 禁止 |
| --- | --- | --- | --- |
| 1. Evaluation set | 外部の評価セットとfixtureを固定する | 固定したEvaluation set capsule | 実行結果を見て同じcycle内のsetを変えること、prompt変更 |
| 2. Execution | prompt set AまたはBで実行する | 成果、token、時間 | 採点、優劣判定、prompt変更 |
| 3. Quality rating | 各成果をblindで採点する | 0〜4のscoreと短い事実根拠 | A / Bの比較、改善提案、artifact変更 |
| 4. KPI comparison | A / Bの3 KPIを比較する | `winner: a | b | tie` | score変更、原因分析、改善提案、prompt変更 |

情報はLayer 1から4へ一方向に渡す。各Layerは自分の出力だけを作り、既存Layerの出力を上書きしない。評価基盤の責務はLayer 4の比較結果で終了する。

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

比較に使うcycleでは、AとBのcase、反復番号、評価条件を一致させる。外部要因を客観的証跡から自動検出したattemptはraw artifactを保持して除外し、同じslotを再実施する。不足または除外後の有効run数が不一致のcycleからwinnerを出さない。

## KPI comparison

判断順は次のとおりとする。

1. `quality_score`が高い方
2. 同点なら`total_tokens`が少ない方
3. さらに同点なら`elapsed_seconds`が短い方

3 KPIがすべて同じ場合は`tie`とする。説明、期待、変更量、改善可能性などKPI以外の情報で結果を逆転させない。

## 最小出力

```yaml
prompt_set_a: <prompt identity>
prompt_set_b: <prompt identity>
repetitions: <N>
quality_score: <a> vs <b>
total_tokens: <a> vs <b>
elapsed_seconds: <a> vs <b>
winner: a | b | tie
```

この出力の利用方法は評価基盤の範囲外とする。
