# Candidate43 / Candidate55 route efficiency gate r2 catalog固定対象試験

## 結論

Candidate55 route gate r2は停止した。

10 / 10がscore `4`、root-only、zero driftで、command protocol violation、TaskSpec外read、禁止操作、worker起動は0件だった。一方、F10はmodel step `48 -> 52`、top-level tool call `43 -> 47`、token合計`848,388 -> 909,468`となり、事前gateの三条件を超えた。

shell commandはCandidate43と同じ55件だった。Candidate55 r1では61 commandでも33 tool callだったが、r2は55 commandで47 tool callだった。command総数と逐次context再送を分離したr2 gateは、今回の差を正しく検出した。

A01 / A02、standard14、A06へ進めない。Candidate55のpromptへ文を追加しない。

## 固定条件

- Candidate43 result: `53f46f39073c4bf1aa1d7dc8fbc4b892`
- Candidate55 r2 result: `04535c8c435e4a5ead57851a4471d0b1`
- Candidate55 r2 result content SHA-256: `27f95d71a010ad7528a2245aa1a8e1bd3f0b6eb8a63c3199dc5c6645e5a474ab`
- Candidate55 r1 result: `d873e7b0a647434487cbbfc5c26acd99`
- compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `high`
- execution: global queue、`M=10`、各case `N=5`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- excluded attempt: `0`

r1とr2は同じCandidate55 bundle、prompt revision、comparison conditionsを使う。結果後のgate変更を既存resultへ適用しないため、profile identity、campaign、resultだけを新しくした。

## KPI view

| prompt | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: |
| Candidate43 | 100.000 | 241,405 | 118.825秒 |
| Candidate55 r2 | 100.000 | 281,603 | 128.947秒 |
| Candidate55 r2 - Candidate43 | 0.000 | +40,198、+16.65% | +10.122秒、+8.52% |

10 runのtoken合計はCandidate43が`1,179,045`、Candidate55 r2が`1,173,675`で、差は`-5,370`、`-0.46%`だった。case間の相殺があるため、全体合計や中央値だけでF10 gateを判定しない。

## Case別診断

| case | 指標 | Candidate43 | Candidate55 r2 | 差 |
| --- | --- | ---: | ---: | ---: |
| F05 | token合計 | 330,657 | 264,207 | -66,450、-20.10% |
| F05 | token中央値 | 75,024 | 73,442 | -1,582、-2.11% |
| F05 | model step / tool call | 22 / 17 | 18 / 13 | -4 / -4 |
| F05 | shell command | 20 | 16 | -4 |
| F05 | elapsed中央値 | 33.201秒 | 33.391秒 | +0.190秒、+0.57% |
| F10 | token合計 | 848,388 | 909,468 | +61,080、+7.20% |
| F10 | token中央値 | 210,270 | 208,612 | -1,658、-0.79% |
| F10 | model step / tool call | 48 / 43 | 52 / 47 | +4 / +4 |
| F10 | shell command | 55 | 55 | 0 |
| F10 | elapsed中央値 | 85.624秒 | 93.822秒 | +8.198秒、+9.57% |

F05はr2 gateの上限をすべて満たした。F10はtoken中央値だけがCandidate43以下で、model step合計、tool call合計、token合計が停止条件に該当した。

## Route分布

F10のiteration順tool call経路は次のとおりだった。

| result | i1 | i2 | i3 | i4 | i5 | 合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate43 | 11 | 3 | 11 | 11 | 7 | 43 |
| Candidate55 r1 | 3 | 11 | 3 | 5 | 11 | 33 |
| Candidate55 r2 | 3 | 11 | 11 | 11 | 11 | 47 |

Candidate55 r2は各run最大11というgateは満たしたが、4 / 5 runが11-call経路となった。Candidate55 r1の短経路は同じpromptと互換条件の新しい5反復で安定して再現しなかった。

同じ11-call経路のCandidate55 r2平均tokenは`209,072`である。Candidate43の11-call 3 run平均`211,200`より`-2,128`、`-1.01%`小さい。短いpromptは同じ経路のcostを増やしていない。全体増加は11-call経路の発生数が3件から4件へ増えたことに対応する。

## r1 / r2比較

| F10指標 | Candidate55 r1 | Candidate55 r2 | r2 - r1 |
| --- | ---: | ---: | ---: |
| model step | 38 | 52 | +14 |
| tool call | 33 | 47 | +14 |
| shell command | 61 | 55 | -6 |
| token合計 | 684,532 | 909,468 | +224,936、+32.86% |

shell commandが6件減る一方でtool callとtokenが増えた。shell command総数をprompt効率の停止条件に使わず、scope監査の診断値としたr2の分離は妥当だった。

## 判断

事実として、Candidate55はC54で欠けたoperation事前bindingを復元し、同じ11-call経路ではC43より小さい。しかし、固定済みreadを少数のtop-level callへまとめるrouteは反復間で安定しなかった。

事実として、TaskSpec外探索や禁止操作は発生していない。今回の問題はread集合の拡大ではなく、同じ11 commandを3または11のtop-level callへ分ける実行形の変動である。

次の設計対象はF系だけの方法境界である。readinessが解決済みで、TaskSpecが有限の独立read-only入力を固定しているoperationに限り、それらを一つのmodel stepで取得するpredicateを検討する。authorityを探索中のA系には適用しない。

これはCandidate50の全域`ROOT_BATCH`を戻す提案ではない。Candidate50はA02で探索集合を広げた。次candidateを作る前に、F系適用条件、消すtop-level call、A系非適用をcandidate作成前gateへ固定する。

## Evidence

- Candidate55 r2 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate55-prebound-operation-graph-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-route-gate-r2-20260721-r1`
- comparison view: campaign直下`comparison-c43-c55-route-gate-r2.json`
- gate: [`Candidate55 route efficiency gate r2`](../../docs/candidate55-route-efficiency-gate-r2.md)
- r1 result: [`Candidate43 / Candidate55 prebound operation graph`](candidate43-candidate55-prebound-operation-graph-catalog-fixed-targeted-n5_2026-07-21.md)

Candidate55 r2は対象試験で停止した。採用、release、本体反映は未判断、未実施である。
