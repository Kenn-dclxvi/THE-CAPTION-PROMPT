# Candidate29 owner role identity binding staged result

## 結論

Candidate29は、C28のF03とF07で起きたowner名の不一致を解消した。

対象5 caseの`N=5`では、25 / 25 runがscore `4`となった。

expanded 12 caseの`N=5`では、F03とF07 dependencyのowner証跡は各5 / 5で成立した。

ただし、expanded全体は59 / 60 runだけがowner証跡の必要条件を満たした。

さらに5 runは現行rating contractでrateableにならなかった。

したがって、expanded resultはLayer 4へ登録していない。

事前に固定した停止条件に従い、continuous `N=5 B=5`は開始していない。

## 変更した境界

Candidate29はCandidate28の直接childである。

変更対象はroot `AGENTS.md`だけである。

`criterion owner`は、TaskSpecの評価criterionを独立して判定する担当名を意味する。

Candidate29は、この担当名の語列をoperationとproducer role identityへ保持する。

区切り文字の正規化は許可する。

短縮と言換えは許可しない。

case名、route名、artifact種別ごとの例外は追加していない。

## 固定条件

- prompt set: `the-caption-3ce91a4-owner-role-identity-binding-r1`
- bundle SHA-256: `e357442e838354ce6238b3704f2d018162db066fd01a1a118bdfa47a04a5d8c1`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`, reasoning effort `high`
- Agent: Codex CLI `0.144.0`, multi-agent enabled, `agents.max_threads=4`, memories disabled
- permission: `workspace-write`, approval `never`
- executor: global queue `M=24`, max attempts `3`
- token accounting: all-agent `v1`
- quality rating: `owner-producer-quality-v2`
- rating contract SHA-256: `31950fcab89cbc86e1b0d028333463a785c47f58e85402d278f7e5942117cc40`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v1`

## 対象試験

対象試験はowner型5 caseを各5回実行した。

対象はF03 state、F04 source、F05 clarification boundary、F07 dependency contract、F10 inventory responseである。

- valid / rateable run: 25 / 25
- score `4`: 25
- owner-producer eligible: 25 / 25
- excluded attempt: 0
- result ID: `2637417dd45a4d79b17a4cf7cf2bbb6f`
- compatibility key: `78e382fc18e33714cdd60a8b0f0648105fc2ea87c3734286f854dce66152a912`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `1,524,459`
- `elapsed_seconds` median: `727.093`
- 25 run all-agent token total: `7,821,233`
- controller execution interval: `299.930` seconds

producer execution identityはcaseごとに次の語列となった。

| case | owner / producer execution identity | 成立数 |
| --- | --- | ---: |
| F03 | `independent state check` / `/root/independent_state_check` | 5 / 5 |
| F04 | `independent source check` / `/root/independent_source_check` | 5 / 5 |
| F05 clarification | `independent boundary check` / `/root/independent_boundary_check` | 5 / 5 |
| F07 dependency | `independent contract check` / `/root/independent_contract_check` | 5 / 5 |
| F10 inventory | `independent response check` / `/root/independent_response_check` | 5 / 5 |

## Expanded試験

expanded試験は`the-caption-revision-2-expanded12-r1`の12 caseを各5回実行した。

60 / 60 runのLayer 2実行はvalidだった。

owner-producer evidenceは59 / 60 runでeligibleだった。

F03は5 / 5で`/root/independent_state_check`へ一致した。

F07 dependencyは5 / 5で`/root/independent_contract_check`へ一致した。

この観測により、C28のF03とF07で発生したowner語の欠落は本試験では再現しなかった。

一方で、quality auditは60 run中55 runだけをrateableとした。

内訳はscore `4`が54 run、score `1`が1 run、unrateableが5 runである。

### Owner証跡が成立しなかったrun

`TC-F10-MONTHLY-FORMAT-TEST-REVIEW` iteration 4では、rootだけが実行された。

rootは`HEAD^`が固定seed commitと一致しないためreviewを開始しなかった。

このrunではproducer workerが起動されず、owner-producer evidenceが成立しなかった。

評価caseのTaskSpecは、現在のHEADを固定seed commitとしてreviewする一方で、`HEAD^`が同じ固定seed commitであることも開始条件にしている。

実行workspaceではHEADが固定seed commitであり、HEAD^はその親commitだった。

このため、開始条件の記述とfixtureの状態は一致していない。

### Rateableにならなかったrun

| case | iteration | 観測した不足 |
| --- | ---: | --- |
| F05 clarification | 3 | child resultは保存されたが、rootがruntime spawn / waitの受領フィールド不足を理由にclarificationを返さなかった |
| F04 | 1 | child resultは保存されたが、rootが受領フィールド不足を理由にNode validationを実行しなかった |
| F03 | 4 | final responseはfull gate成功を主張したが、descendantを含むcommand evidenceにfull gateがなかった |
| F07 dependency | 5 | 指定Python static validationのsuccessful command evidenceがなかった |
| F07 dependency | 1 | 指定した3つのstatic validationすべてにsuccessful command evidenceがなかった |

## 判断

事実として、owner語列をproducer role identityへ保持する変更はF03とF07の判定不一致を解消した。

事実として、C29はexpanded全体のowner resultとrequired commandを保証していない。

判断として、C29をcontinuous試験、採用、release判断へ進める根拠は不足している。

判断として、次の修正対象はowner名ではない。

次の修正対象は、実行環境が実際に返すspawn結果とwait結果だけでowner result gateを構成することである。

例として、現行gateが要求する`runtime_spawn_result.child_execution_identity`と`runtime_spawn_result.producer_role_identity`は、実際のspawn結果に同名フィールドとして存在しない。

rootは存在しない受領フィールドを待つのではなく、起動時に固定したtask identityと、完了通知に結び付いたchild final resultを使う必要がある。

F10 monthlyの開始identity条件は、prompt変更と混ぜず、新しいEvaluation set revisionで修正する必要がある。

不足commandをscoreへ写像する場合も、結果確認後の変更になるため、新しいrating revisionが必要である。

## Evidence boundary

- targeted registered campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate29-owner-role-identity-binding-owner-producer-v2-targeted5-global-m24-n5-20260717-v3-r1`
- targeted registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/2637417dd45a4d79b17a4cf7cf2bbb6f.json`
- expanded incomplete campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate29-owner-role-identity-binding-owner-producer-v2-expanded12-global-m24-n5-20260717-v3-r1`
- expanded incomplete summary: `batch-001/incomplete-rating-summary.json`
- targeted resultだけがquality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- expanded resultはseal済みだが、quality auditのrateable条件を満たさずLayer 4未登録である。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
