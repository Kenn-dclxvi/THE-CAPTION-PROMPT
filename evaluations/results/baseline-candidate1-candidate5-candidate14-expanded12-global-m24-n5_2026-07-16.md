# Baseline, Candidate1, Candidate5 and Candidate14 expanded 12-case N=5 comparison view

## Compared results

| label | prompt set identity | result ID |
| --- | --- | --- |
| Baseline | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `b38148b0022343539b928058aa15d3a2` |
| C1 | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `fd30705e3c2e4f45b891d468f75badde` |
| C5 | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `da8505348e4741a4a413618fbfa9aa1f` |
| C14 | `the-caption-9b3a96a-validation-authority-precedence-r1` / `r1` / `31417f…713f` | `dceb30c459f14796a2e33f05f089190f` |

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
| C1 | 97.917 | 5,732,480 | 1,932.971秒 |
| C5 | 100.000 | 5,740,441 | 1,714.914秒 |
| C14 | 100.000 | 4,648,809 | 1,753.159秒 |

C14から各setを引いた中央値差を示す。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| C14 - Baseline | 0.000 | -4,276,989 | -1,074.874秒 |
| C14 - C1 | +2.083 | -1,083,671 | -179.812秒 |
| C14 - C5 | 0.000 | -1,091,632 | +38.245秒 |

KPIへ優先順位や閾値を設定せず、差分をwinner、採用可否、release判断へ変換しない。

## Iteration KPI

| set | iteration 1 | iteration 2 | iteration 3 | iteration 4 | iteration 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline quality | 97.917 | 97.917 | 100.000 | 100.000 | 100.000 |
| C1 quality | 100.000 | 100.000 | 97.917 | 97.917 | 97.917 |
| C5 quality | 100.000 | 100.000 | 100.000 | 100.000 | 100.000 |
| C14 quality | 97.917 | 100.000 | 100.000 | 100.000 | 100.000 |
| Baseline tokens | 7,581,140 | 9,484,133 | 8,925,798 | 7,941,733 | 8,928,098 |
| C1 tokens | 5,543,280 | 6,415,299 | 5,062,687 | 7,614,525 | 5,732,480 |
| C5 tokens | 5,855,472 | 5,412,804 | 5,740,441 | 5,488,979 | 6,048,087 |
| C14 tokens | 4,247,596 | 4,838,340 | 4,877,774 | 4,648,809 | 4,409,069 |
| Baseline seconds | 2,785.312 | 3,255.848 | 2,764.735 | 2,975.869 | 2,828.032 |
| C1 seconds | 1,932.971 | 1,735.112 | 1,513.648 | 2,221.309 | 2,022.353 |
| C5 seconds | 1,735.306 | 1,626.771 | 1,714.914 | 1,651.643 | 1,757.682 |
| C14 seconds | 1,579.889 | 1,713.747 | 1,887.801 | 1,860.651 | 1,753.159 |

## Quality distribution

| set | score `3` | score `4` |
| --- | ---: | ---: |
| Baseline | 2 | 58 |
| C1 | 3 | 57 |
| C5 | 0 | 60 |
| C14 | 1 | 59 |

C14のscore `3`はF10 entrypoint inventory iteration 1の独立response check未開始による未完了停止である。F04とF06の既知未完了はC14では再現していない。

## Case elapsed comparison

caseごと5回の`elapsed_seconds`中央値をC14の値が大きい順に示す。これは補助分析であり、Layer 4の標準KPIはiteration別totalとその中央値である。

| case | Baseline | C1 | C5 | C14 | C14 - C1 | C14 - C5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F02 history date bound | 408.171 | 174.652 | 352.938 | 214.562 | +39.909 | -138.377 |
| F07 canonical runner | 391.545 | 311.160 | 250.493 | 211.774 | -99.386 | -38.719 |
| F04 web audit column | 326.652 | 145.291 | 193.282 | 206.359 | +61.068 | +13.077 |
| F08 CLI sync | 285.836 | 220.850 | 136.860 | 206.203 | -14.647 | +69.343 |
| F03 atomic cleanup | 370.910 | 118.382 | 153.752 | 193.619 | +75.237 | +39.868 |
| F06 empty snapshot | 314.481 | 342.937 | 183.470 | 180.111 | -162.827 | -3.360 |
| F07 dependency pair | 250.049 | 130.487 | 119.844 | 156.420 | +25.933 | +36.577 |
| F10 inventory review | 89.488 | 90.454 | 71.694 | 130.894 | +40.439 | +59.199 |
| F01 duplicate asset key | 300.817 | 92.981 | 84.063 | 89.830 | -3.150 | +5.768 |
| F05 production deploy | 28.069 | 23.140 | 31.262 | 65.810 | +42.671 | +34.549 |
| F10 monthly review | 60.770 | 50.996 | 56.077 | 60.821 | +9.825 | +4.744 |
| F05 clarify units | 22.783 | 22.356 | 16.637 | 24.413 | +2.056 | +7.775 |

C14の標準elapsed中央値はC1より179.812秒短く、C5より38.245秒長い。case別にはF06とF07 runnerがC1 / C5の両方より短く、F03、F04、F10 inventory等はC5より長い。case中央値を単純合計して標準KPI中央値差へ読み替えない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate5-candidate14-expanded12-n5-20260716.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v2`
- generated at: `2026-07-16T18:56:38+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。この12 case、`N=5`の観測範囲を超えて一般化しない。
