# Candidate43 / Candidate55 prebound operation graph catalog固定対象試験

## 結論

Candidate55はF05 / F10各`N=5`の10 runすべてでscore `4`、root-only、zero driftを満たした。

Candidate43比でF10のmodel stepは`48 -> 38`、tool callは`43 -> 33`、token合計は`848,388 -> 684,532`、`-19.31%`だった。C54で失われた固定済みpredicate・permission・constraintの実行前bindingを戻す方向は、段階的な再判断の削減と整合する。

一方、F10のshell commandは`55 -> 61`へ6件増えた。事前gateはCandidate43以下を通過条件としていたため、Candidate55は`catalog_fixed_targeted_n5 / stopped`とする。A01 / A02、standard14、A06へ進めない。

## 固定条件

- Candidate43 result: `53f46f39073c4bf1aa1d7dc8fbc4b892`
- Candidate55 result: `d873e7b0a647434487cbbfc5c26acd99`
- Candidate55 result content SHA-256: `7365ad6696d93fa8d4863cc8e92710ae5b1eb270024bc2d25ae04e7ab6c788c7`
- compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `high`
- execution: global queue、`M=10`、各case `N=5`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- excluded attempt: `0`

profile間でprompt identity以外を変更していない。Candidate55の変更対象はroot `AGENTS.md`だけで、残り18 targetはCandidate43とbit identityが同じである。

## 静的差分

| prompt | root `AGENTS.md` bytes | C43差 |
| --- | ---: | ---: |
| Candidate43 | 3,980 | — |
| Candidate55 | 2,673 | -1,307、-32.84% |

Candidate55はA系、F系、条件付きD系を別sectionへ並べない。初回predicate前にTaskSpecで確定済みの`required outcome / predicate / permission / constraint`を一つのoperationへbindする関係を復元した。tool API、command結合、read順序は指定していない。

## KPI view

| prompt | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: |
| Candidate43 | 100.000 | 241,405 | 118.825秒 |
| Candidate55 | 100.000 | 193,015 | 107.440秒 |
| Candidate55 - Candidate43 | 0.000 | -48,390、-20.05% | -11.385秒、-9.58% |

10 runのtoken合計はCandidate43が`1,179,045`、Candidate55が`1,007,105`で、差は`-171,940`、`-14.58%`だった。

Candidate43はF10の1 runが既知のfinding locationずれでscore `3`、残り9 runがscore `4`だった。Candidate55は10 / 10がscore `4`だった。N=5の差を一般的な品質差へ読み替えない。

## Case別診断

| case | 指標 | Candidate43 | Candidate55 | 差 |
| --- | --- | ---: | ---: | ---: |
| F05 | token合計 | 330,657 | 322,573 | -8,084、-2.44% |
| F05 | token中央値 | 75,024 | 73,210 | -1,814、-2.42% |
| F05 | model step / tool call | 22 / 17 | 22 / 17 | 0 / 0 |
| F05 | shell command | 20 | 20 | 0 |
| F05 | elapsed中央値 | 33.201秒 | 31.152秒 | -2.049秒、-6.17% |
| F10 | token合計 | 848,388 | 684,532 | -163,856、-19.31% |
| F10 | token中央値 | 210,270 | 120,083 | -90,187、-42.89% |
| F10 | model step / tool call | 48 / 43 | 38 / 33 | -10 / -10 |
| F10 | shell command | 55 | 61 | +6 |
| F10 | elapsed中央値 | 85.624秒 | 82.240秒 | -3.384秒、-3.95% |

F10のtool call経路はCandidate43がiteration順に`11 / 3 / 11 / 11 / 7`、Candidate55が`3 / 11 / 3 / 5 / 11`だった。Candidate55は3-call経路を1件から2件へ増やし、総tool callを10件減らした。全runを3-callへ固定したわけではない。

## Shell command増分

F10 iteration 4だけが標準の11 commandではなく17 commandを実行した。増分6件は許可範囲内で、次の再取得だった。

- changed fileとengineを全体取得した後の、line番号付き範囲readが4件。
- 終了status 1回に加えた途中statusが2件。

別path、test、application、dependency、network、workerへ探索を広げていない。このrunも5 tool call、120,083 tokensであり、Candidate43 iteration 4の11 tool call、212,342 tokensより小さかった。

事実として、command増分はtop-level context再送の増加にならなかった。事実として、事前gateはcommand数もCandidate43以下と定めていた。結果を見た後にgateを緩めず、Candidate55を停止する。

## 判断

事実として、C54で削った`predicate / permission / constraint`の事前bindingは、単なる説明重複ではなかった。復元後のCandidate55は、C43より短いroot promptのままF10のmodel step、tool call、tokenを減らした。

事実として、A系readinessとF系fixed operationの境界は維持できた。readinessは未確定値の開始禁止、fixed operationは開始前に確定済み入力を一つのoperationへbindする責務であり、三sectionを順に処理するphaseにはしていない。

判断として、次にprompt文を追加する根拠はまだない。残るcommand増分は一つのrunで発生したline evidenceの再取得であり、C55のoperation graph不足か、N=5内の経路変動かを現結果だけでは分離できない。

次の設計対象はcandidateではなくgateである。shell commandの単純合計と、model stepを増やす逐次再取得を分け、どの観測をcandidate停止条件にするかを新しい評価profile revisionの実行前に固定する。Candidate55の保存済みresultと事前gateは変更しない。

## Evidence

- Candidate55 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate55-prebound-operation-graph-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-20260721-r1`
- comparison view: campaign直下`comparison-c43-c55.json`
- design: [`Candidate55 prebound operation graph`](../../docs/candidate55-prebound-operation-graph-design.md)
- classification: [`Candidate43制御要素の目的別分別`](../../docs/candidate43-control-element-classification.md)

candidate作成、対象試験、採用、release、本体反映は別状態である。Candidate55は対象試験で停止し、採用、release、本体反映は未判断、未実施である。
