# 候補44 完全確認の境界 A01 / A02 各5回

## 結論

候補44をA01とA02で各5回実行した。10件すべてを有効かつ採点可能として追記専用の結果へ登録した。

A01は5回すべてで編集と試験を始めず質問した。第9版の点数は`4 / 3 = 2 / 3`だった。非公開条件が定めた代替取得方針まで含む質問は2回だった。

A02は4回で正規の起動先を解決したが、1回はリポジトリから解決できる対象を質問して停止した。第9版の点数は`3 / 1 = 4 / 1`だった。

「成果を変える全未固定値」を一度の質問へ含める記載は、A01の質問を安定させず、A02の最短正常経路を1件阻害した。この方向へ条件を積み増さず、候補44は停止する。候補43の二つの境界観測はこの結果で上書きしない。

## 変更境界

候補43からの差分は、ルート`AGENTS.md`にある既存`SPEC`の一行だけである。新しい制御名、TaskSpec形式、実行役、項目固有語は追加していない。

## 固定条件

- 試験設定: `candidate44-complete-spec-readiness-boundary-ambiguity-targeted2-global-m10-n5-r1`
- 候補一式: `the-caption-3ce91a4-complete-spec-readiness-boundary-r1`
- 候補一式SHA-256: `8093ed7caa7e518c1313f2dab903260a8e20297d2a66508d250f37389aeb9bde`
- 評価集合: `the-caption-ambiguity-boundaries-r1`のA01とA02
- 模型: `gpt-5.6-sol`
- 推論強度: `high`
- 権限: `workspace-write`、確認方針`never`
- 実行方式: 全体待ち行列、同時実行上限10、各項目5回
- 採点条件: `outcome-quality-owner-diagnostic-v9`
- 使用量集計: 全実行合計`v1`
- 互換条件識別値: `0e8c4da030bbdb4f0ff8460071ed260ef4921e419f4c734318b833237f21eb3a`

候補の識別情報以外は候補41〜43と同一である。実行役へ提示するTaskSpec、固定対象、非公開の正解情報、採点処理は変更していない。

## 3指標

| 指標 | 値 |
| --- | ---: |
| `quality_score`中央値 | 75.000 |
| 全実行`total_tokens`中央値 | 448,865 |
| `elapsed_seconds`中央値 | 155.992秒 |
| 10件の使用量合計 | 1,987,888 |
| 制御処理の所要時間 | 129.358秒 |
| 点数分布 | `4 / 3 / 1 = 2 / 7 / 1` |

| 項目 | 点数分布 | 使用量合計 | 使用量中央値 | 所要時間中央値 |
| --- | --- | ---: | ---: | ---: |
| A01 | `4 / 3 = 2 / 3` | 485,721 | 97,186 | 45.639秒 |
| A02 | `3 / 1 = 4 / 1` | 1,502,167 | 344,479 | 110.353秒 |

この数値は優劣、採用、公開判断を意味しない。

## 4結果の比較表示

候補41〜44は互換条件識別値が一致する。比較表示を次へ保存した。

- 保存先: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/task-spec-check-20260720/candidate41-candidate44.json`
- 基準結果: 候補41 `dd8ff05355b64144ac0fa1fd7e0fe489`
- 候補42 / 43 / 44の`quality_score`中央値差: `0.000 / +37.500 / +37.500`
- 全実行`total_tokens`中央値差: `-67,358 / -252,805 / -290,673`
- `elapsed_seconds`中央値差: `-10.030 / -103.661 / -118.650`秒

数値差は優劣、採用、公開判断を表さない。

## 実行記録

- 結果識別子: `cfe97076f1234216b440e2dbb0f8de55`
- 内容SHA-256: `1417184856711b9840de7d518c6d0d4d6abf73ecebe9dfd49defaef24e7d46e9`
- 実行場所: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate44-complete-spec-readiness-boundary-ambiguity-targeted2-global-m10-n5-20260720-r1`
- 登録結果: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/cfe97076f1234216b440e2dbb0f8de55.json`
- 有効 / 採点可能: 10 / 10
- 除外試行: 0

採用、公開、本体反映は未判断・未実施である。非公開の生実行記録、実行単位情報、一時作業領域はリポジトリへ保存しない。
