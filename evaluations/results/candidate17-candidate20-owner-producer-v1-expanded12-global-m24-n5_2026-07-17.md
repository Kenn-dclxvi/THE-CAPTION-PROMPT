# Candidate17 / Candidate20 owner-producer quality v1 expanded 12-case N=5

## Scope

Candidate17と、その直接childで`AGENTS.md`だけを変更したCandidate20を、owner-producer証跡をscore `4`の必要条件にする新しいquality rating revisionで新規実行した。旧rating revisionのCandidate15 / 17 resultは変更せず、本resultとの互換比較へ混ぜない。

- evaluation set: `the-caption-revision-2-expanded12-r1` / identity `787521e5f0c0c261dcec0e3933d9f8b839481ed363fff6c5ae7672cdb699ef88`
- repetition / execution: `N=5` / `global_queue` / `M=24`
- model / Codex CLI / Python: `gpt-5.6-sol` / `0.144.0` / `3.14.5`
- rating contract: `owner-producer-quality-v1`
- contract SHA-256: `65021fa3ff60f0daed4e79ecec687a61ae46288d9bf0032582a19751c6da961d`
- compatibility key: `46787dae7e03a4f182915b5eff62c17f40673d8d08ae86fdaf2cfb88284a72c8`
- excluded attempt: Candidate17 `0`、Candidate20 `0`

両profileのEvaluation set、target ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、反復条件、quality rating revisionは同一で、prompt identityだけが異なる。

## KPI median

| prompt set | `quality_score` | all-agent `total_tokens` | `elapsed_seconds` | score 4 / 3 / 1 |
| --- | ---: | ---: | ---: | ---: |
| Candidate17 | 95.833 | 4,510,093 | 1,635.175 | 49 / 11 / 0 |
| Candidate20 | 95.833 | 4,404,154 | 1,613.670 | 49 / 10 / 1 |
| Candidate20 - Candidate17 | 0.000 | -105,939 | -21.506 | — |

KPI差は保存済みcomparison viewの数値差であり、winner、改善・悪化、採用判断へ変換しない。

## Iteration KPI

| iteration | C17 quality | C17 tokens | C17 elapsed | C20 quality | C20 tokens | C20 elapsed |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 95.833 | 4,320,164 | 1,557.661 | 95.833 | 5,038,026 | 1,683.665 |
| 2 | 93.750 | 5,595,092 | 1,825.868 | 95.833 | 4,224,133 | 1,613.670 |
| 3 | 95.833 | 4,426,804 | 1,608.902 | 93.750 | 4,056,329 | 1,492.350 |
| 4 | 95.833 | 5,337,220 | 1,635.175 | 95.833 | 4,606,826 | 1,769.104 |
| 5 | 95.833 | 4,510,093 | 1,643.968 | 91.667 | 4,404,154 | 1,566.070 |

## Owner-producer evidence

| prompt set | score 4 eligible | ineligible | ineligible case |
| --- | ---: | ---: | --- |
| Candidate17 | 49 / 60 | 11 | F05 clarify 5、F07 dependency provenance 1、F10 monthly review 5 |
| Candidate20 | 49 / 60 | 11 | F05 clarify 5、F05 out-of-scope 1、F10 monthly review 5 |

成果内容を満たし、owner-producer証跡だけが未成立だったrunはscore `3`とした。Candidate20のF10 monthly iteration 5は開始identityを誤認してsourceとdiffを読まず、reviewを実施しなかったためscore `1`とした。Candidate20の変更対象だったF10 monthlyは5 / 5でownerに対応するproducer resultがなく、4件がscore `3`、1件がscore `1`だった。このN=5では、criterion ownerとproducer execution identityをevidence成立条件へ接続する狙いの挙動は観測できなかった。

## Fail-closed correction before the valid run

最初のCandidate17 dispatchは、固定adapter snapshotの実体が外部tooling directoryから欠落していたため、全adapterがexit `2`で終了した。`evaluation_loop.py`が非zero exitとtoken usage欠落を誤って`valid` bindingへ保存する再現可能なfail-open不具合も同時に検出した。

このcycleは結果登録と採点に使用せず、名前へ`invalid-missing-tooling`を付けて隔離した。adapter 3ファイルをGit HEADとbyte-identicalな内容で同じ固定pathへ復元し、非zero exitまたはusage欠落をvalidとして保存しない回帰修正を追加した。60件のunit testを通した後、Candidate17 / 20の有効cycleを新規作成して全slotを再実行した。

## Result identity and storage

| artifact | Candidate17 | Candidate20 |
| --- | --- | --- |
| runner wall time | `453.398`秒 | `477.165`秒 |
| result ID | `39970c0dd70942d1940f9135873f4bdc` | `4801fe6ba99b469691fd82e9eca72382` |
| final archive SHA-256 | `c1a9689c597c056f3799577f41491e4236c3aefecf527edd9d994a5938a89673` | `a5dbbeb2cffce6cb2764c45ac6768edb24e3845a2b2dd96edba35d1e60362730` |

- registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate17-candidate20-owner-producer-v1-expanded12-n5-20260717.json`
- Candidate17 raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate17-operation-qualified-evidence-owner-producer-v1-expanded12-global-m24-n5-20260717-v3-r1`
- Candidate20 raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate20-criterion-owner-evidence-binding-owner-producer-v1-expanded12-global-m24-n5-20260717-v3-r1`
- invalid preflight evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate17-operation-qualified-evidence-owner-producer-v1-expanded12-global-m24-n5-20260717-v3-r1-invalid-missing-tooling`

採点は保存evidenceに基づくが、独立blind quality raterによるものではない。raw evidenceとregistry artifactはrepositoryへcommitしない。本結果は採用、release承認、THE-CAPTION本体へのruntime反映を意味しない。
