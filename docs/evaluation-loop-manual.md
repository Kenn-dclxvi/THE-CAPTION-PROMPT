# Evaluation loop manual

## 1. 対象

この文書は、`scripts/evaluation_loop.py`を使って4 LayerのKPI evidence cycleを実行する方法を説明する。

この基盤には次を含めない。

- 評価scenario
- prompt set A
- prompt set B
- quality rater用prompt
- THE-CAPTION本体への反映

これらは実行時に外部から与える。

## 2. 4 Layer

| Layer | subcommand | 役割 |
| --- | --- | --- |
| 1. Evaluation set | `freeze-set` | 外部のsetとfixtureをcycleへ固定する |
| 2. Execution | `run` | 1 condition、1 case、1 repetitionを実行する |
| 3. Quality rating | `rate` | 1 runへ0〜4のscoreを記録する |
| 4. KPI comparison | `compare` | A / Bの3 KPIと数値差を記録する |

各subcommandは対応するLayerだけへ書き込む。既存のLayer出力は上書きしない。

## 3. Capsule boundary

workflowへ個別parameterを追加しない。変化する入力は次の2 capsuleへ格納し、CLIにはcapsule pathだけを渡す。

- Evaluation set capsule: caseとfixtureを保持する
- Run capsule: 1 runのbinding、adapter、任意parameterを保持する

基盤が解釈するのはLayerを接続するための最小fieldだけである。`payload`と`parameters`の内部構造は基盤にとってopaqueであり、将来fieldが増えてもworkflowを変更しない。

評価基盤のtoken出力は`total_tokens`だけとする。詳細分析用データは`layer2/extensions/<run_id>/<feature>/`へ分離し、評価基盤はそのschemaや内容を解釈しない。

capsuleへsecretやcredentialを直接保存しない。

## 4. 必要なもの

実行前に次を用意する。

1. Evaluation set capsule
2. caseごとのrepository fixture directory
3. 各runのRun capsule
4. run成果を0〜4で採点できるquality rater

## 5. Evaluation set capsule

評価setとfixtureはrepository外に置いてよい。

```text
/path/to/evaluation/
├── set.json
├── fixture-a/
└── fixture-b/
```

基盤が必要とする最小形式は次のとおり。

```json
{
  "set_id": "<set identity>",
  "cases": [
    {
      "id": "<case id>",
      "fixture": "fixture-a",
      "payload": {
        "<任意parameter>": "<value>"
      }
    }
  ]
}
```

`fixture`は`set.json`からの相対pathで指定する。基盤が解釈するcase fieldは`id`と`fixture`だけである。それ以外のfieldは変更せず固定setへcopyする。

## 6. Run capsule

1 condition、1 case、1 repetitionにつき1つ用意する。

```json
{
  "schema_version": "the-caption-prompt.execution-capsule/v1",
  "binding": {
    "condition": "a",
    "prompt_identity": "<prompt identity>",
    "case_id": "<case id>",
    "repetition": 1
  },
  "adapter": {
    "argv": ["python3", "/path/to/executor.py"]
  },
  "parameters": {
    "<任意parameter>": "<value>"
  }
}
```

基盤が解釈するのは次だけである。

- `binding.condition`: `a`または`b`
- `binding.prompt_identity`: conditionへbindするidentity
- `binding.case_id`: 固定set内のcase ID
- `binding.repetition`: 1から始まる反復番号
- `adapter.argv`: shellを介さず実行するcommand配列

model、reasoning、Agent環境、permission、prompt pathなどの可変入力は`parameters`へ入れる。基盤は`parameters`を解釈せずexecutorへ渡す。

同一conditionの全runでは同じprompt identityを使う。

## 7. Executor contract

`run`は`adapter.argv`を、case fixtureのcopyをworking directoryとして直接実行する。

executorには次の環境変数が渡される。

