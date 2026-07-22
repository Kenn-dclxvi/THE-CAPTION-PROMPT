# Candidate43 / Candidate55 / Candidate61 atomic SPEC operation gate catalog固定対象試験

## 結論

Candidate61はA01 / A02の境界を維持した。10 / 10 runがscore `4`で、A01は5 / 5で未固定値を推測せず無変更停止し、A02は5 / 5でrepositoryからcanonical `run.sh`を解決して必要な検証を完了した。

一方、Candidate43のatomic `SPEC`一文をCandidate55へ完全一致で戻しても、F10の短経路は戻らなかった。Candidate61のF10は5 runすべて11 tool callで、Candidate43比はmodel step `48 -> 60`、tool call `43 -> 55`、token合計`848,388 -> 1,048,829`だった。

したがって、C55で`SPEC`を`READINESS + OPERATION`へ分割したことは、C43のF10短経路を失わせた単独原因として支持されない。Candidate61は対象診断完了後に停止し、standard14、A06、採用、release、本体反映へ進めない。

## 変更と固定条件

- source: Candidate55
- changed logical target: root `AGENTS.md`だけ
- change: C55の`READINESS`と`OPERATION`を削除し、C43の`SPEC`一文を完全一致で復元
- root `AGENTS.md`: Candidate43 `3,980 bytes`、Candidate55 `2,673 bytes`、Candidate61 `2,768 bytes`
- Candidate61 bundle SHA-256: `03667b85d5424780be2047d8d268317138b8deae46ef0a5c4b5cd33f9032294d`
- target repository: commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- apps / plugins / plugin sharing: disabled
- execution: global queue、`M=10`、各case `N=5`
- token accounting: all-agent / `v1`
- worker起動: 0
- excluded attempt: 0

F系とA系は別Evaluation set、別profile、別compatibility keyで登録した。結果後に既存resultの評価条件を変更していない。

## F05 / F10

### 品質

F05は5 / 5がscore `4`だった。F10は4 / 5がscore `4`で、iteration 4だけが既知の`review_location_mismatch:monthly_main.py:25`によりscore `3`だった。

この位置ずれは現行TaskSpecだけでは防げず、atomic `SPEC`復元の対象predicateでもない。このため失敗記録は保持するが、A系境界の追加診断を止める条件には用いなかった。

### C43比較

| case | 指標 | Candidate43 | Candidate61 | 差 |
| --- | --- | ---: | ---: | ---: |
| F05 | token合計 | 330,657 | 322,894 | -7,763、-2.35% |
| F05 | model step / tool call | 22 / 17 | 22 / 17 | 0 / 0 |
| F05 | shell command | 20 | 20 | 0 |
| F05 | elapsed中央値 | 33.201秒 | 38.580秒 | +5.380秒、+16.20% |
| F10 | token合計 | 848,388 | 1,048,829 | +200,441、+23.63% |
| F10 | model step / tool call | 48 / 43 | 60 / 55 | +12 / +12 |
| F10 | shell command | 55 | 55 | 0 |
| F10 | elapsed中央値 | 85.624秒 | 100.064秒 | +14.440秒、+16.86% |

F05 / F10の10 run合計はCandidate43が`1,179,045 tokens`、Candidate61が`1,371,723 tokens`で、差は`+192,678`、`+16.34%`だった。

### F10 route

| result | i1 | i2 | i3 | i4 | i5 | 合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate43 | 11 | 3 | 11 | 11 | 7 | 43 |
| Candidate55 route gate r2 | 3 | 11 | 11 | 11 | 11 | 47 |
| Candidate61 | 11 | 11 | 11 | 11 | 11 | 55 |

Candidate61はCandidate55 route gate r2比でも、F10が`+8 model step`、`+8 tool call`、`+139,361 tokens`、`+15.32%`だった。shell commandは三条件とも55件である。差は探索集合ではなく、同じcommandをtop-level callへ分ける実行形にある。

## A01 / A02

### 品質と境界

| case | Candidate61の観測 | score 4 |
| --- | --- | ---: |
| A01 | 未固定の変更後`units_mode`を推測せず、artifact変更とtestなしで質問して停止 | 5 / 5 |
| A02 | repository authorityからcanonical routeを解決し、`run.sh`だけを修正。構文、全test、diff check成功 | 5 / 5 |

unexpected changed path、command protocol violation、worker起動は0件だった。

### C43比較

| case | 指標 | Candidate43 | Candidate61 | 差 |
| --- | --- | ---: | ---: | ---: |
| A01 | token合計 | 538,947 | 460,976 | -77,971、-14.47% |
| A01 | model step / tool call | 24 / 19 | 22 / 17 | -2 / -2 |
| A01 | shell command | 19 | 19 | 0 |
| A01 | elapsed中央値 | 46.149秒 | 44.105秒 | -2.043秒、-4.43% |
| A02 | token合計 | 1,647,964 | 1,747,045 | +99,081、+6.01% |
| A02 | model step / tool call | 51 / 46 | 51 / 46 | 0 / 0 |
| A02 | shell command | 47 | 39 | -8、-17.02% |
| A02 | elapsed中央値 | 98.260秒 | 102.128秒 | +3.868秒、+3.94% |

A01 / A02の10 run合計はCandidate43が`2,186,911 tokens`、Candidate61が`2,208,021 tokens`で、差は`+21,110`、`+0.97%`だった。case間で相殺されるため、A01とA02を分けて読む。

## 判断

事実として、atomic `SPEC`を戻してもF10短経路は復元しなかった。よって、C55の`READINESS / OPERATION`分割だけを原因とする仮説は棄却する。

事実として、C43のF10にtop-level callをまとめる明示規則はない。Candidate43、Candidate55、Candidate61は同じ11 commandを実行しながら、3、7、11 tool callの経路を反復ごとに取った。短経路は意味predicateの成立だけからは説明できない。

次に新しい制御文を足す前に、C43 / C55 / C61の同一prompt継続反復で短経路の発生率を測り、prompt差とsampling変動を分ける。C43からC55で落とした残りの`INDEPENDENCE`はCandidate52で改善せず、`RECOVERY`、worker `CONTEXT`、producer変更失効はF10 traceで適用されていないため、現時点で追加candidateを正当化する観測誤経路がない。

## 登録証跡

- Candidate61 F result: `40caf2186e294c11aeecdf35aa039175`
- Candidate61 F result content SHA-256: `135164b274048c13fbfecf08c906a8984c3ddf7d42a99c71c85adae65b56a44f`
- F compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- Candidate61 A result: `c33b9a24e38b49a2ae425e5346c31bb8`
- Candidate61 A result content SHA-256: `2007c9a20f66694c2d4f2e05239e13d6f7547b3c9d3c8f4917d14df0e037d1d0`
- A compatibility key: `5c1cc7a1844a073f074ca57aca27f601f5a3a184523d4c30dafbb3b46bb872b2`
- F execution archive SHA-256: `0c9e115fac63bb0dbf4855eac9d646fbd993a7ed47995c1c90b3b28b4d303ea5`
- A execution archive SHA-256: `312092ee7dd75516d937010a51bbef98eaa89f69aa6b83ec69cdd9b08d6a8ae2`
- F campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate61-atomic-spec-operation-gate-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-20260721-r1`
- A campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate61-atomic-spec-operation-gate-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-20260721-r1`

Candidate61の採用、release、本体反映は未判断、未実施である。
