# Prompt set KPI evidence workflow

## 目的

固定条件下で1つのprompt setを実行した結果を独立して保存し、後から互換条件を満たす2つ以上のresultを任意に取得・比較する。

扱うKPIは次の3つだけとする。

- `quality_score`: case成果全体の0〜4 scoreから算出した値
- `total_tokens`: root agentと、そのrunから起動された全SA sessionの最終token usageの合計
- `elapsed_seconds`: task開始から終了までの時間

各iterationの`total_tokens`と`elapsed_seconds`は全caseの合計、`quality_score`は全case scoreを0〜100へ正規化した値とする。代表値は`1..N`の中央値である。数値差は明示したminuend resultからsubtrahend resultを引くが、優先順位、閾値、`winner`、改善・悪化を出力しない。

このworkflowはpromptの作成、改善、採用、release判断、THE-CAPTION本体反映を行わない。

## 保存単位

一次結果の単位は、1つのEvaluation set上で1つのimmutableな`prompt_set_identity`を`1..N`回実行したprompt set resultである。1 cycleへ複数prompt setを混ぜず、固定A / B pairやcondition labelを保存identityにしない。

`prompt_set_identity`は少なくとも次を含む。

```json
{
  "name": "<prompt set name>",
  "revision": "<immutable revision>"
}
```

`revision`の代わりに、または併記してlowercase SHA-256の`bundle_sha256`を使用できる。可変の名前だけではresultを登録できない。

## Layer

| Layer | 役割 | 出力 | 禁止 |
| --- | --- | --- | --- |
| 1. Evaluation set | 外部setとfixtureを固定する | revision、set identity、case別fixture identityを含むcapsule | 結果を見た後のin-place変更、prompt変更 |
| 2. Execution | 1 prompt setの1 case / 1 iterationを実行する | 成果、`total_tokens`、時間、model-invisible binding | 採点、比較、prompt変更 |
| 3. Quality rating | 各成果をblindで採点する | 0〜4のscoreと短い事実根拠 | prompt identityの参照、比較、改善提案 |
| 4. KPI comparison | prompt set resultを登録し、保存resultからviewを作る | append-only result、任意個の一覧・中央値・明示差分 | 一次結果の変更、優劣判定、改善提案 |

情報はLayer 1から4へ一方向に渡す。各Layerは自分の出力だけを作り、既存出力を上書きしない。比較viewは保存済みresultを参照する派生artifactであり、一次結果を変更しない。

