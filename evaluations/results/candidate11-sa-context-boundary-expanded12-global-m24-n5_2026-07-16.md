# Candidate11 SA context sufficiency boundary expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- valid run window: `2026-07-16T17:26:02+09:00`から`2026-07-16T17:35:31+09:00`
- profile: `candidate11-sa-context-boundary-expanded12-global-m24-n5-r1`
- set ID / Layer 1 identity: `the-caption-revision-2-expanded12-r1` / `787521e5f0c0c261dcec0e3933d9f8b839481ed363fff6c5ae7672cdb699ef88`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはCandidate11を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-sa-context-sufficiency-boundary-r1` / `r1`
- bundle SHA-256: `a28b65fe0d4e5b140ef475499403c3c05bf34d9fe90ad79158fa6f54e33173fd`
- direct source identity: `the-caption-9b3a96a-c1-counter-applicability-boundary-r1`
- changed target: `AGENTS.md`だけ
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`

Candidate11はC10の構造とcounter applicability境界を維持し、rootがworkerへ明示的なtask packetを渡すこと、packetと許可済みreadで担当criterionに十分なら追加の会話履歴を継承しないこと、不足する場合だけ必要最小範囲を追加することをJIT Contextへ並列の境界として追加した。SA起動の要否、worker数、担当criterionは固定せず、モデル判断のまま維持する。

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 4,547,060 | 1,974.255 |
| 2 | 100.000 | 5,728,147 | 2,301.432 |
| 3 | 100.000 | 6,155,614 | 2,365.843 |
| 4 | 100.000 | 5,070,202 | 2,177.196 |
| 5 | 100.000 | 5,726,760 | 2,330.804 |
| median | 100.000 | 5,726,760 | 2,301.432 |

60 runのscore内訳はscore `4`が60件である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Case observation

- F03 / F06は各5 runともvalidation authorityの競合で停止せず、所定成果とrequired validationへ到達した。
- F08の5 runはweekly / monthly command同期を完了し、F10の10 runは指定されたread-only review結果を返した。
- F04の5 runはNode validation後のtest-owned temporary outputをcleanupした。
- `machine_rework_max=not_applicable`または`environment_recovery_max=not_applicable`を持つcaseもcounter domain停止へ分岐しなかった。
- 60 runで許可外path差分とexternal failureはなく、rootと全descendant SAの最終token usageを完全に取得した。

この観測は固定した12 case、各5反復に限定する。未観測のTaskSpec、別のmodelまたはAgent環境へ一般化しない。

## SA context diagnostic

`layer2/extensions`のsession usageとspawn記録を使い、Candidate11の追加境界が対象としたSA context継承を補助分析した。この内訳はquality ratingまたは標準KPI comparisonへ入力しない。

F07 canonical v4 runnerでは、各iterationともcontract auditとquality reviewの2 workerを起動し、10 spawnすべてが`fork_turns=none`だった。worker数を減らしたのではなく、明示packetで担当criterionを実行し、root会話履歴の全継承を選ばなかった。

| iteration | `fork_turns` | root tokens | SA tokens | all-agent tokens |
| ---: | --- | ---: | ---: | ---: |
| 1 | `none`, `none` | 540,428 | 99,387 | 639,815 |
| 2 | `none`, `none` | 674,650 | 112,510 | 787,160 |
| 3 | `none`, `none` | 1,269,894 | 301,097 | 1,570,991 |
| 4 | `none`, `none` | 711,681 | 114,395 | 826,076 |
| 5 | `none`, `none` | 872,441 | 215,439 | 1,087,880 |

同caseのall-agent中央値はC1が1,235,665、C10が1,836,061、C11が826,076である。C1は`fork_turns=all`が2 / 5、C10は3 / 5だったのに対し、C11は5 / 5で全workerが`none`だった。C11 - C10のcase中央値差は-1,009,985 tokensである。

F10 entrypoint inventory reviewはC11でresponse-check SAを起動したのが2 / 5で、どちらも`fork_turns=none`だった。残り3 runはSAを起動せず、read-only結果をrootが返した。all-agent中央値はC1が108,190、C10が273,845、C11が91,451である。

以上は、Candidate11の境界と「必要なworkerは維持し、十分なpacketがある場合は追加履歴を継承しない」という実行選択が、このN=5で整合したことを示す。ただしprompt変更だけを原因とする因果推定や、今後も必ず`none`へ固定されるという一般化は行わない。

## Conclusion

Candidate11はC10直接派生として、SAの起動判断をモデルへ残したまま、worker contextの十分性境界だけを`AGENTS.md`へ追加した。固定expanded 12 caseのN=5では60 / 60 runがscore `4`となり、設計対象のF07 runnerでは必要な2 workerを各runで維持しながら、全spawnが`fork_turns=none`へ揃った。

Candidate11のprompt構築と固定N=5評価は完了とする。この結論は採用、release承認、THE-CAPTION本体へのruntime反映を意味しない。これらは未判断、未実施のまま保持する。

## Result identity and storage

- runner wall time: `568.812`秒
- result ID: `92122870831b49f19114aeaf906fc5bb`
- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/92122870831b49f19114aeaf906fc5bb.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate11-sa-context-boundary-expanded12-global-m24-n5-20260716-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。
