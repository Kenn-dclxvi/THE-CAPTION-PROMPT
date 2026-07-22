# Candidate43 / Candidate58 purpose-bound read route catalog固定A系N=5

## 結論

Candidate58はA系品質を10 / 10 score `4`へ戻したが、A02 route costがCandidate43を超えたため停止した。

repository authority / state探索を一result一decisionへ固定した結果、A02のmodel stepは`51 -> 80`、tool callは`46 -> 75`、shell commandは`47 -> 81`、token合計は`1,647,964 -> 2,130,842`となった。A側の明示route制御costが、抑止した探索batchより大きい。

F05 / F10、standard14、A06、採用、release、本体反映へ進めない。

## 固定条件

- Candidate43 result: `c9c2d55acbd944a2a7026457aa1d6efd`
- Candidate58 result: `0f20c0e0ccc6468ea2d9e010e29dd0f9`
- compatibility key: `5c1cc7a1844a073f074ca57aca27f601f5a3a184523d4c30dafbb3b46bb872b2`
- case: A01 / A02第2版、各`N=5`
- model / reasoning: `gpt-5.6-sol` / `high`
- execution: global queue、`M=10`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- apps / plugins / plugin sharing: disabled
- excluded attempt: `0`

## 結果

| case | 指標 | Candidate43 | Candidate58 | 差 |
| --- | --- | ---: | ---: | ---: |
| A01 | score `4` | 5 / 5 | 5 / 5 | 0 |
| A01 | token合計 | 538,947 | 141,161 | -397,786、-73.81% |
| A01 | model step / tool call | 24 / 19 | 9 / 4 | -15 / -15 |
| A01 | shell command | 19 | 7 | -12 |
| A02 | score `4` | 5 / 5 | 5 / 5 | 0 |
| A02 | token合計 | 1,647,964 | 2,130,842 | +482,878、+29.30% |
| A02 | model step / tool call | 51 / 46 | 80 / 75 | +29 / +29 |
| A02 | shell command | 47 | 81 | +34、+72.34% |
| A02 | elapsed中央値 | 98.260秒 | 131.248秒 | +32.988秒、+33.57% |

10 run合計tokenは`2,186,911 -> 2,272,003`、`+85,092`、`+3.89%`だった。A01の減少がA02増加の一部を相殺しているため、全体中央値だけで通過としない。

## 判断

Candidate57はF系methodの非適用だけを書き、A系parallel readを止められなかった。Candidate58はA系routeを直接書き、探索集合の並列拡大を止めたが、逐次context再送を増やした。

次の境界はAの方法を指定しない。operation全体が`edit=false`、`test=false`、`dependency=false`で、TaskSpecが許可readとread-only validationを実行前に有限列挙した場合だけをF系methodの適用対象とする。一条件でも欠けるA系operationは、既存のC43 routeへ委ねる。

## Evidence

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate58-purpose-bound-read-route-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-20260721-r1`
- comparison: campaign直下`comparison-c43-c58-a.json`

Candidate58は対象試験で停止した。candidate作成、評価、採用、release、本体反映は別状態である。
