# Candidate15 selected-role control input expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- valid run window: `2026-07-16T19:53:36+09:00`から`2026-07-16T20:00:57+09:00`
- profile: `candidate15-selected-role-control-input-expanded12-global-m24-n5-r1`
- set ID / Layer 1 identity: `the-caption-revision-2-expanded12-r1` / `787521e5f0c0c261dcec0e3933d9f8b839481ed363fff6c5ae7672cdb699ef88`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはCandidate15を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-selected-role-control-input-boundary-r1` / `r1`
- bundle SHA-256: `1a2ef9e069bd81c361775ec1acbc5806d116a93328a74abc19137ef17b576db8`
- direct source identity: `the-caption-9b3a96a-validation-authority-precedence-r1`
- changed target from direct source: `AGENTS.md`だけ
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`

Candidate15はCandidate14のroute、role、validation authority境界を維持し、ordered input manifestへ事前bindされactive gateが選んだroot authority / role promptをcontrol inputとして扱う境界を追加した。selected roleはcriterion evidence、permission、worker read scopeを増やさず、TaskSpecのrepository read scopeは対象repositoryの事実取得へ適用する。TaskSpec、role prompt、required command、worker route自体は変更していない。

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 4,593,031 | 1,765.415 |
| 2 | 100.000 | 4,590,751 | 1,698.772 |
| 3 | 100.000 | 4,878,140 | 1,784.063 |
| 4 | 100.000 | 4,366,566 | 1,640.927 |
| 5 | 100.000 | 4,178,176 | 1,723.986 |
| median | 100.000 | 4,590,751 | 1,723.986 |

60 runのscore内訳はscore `4`が60件である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Boundary observations

- F10 entrypoint inventoryは5 / 5でinventory、zero drift、独立response checkを完了し、Candidate14で観測したrole promptとrepository read scopeの競合停止は再現しなかった。
- F10 inventory iteration 1は初回worker packetにF10-C1〜C3の判定文がなくblockerとなり、criterionを補ったfresh packetでnon-machine reworkを1回実行した。最終成果は全criterionを満たしたが、このrunだけchild workerは2本だった。
- 残るF10 inventory 4 runは各worker 1本で完了した。
- F04は5 / 5でNode 3 commandと独立reviewを完了した。
- F06は5 / 5でTaskSpec明示の対象testとtests全体を実行し、対象`23 passed`、全体`326 passed, 3 skipped`、独立contract audit停止0まで完了した。`main_verify.sh`は5 runとも0回だった。
- 許可外path差分とexternal failureはなく、rootと全descendant SAの最終token usageを60 / 60で完全取得した。

all-agent usageでは43 runがworkerを起動し、17 runはworkerを起動しなかった。child worker総数は44で、59 runはworker最大1本、F10 inventory iteration 1だけ2本だった。C15の「selected roleを一度control inputとして解決する」境界はrole接続停止を解消した一方、packet不足後のfresh confirmationまで一律に1 workerへ閉じるものではなかった。

## Direct-parent observation

Candidate14中央値はquality `100.000`、tokens `4,648,809`、elapsed `1,753.159`秒だった。Candidate15 - Candidate14はquality `0.000`、tokens `-58,058`、elapsed `-29.172`秒である。quality分布はCandidate14のscore `4` 59件 / score `3` 1件から、Candidate15のscore `4` 60件へ変わった。

このN=5では既知のrole接続停止を再現しなかったが、F10 inventoryの1 runでpacket completenessを原因とするworker再実行が観測された。構築と固定N=5評価は完了したが、全runでworker最大1本へ収束した状態ではない。

## Result identity and storage

- runner wall time: `440.538`秒
- result ID: `010b5b71f3154b6593590e9c6655ec1b`
- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/010b5b71f3154b6593590e9c6655ec1b.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate15-selected-role-control-input-expanded12-global-m24-n5-20260716-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。この結論は採用、release承認、THE-CAPTION本体へのruntime反映を意味しない。