| 変数 | 内容 |
| --- | --- |
| `EVAL_CASE_FILE` | 固定済みcase capsuleのJSON path |
| `EVAL_RUN_CAPSULE_FILE` | 固定済みRun capsuleのJSON path |
| `EVAL_USAGE_FILE` | executorが`total_tokens`を書く一時JSON path |
| `EVAL_RUN_STATUS_FILE` | executorが外部要因による除外を通知する一時JSON path |
| `EVAL_EXTENSION_DIR` | 配下機能が任意の詳細データを書くopaqueなdirectory |

executorは`EVAL_CASE_FILE`と`EVAL_RUN_CAPSULE_FILE`を読み、必要なmodel-visible入力や実行parameterへ変換する。この変換はadapterの責務でありworkflowへ持ち込まない。

executorは終了までに`EVAL_USAGE_FILE`へ次を書く。

```json
{
  "total_tokens": 12345
}
```

`total_tokens`は0以上の整数とする。基盤はこの値だけを`evidence/usage.json`へ正規化して保存する。`input_tokens`、`output_tokens`、turn別内訳などは評価出力へ含めない。それらが必要な配下機能は、独自schemaを`EVAL_EXTENSION_DIR/<feature>/`へ保存する。

executorがpromptまたはtask behaviorではない外部要因を客観的な実行証跡から検出した場合だけ、`EVAL_RUN_STATUS_FILE`へ次を書く。

```json
{
  "schema_version": "the-caption-prompt.run-status/v1",
  "status": "excluded",
  "category": "external_failure",
  "reason_code": "<stable reason code>"
}
```

基盤はこのattemptのstdout、stderr、workspace、usage、execution、bindingを保存し、`evidence/<run_id>/exclusion.json`へ除外理由を固定する。`excluded` attemptはquality ratingとKPI比較へ入力せず、同じcondition / case / repetitionを占有しない。したがって、同じRun capsuleを再実施して有効回数をA / Bで揃える。Agentの自己申告や最終応答の文言だけを除外根拠にしてはならない。

`extensions/`の内容はKPI集計へ入力しない。詳細分析の追加やschema変更は配下機能だけで完結させる。`elapsed_seconds`は基盤側が自動計測する。

## 8. Cycleの実行

以下ではCLIとcycle pathを次のように表す。

```bash
CLI=/Users/kenn/repos/THE-CAPTION-PROMPT/scripts/evaluation_loop.py
CYCLE=/tmp/the-caption-prompt-cycle-001
```

### Layer 1: 評価setを固定する

空のcycle pathを指定する。

```bash
python3 "$CLI" freeze-set \
  --set /path/to/evaluation/set.json \
  --cycle "$CYCLE"
```

成功するとsetとfixtureが`$CYCLE/layer1/`へcopyされる。以後、そのcycleでは元のsetを変更しても反映されない。

### Layer 2: Run capsuleを実行する

```bash
python3 "$CLI" run \
  --cycle "$CYCLE" \
  --capsule /path/to/run-capsules/set-a-case-001-r1.json
```

成功するとJSONで`run_id`とevidence pathが返る。

```json
{
  "layer": 2,
  "run_id": "<blind run id>",
  "evidence": "<evidence path>",
  "status": "valid"
}
```

prompt set BもB用Run capsuleを渡して実行する。

```bash
python3 "$CLI" run \
  --cycle "$CYCLE" \
  --capsule /path/to/run-capsules/set-b-case-001-r1.json
```

全caseについてprompt set AとBを同じ回数実行する。`N`回測定する場合は、両conditionで`repetition: 1`から`repetition: N`までのRun capsuleを用意する。

同じcondition、case、repetitionの有効runは重複実行できない。`excluded` attemptはraw artifactを保持したまま有効回数から除外されるため、同じcondition、case、repetitionで再実施できる。再実施後もA / Bの有効runが同じ`1..N`を満たさない間はLayer 4へ進まない。

### Layer 3: runを採点する

quality raterには次だけを渡す。

