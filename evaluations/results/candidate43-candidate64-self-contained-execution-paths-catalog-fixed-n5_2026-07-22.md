# Candidate43 / Candidate64 self-contained execution paths catalog固定 N=5

## 結論

Candidate64はA01 / A02、F05 / F10、明示producer D01の25 / 25 runでscore `4`を維持した。A / Fの20 runはroot-onlyだった。D01は保存rollout上、5 / 5で指定workerだけがreviewを実行し、rootによるreview再実行はなかった。

一方、事前停止条件にしたroot-only F10は、Candidate43比でtop-level tool callが`43 -> 54`、model stepが`48 -> 59`、all-agent token合計が`848,388 -> 1,093,565`へ増えた。3条件すべてを超えたため、Candidate64は`targeted_evaluated / stopped`とする。

4 blockへの意味分別は成果を壊さなかった。しかし、root / delegatedへF coreを全文重複した構造は実行を単純化しなかった。Candidate64へ条件を追加せず、次はCandidate43の32 clauseを保持したまま、共通operation coreとdelegation固有extensionを重複なしで短文化する。

## 固定条件

- Candidate43: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate43 bundle SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- Candidate64: `the-caption-3ce91a4-self-contained-execution-paths-r1`
- Candidate64 bundle SHA-256: `b5b8d9486b901336d86d062af3d3fca0ec82dd797d39ef3e28ea89857e121e42`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- memories / apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- repetition: 各case `N=5`
- excluded attempt: 0

A / F / Dは別Evaluation set、別compatibility keyである。各set内ではCandidate43とCandidate64のprofile差を`profile_id`と`prompt_set_identity`だけに固定した。

| scope | Layer 1 identity | compatibility key |
| --- | --- | --- |
| A01 / A02 | `9814b0a53807151e8d4a4f2bf5d089a765e0c9efc66888f77d22616fc98dd8b5` | `5c1cc7a1844a073f074ca57aca27f601f5a3a184523d4c30dafbb3b46bb872b2` |
| F05 / F10 | `1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90` | `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a` |
| D01 | `4b36be3a9fd5c89bb7ea3cf9e1b150e9cd5d83eab632db055ec6044161ee998e` | `4a8e61d6c314a12b30650bb3c64edb49c80938a8f3d2cb77eb9f5874817000b1` |

## KPI

| scope | score `4` C43 | score `4` C64 | token合計 C43 | token合計 C64 | C64 - C43 | elapsed中央値 C43 | elapsed中央値 C64 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 / A02 | 10 / 10 | 10 / 10 | 2,186,911 | 2,478,271 | +291,360（+13.32%） | 141.235秒 | 169.953秒 |
| F05 / F10 | 9 / 10 | 10 / 10 | 1,179,045 | 1,339,080 | +160,035（+13.57%） | 118.825秒 | 131.331秒 |
| D01 | 5 / 5 | 5 / 5 | 1,318,767 | 1,481,673 | +162,906（+12.35%） | 138.809秒 | 132.446秒 |

F scopeのCandidate43 score `3` 1件は、F10の主要findingを得たが指摘位置が実変更行と一致しなかった既存観測である。Candidate64の25 runはすべてscore `4`だった。これを単一`N=5`の範囲外へ一般化しない。

case別のtokenとelapsed中央値は次のとおりである。

| case | token合計 C43 | token合計 C64 | token差 | elapsed中央値 C43 | elapsed中央値 C64 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 | 538,947 | 486,955 | -51,992（-9.65%） | 46.149秒 | 42.380秒 |
| A02 | 1,647,964 | 1,991,316 | +343,352（+20.83%） | 98.260秒 | 126.807秒 |
| F05 | 330,657 | 245,515 | -85,142（-25.75%） | 33.201秒 | 24.940秒 |
| F10 | 848,388 | 1,093,565 | +245,177（+28.90%） | 85.624秒 | 92.982秒 |
| D01 | 1,318,767 | 1,481,673 | +162,906（+12.35%） | 138.809秒 | 132.446秒 |

## Root-only F10の停止判定

| 指標 | Candidate43 | Candidate64 | 差 |
| --- | ---: | ---: | ---: |
| top-level tool call | 43 | 54 | +11（+25.58%） |
| model step | 48 | 59 | +11（+22.92%） |
| all-agent token合計 | 848,388 | 1,093,565 | +245,177（+28.90%） |
| all-agent token中央値 | 210,270 | 218,708 | +8,438（+4.01%） |
| elapsed中央値 | 85.624秒 | 92.982秒 | +7.358秒（+8.59%） |
| worker / SA session | 0 | 0 | 0 |

iteration順のtool callはCandidate43 `11 / 3 / 11 / 11 / 7`、Candidate64 `11 / 12 / 11 / 9 / 11`だった。model stepはCandidate43 `12 / 4 / 12 / 12 / 8`、Candidate64 `12 / 13 / 12 / 10 / 12`だった。

F10のtoken差`245,177`のうち、input token差は`242,623`で`98.96%`を占めた。Candidate64は5 runすべて正しいevidenceを得たが、短い経路へ収束しなかった。iteration 2では`monthly_engine.py`を重複readしたが、重複readのない残り4 runでも3 runのtokenが増えているため、一つの追加commandだけを全差分の原因にはしない。

