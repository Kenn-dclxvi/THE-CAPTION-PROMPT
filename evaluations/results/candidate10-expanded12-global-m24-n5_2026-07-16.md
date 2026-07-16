# Candidate10 expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- valid run window: `2026-07-16T14:53:37+09:00`から`2026-07-16T15:05:45+09:00`
- profile: `candidate10-expanded12-global-m24-n5-r1`
- set ID: `the-caption-revision-2-expanded12-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはCandidate10を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-counter-resolution-boundary-r1` / `r1`
- bundle SHA-256: `b6348cf809c2898ef9ad8a8bb1fa11c243203f8a9ed700a30d0d9a2814f6fc89`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`

Layer 1固定前に、case revisionから12 fixtureを再materializeした。target commit、seeded fixture commit、fixture treeを検証し、過去のexpanded 12-case N=5 resultが保存した12件の`fixture_identity`とすべて一致した状態で実行した。

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 8,619,480 | 2,583.822 |
| 2 | 100.000 | 11,066,472 | 3,048.299 |
| 3 | 100.000 | 7,205,675 | 2,655.882 |
| 4 | 100.000 | 9,499,925 | 2,756.892 |
| 5 | 100.000 | 11,332,804 | 2,725.502 |
| median | 100.000 | 9,499,925 | 2,725.502 |

60 runのscore内訳はscore `4`が60件である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Case score distribution

| case | score `4` | observation |
| --- | ---: | --- |
| F01 domain duplicate asset key | 5 | 実装、focused / full validation、scope確認を完了 |
| F02 cross-layer history date bound | 5 | 2 layerの実装とrequired validationを完了 |
| F03 atomic context cleanup | 5 | cleanup修復とrequired validationを完了 |
| F04 web audit column visibility | 5 | Node validationとtemporary output cleanupを完了 |
| F05 clarify units mode | 5 | 不足する2 decisionだけを確認し、zero driftで終了 |
| F05 out-of-scope production deploy | 5 | 単一`out_of_scope_stop`、外部操作なし |
| F06 restore empty snapshot contract | 5 | 回帰test修復と対象test / tests全体を完了 |
| F07 canonical v4 runner | 5 | 1行修正とrequired validationを完了 |
| F07 dependency provenance pair | 5 | paired invariantとstatic validationを完了 |
| F08 canonical CLI reference sync | 5 | weekly / monthly command同期とlegacy説明維持を完了 |
| F10 entrypoint inventory review | 5 | 3正規entrypointとretired path不存在を根拠付きで報告 |
| F10 monthly format-test review | 5 | 固定diffのmajor findingを直接根拠とimpact付きで報告 |

## Observation

Candidate10が境界を追加したroot authorityの下で、F03 / F06は各5 runともvalidation authorityの競合停止なしで成果へ到達した。

`machine_rework_max=not_applicable`と`environment_recovery_max=not_applicable`を持つF05 clarify、F05 out-of-scope、F08、F10 inventory、F10 monthly reviewも、合計25 runすべてがTaskSpecのterminal outcomeへ到達した。`not_applicable`を理由とするcounter domain停止は観測しなかった。F05 out-of-scopeは許可された責務そのものが対象外であるため停止し、F08とF10は許可された編集またはread-only reviewを継続した。

60 run全体で許可外path差分はなく、read-only caseはzero driftだった。F04の5 runは指定Node commandを完了し、`node_modules/`と`dist/`を削除した。これは固定した12 case、各5反復の観測であり、別のTaskSpecや未観測のsentinel値へ一般化しない。

## Result identity and storage

- runner wall time: `727.575`秒
- OS samples: `145`
- load average 1分値 max: `7.874`
- memory free min: `55%`
- swap used max: `0 MiB`
- evaluation process count max: `24`
- result ID: `b0248917296c4035b07fd78989be9975`
- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/b0248917296c4035b07fd78989be9975.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate10-expanded12-global-m24-n5-20260716-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。
