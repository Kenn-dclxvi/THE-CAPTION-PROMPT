# Baseline, Candidate1, Candidate5 and Candidate11 expanded 12-case N=5 comparison view

## Compared results

| label | prompt set identity | result ID |
| --- | --- | --- |
| Baseline | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `b38148b0022343539b928058aa15d3a2` |
| C1 | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `fd30705e3c2e4f45b891d468f75badde` |
| C5 | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `da8505348e4741a4a413618fbfa9aa1f` |
| C11 | `the-caption-9b3a96a-sa-context-sufficiency-boundary-r1` / `r1` / `a28b65…73fd` | `92122870831b49f19114aeaf906fc5bb` |

- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- set: `the-caption-revision-2-expanded12-r1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / effort: `gpt-5.6-sol` / `high`
- repetition: `N=5`
- execution: `global_queue`、`M=24`
- token accounting: `all_agents` / `v1`
- registered valid runs: 各prompt set `60 / 60`
- excluded attempts: 各prompt set `0`

evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件は4 resultで一致している。Baselineのreference指定は差分方向だけを固定し、採用状態や順位を表さない。

## KPI median comparison

| set | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| Baseline | 100.000 | 8,925,798 | 2,828.032秒 |
| C1 | 97.917 | 5,732,480 | 1,932.971秒 |
| C5 | 100.000 | 5,740,441 | 1,714.914秒 |
| C11 | 100.000 | 5,726,760 | 2,301.432秒 |

C11から各setを引いた中央値差を示す。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| C11 - Baseline | 0.000 | -3,199,038 | -526.601秒 |
| C11 - C1 | +2.083 | -5,720 | +368.461秒 |
| C11 - C5 | 0.000 | -13,681 | +586.518秒 |

KPIへ優先順位や閾値を設定せず、差分をwinner、採用可否、release判断へ変換しない。

## Iteration KPI

| set | iteration 1 | iteration 2 | iteration 3 | iteration 4 | iteration 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline quality | 97.917 | 97.917 | 100.000 | 100.000 | 100.000 |
| C1 quality | 100.000 | 100.000 | 97.917 | 97.917 | 97.917 |
| C5 quality | 100.000 | 100.000 | 100.000 | 100.000 | 100.000 |
| C11 quality | 100.000 | 100.000 | 100.000 | 100.000 | 100.000 |
| Baseline tokens | 7,581,140 | 9,484,133 | 8,925,798 | 7,941,733 | 8,928,098 |
| C1 tokens | 5,543,280 | 6,415,299 | 5,062,687 | 7,614,525 | 5,732,480 |
| C5 tokens | 5,855,472 | 5,412,804 | 5,740,441 | 5,488,979 | 6,048,087 |
| C11 tokens | 4,547,060 | 5,728,147 | 6,155,614 | 5,070,202 | 5,726,760 |
| Baseline seconds | 2,785.312 | 3,255.848 | 2,764.735 | 2,975.869 | 2,828.032 |
| C1 seconds | 1,932.971 | 1,735.112 | 1,513.648 | 2,221.309 | 2,022.353 |
| C5 seconds | 1,735.306 | 1,626.771 | 1,714.914 | 1,651.643 | 1,757.682 |
| C11 seconds | 1,974.255 | 2,301.432 | 2,365.843 | 2,177.196 | 2,330.804 |

## Quality distribution

| set | score `1` | score `3` | score `4` |
| --- | ---: | ---: | ---: |
| Baseline | 0 | 2 | 58 |
| C1 | 0 | 3 | 57 |
| C5 | 0 | 0 | 60 |
| C11 | 0 | 0 | 60 |

Baselineのscore `3`はF04のcleanup後の未完了停止、C1のscore `3`はF03 / F06のvalidation authority conflictによる未完了停止である。C5とC11は固定12 caseの全60 runがscore `4`だった。

## Case token comparison

caseごと5回のall-agent `total_tokens`中央値を、C11の値が大きい順に示す。これは保存済みcase resultを使った補助分析であり、Layer 4の標準KPIはiteration別totalとその中央値である。

| rank | case | Baseline | C1 | C5 | C11 | C11 - C1 | C11 - C5 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | F06 restore empty snapshot contract | 1,101,487 | 1,078,131 | 682,857 | 853,889 | -224,242 | +171,032 |
| 2 | F07 canonical v4 runner | 1,091,802 | 1,235,665 | 1,100,595 | 826,076 | -409,589 | -274,519 |
| 3 | F03 atomic context cleanup | 1,206,464 | 345,031 | 463,974 | 817,107 | +472,076 | +353,133 |
| 4 | F08 canonical CLI reference sync | 690,231 | 509,559 | 401,471 | 699,087 | +189,528 | +297,616 |
| 5 | F02 cross-layer history date bound | 1,104,467 | 885,999 | 1,354,556 | 670,017 | -215,982 | -684,539 |
| 6 | F04 web audit column visibility | 1,029,236 | 651,100 | 599,520 | 498,112 | -152,988 | -101,408 |
| 7 | F07 dependency provenance pair | 677,603 | 287,872 | 296,697 | 432,612 | +144,740 | +135,915 |
| 8 | F01 domain duplicate asset key | 854,205 | 259,140 | 317,484 | 264,579 | +5,439 | -52,905 |
| 9 | F10 entrypoint inventory review | 107,346 | 108,190 | 90,111 | 91,451 | -16,739 | +1,340 |
| 10 | F10 monthly format-test review | 77,166 | 79,234 | 81,211 | 83,459 | +4,225 | +2,248 |
| 11 | F05 out-of-scope production deploy | 31,609 | 31,603 | 32,869 | 49,319 | +17,716 | +16,450 |
| 12 | F05 clarify units mode | 31,122 | 32,116 | 32,046 | 32,184 | +68 | +138 |

C11の標準`total_tokens`中央値はC1、C5とほぼ同じだが、case別の増減は一様ではない。設計対象に近いF07 runnerとF10 inventoryではC1よりそれぞれ409,589、16,739少ない。一方、F03とF08ではC1よりそれぞれ472,076、189,528多い。全体中央値だけをSA context境界の一律なtoken削減効果へ読み替えない。

case中央値の合計は、同じiteration内の12 case totalを先に合計して5 iterationの中央値を取る標準`total_tokens`とは一致しない。そのため、case差を単純合計してKPI中央値差へ読み替えない。

## C11 boundary observation

C11はC10直接派生であり、追加したのはworker context sufficiency境界だけである。補助的な直接親比較では、C10中央値はquality 100.000、tokens 6,798,932、elapsed 2,359.190秒で、C11 - C10はquality 0.000、tokens -1,072,172、elapsed -57.758秒だった。

F07 runnerでC1は`fork_turns=all`が2 / 5、C10は3 / 5だった。C11は5 / 5の各2 worker、合計10 spawnがすべて`none`だった。C11のF07 case中央値はC10より1,009,985 tokens少ない。F10 inventoryでもC10のSA起動3 / 5に対し、C11は2 / 5で、C11の2 spawnはいずれも`none`だった。

この観測は、SA起動判断をモデルへ残しつつ、明示packetと許可済みreadで十分な場合は全履歴を追加しないという境界へ、このN=5の実行が収束したことと整合する。ただし、未観測caseでの安定性、prompt変更との因果、N=5を超えたtoken効果は確定しない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate5-candidate11-expanded12-n5-20260716.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v2`
- generated at: `2026-07-16T17:36:37+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。この12 case、`N=5`の観測範囲を超えて一般化しない。
