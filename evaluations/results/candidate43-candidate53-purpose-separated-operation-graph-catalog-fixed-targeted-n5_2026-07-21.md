# Candidate43 / Candidate53 目的分離operation graph capability catalog固定対象試験 N=5

## 結論

Candidate53はF05 / F10の10 / 10 runでscore `4`、root-only、zero driftを維持した。一方、Candidate43比で10 runのall-agent `total_tokens`合計は`+153,562`、`+13.02%`、F10のmodel stepは`48 -> 54`、tool callは`43 -> 49`だった。

Candidate53のroot `AGENTS.md`はCandidate43より`626 bytes`、`15.73%`小さい。同じ11 tool call経路の平均tokenはCandidate43比`-0.09%`だったが、短い経路の発生が減ったため、prompt短縮をrun全体の効率化へ接続できなかった。

作成前gateの停止条件に従い、Candidate53は`targeted_evaluated / stopped`とする。A01 / A02、標準14項目、A06、採用、release、本体反映へ進めない。

## Identityと互換条件

| 項目 | Candidate43 | Candidate53 |
| --- | --- | --- |
| prompt identity | `the-caption-3ce91a4-outcome-authority-boundary-r1` | `the-caption-3ce91a4-purpose-separated-operation-graph-r1` |
| bundle SHA-256 | `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531` | `8a61397bcd267800f9e55bd63427734671fa76a9fa97625137113e084f0366c7` |
| result ID | `53f46f39073c4bf1aa1d7dc8fbc4b892` | `9620996713a140789a6635d4e3657e65` |
| result content SHA-256 | `1c91cd9edaf8b47776c63f2e69bc9c47260fb1476a821eb185fded5011c69a96` | `882e174b1e908be92dafe4645c6320b7fc87721b5ba7e9a5fa9a41870c55bb77` |

両resultのcompatibility keyは`f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`で一致する。

- 固定Layer 1 identityは`1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90`で一致した。
- 20 / 20 runのmodel-visible capability catalog SHA-256は`e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`で一致した。
- 比較対象はF05 `r1`とF10 `r3`、各`N=5`である。
- model、reasoning、permission、runtime、TaskSpec、fixture、外側並行度、token accountingは同一である。
- excluded attemptは0件だった。

## 成果品質

| 観測 | Candidate43 | Candidate53 |
| --- | ---: | ---: |
| valid / rateable | 10 / 10 | 10 / 10 |
| score `4` | 9 | 10 |
| score `3` | 1 | 0 |
| root-only | 10 | 10 |
| command protocol violation | 0 | 0 |
| unexpected changed path | 0 | 0 |

Candidate43のscore `3`は既知のF10指摘位置ずれである。Candidate53は全runで所定responseとzero driftを満たした。成果品質中央値は両方`100.000`だった。

## KPI

保存済みcomparison viewの差分方向は`Candidate53 - Candidate43`である。

| KPI中央値 | Candidate43 | Candidate53 | 差 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| `total_tokens` | 241,405 | 285,064 | +43,659（+18.09%） |
| `elapsed_seconds` | 118.825 | 126.848 | +8.024（+6.75%） |

10 run合計はCandidate43の`1,179,045`に対しCandidate53が`1,332,607`で、差は`+153,562`、`+13.02%`だった。

外側10並行のcampaign wall clockは`102.900秒 -> 102.288秒`だった。各runのKPI中央値は増えており、campaign wall clockの`-0.61%`をpromptの実行時間短縮とは扱わない。

## case別診断

| case | 指標 | Candidate43 | Candidate53 | 差 |
| --- | --- | ---: | ---: | ---: |
| F05 | token合計 | 330,657 | 370,727 | +40,070（+12.12%） |
| F05 | token中央値 | 75,024 | 74,092 | -932（-1.24%） |
| F05 | model step / tool call | 22 / 17 | 25 / 20 | +3 / +3 |
| F10 | token合計 | 848,388 | 961,880 | +113,492（+13.37%） |
| F10 | token中央値 | 210,270 | 211,046 | +776（+0.37%） |
| F10 | elapsed中央値 | 85.624 | 91.399 | +5.775（+6.75%） |
| F10 | model step / tool call | 48 / 43 | 54 / 49 | +6 / +6 |

F10のtool call分布はCandidate43が`11 / 3 / 11 / 11 / 7`、Candidate53が`11 / 11 / 5 / 11 / 11`だった。Candidate53の5-call runは13 shell commandを5 callへまとめたが、標準の11 commandに加えて2回のsource範囲再読を行った。

同じ11-call経路だけを比較すると、平均input tokenは`207,889 -> 207,636`、平均total tokenは`211,200 -> 211,013`だった。Candidate53は同じ経路で`-0.12% input`、`-0.09% total`であり、短いprompt自体が同一経路を高cost化した観測ではない。

F05のtool call分布はCandidate43が`1 / 4 / 4 / 4 / 4`、Candidate53が全run `4`だった。Candidate53のtoken中央値は小さいが、Candidate43に1-callの短いrunが1件あったため合計は増えた。

## 判断

- 事実: A系readiness、F系operation graph、明示委譲を別領域へ分けても、F10の短いroutingはCandidate43と同じ頻度で再現しなかった。
- 事実: 同じtool-call経路ではCandidate53のtokenはCandidate43とほぼ同じだった。
- 推測: N=5の観測範囲では、C43の短いroutingはoperation graphの意味保存だけで決まらず、文面配置または実行分散の影響を受ける。ただし一つの文言へ因果帰属しない。
- 判断: C53へC43の文を追加復元しない。A系試験にも進まない。
- 次の検討点: 新candidateを作る前に、C43内でも短いrunと長いrunが混在する理由をtrace差分で分離し、promptで消せる判断点が存在するかを確認する。

## Evidence

- Candidate53 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate53-purpose-separated-operation-graph-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-20260721-r1`
- comparison view: `comparison-c43-c53.json`
- design gate: [`Candidate53 目的分離operation graph`](../../docs/candidate53-purpose-separated-operation-graph-design.md)
- Candidate43 / Candidate51固定比較: [`capability catalog固定対象試験`](candidate43-candidate51-catalog-fixed-targeted-n5_2026-07-21.md)
- Candidate31 / Candidate34圧縮実績: [`owner-producer v7 expanded N=5`](candidate31-candidate34-owner-producer-v7-expanded12-global-m24-n5_2026-07-18.md)
