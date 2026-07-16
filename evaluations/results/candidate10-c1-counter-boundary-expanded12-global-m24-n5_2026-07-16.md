# Candidate10 C1-derived counter boundary expanded 12-case global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- valid run window: `2026-07-16T16:01:39+09:00`から`2026-07-16T16:12:00+09:00`
- profile: `candidate10-c1-counter-boundary-expanded12-global-m24-n5-r1`
- set ID / Layer 1 identity: `the-caption-revision-2-expanded12-r1` / `787521e5f0c0c261dcec0e3933d9f8b839481ed363fff6c5ae7672cdb699ef88`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultは、Candidate1を直接sourceとするCandidate10を1つのimmutableな`prompt_set_identity`として保存した一次結果である。比較、winner、改善・悪化、採用判断はこのresultへ含めない。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-c1-counter-applicability-boundary-r1` / `r1`
- bundle SHA-256: `8309a7d83704849979c3c3972f5bf8c005b9ba377b2f8c866b2f8ab5ee576592`
- direct source identity: `the-caption-9b3a96a-revision-2-r1`
- changed target: `AGENTS.md`だけ
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 6,043,766 | 2,324.745 |
| 2 | 100.000 | 6,456,037 | 1,903.098 |
| 3 | 100.000 | 6,798,932 | 2,489.997 |
| 4 | 100.000 | 7,685,886 | 2,359.190 |
| 5 | 100.000 | 9,505,778 | 2,447.297 |
| median | 100.000 | 6,798,932 | 2,359.190 |

60 runのscore内訳はscore `4`が60件である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Case observation

- F03 / F06は各5 runともvalidation authorityの競合で停止せず、所定成果とrequired validationへ到達した。
- `machine_rework_max=not_applicable`と`environment_recovery_max=not_applicable`を含むF05 clarify、F05 out-of-scope、F08、F10 inventory、F10 monthly reviewの合計25 runは、counter値を要求する停止へ分岐しなかった。
- F08の5 runはweekly / monthly command同期を完了し、F10の10 runは指定されたread-only review結果を返した。
- F04の5 runはNode validation後のtest-owned temporary outputをcleanupした。
- 60 runで許可外path差分とexternal failureはなく、all-agent token usageを完全に取得した。

この観測は固定した12 case、各5反復に限定する。未観測のTaskSpec、counter sentinel、別のmodelまたはAgent環境へ一般化しない。

## Conclusion

Candidate10は、Candidate1を直接sourceとし、Candidate9のTaskSpec / default resolutionを取り込まず、machine reworkとenvironment recoveryのcounter domainを責務が適用対象の場合だけ評価する境界を`AGENTS.md`だけに追加した。bundle verifierとsource差分確認により、C1直接派生の1 target改訂として構築を完了した。

固定expanded 12 caseのN=5では60 / 60 runがscore `4`となった。C1で観測したF03 / F06のvalidation authority conflictによる未完了停止は再現せず、`not_applicable`を持つF08 / F10等もcounter domain停止に分岐しなかった。この観測範囲で、Candidate10のprompt構築とN=5評価は完了とする。

C10の`total_tokens`中央値はC1より1,066,452大きい。ただしsession内訳では、C1とC10で変更していないSA context継承の`fork_turns`選択とresponse-check起動回数が反復間で異なる。このため、このN=5のtoken差をcounter applicability境界の固有overheadとは結論しない。

上記はCandidate10の構築と固定評価の完了結論であり、採用、release承認、THE-CAPTION本体へのruntime反映を意味しない。これらは未判断、未実施のまま保持する。

## Result identity and storage

- runner wall time: `621.695`秒
- result ID: `f4eb6203148a4baa872a371298e2c2e3`
- compatibility key: `ede1a4825c938d5df341780593daa3a7bdcf5c6847e0cbdb29512184aba5d951`
- registry artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/f4eb6203148a4baa872a371298e2c2e3.json`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate10-c1-counter-boundary-expanded12-global-m24-n5-20260716-v3-r2`

正式run前のcycleではcopy-on-write複製によりfixtureのdirectory / symlink modeが`0755`から`0700`へ変わり、Layer 1 identityが既存expanded 12-case resultと一致しなかった。その一次result `ac2c9e6d7edb40be9dc0279c75862616`はappend-only履歴として保持するが、本N=5結果と既存resultの互換比較には使用しない。正式runはmodeを保持するcopyでfixtureを固定し、既存の12 fixture identityすべてとの一致を確認してから実行した。

raw evidenceとregistry resultはrepositoryへcommitしない。
