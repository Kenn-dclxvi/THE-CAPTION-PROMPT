# Parallel execution extension

## 目的

1つのprompt set resultに属する独立したLayer 2 runを、外側並列度`M`で実行する。wave barrierとglobal queueを提供するが、評価基盤v3の保存単位、4 Layer、3 KPIを変更しない。

このextensionはcontroller起動、客観的`external_failure`の再実施、OS sample、実行summaryだけを扱う。採点、result登録、複数prompt set比較、改善、release判断は行わない。

1 planの全capsuleは同じ`prompt_set_identity`と`comparison_conditions`を持たなければならない。重複する`case_id / iteration`は実行前に拒否する。

## Wave plan

caseごとにRun capsule templateを1つ用意する。generatorはその他の値を変更せず、`binding.iteration`だけを`1..N`へ展開する。

```bash
python3 layer2/extensions/parallel_execution/prepare_plan.py \
  --template /absolute/path/to/F01-template.json \
  --template /absolute/path/to/F02-template.json \
  --iterations 3 \
  --cycle /absolute/path/to/frozen-cycle \
  --evaluation-loop /absolute/path/to/scripts/evaluation_loop.py \
  --max-workers 2 \
  --output /absolute/path/to/new-parallel-inputs
```

同じiterationのcaseを`max_workers`件ずつwaveへ置き、全job終了後に次waveへ進む。plan schemaは`the-caption-prompt.parallel-execution-plan/v3`、`schedule_policy`は`wave_barrier`である。

## Global queue

空いたworkerへlongest-firstで次のslotを投入する。duration hintはcase IDから正の秒数へのmappingであり、処理時間短縮にだけ使う。KPI、quality score、互換条件の補正には使わない。

```json
{
  "duration_hints_seconds": {
    "F01": 120,
    "F02": 45
  }
}
```

```bash
python3 layer2/extensions/parallel_execution/prepare_global_plan.py \
  --template /absolute/path/to/F01-template.json \
  --template /absolute/path/to/F02-template.json \
  --iteration 1 \
  --iteration 2 \
  --cycle /absolute/path/to/frozen-cycle \
  --evaluation-loop /absolute/path/to/scripts/evaluation_loop.py \
  --duration-hints /absolute/path/to/duration-hints.json \
  --output /absolute/path/to/new-global-inputs
```

`--max-workers`の既定は、履歴上このhostでqualification済みの`24`である。別host、model、Agent条件または別`M`は新しい`comparison_conditions.executor_parameters`として固定し、必要なqualificationを別cycleで行う。既存v1 / v2 profileは変更しない。

## 実行

```bash
python3 layer2/extensions/parallel_execution/parallel_runner.py \
  --plan /absolute/path/to/plan.json \
  --output /absolute/path/to/new-runner-evidence
```

outputはwrite-onceで次を作る。

```text
runner-evidence/
├── plan.json
├── attempts.jsonl
├── os-samples.jsonl
└── summary.json
```

`attempts.jsonl`とOS sampleはmodel-visible入力ではない。Layer 2のworkspace、capsule、binding、execution artifactはcycle内へ保存される。resource競合、workspace衝突、未分類controller failureがあるcycleはprompt set resultへ登録しない。
