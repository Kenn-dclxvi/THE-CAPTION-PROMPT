# Candidate43 / Candidate66 topology-preserving compression catalog固定 N=5

## 結論

Candidate66はCandidate43の一層9 label、label順、32 clauseの所属を変えず、root `AGENTS.md`を`3,980 bytes`から`3,923 bytes`へ`57 bytes`、`1.43%`短くした。

F10-only、A01 / A02、F05 / F10、明示producer D01の合計30 runはすべてscore `4`だった。A / Fの25 runはroot-onlyだった。D01は5 / 5で指定workerだけがreviewを実行し、rootによるreview対象の再読はなかった。表面圧縮による意味欠落は、この観測範囲では確認しなかった。

一方、実行時削減は再現しなかった。最初のF10-only `N=5`ではCandidate43比でtool call `40 -> 39`、model step `29 -> 28`、token合計`-2.04%`となり事前gateを通過した。しかし、追加したF05 / F10 set内のF10 `N=5`ではtool call `43 -> 57`、model step `48 -> 62`、token合計`+31.36%`となった。

したがって、Candidate66は`targeted_evaluated / stopped`とする。Candidate43を参照promptとして維持し、Candidate66の採用、standard14、release、本体反映へ進めない。次に短くする場合は表面表現を続けて削らず、分別済みの重複predicateと常時coreから分離可能な要素を意味単位で扱う。

## 静的差分

- 直接source: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate66: `the-caption-3ce91a4-topology-preserving-compression-r1`
- Candidate43 bundle SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- Candidate66 bundle SHA-256: `7468c94831164ecbb9ce086ce2fd1e549b2bcbdc97bcad37f6d41575253d690a`
- changed target: root `AGENTS.md`だけ
- label: `SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / METHOD / RECOVERY`
- clause: 32 / 32を元label内へ保持
- root bytes: `3,980 -> 3,923`、`-57`、`-1.43%`

変更したのは`SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / METHOD`内の主語、助詞、接続だけである。`ROOT / INDEPENDENCE / RECOVERY`は逐語一致である。labelをまたぐ明示委譲gateとproducer再割当て禁止の重複も削除していない。

## 固定条件

- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- memories / apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- repetition: 各case `N=5`
- excluded attempt: 0

各scopeのCandidate66 profileは、対応するCandidate43 profileから`profile_id`と`prompt_set_identity`だけを変更した。F10-only、A、F、Dは別Evaluation set、別compatibility keyなので、各set内だけで比較した。

| scope | Layer 1 identity | compatibility key |
| --- | --- | --- |
| F10-only | `98da7e8c9ea12d91be50bb4d66ac15926b53a4ddee4d2035bc61bace13b01507` | `cc9fcfebbc698f3f2601439eed2783fd2786082b847bd526f1c31ece4bfce083` |
| A01 / A02 | `9814b0a53807151e8d4a4f2bf5d089a765e0c9efc66888f77d22616fc98dd8b5` | `5c1cc7a1844a073f074ca57aca27f601f5a3a184523d4c30dafbb3b46bb872b2` |
| F05 / F10 | `1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90` | `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a` |
| D01 | `4b36be3a9fd5c89bb7ea3cf9e1b150e9cd5d83eab632db055ec6044161ee998e` | `4a8e61d6c314a12b30650bb3c64edb49c80938a8f3d2cb77eb9f5874817000b1` |

## 最初のF10-only gate

| 指標 | Candidate43 | Candidate66 | Candidate66 - Candidate43 |
| --- | ---: | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 | 0 |
| top-level tool call | 40 | 39 | -1（-2.50%） |
| model step | 29 | 28 | -1（-3.45%） |
| shell command | 55 | 55 | 0 |
| token合計 | 811,578 | 795,013 | -16,565（-2.04%） |
| token中央値 | 211,070 | 212,762 | +1,692（+0.80%） |
| elapsed中央値 | 87.367秒 | 77.944秒 | -9.423秒（-10.79%） |

iteration順のtool callはCandidate43 `11 / 3 / 11 / 11 / 4`、Candidate66 `11 / 11 / 3 / 3 / 11`だった。model stepはCandidate43 `7 / 4 / 6 / 7 / 5`、Candidate66 `7 / 7 / 4 / 4 / 6`だった。

両promptとも同じ11 shell commandを各runで実行し、workerは起動しなかった。Candidate66は事前gateの上限を超えなかったため、A / F / Dへ進んだ。

