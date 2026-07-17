# Candidate28 single-producer operation binding N=5 incomplete rating result

## Scope

Candidate24を直接sourceとし、各operation identityへproducerを一つだけbindするCandidate28を、expanded 12 case、`N=5`、global queue `M=24`、`owner-producer-quality-v1`で実行した。

60 / 60 runのLayer 2 executionとowner-producer evidence生成までは完了した。一方、quality auditは55 runだけをrateableとし、5 runをrequired validationの成功証跡不足としてfail-closedにした。このため本試験から60 run全体の`quality_score`は確定せず、Layer 4 result登録、KPI comparison view、winner、採用、release判断は生成しない。

## Fixed conditions

- prompt set: `the-caption-3ce91a4-single-producer-operation-binding-r1`
- bundle SHA-256: `2eb1e8b04af3b0de3468cf1654b361a5e2ec901a5bc15eb82ad6ccb11cd32f1b`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- evaluation set: `the-caption-revision-2-expanded12-r1` / `r1`
- model: `gpt-5.6-sol`, reasoning effort `high`
- Agent: Codex CLI `0.144.0`, multi-agent enabled, `agents.max_threads=4`, memories disabled
- permission: `workspace-write`, approval `never`
- executor: global queue `M=24`, max attempts `3`
- token accounting: all-agent `v1`
- quality rating: `owner-producer-quality-v1`
- compatibility key: `9e7634c52c97ff5d882a8d693f3b4712e4d31245a2a2345a747b643d33aabfb1`

## Execution observation

| observation | value |
| --- | ---: |
| valid execution | 60 / 60 |
| owner-producer eligible | 60 / 60 |
| quality-audit rateable | 55 / 60 |
| rateable runのscore `4` | 55 / 55 |
| unrateable | 5 / 60 |
| all-agent `total_tokens` | 20,350,476 |
| controller execution interval | 395.981 seconds |

`total_tokens`とexecution intervalは完了したLayer 2の観測値である。5 runのratingが未確定のため、これらを登録済みprompt-set resultのKPIや他resultとの比較値として扱わない。

## Unrateable runs

| case | iteration | run ID | quality auditが不足とした証跡 |
| --- | ---: | --- | --- |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 1 | `80df3df904414630b5ead28de2ee3a40` | 指定Python validation、`git diff --check`、`git diff --name-only` |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 3 | `e7ef5e1a2ef146d09cb1423b763d541e` | 指定Python validation、`git diff --check`、`git diff --name-only` |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 4 | `02cfba2db0b542cb92a6c35f2c8bbed1` | 指定Python validation、`git diff --check`、`git diff --name-only` |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 5 | `d0940829b81040cca9dd811760cc4b28` | 指定Python validation、`git diff --check`、`git diff --name-only` |
| `TC-F07-CANONICAL-V4-RUNNER` | 2 | `b7f0e029ee194158af80397af2daa59d` | `bash -n run.sh`、`bash scripts/dev/main_verify.sh` |

5 runでは、single-producer bindingに従ってowner workerがrequired validationのproducerになった。保存済みchild rolloutを確認すると、dependency 4 runの各指定validationとcanonical runner 1 runの`bash -n run.sh`、`bash scripts/dev/main_verify.sh`、`git diff --check`は成功している。canonical runnerのtest結果は326 passed / 3 skippedだった。

しかし、固定済みquality auditは各runのroot `codex-events.jsonl`だけからsuccessful commandを検索し、descendant sessionのcommand eventを採点入力に含めない。そのため実行済みのvalidationを現rating contract上のadmissible evidenceとして扱えず、5 runを事後にscore `4`へ補完できない。

## Interpretation

本試験で確認できたのは、Candidate28が12 caseすべてでowner-producer evidenceを成立させたことと、rateableな55 runがscore `4`だったことまでである。60 / 60のscore `4`、既存CandidateとのKPI差、低頻度失敗の解消へ一般化しない。

問題はCandidate28のoperation bindingと、既存rating evidenceのsession範囲が一致していないことである。次に再試験する場合は、rootとdescendantのどのcommand evidenceをadmissibleにするかを事前に定義した新しいratingまたはaccounting revisionが必要になる。本runの採点条件は変更せず、履歴として保持する。

このevidence scope不足は後続の[`owner-producer-quality-v2 N=5 result`](candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5_2026-07-17.md)で別revisionとして更新した。v1の本runは未登録のまま変更しない。

## Evidence boundary

- raw run: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate28-single-producer-operation-binding-owner-producer-v1-expanded12-global-m24-n5-20260717-v3-r1`
- batch 1は60 run execution、owner-producer evidence生成、quality audit、seal、lossless archive、prune receiptまで完了した。
- quality auditは5 run未確定のためrating適用を拒否し、Layer 4 registryへ登録していない。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
