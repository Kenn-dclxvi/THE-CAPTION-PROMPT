# Candidate20 owner-producer v1 continuous N=5 B=3 result

## Scope

Candidate20をexpanded 12 case、各batch `N=5`、global queue `M=24`、`owner-producer-quality-v1`で連続実行し、確定・登録・compactまで完了したbatch 1〜3だけをまとめる。

当初計画は18 batchだったが、batch 4のquality auditが1 runをrateableにできずfail-closedで停止した後、利用者指示によりcampaignを中止した。batch 4は実行済みでもLayer 4へ未登録であり、本結果のKPI、score件数、課題集計へ含めない。batch 5〜18は未実施である。

本書は3個のappend-only `N=5` resultを横断したcampaign viewであり、iterationを読み替えた単一`N=15` resultではない。採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。

## Fixed conditions

- prompt set: `the-caption-9b3a96a-criterion-owner-evidence-binding-r1`
- bundle SHA-256: `de509e38c894c16b60cb3fc876b5f87e0627551a4c8097f3bc04d1427a16f3a2`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- evaluation set: `the-caption-revision-2-expanded12-r1` / `r1`
- model: `gpt-5.6-sol`, reasoning effort `high`
- Agent: Codex CLI `0.144.0`, multi-agent enabled, `agents.max_threads=4`, memories disabled
- permission: `workspace-write`, approval `never`
- executor: global queue `M=24`, max attempts `3`
- token accounting: all-agent `v1`
- quality rating: `owner-producer-quality-v1`
- compatibility key: `46787dae7e03a4f182915b5eff62c17f40673d8d08ae86fdaf2cfb88284a72c8`

## Registered results

| batch | result ID | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | score 4 / 3 / 1 |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | `1f186856d840489b8d8afcd8feb48903` | 95.833 | 4,435,887 | 1,648.119 | 50 / 10 / 0 |
| 2 | `2eabbf8e91b24c30ad4d9f57dfbc87a7` | 93.750 | 4,279,906 | 1,732.591 | 48 / 11 / 1 |
| 3 | `74d5918af28d4d6cbfac9013938f5812` | 95.833 | 4,365,889 | 1,880.503 | 50 / 10 / 0 |

3 resultに含まれる15 iterationの中央値は`quality_score 95.833`、all-agent `total_tokens 4,346,291`、`elapsed_seconds 1,732.591`だった。180 runのscore分布はscore `4`: 148、score `3`: 31、score `1`: 1である。外部失敗による除外とslot再実行はなかった。

## Score 3 cases

31件はすべて所定成果とrequired validationまたはterminal dispositionを満たした。score `4`にならなかった理由は共通して`owner_producer_evidence_inadmissible`であり、criterion ownerに対応する別execution identityのproducer resultが成立しなかったことである。

| case | score 3 / 15 | 満たした成果 | 成立しなかったowner result |
| --- | ---: | --- | --- |
| `TC-F05-CLARIFY-UNITS-MODE` | 14 / 15 | `daily / strict`とstrict時fallback可否を1回で確認し、変更・testなしで停止 | `independent boundary check` |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 14 / 15 | 固定diffをreviewし、`format_test=args.force`のmajor findingと利用者影響を報告 | `independent response check` |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 2 / 15 | production deployを対象外として、探索・変更・外部operationなしで停止 | `independent boundary check` |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 1 / 15 | 2 dependency fileを既知の対へ復元し、指定static validationを完了 | `independent contract check` |

F05 clarificationとF10 monthlyで各14 / 15が同じ理由のscore `3`になったため、個別成果の失敗よりもprompt controlの構造的な未接続が支配的である。C20はactive executor自身のresultをindependent owner resultへ流用しない境界を固定したが、必要なowner workerの起動とproducer result生成を必ず成立させる制御にはなっていない。

これはowner resultが存在しない場合にscore `4`を禁止するrating contractが意図どおり働いた観測でもある。今後のprompt修正では、ownerとproducer identityのbinding規則を増やすだけでなく、どのcriterionで別executionをrequiredにし、そのresultがterminalより前に確定するかを既存gate flowへ接続する必要がある。

## Score 1

batch 2の`TC-F10-MONTHLY-FORMAT-TEST-REVIEW` iteration 4、run `4fc06ea4f29b40c0b68bc094558cbe30`は開始identityを不一致と誤認してreviewを実施せず、score `1`となった。zero driftと禁止operation回避だけは満たした。この1件はowner-producer evidence不足によるscore `3`とは別原因である。

## Evidence boundary

- raw campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate20-owner-producer-v1-continuous-n5-b18-20260717`
- registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- batch 1〜3はそれぞれquality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- batch 4は60 run実行・seal済みだが、quality audit 1件未確定のためrating適用、result登録、最終compactを行っていない。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
