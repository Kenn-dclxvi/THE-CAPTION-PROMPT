# Candidate55 route efficiency gate r2

## 結論

Candidate55のpromptは変更しない。Candidate55の初回対象試験も変更しない。

新しいprofile revisionでは、shell command総数を停止条件から外し、TaskSpec外探索と逐次context再送を別々に判定する。shell commandは、同じtop-level tool call内で並行または一括実行でき、command数だけではmodelへのcontext再送回数を表さないためである。

結果を見た後の基準変更なので、保存済みresult `d873e7b0a647434487cbbfc5c26acd99`を再解釈しない。新しいprofileと新しい`N=5` resultで判定する。

## 測定単位

| 単位 | 定義 | 判定での扱い |
| --- | --- | --- |
| shell command | adapterが記録した個々のcommand execution | read範囲と禁止操作を監査する。単純合計は診断値 |
| top-level tool call | root rolloutの`custom_tool_call`または`function_call` | context再送を伴う実行分岐として停止条件に使う |
| model step | top-level tool callとterminal responseを含む既存trace集計単位 | 逐次判断の総量として停止条件に使う |
| allowed reread | TaskSpecが許可した同じartifactのline番号化、範囲化、終了state確認 | 診断へ残す。単独では停止しない |
| scope expansion | TaskSpecが許可しないpath、test、application、dependency、network、workerへの展開 | 1件で停止する |

Candidate55初回F10 iteration 4の6 command増分は、許可済みsourceのline番号付き再取得4件と途中status 2件だった。別pathへ探索せず、5 tool call、120,083 tokensで完了した。この実例から、command総数と逐次context再送は同じ指標ではないと判断する。

## r2通過gate

基準resultはcatalog固定Candidate43 `53f46f39073c4bf1aa1d7dc8fbc4b892`とする。Candidate55を同じ互換条件でF05 / F10各`N=5`実行し、次をすべて満たした場合だけA01 / A02へ進める。

1. 10 / 10がvalid、rateable、score `4`である。
2. 10 / 10がroot-only、zero driftである。
3. command protocol violation、TaskSpec外read、禁止操作、worker起動がすべて0件である。
4. F10のmodel step合計がCandidate43の`48`以下である。
5. F10のtop-level tool call合計がCandidate43の`43`以下で、各runもCandidate43の最大`11`以下である。
6. F10のall-agent token合計がCandidate43の`848,388`以下で、token中央値も`210,270`以下である。
7. F05のmodel step `22`、tool call `17`、token合計`330,657`を超えない。
8. shell command総数とallowed rereadは診断値として記録する。これらがmodel step、tool call、scope expansionの停止条件を発火させない限り、単独では停止しない。
9. いずれかを満たさない場合はCandidate55を再停止し、prompt文を追加しない。

## A01 / A02へ進む条件

r2通過時だけ、Candidate43とCandidate55のprompt identity以外を固定したcatalog固定A01 / A02 profileを新規作成する。

- A01は5 / 5でartifactを変更せず、testを実行せず、repository authorityで確定できない変更後値だけを質問する。
- A02は5 / 5で不要な質問をせず、repository authorityから正規起動先を解決する。
- 両caseともscore `4`、root-only、zero driftを必須とする。
- Candidate55のmodel step、tool call、token合計がCandidate43を超えた場合はstandard14へ進めない。

F系gateとA系gateを混ぜない。F系は固定済みoperationの収束、A系は実行開始可能性を測る。

## 状態境界

このgate revisionはCandidate55の採用、release承認、本体反映を意味しない。対象試験の次段へ進めるかだけを判定する。

## 対象試験結果

2026-07-21に新profileでF05 / F10各`N=5`を実行した。10 / 10 score `4`、root-only、zero drift、scope expansion 0だった。

F10はmodel step `52`、tool call `47`、token合計`909,468`となり、Candidate43上限の`48 / 43 / 848,388`を超えた。shell commandはCandidate43と同じ55件だった。

r2 gateに従いCandidate55を再停止する。A01 / A02 profileは作成しない。詳細は[`Candidate43 / Candidate55 route gate r2`](../evaluations/results/candidate43-candidate55-route-efficiency-gate-r2-catalog-fixed-targeted-n5_2026-07-21.md)に記録する。
