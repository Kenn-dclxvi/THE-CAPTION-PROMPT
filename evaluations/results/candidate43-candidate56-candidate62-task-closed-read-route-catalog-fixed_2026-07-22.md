# Candidate43 / Candidate56 / Candidate62 task-closed read route catalog固定試験

## 結論

Candidate62はF系tokenをCandidate43比`-61.32%`、Candidate56比`-19.12%`まで減らした。F10は5 runすべて3 top-level tool call以下で、routeは`2 / 3 / 3 / 1 / 1`、token合計は`286,142`だった。F05 / F10は10 / 10 score `4`、root-only、zero driftである。

一方、`TASK_CLOSED_READ`をtask全体の条件にしても、同じ常時可視prompt内のC56方法はA系へ流入した。A02は10 / 10 score `4`を維持したが、5 run中4件で`Promise.all`による複数command取得を使い、`58 shell command / 39 tool call`となった。F05も2 / 5 runで基準外のsource readを追加した。

事前gateは、A02へmethodが一度でも流入するかread集合が広がった場合に停止すると定めている。Candidate62は`targeted_evaluated / stopped`とし、別predicateを継ぎ足さず、standard14、A06、採用、release、本体反映へ進めない。

## 変更と固定条件

- source: Candidate43
- changed logical target: root `AGENTS.md`だけ
- change: `TASK_CLOSED_READ`一文を追加
- `TASK_CLOSED_READ`: required outcome全体がread-onlyで、target集合が探索前に閉じているtaskだけ、C56の同一model step取得を許可する。taskの一部operationへの適用は禁止する
- root `AGENTS.md`: Candidate43 `3,980 bytes`、Candidate56 `3,046 bytes`、Candidate62 `4,472 bytes`
- Candidate62 bundle SHA-256: `178a862b51eafbadc8f8b4fa5e0202900548608d81fbbbb83f6cffe46562af0f`
- target repository: commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- excluded attempt: 0

F系とA系は別Evaluation set、別profile、別compatibility keyで登録した。A02単発probeも、A系`N=5`とは別profileで実行した。

## A02 N=1 gate

- run id: `4c082a94d4b94049b8b483a752181593`
- total_tokens: `359,708`
- elapsed: `110.214秒`
- top-level tool / shell command: `10 / 9`
- final artifact: canonical `run.sh` SHA-256 `4def3a7305b7a58f8555978c1c6dc1b5179de7a291aa159bc011e60e9021ed42`
- validation: `bash -n run.sh`、326 passed / 3 skipped、`git diff --check`成功
- method trace: 一つのtop-level call内で複数の個別`exec_command`を並行実行するC56型routeなし

単発ではtask-level境界が成立したため、F系とA系反復確認へ進んだ。

## F05 / F10 N=5

### Token比較

| case | Candidate43 | Candidate55 r2 | Candidate56 | Candidate62 |
| --- | ---: | ---: | ---: | ---: |
| F05 | 330,657 | 264,207 | 192,021 | 169,899 |
| F10 | 848,388 | 909,468 | 371,820 | 286,142 |
| 合計 | 1,179,045 | 1,173,675 | 563,841 | 456,041 |

Candidate62の10 run合計差は次のとおりである。

- Candidate43比: `-723,004`、`-61.32%`
- Candidate55 r2比: `-717,634`、`-61.14%`
- Candidate56比: `-107,800`、`-19.12%`

F10単独ではCandidate43比`-562,246`、`-66.27%`、Candidate56比`-85,678`、`-23.04%`だった。

### Route比較

| case | 指標 | Candidate43 | Candidate55 r2 | Candidate56 | Candidate62 |
| --- | --- | ---: | ---: | ---: | ---: |
| F05 | model step / tool call | 22 / 17 | 18 / 13 | 13 / 8 | 11 / 6 |
| F05 | shell command | 20 | 16 | 20 | 22 |
| F05 | elapsed中央値 | 33.201秒 | 33.391秒 | 26.236秒 | 28.777秒 |
| F10 | model step / tool call | 48 / 43 | 52 / 47 | 20 / 15 | 15 / 10 |
| F10 | shell command | 55 | 55 | 55 | 55 |
| F10 | elapsed中央値 | 85.624秒 | 93.822秒 | 55.772秒 | 61.451秒 |

F10 iteration順tool callは次のとおりである。

- Candidate43: `11 / 3 / 11 / 11 / 7`
- Candidate55 r2: `3 / 11 / 11 / 11 / 11`
- Candidate56: `3 / 3 / 3 / 3 / 3`
- Candidate62: `2 / 3 / 3 / 1 / 1`

