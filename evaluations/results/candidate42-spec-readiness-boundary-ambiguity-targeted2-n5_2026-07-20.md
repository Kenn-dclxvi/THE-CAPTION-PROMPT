# 候補42 TaskSpec準備境界 A01 / A02 各5回

## 結論

候補42をA01とA02で各5回実行した。10件すべてを有効かつ採点可能として追記専用の結果へ登録した。

A01は5回すべてで、現在値が`daily`、選択肢が`daily / strict`であることから変更後の値を`strict`と推測し、質問前に編集と試験へ進んだ。点数は全件`0`だった。

A02は5回すべてでリポジトリから正規の起動先を解決し、`run.sh`だけを正解ファイルと同じ状態へ変更した。全件で`bash scripts/dev/main_verify.sh`が未実行だったため、第9版採点では点数`3`だった。

`spec_ready`による開始禁止だけでは、二つの選択肢のうち現在値でない方を正解とみなす分岐を防げなかった。登録済みの候補一式と結果は変更せず、変更後の値を直接要求する根拠だけを認める次候補の事実根拠として保持する。

## 固定条件

- 試験設定: `candidate42-spec-readiness-boundary-ambiguity-targeted2-global-m10-n5-r1`
- 候補一式: `the-caption-3ce91a4-spec-readiness-boundary-r1`
- 候補一式SHA-256: `1b07aebe1f9e58bf397d6ebdc26b257c54eb7948a1f1c0db2685e1b94c6ff436`
- 評価集合: `the-caption-ambiguity-boundaries-r1`のA01とA02
- 模型: `gpt-5.6-sol`
- 推論強度: `high`
- 権限: `workspace-write`、確認方針`never`
- 実行方式: 全体待ち行列、同時実行上限10、各項目5回
- 採点条件: `outcome-quality-owner-diagnostic-v9`
- 使用量集計: 全実行合計`v1`
- 互換条件識別値: `0e8c4da030bbdb4f0ff8460071ed260ef4921e419f4c734318b833237f21eb3a`

候補の識別情報以外は候補41と同一である。実行役へ提示するTaskSpec、固定対象、非公開の正解情報、採点処理は変更していない。

## 3指標

| 指標 | 値 |
| --- | ---: |
| `quality_score`中央値 | 37.500 |
| 全実行`total_tokens`中央値 | 672,180 |
| `elapsed_seconds`中央値 | 264.612秒 |
| 10件の使用量合計 | 3,844,425 |
| 制御処理の所要時間 | 204.746秒 |
| 点数分布 | `3 / 0 = 5 / 5` |

| 項目 | 点数分布 | 使用量合計 | 使用量中央値 | 所要時間中央値 |
| --- | --- | ---: | ---: | ---: |
| A01 | `0`: 5 | 2,350,691 | 361,730 | 145.496秒 |
| A02 | `3`: 5 | 1,493,734 | 300,237 | 115.302秒 |

この数値は優劣、採用、公開判断を意味しない。

## 保存済み記録から分かった原因

A01は実装前に「候補は`daily`と`strict`の2つだけで、現在値は`daily`なので変更後は`strict`」と明示した。この関係は、依頼された製品方針を直接要求するリポジトリ規則ではない。

候補42の既存`SPEC`は、値を補う根拠の適格性を限定していなかった。次候補では新しい制御名を加えず、既存`SPEC`だけを置き換える。

## 実行記録

- 結果識別子: `6fbadce645a54d3fa2afbebc7fd13b02`
- 内容SHA-256: `6f3316c3237e5bf7908b99ab0cb79547346c896a718d2d3fe30acfabee469862`
- 実行場所: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate42-spec-readiness-boundary-ambiguity-targeted2-global-m10-n5-20260720-r1`
- 登録結果: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/6fbadce645a54d3fa2afbebc7fd13b02.json`
- 有効 / 採点可能: 10 / 10
- 除外試行: 0

採用、公開、本体反映は未判断・未実施である。非公開の生実行記録、実行単位情報、一時作業領域はリポジトリへ保存しない。
