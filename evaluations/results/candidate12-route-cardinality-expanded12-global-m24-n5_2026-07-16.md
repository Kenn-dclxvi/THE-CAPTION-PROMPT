# Candidate12 non-machine route cardinality expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- valid run window: `2026-07-16T18:12:03+09:00`から`2026-07-16T18:19:43+09:00`
- profile: `candidate12-route-cardinality-expanded12-global-m24-n5-r1`
- set ID / Layer 1 identity: `the-caption-revision-2-expanded12-r1` / `787521e5f0c0c261dcec0e3933d9f8b839481ed363fff6c5ae7672cdb699ef88`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultはCandidate12を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-non-machine-route-cardinality-r1` / `r1`
- bundle SHA-256: `4e83de8aaa147c5aed2fc92e74d2472fae0d87879c20d849e367b12c094af7fd`
- direct source identity: `the-caption-9b3a96a-sa-context-sufficiency-boundary-r1`
- changed target: `AGENTS.md`だけ
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`

Candidate12はC11のcounter applicability境界とworker context sufficiency境界を維持し、TaskSpecの1つのcriterion / ownerをauditまたはreviewの必要な片方へ割り当て、別々のcontract側とquality側criterionが固定された場合だけaudit後にreviewを実行する境界を追加した。required validation、drift、実装主体、worker contextの具体的な継承値は変更していない。

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 97.917 | 4,757,900 | 1,777.127 |
| 2 | 97.917 | 4,300,587 | 1,663.078 |
| 3 | 100.000 | 4,197,262 | 1,658.371 |
| 4 | 97.917 | 5,052,635 | 1,927.122 |
| 5 | 100.000 | 5,020,031 | 1,903.191 |
| median | 97.917 | 4,757,900 | 1,777.127 |

60 runのscore内訳はscore `4`が57件、score `3`が3件である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Quality observation

- F04 WEB AUDIT COLUMN VISIBILITY iteration 1は所定変更、Node 3 command、temporary output cleanup、許可外driftなしまで完了したが、quality側の単一ownerに対応するreviewを実行できず未完了停止した。
- F06 RESTORE EMPTY SNAPSHOT CONTRACT iteration 2は所定test、対象23件、tests全体326件pass・3件skip、許可外driftなしまで完了したが、明示された2 commandとrootのgeneric Python gateの競合からrequired machine gateを完了扱いにできず停止した。
- F06 iteration 4も同じmachine結果を得た後、独立auditが重複scopeを`contract_stop=1`として返し未完了停止した。
- 残る57 runは所定成果、required validation、許可範囲、terminal dispositionを満たした。
- 60 runで許可外path差分とexternal failureはなく、rootと全descendant SAの最終token usageを完全に取得した。

F04 iteration 1では、C12 root contractがquality ownerをreviewだけへ割り当てた一方、変更していない`prompts/review.md`がvalid audit停止0とaudit output identityをreviewの起動条件にしている。このためroute cardinality境界とrole promptが接続されず、必要なreviewを起動できなかった。

F06の2件はC12で新設したcardinality境界ではなく、C11から維持したgeneric Python completionとTaskSpec明示validationのauthority競合である。C12ではvalidation境界を変更しないnon-goalとしていたため、このN=5でも未解決のまま残った。

## Route cardinality observation

all-agent usageとroot rolloutのspawn記録では、60 run中41 runがworkerを1本起動し、19 runはworkerを起動しなかった。2本以上を起動したrunは0で、child worker総数は41だった。`fork_turns`は`none`が40、`all`がF10 inventoryのresponse check 1件だった。

| case | 5 runのworker数 | worker合計 | all-agent tokens中央値 | elapsed中央値 |
| --- | --- | ---: | ---: | ---: |
| F02 history date bound | `1, 1, 1, 1, 1` | 5 | 989,425 | 236.203秒 |
| F03 atomic cleanup | `1, 1, 1, 1, 1` | 5 | 507,135 | 188.865秒 |
| F04 web audit column | `0, 1, 1, 1, 1` | 4 | 515,761 | 279.585秒 |
| F06 empty snapshot | `1, 0, 1, 1, 1` | 4 | 655,066 | 216.986秒 |
| F07 runner | `1, 1, 1, 1, 1` | 5 | 596,824 | 204.778秒 |
| F07 dependency | `1, 1, 1, 1, 1` | 5 | 313,236 | 142.822秒 |
| F08 CLI sync | `1, 1, 1, 1, 1` | 5 | 381,371 | 174.610秒 |

C11ではchild worker総数59、workerありrun36、2 worker以上のrunが21件だった。C12ではworkerありrunが41へ増えても各run最大1 workerとなり、route cardinality自体はこのN=5で意図した一対一対応へ収束した。C12の`total_tokens`中央値はC11より968,860、`elapsed_seconds`中央値は524.305秒少ない。

ただし、F04の未完了停止が示すように、一対一routeを完了可能にするには対応するrole promptも単独起動を許す必要がある。worker数減少だけをqualityを維持したelapsed短縮と結論しない。

## Conclusion

Candidate12はC11直接派生として、non-machine criterion / ownerとrequired workerのcardinality境界だけを`AGENTS.md`へ追加した。固定expanded 12 caseのN=5では、全spawn runが最大1 workerへ収束し、tokensとelapsedはC11から減少した。

一方、3 runがscore `3`となり、quality中央値は97.917だった。C12の構築と固定N=5評価は完了したが、quality維持を確認した状態ではない。review単独routeと`prompts/review.md`の起動前提、およびTaskSpec明示validationとgeneric Python completionのauthority競合を未解決事項として保持する。

この結論は採用、release承認、THE-CAPTION本体へのruntime反映を意味しない。これらは未判断、未実施のままである。

## Result identity and storage

- runner wall time: `460.570`秒
- result ID: `7ed431c7fc1b436b8de73ae336645089`
- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/7ed431c7fc1b436b8de73ae336645089.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate12-route-cardinality-expanded12-global-m24-n5-20260716-v3-r1`

raw evidenceとregistry resultはrepositoryへcommitしない。
