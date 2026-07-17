# Candidate17 operation-qualified evidence expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-17`（Asia/Tokyo）
- valid run window: `2026-07-17T04:49:08+09:00`から`2026-07-17T04:55:00+09:00`
- profile: `candidate17-operation-qualified-evidence-expanded12-global-m24-n5-r1`
- set ID / Layer 1 identity: `the-caption-revision-2-expanded12-r1` / `787521e5f0c0c261dcec0e3933d9f8b839481ed363fff6c5ae7672cdb699ef88`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはCandidate17を1つのimmutableな`prompt_set_identity`として保存した一次結果である。Candidate15連続試験と同じexecution compatibilityへ固定し、prompt identityだけをC17へ替えた。winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-operation-qualified-evidence-r1` / `r1`
- bundle SHA-256: `4c492dbb7b7bdf62d1602c6e6b1235cbce5ba2116f763cc64ae876527a740d4a`
- direct source identity: `the-caption-9b3a96a-gate-evidence-binding-r1`
- changed target from direct source: `AGENTS.md`だけ
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`
- compatibility conditions SHA-256: `bbd2c9e1302a2e8b6a613b7d8e556ab528d88532b7abc6df3dae84fc67d4a469`
- adapter: `the-caption-prompt.codex-adapter/v3`、repository snapshot `8542c647a8cfa19253df368738ddb1f86306c4c3`
- quality audit SHA-256: `b2a83dc1145c66d7c7f7a894ac02be15b7a25c4b8b2c24f458e4ee7d9002073a`

adapterとquality auditはCandidate15連続試験時点のsnapshotから実行し、quality auditは当時使用したfileとbyte-identicalである。Evaluation set、fixture、TaskSpec、permission、executor parameter、rating ruleは変更していない。

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 4,487,926 | 1,388.239 |
| 2 | 100.000 | 4,422,933 | 1,438.217 |
| 3 | 100.000 | 4,208,255 | 1,325.633 |
| 4 | 100.000 | 5,772,040 | 1,511.688 |
| 5 | 100.000 | 4,376,802 | 1,326.123 |
| median | 100.000 | 4,422,933 | 1,388.239 |

60 runのscore内訳はscore `4`が60件である。無変更のquality auditは60 / 60をrateableとし、failure countは0だった。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Candidate15との同条件数値差

| KPI中央値 | Candidate15 | Candidate17 | Candidate17 - Candidate15 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| `total_tokens` | 4,590,751 | 4,422,933 | -167,818 |
| `elapsed_seconds` | 1,723.986 | 1,388.239 | -335.747 |

Candidate15とCandidate17のcompatibility keyは同じ`ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`である。この表は3 KPIの数値差だけを示し、優劣や採用判断へ変換しない。

## Boundary observations

- F04 web audit columnは5 / 5で所定実装、`npm ci`、lint、build、cleanupを完了し、test-owned temporary outputを残した停止は0件だった。
- F10 monthly format-test reviewは5 / 5で固定diffのmajor finding、直接根拠、user-visible impact、zero driftを返し、開始identity誤認は0件だった。
- F10 entrypoint inventoryは5 / 5でinventoryとzero driftを完了した。
- unexpected changed path、adapter failure、token usage欠落は0件だった。

## 別条件runの扱い

本runの前に、typed boundary adapterと変更後の監査を使った60 runを実行し、result `bd3e27788c0e4d59b8c7fc44d13d5a0f`としてappend-only registryへ保存した。このrunはexecution compatibility key `29d023363e4458ca0c0c97b6dbcc7daee3af822267d456842b1eaa442fa8060b`であり、Candidate15連続試験と条件が異なる。履歴は削除しないが、本resultやCandidate15との同条件比較へ使用しない。

## Result identity and storage

- runner wall time: `351.998`秒
- result ID: `a5fa70a170664b23be9204d0c5a62710`
- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/a5fa70a170664b23be9204d0c5a62710.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate17-operation-qualified-evidence-expanded12-global-m24-n5-20260717-v3-r1`
- final archive SHA-256: `cec1969b493044f8f8e5ac77420060065fa9eba340a05f4ca1c9bafd500232ea`

raw evidenceとregistry resultはrepositoryへcommitしない。この結論は採用、release承認、THE-CAPTION本体へのruntime反映を意味しない。