## A / F / DのKPI

| scope | score `4` C43 | score `4` C66 | token合計 C43 | token合計 C66 | C66 - C43 | 反復別token中央値 C43 | C66 | elapsed中央値 C43 | C66 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 / A02 | 10 / 10 | 10 / 10 | 2,186,911 | 1,825,021 | -361,890（-16.55%） | 452,817 | 385,275 | 141.235秒 | 128.052秒 |
| F05 / F10 | 9 / 10 | 10 / 10 | 1,179,045 | 1,443,293 | +264,248（+22.41%） | 241,405 | 288,945 | 118.825秒 | 129.850秒 |
| D01 | 5 / 5 | 5 / 5 | 1,318,767 | 1,378,655 | +59,888（+4.54%） | 272,781 | 273,667 | 138.809秒 | 118.853秒 |

F scopeのCandidate43 score `3` 1件は、主要findingを得たが指摘位置が実変更行と一致しなかった既存観測である。Candidate66の25 runはすべてscore `4`だった。この結果を各`N=5`の範囲外へ一般化しない。

case別の値は次のとおりである。

| case | token合計 C43 | token合計 C66 | token差 | elapsed中央値 C43 | elapsed中央値 C66 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 | 538,947 | 313,035 | -225,912（-41.92%） | 46.149秒 | 35.465秒 |
| A02 | 1,647,964 | 1,511,986 | -135,978（-8.25%） | 98.260秒 | 89.341秒 |
| F05 | 330,657 | 328,860 | -1,797（-0.54%） | 33.201秒 | 31.346秒 |
| F10 | 848,388 | 1,114,433 | +266,045（+31.36%） | 85.624秒 | 96.784秒 |
| D01 | 1,318,767 | 1,378,655 | +59,888（+4.54%） | 138.809秒 | 118.853秒 |

## F10経路の再現性

追加F set内のF10は、最初のF10-only gateと逆方向になった。

| 指標 | Candidate43 | Candidate66 | 差 |
| --- | ---: | ---: | ---: |
| top-level tool call | 43 | 57 | +14（+32.56%） |
| model step | 48 | 62 | +14（+29.17%） |
| shell command | 55 | 57 | +2（+3.64%） |
| token合計 | 848,388 | 1,114,433 | +266,045（+31.36%） |
| token中央値 | 210,270 | 214,116 | +3,846（+1.83%） |
| elapsed中央値 | 85.624秒 | 96.784秒 | +11.160秒（+13.03%） |
| worker / SA session | 0 | 0 | 0 |

iteration順のtool callはCandidate43 `11 / 3 / 11 / 11 / 7`、Candidate66 `13 / 11 / 11 / 11 / 11`だった。model stepはCandidate43 `12 / 4 / 12 / 12 / 8`、Candidate66 `14 / 12 / 12 / 12 / 12`だった。

Candidate66のiteration 1だけは、許可された2 source fileへ追加の`git grep`を2回実行した。残り4 runはCandidate43の完全経路と同じ11 commandだったが、5 runとも短いtop-level cycleへ収束しなかった。

token差`266,045`のうちinput token差は`262,301`で`98.59%`を占めた。同じevidence commandを複数のmodel stepへ分け、それまでのcontextを後続stepへ再入力した観測と整合する。ただし、最初のF10-onlyではCandidate66も2 / 5で短いcycleへ収束したため、57 bytes中の特定表現がroute差を起こした因果は確定しない。

事実として確定できるのは、表面圧縮による実行時削減を二つ目の`N=5`で再現できなかったことである。

## A系と明示producer D01

A01は5 / 5で未固定値を推測せず、変更と試験の前に確認して停止した。A02は5 / 5でrepositoryから正規の起動先を解決し、`run.sh`だけを修正して必要な試験を成功させた。10 runはroot-onlyだった。

D01は保存rolloutで次を5 / 5確認した。

1. session数はrootとworkerの2つだった。
2. rootは`spawn_agent`を1回だけ呼び、childの`agent_path`は`/root/monthly_format_review_producer`だった。
3. review対象のdiff、`monthly_main.py`、`monthly_engine.py`を読むcommandはworkerだけが実行した。
4. rootのreview対象readは0件だった。
5. response、zero drift、許可範囲、command protocolを満たした。

D01のroot token合計はCandidate43 `554,833`からCandidate66 `510,715`へ`44,118`、`7.95%`減った。child token合計は`763,934`から`867,940`へ`104,006`、`13.61%`増えた。正しい分担を保ったが、all-agent合計は`4.54%`増えた。

