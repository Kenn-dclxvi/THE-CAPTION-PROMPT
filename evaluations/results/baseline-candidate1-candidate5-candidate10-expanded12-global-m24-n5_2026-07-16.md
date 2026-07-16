# Baseline, Candidate1, Candidate5 and Candidate10 expanded 12-case N=5 comparison view

## Compared results

| label | prompt set identity | all-agent v2 result ID |
| --- | --- | --- |
| Base | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `b38148b0022343539b928058aa15d3a2` |
| C1 | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `fd30705e3c2e4f45b891d468f75badde` |
| C5 | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `da8505348e4741a4a413618fbfa9aa1f` |
| C10 | `the-caption-9b3a96a-counter-resolution-boundary-r1` / `r1` / `b6348c…fc89` | `b0248917296c4035b07fd78989be9975` |

- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- token accounting: `all_agents` / `v1`
- set: `the-caption-revision-2-expanded12-r1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / effort: `gpt-5.6-sol` / `high`
- repetition: `N=5`
- execution: `global_queue`、`M=24`
- registered valid runs: 各prompt set `60 / 60`
- excluded attempts: 各prompt set `0`

evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件、token accountingは4 resultで一致している。既存standalone resultのroot-only token値は履歴として保持し、この比較ではappend-onlyで追加されたall-agent v2 resultだけを使用する。

## KPI median comparison

| set | `quality_score` | `total_tokens` | `elapsed_seconds` | runner wall time |
| --- | ---: | ---: | ---: | ---: |
| Base | 100.000 | 8,925,798 | 2,828.032秒 | 733.867秒 |
| C1 | 97.917 | 5,732,480 | 1,932.971秒 | 635.451秒 |
| C5 | 100.000 | 5,740,441 | 1,714.914秒 | 426.528秒 |
| C10 | 100.000 | 9,499,925 | 2,725.502秒 | 727.575秒 |

C10から各setを引いた中央値差を示す。runner wall timeはLayer 4 KPIではない。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` | runner wall time |
| --- | ---: | ---: | ---: | ---: |
| C10 - Base | 0.000 | +574,127 | -102.530秒 | -6.292秒 |
| C10 - C1 | +2.083 | +3,767,445 | +792.532秒 | +92.124秒 |
| C10 - C5 | 0.000 | +3,759,484 | +1,010.588秒 | +301.047秒 |

KPIへ優先順位や閾値を設定せず、差分をwinner、採用可否、release判断へ変換しない。

## Quality distribution

| set | iteration quality | score `3` | score `4` | score `4`率 |
| --- | --- | ---: | ---: | ---: |
| Base | `97.917 / 97.917 / 100 / 100 / 100` | 2 | 58 | 96.7% |
| C1 | `100 / 100 / 97.917 / 97.917 / 97.917` | 3 | 57 | 95.0% |
| C5 | `100 / 100 / 100 / 100 / 100` | 0 | 60 | 100.0% |
| C10 | `100 / 100 / 100 / 100 / 100` | 0 | 60 | 100.0% |

| set | score `3`の観測箇所 |
| --- | --- |
| Base | F04 iteration 1 / 2でcleanup command拒否後に別commandへ切り替え、未完了停止 |
| C1 | F03 iteration 4、F06 iteration 3 / 5で成果と主要validation後にauthority conflictを理由として未完了停止 |
| C5 | なし |
| C10 | なし |

quality中央値が100のBaseにもscore `3`が2件あるため、中央値だけでなく60 runの分布を併記する。

## Observation

- C10とC5は60 runすべてscore `4`だった。
- C1でauthority conflict停止が出たF03 / F06は、C10では10 runすべて成果とrequired validationへ到達した。
- C10で境界対象となった`not_applicable`を持つF05、F08、F10の25 runも、counter domain停止なしでTaskSpecのterminal outcomeへ到達した。
- 同じ12 caseではC5も60 runすべてscore `4`であり、quality分布だけではC10固有の境界変更をC5に対する追加差として分離できない。
- C10の`total_tokens`中央値はBaseより574,127多く、C1より3,767,445、C5より3,759,484多い。`elapsed_seconds`中央値はBaseより102.530秒短く、C1より792.532秒、C5より1,010.588秒長い。

これは固定した12 case、各5反復の観測であり、未観測TaskSpecや別のsentinel値へ一般化しない。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate5-candidate10-expanded12-n5-20260716.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v2`
- generated at: `2026-07-16T15:16:21+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。
