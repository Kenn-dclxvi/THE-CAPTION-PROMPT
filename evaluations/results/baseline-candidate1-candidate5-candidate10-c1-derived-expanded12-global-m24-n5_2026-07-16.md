# Baseline, Candidate1, Candidate5 and C1-derived Candidate10 expanded 12-case N=5 comparison view

## Compared results

| label | prompt set identity | result ID |
| --- | --- | --- |
| Baseline | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `b38148b0022343539b928058aa15d3a2` |
| C1 | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `fd30705e3c2e4f45b891d468f75badde` |
| C5 | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `da8505348e4741a4a413618fbfa9aa1f` |
| C10 | `the-caption-9b3a96a-c1-counter-applicability-boundary-r1` / `r1` / `8309a7…6592` | `f4eb6203148a4baa872a371298e2c2e3` |

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
| C10 | 100.000 | 6,798,932 | 2,359.190秒 |

C10から各setを引いた中央値差を示す。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| C10 - Baseline | 0.000 | -2,126,866 | -468.843秒 |
| C10 - C1 | +2.083 | +1,066,452 | +426.219秒 |
| C10 - C5 | 0.000 | +1,058,491 | +644.276秒 |

KPIへ優先順位や閾値を設定せず、差分をwinner、採用可否、release判断へ変換しない。

## Iteration KPI

| set | iteration 1 | iteration 2 | iteration 3 | iteration 4 | iteration 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline quality | 97.917 | 97.917 | 100.000 | 100.000 | 100.000 |
| C1 quality | 100.000 | 100.000 | 97.917 | 97.917 | 97.917 |
| C5 quality | 100.000 | 100.000 | 100.000 | 100.000 | 100.000 |
| C10 quality | 100.000 | 100.000 | 100.000 | 100.000 | 100.000 |
| Baseline tokens | 7,581,140 | 9,484,133 | 8,925,798 | 7,941,733 | 8,928,098 |
| C1 tokens | 5,543,280 | 6,415,299 | 5,062,687 | 7,614,525 | 5,732,480 |
| C5 tokens | 5,855,472 | 5,412,804 | 5,740,441 | 5,488,979 | 6,048,087 |
| C10 tokens | 6,043,766 | 6,456,037 | 6,798,932 | 7,685,886 | 9,505,778 |
| Baseline seconds | 2,785.312 | 3,255.848 | 2,764.735 | 2,975.869 | 2,828.032 |
| C1 seconds | 1,932.971 | 1,735.112 | 1,513.648 | 2,221.309 | 2,022.353 |
| C5 seconds | 1,735.306 | 1,626.771 | 1,714.914 | 1,651.643 | 1,757.682 |
| C10 seconds | 2,324.745 | 1,903.098 | 2,489.997 | 2,359.190 | 2,447.297 |

## Quality distribution

| set | score `1` | score `3` | score `4` |
| --- | ---: | ---: | ---: |
| Baseline | 0 | 2 | 58 |
| C1 | 0 | 3 | 57 |
| C5 | 0 | 0 | 60 |
| C10 | 0 | 0 | 60 |

Baselineのscore `3`はF04のcleanup後の未完了停止、C1のscore `3`はF03 / F06のvalidation authority conflictによる未完了停止である。C5とC10は固定12 caseの全60 runがscore `4`だった。

## Case token comparison

caseごと5回のall-agent `total_tokens`中央値を、C10の値が大きい順に示す。これは保存済みcase resultを使った補助分析であり、Layer 4の標準KPIはあくまでiteration別totalとその中央値である。

| rank | case | Baseline | C1 | C5 | C10 | C10 - C1 | C10 - C5 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | F07 canonical v4 runner | 1,091,802 | 1,235,665 | 1,100,595 | 1,836,061 | +600,396 | +735,466 |
| 2 | F02 cross-layer history date bound | 1,104,467 | 885,999 | 1,354,556 | 1,238,743 | +352,744 | -115,813 |
| 3 | F06 restore empty snapshot contract | 1,101,487 | 1,078,131 | 682,857 | 967,480 | -110,651 | +284,623 |
| 4 | F03 atomic context cleanup | 1,206,464 | 345,031 | 463,974 | 641,869 | +296,838 | +177,895 |
| 5 | F04 web audit column visibility | 1,029,236 | 651,100 | 599,520 | 590,487 | -60,613 | -9,033 |
| 6 | F07 dependency provenance pair | 677,603 | 287,872 | 296,697 | 566,250 | +278,378 | +269,553 |
| 7 | F08 canonical CLI reference sync | 690,231 | 509,559 | 401,471 | 554,297 | +44,738 | +152,826 |
| 8 | F01 domain duplicate asset key | 854,205 | 259,140 | 317,484 | 282,365 | +23,225 | -35,119 |
| 9 | F10 entrypoint inventory review | 107,346 | 108,190 | 90,111 | 273,845 | +165,655 | +183,734 |
| 10 | F10 monthly format-test review | 77,166 | 79,234 | 81,211 | 83,026 | +3,792 | +1,815 |
| 11 | F05 out-of-scope production deploy | 31,609 | 31,603 | 32,869 | 32,910 | +1,307 | +41 |
| 12 | F05 clarify units mode | 31,122 | 32,116 | 32,046 | 31,628 | -488 | -418 |

