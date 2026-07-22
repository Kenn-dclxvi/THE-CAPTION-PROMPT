# Candidate43 / Candidate51 capability catalog固定 対象試験 N=5

## 結論

Candidate43とCandidate51を、model-visible capability catalogまで固定してF05 / F10各`N=5`で再実行した。C49は再実行していない。

両resultはEvaluation set、fixture、model、reasoning、permission、外側並列度に加え、skills / apps / plugins blockのSHA-256も一致した。20 / 20 runのcatalog identityは`e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`だった。apps、plugins、plugin sharingは明示的に無効化した。excluded attemptは0件である。

Candidate51は10 / 10がscore `4`だった。Candidate43は9 / 10がscore `4`、F10の1件が既知の指摘行ずれによりscore `3`だった。median qualityは両方`100.000`である。

10 run token合計はCandidate43 `1,179,045`、Candidate51 `1,362,976`で、差は`+183,931`、`+15.60%`だった。差はF10に集中し、F05は`-2.61%`、F10は`+22.70%`だった。

F10でCandidate43は独立したreadを1 model step内の1 tool callへまとめるrunがあった。Candidate51は5 / 5 runで11 tool callへ分割した。同じ11 tool call経路だけを比べるとCandidate51の平均input tokenはCandidate43より`-1.54%`だった。したがって、Candidate51の短いprompt自体が1 step当たりのtokenを増やしたのではなく、独立predicateを逐次model stepへ分けるroutingが合計増加を作った。

## 固定条件

- Evaluation set identity: `1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90`
- case / iteration: F05 clarification、F10 monthly review x `1..5`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- Agent環境: `agents.max_threads=4`、`memories=false`
- capability policy: `apps=false`、`plugins=false`、`plugin_sharing=false`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- capability block: `skills_instructions` 1 block、3,767 bytes
- executor: global queue `M=10`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- token accounting: all-agent `v1`

adapterは各root rolloutから`skills_instructions / apps_instructions / plugins_instructions` blockを抽出した。profileのexpected SHA-256と異なるrunはexternal failureとして除外し、同じslotを再試行する。今回の20 runにcatalog mismatchはなかった。

## KPI

| KPI | Candidate43 | Candidate51 | C51 - C43 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 241,405 | 280,870 | +39,465 (+16.35%) |
| median `elapsed_seconds` | 118.825 | 132.023 | +13.198 (+11.11%) |
| 10 run token合計 | 1,179,045 | 1,362,976 | +183,931 (+15.60%) |
| score `4` | 9 / 10 | 10 / 10 | +1 |

Candidate43のscore `3`はF10 iteration 3の`monthly_main.py:25`指摘行ずれである。主要finding、zero drift、許可範囲は維持した。

## case別token

| case | Candidate43 | Candidate51 | C51 - C43 |
| --- | ---: | ---: | ---: |
| F05 | 330,657 | 322,042 | -8,615 (-2.61%) |
| F10 | 848,388 | 1,040,934 | +192,546 (+22.70%) |

## raw execution

| case | 指標 | Candidate43 | Candidate51 | C51 - C43 |
| --- | --- | ---: | ---: | ---: |
| F05 | model step | 22 | 22 | 0 |
| F05 | tool call | 17 | 17 | 0 |
| F05 | input token | 325,704 | 317,386 | -8,318 |
| F05 | output token | 4,953 | 4,656 | -297 |
| F10 | model step | 48 | 60 | +12 |
| F10 | tool call | 43 | 55 | +12 |
| F10 | input token | 833,680 | 1,023,426 | +189,746 |
| F10 | output token | 14,708 | 17,508 | +2,800 |

F10のrun別分布は次だった。

| prompt set | model step | tool call |
| --- | --- | --- |
| Candidate43 | `12 / 4 / 12 / 12 / 8` | `11 / 3 / 11 / 11 / 7` |
| Candidate51 | `12 / 12 / 12 / 12 / 12` | `11 / 11 / 11 / 11 / 11` |

Candidate43 iteration 2は、開始条件5 commandを1 tool call、authority / diff / source 5 readを1 tool call、最終statusを1 tool callで実行した。Candidate51 iteration 2は、同じ11 commandを11 tool callへ分けた。

11 tool call経路の平均input tokenはCandidate43が`207,889`、Candidate51が`204,685`だった。Candidate51は同経路で`-3,204`、`-1.54%`である。token合計差は1 step当たりのprompt overheadではなく、経路分布の差である。

## 判定

- 事実: capability catalogを含む比較条件は一致した。
- 事実: Candidate51はF05でCandidate43と同じstep数となり、input tokenは小さかった。
- 事実: Candidate51はF10で全runを11 tool callへ分割し、Candidate43より12 model step増えた。
- 事実: 同じ11 tool call経路ではCandidate51のinput tokenが小さかった。
- 推測: C49圧縮で消え、Candidate51でも未復元のroot適用可能な要素は、先行依存のないpredicateを逐次operationとして扱わない`INDEPENDENCE`境界である可能性が高い。
- 未確定: Candidate43とCandidate51はroot `AGENTS.md`の複数文が異なるため、このN=5だけで`INDEPENDENCE`文単独の因果効果とは確定しない。
- 提案: 次candidateを作る場合はCandidate51をsourceとし、worker制御全体ではなく、固定済みroot predicate間の依存境界だけを一つ復元する。tool API、code mode、command結合を方法として指定しない。

## Evidence

- Candidate43 result: `53f46f39073c4bf1aa1d7dc8fbc4b892`
- Candidate43 content SHA-256: `1c91cd9edaf8b47776c63f2e69bc9c47260fb1476a821eb185fded5011c69a96`
- Candidate51 result: `50e40c93bb20426c8fbf6e0be34df390`
- Candidate51 content SHA-256: `1cfa30832fc83390a17f0c3a5b95e475a4febc7cae65c0f79a795c8c3a1e0c7c`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate51-root-operation-completion-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-20260721-r1/comparison-c43-c51.json`

両campaignはvalid 10 / 10、retry 0、excluded attempt 0である。quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。Candidate51の採用、release、本体反映は未判断・未実施である。
