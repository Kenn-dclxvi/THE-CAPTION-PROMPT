# Candidate43 / Candidate54 evidence-backed control core catalog固定対象試験

## 結論

Candidate54はF05 / F10各`N=5`の10 runすべてでscore `4`、root-only、zero driftを満たした。

一方、Candidate43比でF10のmodel stepは`48 -> 53`、tool callは`43 -> 48`、token合計は`848,388 -> 928,478`、`+9.44%`だった。事前停止条件に該当したため、Candidate54は`catalog_fixed_targeted_n5 / stopped`とする。A01 / A02、standard14、A06へ進めない。

## 固定条件

- Candidate43 result: `53f46f39073c4bf1aa1d7dc8fbc4b892`
- Candidate54 result: `703503d769254f3ab3f302fefd2e3399`
- Candidate54 result content SHA-256: `70f0a5e8a1908ad9736b06411fb15b048d2de0da8cb03984f88a0480e5a1f98d`
- compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `high`
- execution: global queue、`M=10`、各case `N=5`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- excluded attempt: `0`

profile間でprompt identity以外を変更していない。Candidate54の変更対象はroot `AGENTS.md`だけで、残り18 targetはCandidate43とbit identityが同じである。

## 静的差分

| prompt | root `AGENTS.md` bytes | C43差 |
| --- | ---: | ---: |
| Candidate43 | 3,980 | — |
| Candidate54 | 2,525 | -1,455、-36.56% |

Candidate54はA系readiness、F系fixed operation、明示委譲を別領域へ分けた。9項目worker packetは5項目へ縮小し、単独効果を確認できないproducer変更の新TaskSpec化、独立確認の常時規則、recovery counter規則を常時coreから外した。

## KPI view

| prompt | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: |
| Candidate43 | 100.000 | 241,405 | 118.825秒 |
| Candidate54 | 100.000 | 237,235 | 127.584秒 |
| Candidate54 - Candidate43 | 0.000 | -4,170、-1.73% | +8.760秒、+7.37% |

中央値だけでは、case間の相殺を隠す。10 runのtoken合計はCandidate43が`1,179,045`、Candidate54が`1,204,695`で、差は`+25,650`、`+2.18%`だった。

Candidate43はF10の1 runが既知のfinding locationずれでscore `3`、残り9 runがscore `4`だった。Candidate54は10 / 10がscore `4`だった。両者のquality中央値は同じであり、N=5から一般的な品質差へ読み替えない。

## Case別診断

| case | 指標 | Candidate43 | Candidate54 | 差 |
| --- | --- | ---: | ---: | ---: |
| F05 | token合計 | 330,657 | 276,217 | -54,440、-16.46% |
| F05 | model step / tool call | 22 / 17 | 19 / 14 | -3 / -3 |
| F05 | elapsed中央値 | 33.201秒 | 31.577秒 | -1.623秒 |
| F10 | token合計 | 848,388 | 928,478 | +80,090、+9.44% |
| F10 | token中央値 | 210,270 | 206,621 | -3,649、-1.74% |
| F10 | model step / tool call | 48 / 43 | 53 / 48 | +5 / +5 |
| F10 | shell command | 55 | 56 | +1 |
| F10 | elapsed中央値 | 85.624秒 | 101.300秒 | +15.676秒、+18.31% |

F10のtool call経路はCandidate43が`11 / 3 / 11 / 11 / 7`、Candidate54が`11 / 6 / 11 / 11 / 9`だった。Candidate54はCandidate53の`11 / 11 / 5 / 11 / 11`より短い経路を増やしたが、Candidate43の3 callと7 callの経路までは戻していない。

shell commandは55から56への1件増加に留まる。Candidate54の差は調査対象を大きく増やしたことより、同じreadを複数model stepとtop-level tool callへ分けたことにある。

### 3 call経路と6 call経路

F10 iteration 2では、Candidate43とCandidate54が同じ開始確認5 commandを最初のtool callへまとめた。その後の分岐は次のとおりだった。

| 段 | Candidate43 | Candidate54 |
| --- | --- | --- |
| 1 | 開始identity 5 command | 同左 |
| 2 | root authority、src authority、固定diff、changed file、engineの5 readを一つのtool callで取得 | authority 2 read |
| 3 | 最終status | 固定diff |
| 4 | — | changed fileとengine |
| 5 | — | 既知tokenの追加`git grep` |
| 6 | — | 最終status |

Candidate54は、TaskSpecで最初から固定されていたauthority、diff、source evidenceを三段へ分け、さらに確認用`git grep`を追加した。成果と最終shell command集合の大部分は同じだが、evidence acquisitionを一つのoperationとして確定せず、各read後に次のread要否を再判断した。

F10 iteration 5でもshell commandは両者11件だったが、Candidate43は7 tool call、Candidate54は9 tool callだった。したがって、追加commandだけでは+5 model step / tool callを説明できない。

## 判断

事実として、要素分別後の最小coreでもF05 / F10の成果品質は10 / 10で成立した。

事実として、prompt byte数`-36.56%`と全体token中央値`-1.73%`だけでは、F10のroute分布とtoken合計の増加を検出できない。

判断として、`F1 / F5 / F9`、9項目packet、`R1 / R2`を一括で戻す根拠はない。F10はroot-onlyでD系とR系を適用せず、C52で`F9`を単独復元してもroutingは改善していない。

次に確認する対象は、C43の3 / 7 tool call経路とCandidate54の6 / 9 tool call経路の分岐点である。新candidateを先に作らず、同じshell readを一つのtool callへまとめた判断と、分割した判断の直前traceを比較する。

推測として、目的分別をruntime promptの三つのsectionへそのまま投影したことが、readiness、fixed operation、delegationを実行phaseとして順番に再評価させた可能性がある。Candidate53とCandidate54の両方で短いF10経路が減ったことはこの推測と整合するが、section見出しだけのablationはないため事実とはしない。

次の設計目標は、A / F / Dの分別を分析上は維持しつつ、runtime promptではphase列ではなく一つの条件付きoperation graphとして表すことである。新candidateを作る前に、消す判断点を「固定済みauthority、diff、sourceを取得するたびに次のread要否を再判定すること」として固定する。

## Evidence

- Candidate54 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate54-evidence-backed-control-core-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-20260721-r1`
- comparison view: campaign直下`comparison-c43-c54.json`
- design: [`Candidate54 evidence-backed control core`](../../docs/candidate54-evidence-backed-control-core-design.md)
- classification: [`Candidate43制御要素の目的別分別`](../../docs/candidate43-control-element-classification.md)

candidate作成、対象試験、採用、release、本体反映は別状態である。Candidate54は対象試験で停止し、採用、release、本体反映は未判断、未実施である。