C10の上位4 caseの中央値合計は4,684,153 tokensで、12 caseのcase中央値合計7,098,961の約66%を占める。C5との差は、F07 runnerの`+735,466`、F06の`+284,623`、F07 dependencyの`+269,553`、F10 inventoryの`+183,734`、F03の`+177,895`が主な増加側であり、F02の`-115,813`などが一部相殺する。

F10 inventoryはC10内の絶対量で9位だが、C5の90,111から273,845へ約3.04倍となっている。一方、F05の2 caseは4 setとも約3.1万から3.3万で、C10の中央値差にはほぼ影響しない。

case中央値の合計は、同じiteration内の12 case totalを先に合計して5 iterationの中央値を取る標準`total_tokens`とは一致しない。そのため、上記のcase差を単純合計してKPI中央値差へ読み替えない。

## C10 root / SA diagnostic

C10の上位caseについて、`layer2/extensions`へ保存したall-agent usageからrootとdescendant SAの中央値を示す。この内訳はquality ratingまたはKPI comparisonへ入力しない診断情報である。各列の中央値は独立に計算するため、rootとSAの表示値の和がall-agent表示値と完全に一致しない場合がある。

| case | root median | SA median | all-agent median | SAありrun |
| --- | ---: | ---: | ---: | ---: |
| F07 canonical v4 runner | 994,507 | 917,727 | 1,836,061 | 5 / 5 |
| F02 cross-layer history date bound | 715,996 | 522,747 | 1,238,743 | 5 / 5 |
| F06 restore empty snapshot contract | 674,689 | 148,782 | 967,480 | 5 / 5 |
| F03 atomic context cleanup | 530,493 | 111,376 | 641,869 | 3 / 5 |
| F04 web audit column visibility | 306,832 | 283,655 | 590,487 | 4 / 5 |
| F07 dependency provenance pair | 304,529 | 182,905 | 566,250 | 4 / 5 |
| F08 canonical CLI reference sync | 363,482 | 193,224 | 554,297 | 5 / 5 |
| F10 entrypoint inventory review | 151,319 | 77,210 | 273,845 | 3 / 5 |

F07 runnerはrootとSAの両方が大きく、SAは5 runすべてで起動している。C10はC1直接派生であるため、SAの原因分析はC1と比較する。

| set | root total median | root input median | SA total median | SA input median | SA output median | SA本数 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| C1 | 731,298 | 725,850 | 279,969 | 273,388 | 7,574 | 2 / run |
| C10 | 994,507 | 987,686 | 917,727 | 905,761 | 11,553 | 2 / run、1 runだけ3 |

C1とC10はどちらもF07でcontract auditとquality reviewの2 workerを原則起動する。C10 iteration 3だけはauditのfresh confirmationにより3 workerとなった。より大きな差はworker数より、spawn時のroot履歴継承にある。

| iteration | C1 `fork_turns` | C1 root | C1 SA | C1 all-agent | C10 `fork_turns` | C10 root | C10 SA | C10 all-agent | C10 - C1 |
| ---: | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `none` | 1,257,160 | 225,490 | 1,482,650 | `none` | 696,013 | 113,372 | 809,385 | -673,265 |
| 2 | `all` | 731,298 | 872,352 | 1,603,650 | `all` | 994,507 | 1,131,694 | 2,126,201 | +522,551 |
| 3 | `all` | 572,853 | 662,812 | 1,235,665 | `none` | 1,379,570 | 297,922 | 1,677,492 | +441,827 |
| 4 | `none` | 827,761 | 168,728 | 996,489 | `all` | 918,334 | 917,727 | 1,836,061 | +839,572 |
| 5 | `none` | 726,524 | 279,969 | 1,006,493 | `all` | 996,852 | 1,101,740 | 2,098,592 | +1,092,099 |

C1は`fork_turns=all`が2 / 5、C10は3 / 5である。`none`のSA total中央値はC1が225,490、C10が205,647で、C10の方が19,843少ない。一方、`all`のSA total中央値はC1が767,582、C10が1,101,740である。C10で`all`が3回となったことにより、5回中央値が高い側へ移った。

`all`はworkerへrootの先行履歴を渡す。F07のC10ではSA input中央値905,761のcached inputが777,728で、SA outputは11,553に留まる。したがって、C1に対するC10のF07 SA増加の主因はoutputの長文化ではなく、`fork_turns=all`の出現回数と、継承したroot contextを各worker turnで再利用したinput tokenである。

F10 inventoryでも、response-check SA起動はC1が1 / 5、C10が3 / 5である。C1のall-agent中央値108,190に対し、C10はroot 151,319、SA 77,210、all-agent 273,845となった。

したがって、C1対C10のSA差は、promptのcounter applicability文言がSA packetを大きくした結果ではない。実行ごとの`fork_turns`選択とresponse-check起動の揺れが、N=5の中央値差を作っている。C10の変更はこれらのroutingまたはcontext継承方法を変更していないため、現在の差をcounter境界の固有costとは扱わない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate5-candidate10-c1-derived-expanded12-n5-20260716.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v2`
- generated at: `2026-07-16T16:16:52+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。この12 case、`N=5`の観測範囲を超えて一般化しない。
