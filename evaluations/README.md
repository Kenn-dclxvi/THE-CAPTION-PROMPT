# Evaluations

prompt比較用のcase、execution profile、再現可能なresultを管理する。

- `cases/`: task入力、fixture contract、oracle / grader境界
- `profiles/`: model、Agent、environment、反復、順序、比較条件
- `results/`: profileとartifact identityへbindした結果

ローカル試行やidentity不一致のrunを正式結果へ昇格させない。

## Minimal four-layer CLI

`scripts/evaluation_loop.py`は、各Layerを別subcommandとして実行する。

1. `freeze-set`: 評価セットとfixtureをcycleへ固定する
2. `run`: 外部Run capsuleのadapterを実行し、成果、token、時間を記録する
3. `rate`: blindなrun IDへ0〜4のscoreと短い事実根拠を記録する
4. `compare`: prompt set A / Bの3 KPI、中央値、`B - A`差分、除外attemptを記録する

評価set、Run capsule、評価case本体はこの基盤に含めず、外部から渡す。executorは`EVAL_CASE_FILE`と`EVAL_RUN_CAPSULE_FILE`から可変入力を読み、`total_tokens`だけを`EVAL_USAGE_FILE`へ書く。客観的証跡から外部要因を検出した場合だけ`EVAL_RUN_STATUS_FILE`へ除外statusを書き、基盤はraw artifactを保持して有効反復数から除外する。詳細分析用データはopaqueな`EVAL_EXTENSION_DIR/<feature>/`へ分離する。Layer出力は既存fileを上書きしない。基盤の出力はKPI比較情報だけであり、`winner`、promptの改善、採用、release判断は行わない。

利用手順は[`docs/evaluation-loop-manual.md`](../docs/evaluation-loop-manual.md)を参照する。