- `$CYCLE/layer1/set.json`の該当case
- `$CYCLE/layer2/evidence/<run_id>/`

`status: excluded`のrunは採点しない。

`layer2/bindings/`はconditionとprompt identityを含むため、quality raterへ渡さない。

evidenceには次が含まれる。

- `case.json`
- `workspace/`
- `stdout.bin`
- `stderr.bin`
- `usage.json`
- `execution.json`

採点後、scoreと短い事実根拠を記録する。

```bash
python3 "$CLI" rate \
  --cycle "$CYCLE" \
  --run-id <run id> \
  --score 3 \
  --reason "<scoreの短い事実根拠>"
```

scoreは0、1、2、3、4のいずれかとする。quality raterは改善提案、A / Bの選択、再実行を行わない。

### Layer 4: KPI比較情報を作る

全condition、全case、全repetitionの実行と採点が終わった後に実行する。

```bash
python3 "$CLI" compare --cycle "$CYCLE"
```

Layer 4は次を集計する。

- A / Bそれぞれの反復別3 KPI
- A / Bそれぞれの中央値
- 中央値の`B - A`差分
- 外部要因により除外したattempt一覧

結果は`$CYCLE/layer4/comparison.json`へ保存される。`winner`、KPIの優先順位、改善・悪化、採用可否は出力しない。

`difference_b_minus_a`は単純な数値差である。`quality_score`では正値がBの高値、`total_tokens`と`elapsed_seconds`では正値がBの多値を表すが、基盤は符号を有利・不利へ変換しない。

## 9. Cycle directory

```text
<cycle>/
├── layer1/
│   ├── set.json
│   └── fixtures/
├── layer2/
│   ├── evidence/<run_id>/
│   │   └── exclusion.json            # excluded attemptだけ
│   ├── capsules/<run_id>.json
│   ├── bindings/<run_id>.json
│   └── extensions/<run_id>/<feature>/
├── layer3/
│   └── ratings/<run_id>.json
└── layer4/
    └── comparison.json
```

`evidence/`はblind採点用、`capsules/`はexecutor入力、`bindings/`はKPI集計用である。quality raterへ渡すのは`evidence/`だけとし、`capsules/`、`bindings/`、`extensions/`は渡さない。`extensions/`は配下機能の領域であり、評価基盤は読み取らない。

## 10. 主なerror

| error | 原因 | 対応 |
| --- | --- | --- |
| `cycle directory is not empty` | 使用済みcycleへsetを固定しようとした | 新しい空cycle pathを使う |
| `run already exists` | 有効なcondition / case / repetitionが重複した | 指定を確認する。excluded attemptなら同じslotで再実施できる |
| `excluded run cannot be quality-rated` | 外部要因で除外済みのrunを採点しようとした | 同じslotを再実施し、有効runだけを採点する |
| `usage must contain...` | `total_tokens`がない、または不正 | executorの`EVAL_USAGE_FILE`出力を修正する |
| `missing file: ...ratings...` | 未採点runがある | 全runへ`rate`を実行する |
| `repetitions must be contiguous` | repetitionが1から連続していない | prompt set A / Bを同じ1..Nで揃える |
| `must cover every frozen case` | condition間でcaseまたは反復が不足 | 不足runを実行・採点する |

## 11. v1 cycleとの非互換点

v1の`decide` subcommandと`layer4/decision.json`は、`winner`を作る旧契約である。v2は`compare` subcommandと`layer4/comparison.json`を使用する。

既存のv1 cycleとresultは当時の記録として保持し、in-placeでv2へ変換しない。v2の比較情報が必要な場合は、新しいcycleとして実行する。

## 12. 基盤のself-test

評価caseやpromptを作らず、temporary fixtureで4 Layerの接続だけを確認できる。

```bash
cd /Users/kenn/repos/THE-CAPTION-PROMPT
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests/test_evaluation_loop.py tests/test_run_codex_evaluation.py
```
