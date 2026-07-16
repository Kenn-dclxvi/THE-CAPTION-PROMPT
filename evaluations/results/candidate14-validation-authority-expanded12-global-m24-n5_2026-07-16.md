# Candidate14 validation authority expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- valid run window: `2026-07-16T18:46:05+09:00`から`2026-07-16T18:53:51+09:00`
- profile: `candidate14-validation-authority-expanded12-global-m24-n5-r1`
- set ID / Layer 1 identity: `the-caption-revision-2-expanded12-r1` / `787521e5f0c0c261dcec0e3933d9f8b839481ed363fff6c5ae7672cdb699ef88`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはCandidate14を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-validation-authority-precedence-r1` / `r1`
- bundle SHA-256: `31417f770dfd1f7072ca9abda10cb3b6e1a27c2a5a898284b40f536aa4a9713f`
- direct source identity: `the-caption-9b3a96a-review-route-entry-boundary-r1`
- changed target from direct source: `AGENTS.md`だけ
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`

Candidate14はCandidate13のreview route / role接続を維持し、TaskSpecがrequired machine commandとscope / pass conditionを明示した場合はその記載をvalidation authorityとする境界を追加した。変更class別completionは明示commandがない場合だけdefaultとして使う。TaskSpec、required command自体、worker cardinality、role prompt、具体的test pathは変更していない。

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 97.917 | 4,247,596 | 1,579.889 |
| 2 | 100.000 | 4,838,340 | 1,713.747 |
| 3 | 100.000 | 4,877,774 | 1,887.801 |
| 4 | 100.000 | 4,648,809 | 1,860.651 |
| 5 | 100.000 | 4,409,069 | 1,753.159 |
| median | 100.000 | 4,648,809 | 1,753.159 |

60 runのscore内訳はscore `4`が59件、score `3`が1件である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Boundary observations

- F04の5 runはすべてNode 3 commandと独立reviewを完了し、Candidate12で観測したreview-only routeの未完了停止は再現しなかった。
- F06の5 runはすべてTaskSpecが明示した対象testとtests全体を実行し、対象`23 passed`、全体`326 passed, 3 skipped`、独立contract audit停止0まで完了した。`main_verify.sh`は5 runとも0回だった。
- F10 entrypoint inventory iteration 1はinventory成果とzero driftを提示したが、rootが独立response check用`prompts/review.md`の読取りとTaskSpecのread scopeを競合と判断し、workerを起動せずF10-C1 / C2を未完了扱いにして停止したためscore `3`とした。
- F10 monthly review iteration 4はTaskSpecが要求する`HEAD^`と固定seedの一致が得られず、diffを読まずzero driftで停止した。これは明示停止条件どおりのterminal dispositionとしてscore `4`とした。
- 許可外path差分とexternal failureはなく、rootと全descendant SAの最終token usageを60 / 60で完全取得した。

all-agent usageでは44 runがworkerを1本起動し、16 runはworkerを起動しなかった。2本以上を起動したrunは0で、child worker総数は44だった。F04とF06は各5 runともworker 1本である。

## Direct-parent observation

Candidate12中央値はquality `97.917`、tokens `4,757,900`、elapsed `1,777.127`秒だった。Candidate14 - Candidate12はquality `+2.083`、tokens `-109,091`、elapsed `-23.968`秒である。Candidate14はCandidate12からCandidate13とCandidate14の2境界を積み上げたidentityであり、この差分を個別境界1つの効果へ分解しない。

F04とF06の既知未完了は解消した一方、F10 inventoryのread scope / response-check接続が1件残った。したがって構築と固定N=5評価は完了したが、60 / 60がscore `4`へ収束した状態ではない。

## Result identity and storage

- runner wall time: `465.174`秒
- result ID: `dceb30c459f14796a2e33f05f089190f`
- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/dceb30c459f14796a2e33f05f089190f.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate14-validation-authority-expanded12-global-m24-n5-20260716-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。この結論は採用、release承認、THE-CAPTION本体へのruntime反映を意味しない。
