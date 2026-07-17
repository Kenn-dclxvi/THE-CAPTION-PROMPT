# Candidate28 owner-producer quality v2 expanded 12-case N=5 result

## Scope

Candidate28のpromptを変更せず、required validation commandの成功証跡をrootと、そのrunへbindされたrecursive descendant sessionから収集する`owner-producer-quality-v2`でexpanded 12 case、`N=5`、global queue `M=24`を新規実行した。

旧`owner-producer-quality-v1`の60 runは5 runをrateableにできなかったため変更せず履歴として保持する。本resultは別rating revision、別compatibility keyのappend-only resultであり、旧resultのscore補完ではない。

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
- quality rating: `owner-producer-quality-v2`
- rating contract SHA-256: `31950fcab89cbc86e1b0d028333463a785c47f58e85402d278f7e5942117cc40`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v1`
- compatibility key: `944736d424b65285de3528af5aeef1a9d0d9541737465505cb1b7513c7de66e0`

## Registered result

- result ID: `1fbf40ab264844b895efaeb78e273775`
- valid / rateable run: 60 / 60
- score `4 / 3`: 58 / 2
- excluded attempt: 0
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `4,153,414`
- `elapsed_seconds` median: `1,440.097`
- 60 run all-agent token total: `21,110,746`
- controller execution interval: `344.531` seconds

iteration別`quality_score`は`100.000 / 97.917 / 100.000 / 100.000 / 97.917`だった。

## Command evidence update

v2 collectorはall-agent usageのexact `root_thread_id`を起点に、parent relationで到達できるrecursive descendantだけを選ぶ。root commandはCodex event、descendant commandは同じthread identityへbindされたrollout tool outputから収集する。同一workspaceにある別root sessionやworker final responseだけではsuccessful commandとしない。

60 runすべてでcommand evidence artifactが成立し、quality auditのrequired command不足は0件だった。旧v1でunrateableとなったF07 dependency 4 runとF07 canonical runner 1 runに相当する証跡境界は、このrevisionで採点可能になった。

collector実装の事前qualification中に、output labelとcommand列の対応形式を扱えない2 campaignが60 run実行後にfail-closedとなった。両campaignはseal済み、Layer 4未登録のまま保持し、本resultへ混ぜていない。collectorは明示command identity、name、0 / 1-based index、successful result列とcommand列の順序bindingをtestし、既存180 runのrequired command再走査で不足0件を確認してから本campaignを実行した。

## Score 3

| case | iteration | run ID | 成果 | score `4`にならなかった理由 |
| --- | ---: | --- | --- | --- |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 5 | `493915052ac54862bc2dc8ebe5d87ca8` | 所定成果とrequired validationを完了 | `independent state check`に対応するproducer candidateが0件 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 2 | `cc1fbc51d8ea4c74972ef1ce27debfe1` | 所定成果とrequired validationを完了 | `independent contract check`に対応するproducer candidateが0件 |

2件はcommand evidence不足ではない。required validationは成功しているが、criterion ownerに対応する別execution identityのproducer resultが成立しなかったため、`owner-producer-quality-v2`のscore `4`必要条件を満たさずscore `3`となった。

## Interpretation

試験更新により、workerがvalidationを実行する正当なsingle-producer operationを「未実行」と誤判定する問題は解消した。そのうえで、Candidate28でも60 run中2件はindependent owner operation自体がproducer resultを生成していないことが分かった。

したがって本結果は、Candidate28が60 / 60でowner resultを保証したことを示さない。score `3`の残存境界はF10固有ではなく、F03とF07で独立owner operationが成立しなかったことである。winner、採用、release判断、THE-CAPTION本体反映へ一般化しない。

## Evidence boundary

- registered raw campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5-20260717-v3-r3`
- collector qualification failure 1: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5-20260717-v3-r1`
- collector qualification failure 2: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5-20260717-v3-r2`
- registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/1fbf40ab264844b895efaeb78e273775.json`
- 正式campaignはquality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
