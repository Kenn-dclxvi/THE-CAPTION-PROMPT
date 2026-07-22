# Candidate43 / Candidate65 shared operation core catalog固定 F系 N=5

## 結論

Candidate65はF05 / F10の10 / 10 runでscore `4`を維持し、全runがroot-onlyだった。root `AGENTS.md`もCandidate43の`3,980 bytes`から`3,701 bytes`へ`279 bytes`、`7.01%`縮小した。

一方、事前停止条件にしたF10は、Candidate43比でtop-level tool callが`43 -> 49`、model stepが`48 -> 54`、all-agent token合計が`848,388 -> 969,284`へ増えた。3条件すべてを超えたため、Candidate65は`targeted_evaluated / stopped`とする。用意済みのA01 / A02、D01 profileは実行せず、Candidate65へ補助predicateを追加しない。

32 source clauseを重複なしの11 labelへ対応させる静的整理は、F系の成果を壊さなかった。しかし、bytes削減だけではtop-level tool cycleを維持できなかった。次に検討する場合はCandidate43の一層9 label、label順、clause所属を変えず、同一label内の表面表現だけを短くする。

## 固定条件

- Candidate43: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate43 bundle SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- Candidate65: `the-caption-3ce91a4-shared-operation-core-r1`
- Candidate65 bundle SHA-256: `2f3da313b82f0e2085e23b6d040a64bee892870a221e3b4158a612dfb8ec4eff`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- Layer 1 identity: `1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90`
- compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- memories / apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- repetition: F05 / F10各`N=5`
- excluded attempt: 0

Candidate65 profileはCandidate43 catalog固定profileから`profile_id`と`prompt_set_identity`だけを変更した。Layer 1、target、model、Agent環境、permission、TaskSpec、fixture、executor parameter、反復条件は同一である。

## KPI

| 指標 | Candidate43 | Candidate65 | Candidate65 - Candidate43 |
| --- | ---: | ---: | ---: |
| score `4` | 9 / 10 | 10 / 10 | +1 |
| F系token合計 | 1,179,045 | 1,252,067 | +73,022（+6.19%） |
| 反復別token中央値 | 241,405 | 263,931 | +22,526（+9.33%） |
| 反復別elapsed中央値 | 118.825秒 | 117.273秒 | -1.551秒（-1.31%） |

Candidate43のscore `3` 1件は、F10の主要findingを得たが指摘位置が実変更行と一致しなかった既存観測である。Candidate65は10 / 10で所定response、zero drift、許可範囲を満たした。この`N=5`を範囲外へ一般化しない。

case別の値は次のとおりである。

| case | token合計 C43 | token合計 C65 | token差 | elapsed中央値 C43 | elapsed中央値 C65 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F05 | 330,657 | 282,783 | -47,874（-14.48%） | 33.201秒 | 35.189秒 |
| F10 | 848,388 | 969,284 | +120,896（+14.25%） | 85.624秒 | 95.975秒 |

## F10停止判定

| 指標 | Candidate43 | Candidate65 | 差 |
| --- | ---: | ---: | ---: |
| top-level tool call | 43 | 49 | +6（+13.95%） |
| model step | 48 | 54 | +6（+12.50%） |
| all-agent token合計 | 848,388 | 969,284 | +120,896（+14.25%） |
| all-agent token中央値 | 210,270 | 213,435 | +3,165（+1.51%） |
| elapsed中央値 | 85.624秒 | 95.975秒 | +10.351秒（+12.09%） |
| worker / SA session | 0 | 0 | 0 |

iteration順のtool callはCandidate43 `11 / 3 / 11 / 11 / 7`、Candidate65 `11 / 12 / 11 / 11 / 4`だった。model stepはCandidate43 `12 / 4 / 12 / 12 / 8`、Candidate65 `12 / 13 / 12 / 12 / 5`だった。

保存command evidence上のshell commandはCandidate43 `50`件、Candidate65 `51`件である。増加の中心は証拠command数ではなく、同じ開始identity確認とsource readを複数のtop-level tool cycleへ分けた回数だった。Candidate43は5 run中2 runが短いcycleへ収束し、Candidate65は1 runだった。

F10のtoken差`120,896`のうちinput token差は`118,836`で`98.30%`を占めた。tool cycle増加により、それまでのinput contextを後続stepへ再入力した観測と整合する。ただし、`N=5`のroute分布だけで個々の文がbatchingを変えた因果までは確定しない。

静的にはCandidate65が`7.01%`短いのにF10 tokenは`14.25%`多い。したがって、prompt byte数をruntime圧縮の代用指標にはできない。

## 判断と次の対象

事実として、Candidate65はF系10 / 10の成果品質とroot-only routeを保持した。事実として、F10のtool call、model step、tokenは事前上限をすべて超えた。

Candidate65は停止し、A / D、standard14、採用、release、本体反映へ進めない。Candidate65の11 labelへ条件を足して修正しない。

次の変更を作る前に、対象を次へ限定する。

1. Candidate43の一層9 labelとlabel順を保持する。
2. source clauseを別labelへ移さず、見出しも追加しない。
3. 同一label内の重複主語、接続語、言換えだけを削る。
4. 32 source clauseの意味対応とroot bytes減少を静的に確認する。
5. 同じF10 `N=5` gateを最初に実行し、上限超過ならA / Dへ進まない。

これは次candidateの作成承認ではなく、Candidate65の結果から限定した次の検討境界である。

## 登録証跡

| prompt | result ID | result content SHA-256 | final evidence archive SHA-256 |
| --- | --- | --- | --- |
| Candidate43 | `53f46f39073c4bf1aa1d7dc8fbc4b892` | `1c91cd9edaf8b47776c63f2e69bc9c47260fb1476a821eb185fded5011c69a96` | `6aaac40bc057662c41187197a8eed7df91cfa720eb650fe5fc23471bf85be595` |
| Candidate65 | `fb74c1db991e4a19920eb4c25cb7bb55` | `2c280fda2815a334ba0ea3dd3c85a55b8ce0c098f361e5c666779f66413ebe46` | `775183444472016865dc3fd249cfb1b05cc51db90c2be38ebcddb221be5c4c14` |

comparison view:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate65-f05-f10-catalog-fixed-n5-20260722-r1.json`

Candidate65の採用、release、本体反映は未判断、未実施である。