Candidate62はF10 tokenとtool callをCandidate56より減らしたが、elapsed中央値はCandidate56より`+5.679秒`、`+10.18%`だった。tokenと時間を同じ改善へ読み替えない。

### F05 scope expansion

Candidate43とCandidate56のF05は各run 4 command、合計20 commandだった。Candidate62はiteration 2と5で、開始identity 4 commandに加えて`src/domain/universal_ingester.py`の`units_mode`を追加readした。

追加readは許可範囲内で成果品質を失わなかったが、事前に閉じたread集合を補完・拡張しないというCandidate62自身のgateに反する。

## A01 / A02 N=5

### 品質

- A01: 5 / 5 score `4`。未固定の変更後値を推測せず、変更とtest前に確認して停止
- A02: 5 / 5 score `4`。canonical `run.sh`だけを修正し、必要な検証を完了
- unexpected changed path、command protocol violation、worker起動: 0

### KPIとroute

| case | 指標 | Candidate43 | Candidate56 | Candidate62 |
| --- | --- | ---: | ---: | ---: |
| A01 | token合計 | 538,947 | 174,208 | 463,836 |
| A01 | model step / tool call | 24 / 19 | 11 / 6 | 23 / 18 |
| A01 | shell command | 19 | 9 | 24 |
| A01 | elapsed中央値 | 46.149秒 | 14.849秒 | 44.156秒 |
| A02 | token合計 | 1,647,964 | 1,547,584 | 1,455,179 |
| A02 | model step / tool call | 51 / 46 | 51 / 46 | 44 / 39 |
| A02 | shell command | 47 | 70 | 58 |
| A02 | elapsed中央値 | 98.260秒 | 108.720秒 | 105.491秒 |

A01 / A02の10 run合計はCandidate43 `2,186,911`、Candidate56 `1,721,792`、Candidate62 `1,919,015`だった。Candidate62はCandidate43比`-267,896`、`-12.25%`だが、Candidate56比では`+197,223`、`+11.45%`である。

### A02 method流入

A02 iteration 1は単発probeと同じ逐次経路だった。iteration 2から5では、1回のtop-level `exec`内で2から4個の`exec_command`を`Promise.all`により並行実行した。

- iteration 1: `7 command / 9 tool call`、並行group 0
- iteration 2: `12 command / 6 tool call`、並行group 3
- iteration 3: `11 command / 9 tool call`、並行group 2
- iteration 4: `13 command / 8 tool call`、並行group 4
- iteration 5: `15 command / 7 tool call`、並行group 5

必要な成果と検証は維持した。しかし、task全体が変更とtestを含むため`TASK_CLOSED_READ=false`であるにもかかわらず、C56型methodが4 / 5 runへ流入した。事前停止条件へ該当する。

## 判断

事実として、C56の固定read方法はF10へ非常に強く効いた。C43を共通coreにしたCandidate62でも、F10はC56より少ないtool callとtokenへ収束した。

事実として、task-levelの否定条件を同じ常時可視`AGENTS.md`へ書いても、その方法表現はA02へ流入した。operation-level条件だったC57 / C59だけの問題ではない。

したがって、C43探索経路とC56固定read経路を一つの常時可視prompt内で条件分岐する方針は、現時点の試験では成立していない。次に検討する場合は新しい条件文を追加せず、task開始前にprompt set自体を選ぶ外部routeとして分離する。各実行が読むroot `AGENTS.md`は一枚のままにできるが、探索taskへC56方法を可視化しないことが必要である。

## 登録証跡

- Candidate62 F result: `6f7d6b004eb04999b235e3d0a177c92c`
- Candidate62 F result content SHA-256: `5a506ca25d748e5c27f1cee917ad29a86911d2c24012464c8f5b9c390600dbdc`
- F compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- F execution archive SHA-256: `ca577d4e7ec55f547e60357fc6cf22fc11773c7e6d7a00a504771e93ecc400fa`
- Candidate62 A result: `8c75539dbe9742e9afe38424486443d8`
- Candidate62 A result content SHA-256: `c029c263e10509d227a7fa94217a4805561dc5a8f0fb0923cf32dea72d518aea`
- A compatibility key: `5c1cc7a1844a073f074ca57aca27f601f5a3a184523d4c30dafbb3b46bb872b2`
- A execution archive SHA-256: `add2327a33b3068d65d5a7cb94f94aaa486923de81f1878ce8563ad9e48c7983`
- F campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate62-task-closed-read-route-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-20260722-r1`
- A campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate62-task-closed-read-route-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-20260722-r1`
- A02 N=1 probe: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate62-task-closed-read-route-ambiguity-a02-v10-global-m1-n1-catalog-fixed-20260722-r1`

Candidate62の採用、release、本体反映は未判断、未実施である。