標準`owner-producer-evidence/v1` collectorはCandidate66の5 runを`inadmissible`とした。保存all-agent usageには指定child identityと親子関係があり、root rolloutにはspawnとchildのterminal result受領がある。rating policyは`diagnostic_only`なのでscoreへ影響しない。上記route判定は保存rolloutによる構造診断であり、標準collectorの正式eligibilityではない。

## 判断と次の対象

Candidate66は意味保持の確認には使えるが、圧縮候補として進めない。

1. Candidate43を参照promptとして維持する。
2. Candidate66へ追加の言換えやroute predicateを足さない。
3. 次は`docs/candidate43-control-element-classification.md`で`merge / review / conditional`とした要素を対象にする。
4. 最初の対象は、`PRODUCER / OWNER_ROLE`の明示委譲gate重複、`PRODUCER / INDEPENDENCE`の再割当て禁止重複、単独効果未確認の`F5 / F9`、9-field packetの`D6`、常時coreから分離可能な`R1 / R2`である。
5. 一つの変更では表面圧縮と要素削除を混ぜず、削除するrelationと対応caseを先に固定する。
6. A / F / Dの同一互換条件で成果とrouteを確認し、通過後だけstandard14を検討する。

これは次candidateの作成承認ではない。表面圧縮を停止し、意味単位の削除候補を確定する次の検討境界である。

## 登録証跡

| scope | prompt | result ID | result content SHA-256 | execution archive SHA-256 |
| --- | --- | --- | --- | --- |
| F10-only | Candidate43 | `6965832090ad4b1b8507c7c8496dc1c5` | `7b08f0ae70c79e41f6c96a4471ba483c7878cf1271ce079a7dc3f9446ab7acb0` | `4f1ea04a29a8e01141985ff311b1f0d82631677fe89511d7825448f6cce9c99f` |
| F10-only | Candidate66 | `9aee7a0f488344dba178945d3c62ddbc` | `bb5492396ee37b5a28dbf37465eae12bc81def4c73d9db9c35cbdf9bc3ed753f` | `7f1aeef7264758329ae32e404eeefafd10a7267ac08f818f9af73c4d59a37ca7` |
| A | Candidate43 | `c9c2d55acbd944a2a7026457aa1d6efd` | `77743feeb4c04bd7d32d73bb2feec82402e93641a5a9487e81ef235efd5a7a7f` | `441b10aac8cff899fe3ea5d608efecff2aec32ab51d825c478fcbfb7dfcac56f` |
| A | Candidate66 | `c58d03f5a99d45eba05b840fb677158d` | `66699aeb435b4d66c050a1e63171f0fe950489e36115571068e0d4fb1cb80583` | `a93d068c6e0949efaf03ebac2f493685e8561ca90a0ea3424c69288771976bb9` |
| F | Candidate43 | `53f46f39073c4bf1aa1d7dc8fbc4b892` | `1c91cd9edaf8b47776c63f2e69bc9c47260fb1476a821eb185fded5011c69a96` | `6aaac40bc057662c41187197a8eed7df91cfa720eb650fe5fc23471bf85be595` |
| F | Candidate66 | `8e7bceae05f044ba883a2c1ebef77597` | `0fd610d2120f02d26056bea6f40bd3ad3ab44c693bbccfa0f3b313be0aacf1e5` | `fd40ba70311fe0632889162ef1f1fc2828b05b15112675a4e96822bd434c843d` |
| D | Candidate43 | `66f795a48d584249acd96d9e4383d89a` | `2de3b06c777ccd197111ecb94fee41690b53b9376a322c914ec0f4baed73e179` | `74f8f1a08a42c23d4dedc9d6c80c8b9b4546b937ec8589898b94fb239ff828be` |
| D | Candidate66 | `382e72942e134cf5827661367eb196e0` | `d7e270cf2fe3c254d8e6191e2f51a69786fd00ce370fdca17bc0494d05dad05c` | `6bb8f958f3e82074c04bf690ad06b56633d08012c3f8bd541a77e3b9b5c0a19e` |

comparison views:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate66-topology-preserving-compression-f10-n5-20260722-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate66-a01-a02-catalog-fixed-n5-20260722-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate66-f05-f10-catalog-fixed-n5-20260722-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate66-d01-catalog-fixed-n5-20260722-r1.json`

Candidate66の採用、release、本体反映は未判断、未実施である。
