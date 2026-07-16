# Baseline, Candidate1, Candidate5 and Candidate12 expanded 12-case N=5 comparison view

## Compared results

| label | prompt set identity | result ID |
| --- | --- | --- |
| Baseline | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `b38148b0022343539b928058aa15d3a2` |
| C1 | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `fd30705e3c2e4f45b891d468f75badde` |
| C5 | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `da8505348e4741a4a413618fbfa9aa1f` |
| C12 | `the-caption-9b3a96a-non-machine-route-cardinality-r1` / `r1` / `4e83de…f7fd` | `7ed431c7fc1b436b8de73ae336645089` |

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
| C12 | 97.917 | 4,757,900 | 1,777.127秒 |

C12から各setを引いた中央値差を示す。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| C12 - Baseline | -2.083 | -4,167,898 | -1,050.906秒 |
| C12 - C1 | 0.000 | -974,580 | -155.844秒 |
| C12 - C5 | -2.083 | -982,541 | +62.213秒 |

KPIへ優先順位や閾値を設定せず、差分をwinner、採用可否、release判断へ変換しない。

## Iteration KPI

| set | iteration 1 | iteration 2 | iteration 3 | iteration 4 | iteration 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline quality | 97.917 | 97.917 | 100.000 | 100.000 | 100.000 |
| C1 quality | 100.000 | 100.000 | 97.917 | 97.917 | 97.917 |
| C5 quality | 100.000 | 100.000 | 100.000 | 100.000 | 100.000 |
| C12 quality | 97.917 | 97.917 | 100.000 | 97.917 | 100.000 |
| Baseline tokens | 7,581,140 | 9,484,133 | 8,925,798 | 7,941,733 | 8,928,098 |
| C1 tokens | 5,543,280 | 6,415,299 | 5,062,687 | 7,614,525 | 5,732,480 |
| C5 tokens | 5,855,472 | 5,412,804 | 5,740,441 | 5,488,979 | 6,048,087 |
| C12 tokens | 4,757,900 | 4,300,587 | 4,197,262 | 5,052,635 | 5,020,031 |
| Baseline seconds | 2,785.312 | 3,255.848 | 2,764.735 | 2,975.869 | 2,828.032 |
| C1 seconds | 1,932.971 | 1,735.112 | 1,513.648 | 2,221.309 | 2,022.353 |
| C5 seconds | 1,735.306 | 1,626.771 | 1,714.914 | 1,651.643 | 1,757.682 |
| C12 seconds | 1,777.127 | 1,663.078 | 1,658.371 | 1,927.122 | 1,903.191 |

## Quality distribution

| set | score `1` | score `3` | score `4` |
| --- | ---: | ---: | ---: |
| Baseline | 0 | 2 | 58 |
| C1 | 0 | 3 | 57 |
| C5 | 0 | 0 | 60 |
| C12 | 0 | 3 | 57 |

Baselineのscore `3`はF04のcleanup後の未完了停止、C1のscore `3`はF03 / F06のvalidation authority conflictによる未完了停止である。C12のscore `3`はF04のreview-only routeとrole prompt前提の不一致1件、F06のvalidation authority conflict 2件である。

## Case elapsed comparison

caseごと5回の`elapsed_seconds`中央値をC12の値が大きい順に示す。これは保存済みcase resultを使った補助分析であり、Layer 4の標準KPIはiteration別totalとその中央値である。

| rank | case | Baseline | C1 | C5 | C12 | C12 - C1 | C12 - C5 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | F04 web audit column | 326.652 | 145.291 | 193.282 | 279.585 | +134.294 | +86.303 |
| 2 | F02 history date bound | 408.171 | 174.652 | 352.938 | 236.203 | +61.551 | -116.735 |
| 3 | F06 empty snapshot | 314.481 | 342.937 | 183.470 | 216.986 | -125.951 | +33.516 |
| 4 | F07 canonical runner | 391.545 | 311.160 | 250.493 | 204.778 | -106.382 | -45.715 |
| 5 | F03 atomic cleanup | 370.910 | 118.382 | 153.752 | 188.865 | +70.483 | +35.113 |
| 6 | F08 CLI sync | 285.836 | 220.850 | 136.860 | 174.610 | -46.240 | +37.750 |
| 7 | F07 dependency pair | 250.049 | 130.487 | 119.844 | 142.822 | +12.335 | +22.978 |
| 8 | F10 inventory review | 89.488 | 90.454 | 71.694 | 133.825 | +43.371 | +62.131 |
| 9 | F01 duplicate asset key | 300.817 | 92.981 | 84.063 | 92.836 | -0.145 | +8.773 |
| 10 | F05 production deploy | 28.069 | 23.140 | 31.262 | 75.583 | +52.443 | +44.321 |
| 11 | F10 monthly review | 60.770 | 50.996 | 56.077 | 46.990 | -4.006 | -9.087 |
| 12 | F05 clarify units | 22.783 | 22.356 | 16.637 | 21.140 | -1.216 | +4.503 |

C12はF07 runnerでC1より106.382秒、C5より45.715秒短く、F08もC1より46.240秒短かった。一方、F04、F03、F10 inventory等はC5より長い。C12とC5の標準elapsed中央値差は62.213秒であり、case別に一様な方向ではない。

case中央値の合計は、同じiteration内の12 case totalを先に合計して5 iterationの中央値を取る標準`elapsed_seconds`とは一致しない。そのため、case差を単純合計してKPI中央値差へ読み替えない。

## Direct-parent diagnostic

C11の中央値はquality 100.000、tokens 5,726,760、elapsed 2,301.432秒だった。C12 - C11はquality -2.083、tokens -968,860、elapsed -524.305秒である。

C11はchild worker 59本、workerあり36 run、2 worker以上21 runだった。C12はchild worker 41本、workerあり41 runで、全runが最大1 workerだった。C11で2 workerだったF03、F07 runner、F07 dependency、F08は、C12では原則1 workerへ収束し、各caseのelapsed中央値はC11からそれぞれ136.143、124.677、127.277、152.405秒少ない。

この結果はroute cardinality境界がworker chainを短くしたことと整合するが、quality維持は確認できなかった。F04のreview-only経路をrole promptが許さない不整合とF06のvalidation authority conflictを解消せず、elapsedだけを理由にC12を一般化しない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate5-candidate12-expanded12-n5-20260716.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v2`
- generated at: `2026-07-16T18:21:52+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。この12 case、`N=5`の観測範囲を超えて一般化しない。