静的にはroot `AGENTS.md`がCandidate43 `3,980 bytes`からCandidate64 `5,594 bytes`へ`40.55%`増えている。F coreの重複とmodel step増加が、input context増加と整合する。ただし、この`N=5`だけで個々の文の因果までは確定しない。

## 明示producer D01

D01はF10 r3の成果条件とfixtureを維持し、TaskSpecへ次だけを追加した。

- operation identity: `monthly-format-review`
- local task name: `monthly_format_review_producer`
- canonical producer identity: `/root/monthly_format_review_producer`

保存rolloutの構造診断では、Candidate43とCandidate64の両方で次を5 / 5確認した。

1. session数はrootとworkerのちょうど2つだった。
2. rootは`spawn_agent`を1回だけ呼び、返却task nameは`/root/monthly_format_review_producer`だった。
3. child sessionの`agent_path`は指定canonical identityと一致した。
4. rootは`author`と`Sender`が同identityの`FINAL_ANSWER`を受信した。
5. review対象のdiff、`monthly_main.py`、`monthly_engine.py`を読むcommandはworkerだけが実行し、rootのreview commandは0件だった。

Candidate64はroot tokenをCandidate43比`-104,262`、`-18.79%`にした一方、child tokenは`+267,168`、`+34.97%`だった。その結果、all-agent合計は`+12.35%`になった。delegated blockの自己完結化はrootの仕事を減らしたが、workerへ渡るcontext costを増やした観測と整合する。

標準`owner-producer-evidence/v1` collectorは、両promptの全runで`producer_candidates=[]`を返した。保存rolloutには`author`と`Sender`を持つcollaboration受信eventがあるため、collectorの対象eventとの間にcoverage差がある。rating policyは`diagnostic_only`なので成果scoreには影響しない。上記5点は保存rolloutとall-agent usage / command evidenceによるroute診断であり、標準collectorによる正式なowner-producer eligibilityではない。

## 判断と次の対象

事実として、Candidate64は32 / 32 source clauseと成果品質を維持した。したがって、C43の意味要素を4 blockへ分類すること自体で必要要素が失われた証拠はない。

事実として、同じF coreをroot / delegatedへ全文重複すると、A、F、Dの3 scopeすべてでtoken合計が12〜14%増えた。特に停止対象F10ではtool call、model step、tokenのすべてが増えた。

次はCandidate64を修正しない。Candidate43を直接sourceに戻し、次の順で一枚のroot `AGENTS.md`を短くする。

1. 32 clauseを`常時必要なoperation core`、`明示delegation時だけ必要なextension`、`failure / recovery`へ分類する。
2. clauseは削らず、同じpredicateの説明、negative example、重複したbinding文だけを統合する。
3. root / delegatedへF coreを複製しない。
4. 静的bytesを確認してから、今回と同じA01 / A02、F05 / F10、D01 `N=5` gateを使う。

standard14、A06、採用、release、本体反映へは進めない。

## 登録証跡

| scope | prompt | result ID | result content SHA-256 | execution archive SHA-256 |
| --- | --- | --- | --- | --- |
| A | Candidate43 | `c9c2d55acbd944a2a7026457aa1d6efd` | `77743feeb4c04bd7d32d73bb2feec82402e93641a5a9487e81ef235efd5a7a7f` | `441b10aac8cff899fe3ea5d608efecff2aec32ab51d825c478fcbfb7dfcac56f` |
| A | Candidate64 | `debab847e9f7454a80339d4abdc97e73` | `2f48f272b894b0b5916c7b3381993f06bec23af345a2d5ed87bf9609556569a2` | `5ba8208cd068469a70f8cfb671f50b48cf4b91504dc92531b361cca9896efef3` |
| F | Candidate43 | `53f46f39073c4bf1aa1d7dc8fbc4b892` | `1c91cd9edaf8b47776c63f2e69bc9c47260fb1476a821eb185fded5011c69a96` | `6aaac40bc057662c41187197a8eed7df91cfa720eb650fe5fc23471bf85be595` |
| F | Candidate64 | `ae86f984296047588715cc9c32c9b101` | `3b8dc5bd530d9f3b1d1150644e9b76f9c97419f9345a0d2138679d47bf1dba05` | `955a0c89e95473421003a3a2ff60508af814c2c912deac6c6cc7246de3cd1dcb` |
| D | Candidate43 | `66f795a48d584249acd96d9e4383d89a` | `2de3b06c777ccd197111ecb94fee41690b53b9376a322c914ec0f4baed73e179` | `74f8f1a08a42c23d4dedc9d6c80c8b9b4546b937ec8589898b94fb239ff828be` |
| D | Candidate64 | `c810112302d34284b2c81094b6441c62` | `3e403873f8831e3e2dacf715200233ad14621802bf41c86cae0c40400cb7ab0b` | `62872f8c9d49e119ae9dc7f2e3ac56fdc9e614996526aa12eb18c26d28e87a8e` |

comparison views:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate64-a01-a02-catalog-fixed-n5-20260722-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate64-f05-f10-catalog-fixed-n5-20260722-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate64-d01-catalog-fixed-n5-20260722-r1.json`

Candidate64の採用、release、本体反映は未判断、未実施である。
