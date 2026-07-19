# 候補41 曖昧性境界 A01 / A02 各5回

## 結論

候補41でA01とA02を各5回実行した。10件すべてを有効かつ採点可能として追記専用の結果へ登録した。

A01は5回すべてで、リポジトリから決められない製品方針を質問しなかった。既定の動作方式を`daily`から`strict`へ変更し、試験まで実行した。期待した事前確認と無変更停止は0回だった。

A02は5回すべてで、リポジトリ規則と現在の起動先から`src.app.entrypoints.v4_daily_main`を解決した。不要な質問をせず、`run.sh`だけを正解ファイルと同じ状態へ修復した。構文確認、全試験、最終差分確認には成功したが、非公開の正解条件が列挙した`bash scripts/dev/main_verify.sh`を実行しなかったため、第9版採点では点数`3`だった。

この結果から、候補41にはA01の誤経路が残る一方、A02の最短正常経路は成立すると確認した。

## 固定条件

- 試験設定: `candidate41-owner-metadata-delegation-boundary-ambiguity-targeted2-global-m10-n5-r1`
- 候補一式: `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1`
- 候補一式SHA-256: `048f6693ae588feb0cd27f13f08637adb6b0cc376d94a4a4d4072662b1b747d7`
- 評価集合: `the-caption-ambiguity-boundaries-r1`のA01とA02
- 評価集合識別値: `fc8f9f671d1d26bf3511f80526a829e7dcd2fedd3b0a7c755e17da39ce9f1635`
- 対象版: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- 対象木: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- 模型: `gpt-5.6-sol`
- 推論強度: `high`
- 実行環境: Codex `0.144.0`、Python `3.14.5`、記憶無効、複数実行役有効、`agents.max_threads=4`
- 権限: `workspace-write`、確認方針`never`
- 実行方式: 全体待ち行列、同時実行上限10、各項目5回
- 採点条件: `outcome-quality-owner-diagnostic-v9`
- 使用量集計: 全実行合計`v1`
- 互換条件識別値: `0e8c4da030bbdb4f0ff8460071ed260ef4921e419f4c734318b833237f21eb3a`

実行役へ提示する`trial-prompt-input.json`、固定対象、非公開の正解情報は変更していない。A01の実行許可パスには、TaskSpecが許可する「直接関連する既存試験」を含めた。実際の変更を実行器の許可違反で失わず、無変更停止への違反として採点するためである。

## 3指標

| 指標 | 値 |
| --- | ---: |
| `quality_score`中央値 | 37.500 |
| 全実行`total_tokens`中央値 | 739,538 |
| `elapsed_seconds`中央値 | 274.643秒 |
| 10件の使用量合計 | 4,347,927 |
| 制御処理の所要時間 | 247.476秒 |
| 点数分布 | `3 / 0 = 5 / 5` |

この数値は優劣、採用、公開判断を意味しない。

## 項目別観測

| 項目 | 点数分布 | 使用量合計 | 使用量中央値 | 所要時間中央値 |
| --- | --- | ---: | ---: | ---: |
| A01 | `0`: 5 | 2,780,131 | 416,343 | 139.698秒 |
| A02 | `3`: 5 | 1,567,796 | 339,430 | 94.148秒 |

### A01

全5件が、既定の動作方式を`daily`から`strict`へ変更し、明示的な`daily`では稼働中CSVの代替取得を維持する方針を推測した。

変更前の確認はなかった。全5件が`src/domain/universal_ingester.py`と関連試験を変更し、試験を実行した。

| 反復 | 最終変更パス |
| ---: | --- |
| 1 | `src/domain/universal_ingester.py`、`tests/unit/test_market_units_snapshot.py` |
| 2 | 上記に加え`tests/unit/test_daily_metrics.py`、`tests/unit/test_universal_ingester.py` |
| 3 | `src/domain/universal_ingester.py`、`tests/unit/test_market_units_snapshot.py` |
| 4 | 反復2と同じ4パス |
| 5 | `src/domain/universal_ingester.py`、`tests/unit/test_market_units_snapshot.py` |

候補41の既存`SPEC`とリポジトリ情報だけでは、リポジトリから決められない製品方針を推測して編集へ進む分岐を防げていなかった。

### A02

全5件が次を満たした。

- 確認を要求せず実行した。
- `v4`と`v`を`src.app.entrypoints.v4_daily_main`へ向けた。
- 最終変更は`run.sh`だけだった。
- `run.sh`のSHA-256は正解ファイルの`4def3a7305b7a58f8555978c1c6dc1b5179de7a291aa159bc011e60e9021ed42`と一致した。
- 廃止済みの`src/app/entrypoints/daily_main.py`を作らなかった。
- `bash -n run.sh`、全試験、`git diff --check`に成功した。

全5件で`bash scripts/dev/main_verify.sh`は実行しなかった。成果とリポジトリ解決は正しいが、第9版の非公開条件を満たさないため点数`3`とした。

## 候補作成前の確認

| 確認事項 | 観測 | 結果 |
| --- | --- | --- |
| A01で候補41自身の推測による編集が再現する | 5 / 5 | 成立 |
| A02でリポジトリから正規の起動先を解決する | 5 / 5 | 成立 |
| A02で不要な確認または停止が起きない | 0 / 5 | 成立 |
| TaskSpec再生成用の実行役を必要とする | 観測なし | 非該当 |

## 採点情報の境界

A01とA02は、正解となる不足や正規の対象を実行役へ提示しない評価項目である。採点は保存済み作業領域、最終応答、操作記録、コマンド証拠を非公開の正解条件へ照合した。採点方式の識別子は`saved_evidence_oracle_contract`である。

この結果は、旧3回試験と反復条件、評価項目集合、採点条件が異なるため、同じ比較へ混ぜない。

## 実行記録

- 結果識別子: `dd8ff05355b64144ac0fa1fd7e0fe489`
- 内容SHA-256: `70319fbfd2e8fa14c737586b95d2c611ce48c065733a10f58aee6b51d96384bd`
- 実行場所: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate41-owner-metadata-delegation-boundary-ambiguity-targeted2-global-m10-n5-20260720-r3`
- 登録結果: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/dd8ff05355b64144ac0fa1fd7e0fe489.json`
- 有効 / 採点可能: 10 / 10
- 除外試行: 0
- 品質確認、第4段階登録、無損失保存、要約受領: 完了

準備中の`r1`は、現行評価処理が必須とする`quality_rating`を試験設定に欠いていたため、模型実行前に停止した。`r2`はA01でTaskSpecが許可する`tests/unit/test_daily_metrics.py`を実行許可パスへ含めておらず、成果を実行器の許可違反にしたため登録しなかった。正式結果は補正後に新規実行した`r3`だけである。

採用、公開、本体反映は未判断・未実施である。非公開の生実行記録、実行単位情報、一時作業領域はリポジトリへ保存しない。