fixtureとworkspaceの物理materializationはLayer接続の実装詳細である。sourceとdestinationの独立性および論理contentを保つ限りCopy-on-Writeを使用でき、copy方式をprompt set identity、互換条件、KPIへ追加しない。storage監査とGCは[`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md)に分離する。

## Capsule boundary

Evaluation set sourceは`set_id`と`revision`を持つ。Run capsuleは次を分離する。

- `binding`: `prompt_set_identity`、`case_id`、`iteration`
- `comparison_conditions`: prompt identity以外の互換条件
- `adapter` / `parameters`: executor入力。`parameters`は基盤に対してopaque

`comparison_conditions`は次を必須とする。

- `target_repository_ref`
- `model`
- `agent_environment`
- `task_spec`
- `permission`
- `executor_parameters`
- `repetition_condition`。少なくとも正の整数`iterations`を含む

prompt bundle pathやprompt固有parameterを`comparison_conditions.executor_parameters`へ混ぜない。比較対象間で固定するexecutor条件だけを格納し、prompt固有値は`binding.prompt_set_identity`またはopaqueな`parameters`へ置く。

`comparison_conditions.executor_parameters.token_accounting`には、`scope: all_agents`、`revision: v1`、`source: codex_rollout_final_usage_by_workspace`を固定する。異なるscopeまたはrevisionを持つresultは互換比較しない。

Layer 1は`.git`内部を除くfixtureのpath、type、mode、contentまたはsymlink targetからcase別fixture identityを計算する。resultの互換条件にはEvaluation setの`set_id`、`revision`、content identity、case別fixture identity、Run capsuleの全`comparison_conditions`、case集合、iteration集合を含める。

## `quality_score`

quality raterが各caseの成果全体を0から4で採点する。

```text
quality_score[i] = sum(case_score[i]) / (4 * case数) * 100
quality_score = median(quality_score[1], ..., quality_score[N])
```

quality raterへ渡すのはmodel-visible caseとblindなexecution evidenceだけである。`layer2/bindings/`、Run capsule、oracle、grader、expected resultをmodel-visible入力へ混ぜない。raterはscoreと短い事実根拠だけを返し、promptの選択や改善提案を行わない。

## Append-only result registry

`record-result`は全caseと`1..N`が揃い、全valid runが採点済みであることを確認して次へwrite-onceで保存する。

```text
<registry>/
└── results/
    └── <result_id>.json
```

各resultは次を保持する。

- immutableな`prompt_set_identity`とそのSHA-256
- 互換条件の実体と`compatibility_key`
- case別の`quality_score`、`total_tokens`、`elapsed_seconds`
- iteration別の3 KPIと中央値
- 除外attempt
- 作成時刻とresult全体のcontent SHA-256

registryはmutableなA / B indexを持たず、`query-results`が保存fileを走査する。既存resultを別比較のために書き換えたり、現行prompt revisionへ読み替えたりしない。

## 互換条件と任意個比較

`compare`は2件以上の`result_id`を受け付ける。全resultの`compatibility_key`と互換条件実体が完全一致しない場合はfail closedする。

viewには選択した全prompt setのidentity、iteration別KPI、中央値、除外attemptを列挙する。数値差は利用者が指定した`reference_result_id`をsubtrahendとし、他の各resultをminuendとして次の形で出力する。

```json
{
  "minuend_result_id": "<selected result>",
  "subtrahend_result_id": "<reference result>",
  "kpis": {
    "quality_score": "minuend - subtrahend",
    "total_tokens": "minuend - subtrahend",
    "elapsed_seconds": "minuend - subtrahend"
  }
}
```

差分の符号を有利・不利へ変換しない。referenceは基準線にすぎず、baseline、採用状態、順位を意味しない。

## Token accountingとextension boundary

評価基盤が解釈するtoken値はall-agentの`total_tokens`だけである。adapterはrootの`codex exec` sessionを起点に、同じevaluation workspaceを持つ全descendant sessionの最終`total_tokens`を合算する。cached inputを含む各sessionのprovider報告値を使用し、親子間の重複を補正しない。

root / SA別値、thread identity、session数、rollout fileなどの集計根拠は`layer2/extensions/<run_id>/all-agent-usage/`へ分離する。これらの内訳はquality ratingとKPI comparisonへ入力しない。root sessionまたはdescendant sessionの最終usageが欠ける場合は推定せず、`codex_all_agent_usage_incomplete`の外部計測失敗としてrunを除外し、同じslotを再実行する。

## 旧artifactの扱い

2026-07-15までに作成したv1 cycle、result、profileには`winner`、`kpi_order`、`decision.json`が含まれる。v2には固定A / Bの`comparison.json`と`difference_b_minus_a`が含まれる。いずれも当時の契約による履歴であり、内容やidentityを遡及変更しない。

v3のall-agent token accounting revisionは`execution-capsule/v2`、`evaluation-set/v2`、`execution/v3`、`prompt-set-result/v2`、`prompt-set-comparison-view/v2`を使用する。root agentだけを`total_tokens`へ保存したv3 `prompt-set-result/v1`と`prompt-set-comparison-view/v1`は履歴として保持し、in-place変更しない。保存sessionから完全に再構成できる場合だけ、元result IDを由来としてv2 resultをappend-only追加する。v1/v2 evaluation foundation cycleをv3 resultとして読み込まない。
