# Parallel execution extension

## 目的

固定済みEvaluation setの独立したLayer 2 runを、外側並列度`M`で同時実行する。評価基盤v1のLayer、KPI、出力schemaは変更しない。

このextensionが担当するのは次だけである。

- `max_workers`を上限とするLayer 2 controllerの起動
- 客観的に`external_failure`と分類されたattemptの再実施
- 実行中のOS sample保存
- slot数、attempt数、除外数、wall timeのsummary保存

採点、A / B比較、prompt改善、release判断は行わない。

## Plan

caseごとにA / BのRun capsule templateが1つずつある場合、反復番号とwaveは機械生成する。

```bash
python3 layer2/extensions/parallel_execution/prepare_plan.py \
  --template /absolute/path/to/F01-a-template.json \
  --template /absolute/path/to/F01-b-template.json \
  --template /absolute/path/to/F02-a-template.json \
  --template /absolute/path/to/F02-b-template.json \
  --repetitions 3 \
  --cycle /absolute/path/to/frozen-cycle \
  --evaluation-loop /absolute/path/to/scripts/evaluation_loop.py \
  --output /absolute/path/to/new-parallel-inputs
```

generatorはtemplateのその他のparameterを変更せず、`binding.repetition`だけを`1..N`へ展開する。case順と反復番号からA / Bの投入順を交互化し、同じcase・反復のA / Bを同じwaveへ置く。

生成されるplanの形式は次のとおりである。

```json
{
  "schema_version": "the-caption-prompt.parallel-execution-plan/v1",
  "cycle": "/absolute/path/to/frozen-cycle",
  "evaluation_loop": "/absolute/path/to/scripts/evaluation_loop.py",
  "max_workers": 2,
  "max_attempts": 3,
  "monitor_interval_seconds": 15,
  "jobs": [
    {"wave": 1, "capsule": "/absolute/path/to/a-case-r1.json"},
    {"wave": 1, "capsule": "/absolute/path/to/b-case-r1.json"},
    {"wave": 2, "capsule": "/absolute/path/to/b-case-r2.json"},
    {"wave": 2, "capsule": "/absolute/path/to/a-case-r2.json"}
  ]
}
```

同じ`condition / case_id / repetition`の重複は実行前に拒否する。同じ`wave`のjobを同時投入し、全jobの終了後に次のwaveへ進む。1 waveのjob数は`max_workers`以下、wave番号は1から連続でなければならない。これによりA / B pairを同じ実行窓へ置き、次の反復との混在を防ぐ。

## 実行

```bash
python3 layer2/extensions/parallel_execution/parallel_runner.py \
  --plan /absolute/path/to/plan.json \
  --output /absolute/path/to/new-runner-evidence
```

outputは既存directoryへ上書きしない。次を新規作成する。

```text
runner-evidence/
├── plan.json
├── attempts.jsonl
├── os-samples.jsonl
└── summary.json
```

`attempts.jsonl`はcontroller実行の順序と外部失敗retryを記録する。model-visibleな入力ではない。Layer 2のworkspace、Codex JSONL、binding、execution artifactは従来どおりcycle内へ保存される。

`os-samples.jsonl`はload average、memory free、swap、disk free、関連process数を保存する。monitor取得の失敗は`sample_errors`として記録し、case結果へ変換しない。

## Qualification boundary

新しい`M`は新しい実行条件として別cycleでqualificationする。直列cycleのrunと混在させない。resource競合、workspace衝突、未分類のcontroller failureがあるcycleは正式なprompt比較へ使用しない。
