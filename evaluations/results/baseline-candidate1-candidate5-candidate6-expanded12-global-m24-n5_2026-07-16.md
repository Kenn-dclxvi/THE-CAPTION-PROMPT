# Baseline, Candidate1, Candidate5 and Candidate6 expanded 12-case N=5 comparison view

## Compared results

| label | prompt set identity | result ID |
| --- | --- | --- |
| Base | `the-caption-3ce91a4-current-r2` / `r2` / `63225d…e48d` | `7748386da9cf4cc8a5fc35025f5972f2` |
| C1 | `the-caption-9b3a96a-revision-2-r1` / `r1` / `f5ea64…c865` | `7105fa9353824d3187ad299c1f3542f3` |
| C5 | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `c93afa1d55b149b6b6499219d07d0f77` |
| C6 | `the-caption-3ce91a4-context-efficiency-r1` / `r1` / `ffd54c…b907` | `db405b73e3ca4ed5aa367bed3fa1e5ce` |

- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- set: `the-caption-revision-2-expanded12-r1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / effort: `gpt-5.6-sol` / `high`
- repetition: `N=5`
- execution: `global_queue`、`M=24`
- registered valid runs: 各prompt set `60 / 60`
- excluded attempts: 各prompt set `0`

evaluation set revision、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件は4 resultで一致している。Baseのreference指定は差分方向だけを固定し、採用状態や順位を表さない。

## KPI median comparison

| set | `quality_score` | `total_tokens` | `elapsed_seconds` | runner wall time |
| --- | ---: | ---: | ---: | ---: |
| Base | 100.000 | 3,888,115 | 2,828.032秒 | 733.867秒 |
| C1 | 97.917 | 4,338,633 | 1,932.971秒 | 635.451秒 |
| C5 | 100.000 | 4,503,816 | 1,714.914秒 | 426.528秒 |
| C6 | 100.000 | 4,692,041 | 1,715.486秒 | 476.489秒 |

C6から各setを引いた値を示す。runner wall timeはLayer 4 KPIではない。

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` | runner wall time |
| --- | ---: | ---: | ---: | ---: |
| C6 - Base | 0.000 | +803,926 | -1,112.547秒 | -257.378秒 |
| C6 - C1 | +2.083 | +353,408 | -217.485秒 | -158.962秒 |
| C6 - C5 | 0.000 | +188,225 | +0.571秒 | +49.961秒 |

KPIへ優先順位や閾値を設定せず、差分をwinner、採用可否、release判断へ変換しない。

## Quality distribution

| set | iteration quality | score 1 | score 3 | score 4 |
| --- | --- | ---: | ---: | ---: |
| Base | `97.917 / 97.917 / 100 / 100 / 100` | 0 | 2 | 58 |
| C1 | `100 / 100 / 97.917 / 97.917 / 97.917` | 0 | 3 | 57 |
| C5 | `100 / 100 / 100 / 100 / 100` | 0 | 0 | 60 |
| C6 | `100 / 100 / 93.750 / 97.917 / 100` | 1 | 1 | 58 |

C6のscore `3`はF04 iteration 4のcleanup未完了、score `1`はF10 monthly review iteration 3の開始identity誤認によるreview未実施である。quality中央値だけではこの2 runを表さないため、分布を併記する。

## Token observation

C6のiteration totalはC5に対してiteration 1、3、4、5で少なく、iteration 2で731,346多い。各setの5値から算出する標準KPI中央値はC6がC5より188,225多い。

case別5回中央値でC6とC5の差が大きい箇所を示す。これはLayer 4 KPIではなく、保存済みcase resultを使った補助観測である。

| case | C1 | C5 | C6 | C6 - C5 |
| --- | ---: | ---: | ---: | ---: |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 549,123 | 978,822 | 1,179,844 | +201,022 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 345,031 | 427,131 | 493,131 | +66,000 |
| `TC-F07-CANONICAL-V4-RUNNER` | 731,298 | 717,248 | 519,244 | -198,004 |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 643,401 | 550,928 | 448,515 | -102,413 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 321,985 | 331,202 | 294,787 | -36,415 |

親runのcommand evidenceでは、`docs/orchestration-process.md`読取outputはC5の834,300文字からC6の728,831文字、`docs/prompt-guide.md`読取outputは161,700文字から24,767文字になった。一方、`total_tokens`中央値は上表の値となった。この文字数はtoken KPIではなく、JIT節参照が実行されたかを見る補助観測である。

## View artifact and boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/baseline-candidate1-candidate5-candidate6-expanded12-n5-20260716.json`
- schema: `the-caption-prompt.prompt-set-comparison-view/v1`
- generated at: `2026-07-16T02:21:26+09:00`

prompt setの優劣、採用、release判断、THE-CAPTION本体変更は行っていない。この12 case、`N=5`の観測範囲を超えて一般化しない。
