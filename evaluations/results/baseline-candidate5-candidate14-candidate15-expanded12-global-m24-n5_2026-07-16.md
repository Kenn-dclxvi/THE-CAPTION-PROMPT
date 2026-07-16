# Baseline, Candidate5, Candidate14 and Candidate15 expanded 12-case N=5 comparison view

## Compared results

| label | prompt set identity | result ID |
| --- | --- | --- |
| Baseline | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `b38148b0022343539b928058aa15d3a2` |
| C5 | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `da8505348e4741a4a413618fbfa9aa1f` |
| C14 | `the-caption-9b3a96a-validation-authority-precedence-r1` / `r1` / `31417f…713f` | `dceb30c459f14796a2e33f05f089190f` |
| C15 | `the-caption-9b3a96a-selected-role-control-input-boundary-r1` / `r1` / `1a2ef9…6db8` | `010b5b71f3154b6593590e9c6655ec1b` |

- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- set: `the-caption-revision-2-expanded12-r1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / effort: `gpt-5.6-sol` / `high`
- repetition / execution: `N=5` / `global_queue` / `M=24`
- token accounting: `all_agents` / `v1`
- registered valid runs: 各prompt set `60 / 60`
- excluded attempts: 各prompt set `0`

evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件は4 resultで一致している。Baselineのreference指定は差分方向だけを固定し、採用状態や順位を表さない。

## KPI median comparison

| set | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| Baseline | 100.000 | 8,925,798 | 2,828.032秒 |
| C5 | 100.000 | 5,740,441 | 1,714.914秒 |
| C14 | 100.000 | 4,648,809 | 1,753.159秒 |
| C15 | 100.000 | 4,590,751 | 1,723.986秒 |

C15から各setを引いた中央値差を示す。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| C15 - Baseline | 0.000 | -4,335,047 | -1,104.046秒 |
| C15 - C5 | 0.000 | -1,149,690 | +9.072秒 |
| C15 - C14 | 0.000 | -58,058 | -29.172秒 |

KPIへ優先順位や閾値を設定せず、差分をwinner、採用可否、release判断へ変換しない。

## Iteration KPI

| set | iteration 1 | iteration 2 | iteration 3 | iteration 4 | iteration 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline quality | 97.917 | 97.917 | 100.000 | 100.000 | 100.000 |
| C5 quality | 100.000 | 100.000 | 100.000 | 100.000 | 100.000 |
| C14 quality | 97.917 | 100.000 | 100.000 | 100.000 | 100.000 |
| C15 quality | 100.000 | 100.000 | 100.000 | 100.000 | 100.000 |
| Baseline tokens | 7,581,140 | 9,484,133 | 8,925,798 | 7,941,733 | 8,928,098 |
| C5 tokens | 5,855,472 | 5,412,804 | 5,740,441 | 5,488,979 | 6,048,087 |
| C14 tokens | 4,247,596 | 4,838,340 | 4,877,774 | 4,648,809 | 4,409,069 |
| C15 tokens | 4,593,031 | 4,590,751 | 4,878,140 | 4,366,566 | 4,178,176 |
| Baseline seconds | 2,785.312 | 3,255.848 | 2,764.735 | 2,975.869 | 2,828.032 |
| C5 seconds | 1,735.306 | 1,626.771 | 1,714.914 | 1,651.643 | 1,757.682 |
| C14 seconds | 1,579.889 | 1,713.747 | 1,887.801 | 1,860.651 | 1,753.159 |
| C15 seconds | 1,765.415 | 1,698.772 | 1,784.063 | 1,640.927 | 1,723.986 |

## Quality distribution

| set | score `3` | score `4` |
| --- | ---: | ---: |
| Baseline | 2 | 58 |
| C5 | 0 | 60 |
| C14 | 1 | 59 |
| C15 | 0 | 60 |

C15ではC14のF10 inventory未完了停止は再現せず、60 runすべてscore `4`だった。C15のF10 inventory iteration 1は独立checkを再実行したが、最終成果とterminal dispositionを満たした。

## Case elapsed comparison

caseごと5回の`elapsed_seconds`中央値をC15の値が大きい順に示す。これは補助分析であり、Layer 4の標準KPIはiteration別totalとその中央値である。

| case | Baseline | C5 | C14 | C15 | C15 - C5 | C15 - C14 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F03 atomic cleanup | 370.910 | 153.752 | 193.619 | 225.644 | +71.893 | +32.025 |
| F02 history date bound | 408.171 | 352.938 | 214.562 | 206.252 | -146.686 | -8.309 |
| F04 web audit column | 326.652 | 193.282 | 206.359 | 193.108 | -0.174 | -13.251 |
| F06 empty snapshot | 314.481 | 183.470 | 180.111 | 189.174 | +5.703 | +9.063 |
| F07 canonical runner | 391.545 | 250.493 | 211.774 | 181.276 | -69.216 | -30.498 |
| F08 CLI sync | 285.836 | 136.860 | 206.203 | 173.812 | +36.952 | -32.391 |
| F07 dependency pair | 250.049 | 119.844 | 156.420 | 159.125 | +39.281 | +2.704 |
| F10 inventory review | 89.488 | 71.694 | 130.894 | 137.401 | +65.707 | +6.508 |
| F01 duplicate asset key | 300.817 | 84.063 | 89.830 | 81.483 | -2.580 | -8.348 |
| F05 production deploy | 28.069 | 31.262 | 65.810 | 75.921 | +44.659 | +10.110 |
| F10 monthly review | 60.770 | 56.077 | 60.821 | 47.219 | -8.858 | -13.602 |
| F05 clarify units | 22.783 | 16.637 | 24.413 | 17.883 | +1.246 | -6.529 |

C15の標準elapsed中央値はC5より9.072秒長く、C14より29.172秒短い。case別にはF03とF10 inventoryがC5 / C14より長い方向で、F02、F04、F07 runner等はC14より短い。case中央値を単純合計して標準KPI中央値差へ読み替えない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate5-candidate14-candidate15-expanded12-n5-20260716.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v2`
- generated at: `2026-07-16T20:01:42+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。この12 case、`N=5`の観測範囲を超えて一般化しない。
