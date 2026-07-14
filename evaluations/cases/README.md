# Evaluation set overview

## 目的

THE-CAPTIONで開発作業を行うAgent向けpromptを、少ない手間で繰り返し比較する。

CONTEXT、CHRONICLEなどruntime内の生成promptは対象にしない。

## 評価セット

評価セットには、THE-CAPTIONで実際に発生した代表的な開発タスクを使う。最初から網羅性を求めず、短時間で繰り返せる小さなセットから始める。

1 caseで基盤が必要とするのは次だけとする。

- case ID
- 開始時のrepository fixture
- adapterへ渡すopaqueなpayload

task、期待する目的、model-visible入力などの可変fieldはpayload内へカプセル化する。基盤はpayloadを解釈しない。exact postimageや細かな採点項目は必須にせず、test結果、diff、変更path、最終応答など、取得できる実行結果を採点材料にする。

## 採点

quality raterが成果全体を見て、caseごとに1つのscoreを付ける。

| score | 意味 |
| ---: | --- |
| 4 | 目的を十分に達成している |
| 3 | ほぼ達成している |
| 2 | 一部を達成している |
| 1 | わずかな進展だけがある |
| 0 | 目的を達成していない |

複数観点への分解、重み付け、機械的な合否判定は行わない。quality raterにはprompt identityとA / Bの名称を見せない。

全caseのscoreを0から100へ正規化した値を`quality_score`とする。quality raterはscoreと短い事実根拠だけを返す。

prompt set A / Bのwinnerは、`quality_score`、`total_tokens`、`elapsed_seconds`の3 KPIだけで決める。

quality raterは改善提案、修正、再実行、A / Bの選択を行わない。

## 増やし方

評価セットへcaseを追加するのは、既存セットでは見えない失敗が実際に見つかったときだけとする。先回りしてcase分類や網羅表を作らない。

日常の改善では同じ小さなセットを使う。このセットでpromptを調整した結果を、そのまま未使用caseでの最終確認結果とは扱わない。

## 現在の状態

評価セットの考え方と実行基盤を定義した段階であり、case本体とpromptは未作成である。
