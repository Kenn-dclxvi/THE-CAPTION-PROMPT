# Candidate43 / Candidate51 / Candidate52 root independence境界 対象試験 N=5

## 結論

Candidate52はCandidate51を直接sourceとし、Candidate43の`INDEPENDENCE`一文だけを完全一致で復元した。producer binding、completion、worker制御、tool方法は変更していない。

capability catalog固定済みF05 / F10各`N=5`は10 / 10がscore `4`、root-only、protocol違反0、zero driftだった。10 / 10のcatalog SHA-256もexpected identityと一致し、excluded attemptは0件だった。

狙ったF10 routingは復元しなかった。Candidate52のF10はCandidate51比でmodel step `60 -> 61`、tool call `55 -> 56`、token合計`1,040,934 -> 1,111,322`、`+6.76%`だった。10 run合計も`+2.01%`となった。

Candidate52では4 tool callへまとめるF10 runが1件発生した一方、16 / 14 tool callまで探索を増やすrunが2件発生した。`INDEPENDENCE`一文はC43の経路分布を安定して復元せず、run間変動と追加探索を増やした。

作成前gateの停止条件に従い、Candidate52へ別のC43要素を継ぎ足さない。Candidate52は`targeted_evaluated / stopped`として保持する。

## Prompt差分

- Candidate51: `the-caption-3ce91a4-root-operation-completion-boundary-r1`
- Candidate52: `the-caption-3ce91a4-root-independence-boundary-r1`
- Candidate52 bundle SHA-256: `8317ca0d9736fc71aed91e0d3612f874496018dd5c1c3d2ce1c0292bcbe31ae4`
- Candidate52 source: Candidate51
- changed target: root `AGENTS.md`だけ
- 変更内容: Candidate43の`INDEPENDENCE`一文を完全一致で追加
- 未変更target: 18 / 18がCandidate51とbit identity一致
- root prompt: C43 `3,980 bytes / 199 words`、C51 `2,473 / 118`、C52 `2,666 / 127`

## 固定条件

- Evaluation set identity: `1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90`
- case / iteration: F05 clarification、F10 monthly review x `1..5`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- Agent環境: `agents.max_threads=4`、`memories=false`
- capability policy: `apps=false`、`plugins=false`、`plugin_sharing=false`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- executor: global queue `M=10`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- token accounting: all-agent `v1`

## KPI

| KPI | Candidate43 | Candidate51 | Candidate52 | C52 - C51 |
| --- | ---: | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 241,405 | 280,870 | 280,880 | +10 |
| median `elapsed_seconds` | 118.825 | 132.023 | 121.399 | -10.624 (-8.05%) |
| 10 run token合計 | 1,179,045 | 1,362,976 | 1,390,337 | +27,361 (+2.01%) |
| score `4` | 9 / 10 | 10 / 10 | 10 / 10 | 0 |

Candidate43のscore `3`は既知のF10指摘行ずれである。Candidate51 / 52では発生しなかった。

## case別token

| case | Candidate43 | Candidate51 | Candidate52 | C52 - C51 |
| --- | ---: | ---: | ---: | ---: |
| F05 | 330,657 | 322,042 | 279,015 | -43,027 (-13.36%) |
| F10 | 848,388 | 1,040,934 | 1,111,322 | +70,388 (+6.76%) |

## raw execution

| case | 指標 | Candidate43 | Candidate51 | Candidate52 | C52 - C51 |
| --- | --- | ---: | ---: | ---: | ---: |
| F05 | model step | 22 | 22 | 19 | -3 |
| F05 | tool call | 17 | 17 | 14 | -3 |
| F05 | input token | 325,704 | 317,386 | 274,740 | -42,646 |
| F05 | output token | 4,953 | 4,656 | 4,275 | -381 |
| F10 | model step | 48 | 60 | 61 | +1 |
| F10 | tool call | 43 | 55 | 56 | +1 |
| F10 | input token | 833,680 | 1,023,426 | 1,092,952 | +69,526 |
| F10 | output token | 14,708 | 17,508 | 18,370 | +862 |

F10のrun別分布は次だった。

| prompt set | model step | tool call |
| --- | --- | --- |
| Candidate43 | `12 / 4 / 12 / 12 / 8` | `11 / 3 / 11 / 11 / 7` |
| Candidate51 | `12 / 12 / 12 / 12 / 12` | `11 / 11 / 11 / 11 / 11` |
| Candidate52 | `17 / 5 / 12 / 12 / 15` | `16 / 4 / 11 / 11 / 14` |

Candidate52の16 / 14 tool call runでは、固定diffと主要sourceを取得した後に、追加の`rg`、複数範囲の`sed`、`nl`による再取得が発生した。4 tool call runでは複数commandを同一model step内へまとめた。単一文の復元は両経路を生み、C43の分布へ収束させなかった。

## 判定

- 事実: Candidate52の成果品質、root-only、catalog identityは維持した。
- 事実: F05ではmodel stepとtokenが減った。
- 事実: F10ではmodel step、tool call、input token、token合計がCandidate51から増えた。
- 事実: Candidate52のmedian elapsedはCandidate51より短かったが、10 run token合計とF10 routingの停止条件を満たさなかった。
- 判定: C43の`INDEPENDENCE`一文だけでは、C43のF10経路を復元できない。
- 推測: C43の挙動は`INDEPENDENCE`単独ではなく、`PRODUCER / TERMINAL / ROOT`を含むoperation graph全体またはrun間変動との組合せで成立している。
- 次段: C51へC43 labelを順次継ぎ足す方法を止める。次に検討する場合は、既知のC43をsourceにしてF系に必要なoperation graphを保持し、A系 / worker固有制御だけを別境界として削る方向をcandidate作成前gateから再設計する。

## Evidence

- Candidate43 result: `53f46f39073c4bf1aa1d7dc8fbc4b892`
- Candidate51 result: `50e40c93bb20426c8fbf6e0be34df390`
- Candidate52 result: `85c129cae73441a7a5e792edf0f2049a`
- Candidate52 content SHA-256: `c6e630f0eb43030a48c1d24ceba63713ec2934315539977638d1be2c95ed37f0`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate52-root-independence-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-20260721-r1/comparison-c43-c51-c52.json`

Candidate52 campaignはvalid 10 / 10、retry 0、excluded attempt 0である。quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。Candidate52の採用、release、本体反映は未判断・未実施である。
