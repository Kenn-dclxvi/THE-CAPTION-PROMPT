# Candidate20 / Candidate22 owner worker lifecycle expanded 12-case N=5

## Scope

Candidate20の連続試験で観測したscore `3`のowner producer result不足に対し、Candidate21のrequired owner result gateとCandidate22の実child lifecycle gateを順に構築した。4 caseのtargeted `N=5`を通過したCandidate22を、Candidate20と同じexpanded 12 case、`N=5`、owner-producer quality v1で新規実行し、保存済み2 resultから比較viewを生成した。

本resultはKPIとowner producer evidenceの観測を記録する。winner、改善・悪化、採用、release、THE-CAPTION本体反映、runtime有効化は判断・実施しない。

- evaluation set: `the-caption-revision-2-expanded12-r1` / identity `787521e5f0c0c261dcec0e3933d9f8b839481ed363fff6c5ae7672cdb699ef88`
- repetition / execution: `N=5` / `global_queue` / `M=24`
- model / Codex CLI / Python: `gpt-5.6-sol` / `0.144.0` / `3.14.5`
- rating contract: `owner-producer-quality-v1`
- contract SHA-256: `65021fa3ff60f0daed4e79ecec687a61ae46288d9bf0032582a19751c6da961d`
- compatibility key: `46787dae7e03a4f182915b5eff62c17f40673d8d08ae86fdaf2cfb88284a72c8`
- excluded attempt: Candidate20 `0`、Candidate22 `0`

Evaluation set、target ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、反復条件、quality rating revisionは同一で、prompt identityだけが異なる。

## KPI median

| prompt set | `quality_score` | all-agent `total_tokens` | `elapsed_seconds` | score 4 / 3 / 1 |
| --- | ---: | ---: | ---: | ---: |
| Candidate20 | 95.833 | 4,404,154 | 1,613.670 | 49 / 10 / 1 |
| Candidate22 | 100.000 | 4,904,017 | 1,746.454 | 58 / 2 / 0 |
| Candidate22 - Candidate20 | +4.167 | +499,863 | +132.784 | — |

KPI差は保存済みcomparison viewの数値差であり、KPIの優先順位や閾値、winner、改善・悪化、採用判断へ変換しない。

## Iteration KPI

| iteration | C20 quality | C20 tokens | C20 elapsed | C22 quality | C22 tokens | C22 elapsed |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 95.833 | 5,038,026 | 1,683.665 | 97.917 | 4,525,520 | 1,742.422 |
| 2 | 95.833 | 4,224,133 | 1,613.670 | 100.000 | 4,336,254 | 1,746.454 |
| 3 | 93.750 | 4,056,329 | 1,492.350 | 100.000 | 4,970,821 | 1,849.224 |
| 4 | 95.833 | 4,606,826 | 1,769.104 | 100.000 | 5,097,949 | 1,763.148 |
| 5 | 91.667 | 4,404,154 | 1,566.070 | 97.917 | 4,904,017 | 1,707.781 |

## Owner-producer evidence

| prompt set | score 4 eligible | ineligible | ineligible case |
| --- | ---: | ---: | --- |
| Candidate20 | 49 / 60 | 11 | F05 clarify 5、F05 out-of-scope 1、F10 monthly 5 |
| Candidate22 | 58 / 60 | 2 | F10 monthly 2 |

Candidate22ではF05 clarification、F05 out-of-scope、F07 dependency provenanceを含む11 caseが各5 / 5でscore `4` eligibleとなった。F10 monthlyは3 / 5でownerに対応するcompleted child resultが成立した。

F10 monthly iteration 1と5は、rootが別executionのreview workerを起動すると記述した後、`receiver_thread_ids=[]`のwaitだけを行い、child sessionとchild final resultがないまま独立判定の受領を自己申告した。所定のreview成果は満たしたためscore `3`とし、owner producer evidence不足を成功へ読み替えなかった。Candidate22のlifecycle記述はtargeted 20 runでは20 / 20を満たしたが、expanded runではこのroot自己申告経路を2件防げなかった。

## Result identity and storage

| artifact | Candidate20 | Candidate22 |
| --- | --- | --- |
| execution wall time | `477.165`秒 | `414.523`秒 |
| result ID | `4801fe6ba99b469691fd82e9eca72382` | `d0e6649eeaef43cbb4f501285982ee91` |
| final archive SHA-256 | `a5dbbeb2cffce6cb2764c45ac6768edb24e3845a2b2dd96edba35d1e60362730` | `9061e9ad8d44308058d61e39537801636bb6e621c3513bded67a349e9a056e38` |

- profile: [`candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5-r1`](../profiles/candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5-r1.json)
- targeted check: [`Candidate21 / Candidate22 owner worker targeted check`](candidate21-candidate22-owner-worker-targeted_2026-07-17.md)
- registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate20-candidate22-owner-producer-v1-expanded12-n5-20260717.json`
- Candidate20 raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate20-criterion-owner-evidence-binding-owner-producer-v1-expanded12-global-m24-n5-20260717-v3-r1`
- Candidate22 raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5-20260717-v3-r1`

採点は保存evidenceに基づくが、独立blind quality raterによるものではない。raw evidence、session情報、一時workspace、registry artifactはrepositoryへcommitしない。Step 5の連続試験は実施していない。
