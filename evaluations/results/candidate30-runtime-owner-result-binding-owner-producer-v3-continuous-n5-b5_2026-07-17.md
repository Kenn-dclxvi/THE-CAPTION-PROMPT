# Candidate30 runtime owner result binding continuous result

## 結論

Candidate30は、子Agentの結果をOwner結果として受け取る境界を、実際のruntime証跡だけで成立させた。

対象5 caseのtargeted `N=5`では、25 / 25 runがscore `4`となった。

expanded 12 caseの`N=5`では、60 / 60 runがrateableだった。

expandedのscoreは`4 / 3 = 59 / 1`だった。

continuous `N=5 B=5`では、300 / 300 runがrateableだった。

continuousのscoreは`4 / 3 = 293 / 7`だった。

targeted、expanded、continuousを通じて、Owner証跡の不成立は0件だった。

したがって、C29で残ったOwner結果受領の問題は、この観測範囲では解消した。

残ったscore `3`は、Owner結果の問題ではない。

残ったscore `3`は、required commandの成功証跡不足である。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 問題だった挙動

C29は、runtimeが返さないfieldをOwner結果の受領条件にしていた。

具体例は`runtime_spawn_result.child_execution_identity`である。

実際のspawn結果が返すidentityは`task_name`である。

実際の子Agent結果は`FINAL_ANSWER.Sender`へ送信元identityを持つ。

wait結果は完了同期を示すが、送信元identityを持たない。

この不一致により、子Agentが正しい結果を返しても、rootが結果未受領として停止する挙動が問題だった。

## 変更した境界

Candidate30はCandidate29の直接childである。

変更対象はroot `AGENTS.md`だけである。

Owner結果の受領条件は、次の既存境界へ限定した。

1. spawn前に、criterion ownerの語列からtask identityを固定する。
2. spawn結果の`task_name`が固定したtask identityと一致することを確認する。
3. 受信した`FINAL_ANSWER.Sender`が同じtask identityと一致することを確認する。
4. final resultが対象criterion、Owner、artifactまたは提案responseへ結び付くことを確認する。

waitは完了を待つためだけに使う。

waitをidentity証跡として使わない。

case名、route名、artifact種別ごとの例外は追加していない。

## 評価条件の別revision

prompt変更と評価条件変更は別artifactにした。

F10 monthlyは、新しいcase revision `r3`を使った。

`r3`は、固定seed commitの存在を開始条件にする。

現在のHEADまたはHEAD^との親子関係は開始条件にしない。

review対象は引き続き固定seed commitの1 diffである。

quality ratingは、新しい`owner-producer-quality-v3`を使った。

v3は、有効runへ必ず0から4のscoreを付ける。

commandまたはOwner証跡が不足したrunも未採点にしない。

不足した証跡と成果全体から、0から3を付ける。

## 固定条件

- prompt set: `the-caption-3ce91a4-runtime-owner-result-binding-r1`
- bundle SHA-256: `61bd28c01477fb22b06f6bbbb7b975ba03ec6bb5862f50105882721725ee04a9`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`, reasoning effort `high`
- Agent: Codex CLI `0.144.0`, multi-agent enabled, `agents.max_threads=4`, memories disabled
- permission: `workspace-write`, approval `never`
- executor: global queue `M=24`, max attempts `3`
- token accounting: all-agent `v1`
- targeted quality rating: `owner-producer-quality-v2`
- expanded / continuous quality rating: `owner-producer-quality-v3`
- rating v3 SHA-256: `7d7a41191fca233eaba7400569e942a8e0c76a5cf773e238da0a1874fc518d5e`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v1`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`

## Targeted試験

targeted試験は、C29のtargeted試験からprompt identityだけを変更した。

対象はF03、F04、F05 clarification、F07 dependency、F10 inventoryである。

- valid / rateable run: 25 / 25
- score `4`: 25
- Owner証跡 eligible: 25 / 25
- all-agent token total: `7,536,514`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `1,477,998`
- `elapsed_seconds` median: `635.240`
- result ID: `01859524fa134db4b59b11589db9a622`
- compatibility key: `78e382fc18e33714cdd60a8b0f0648105fc2ea87c3734286f854dce66152a912`

## Expanded試験

expanded試験は12 caseを各5回実行した。

F10 monthlyだけを`r3`へ替えた。

quality ratingをv3へ替えた。

- valid / rateable run: 60 / 60
- score `4 / 3`: 59 / 1
- Owner証跡 eligible: 60 / 60
- all-agent token total: `18,543,919`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `3,632,957`
- `elapsed_seconds` median: `1,452.015`
- result ID: `66a4c8440e794f42bfecb822fde63815`
- compatibility key: `a72ab0793eb8dbd2407feb45a6569df55f51cd0b32ae1380fd11d542f87417b3`

score `3`は、F07 dependencyの1 runだった。

成果とOwner結果は確認できた。

指定した3つのstatic validation commandの成功証跡が不足した。

F10 monthlyは5 / 5がscore `4`だった。

## Continuous試験

continuous試験は、expandedと同じ12 case、rating、実行条件を5 batch繰り返した。

- valid / rateable run: 300 / 300
- score `4 / 3`: 293 / 7
- Owner証跡 eligible: 300 / 300
- all-agent token total: `92,371,993`
- 25 iteration valueの`quality_score` median: `100.000`
- 25 iteration valueのall-agent `total_tokens` median: `3,654,114`
- 25 iteration valueの`elapsed_seconds` median: `1,505.668`
- controller execution interval合計: `1,773.592`秒
- compatibility key: `a72ab0793eb8dbd2407feb45a6569df55f51cd0b32ae1380fd11d542f87417b3`

登録したresult IDは次の5件である。

1. `b3c3ee12bcc24f878575f5bbe5d8ce5e`
2. `c6f8a654f62b4963b6ee2def6c58828b`
3. `4edaf0e4964c4dd6af7561df0d5d9309`
4. `d43e7dfb0a5d464099f7df3c22ebf122`
5. `14c4de006f0d4bdc9d15a7b7295cb452`

batch 1では、2 attemptが`codex_model_at_capacity`で除外された。

同じslotを再実行し、2件とも有効runとして回収した。

除外attemptは300 valid runのscoreへ含めていない。

## Case別結果

| case | score 4 | score 3 | Owner証跡不成立 |
| --- | ---: | ---: | ---: |
| F03 atomic cleanup | 25 | 0 | 0 |
| F06 empty snapshot | 24 | 1 | 0 |
| F07 canonical runner | 22 | 3 | 0 |
| F07 dependency provenance | 22 | 3 | 0 |
| F10 inventory | 25 | 0 | 0 |
| F10 monthly review | 25 | 0 | 0 |
| その他6 case | 150 | 0 | 0 |

F06のscore `3` 1件は、required pytestの成功証跡不足だった。

F07 canonical runnerのscore `3` 3件は、`bash -n run.sh`またはfull gateの成功証跡不足だった。

F07 dependency provenanceのscore `3` 3件は、指定static validationの成功証跡不足だった。

7件すべてで主要成果とOwner結果は確認できた。

## 判断

事実として、spawn `task_name`と`FINAL_ANSWER.Sender`を使うC30のOwner結果境界は、targeted 25件、expanded 60件、continuous 300件で不成立0件だった。

事実として、F03はcontinuous 25 / 25がscore `4`だった。

事実として、F10の2 caseはcontinuous 50 / 50がscore `4`だった。

事実として、F07のscore `3` 6件はOwner結果不足ではなくrequired command証跡不足だった。

判断として、C30が対象としたOwner結果受領の問題は、予定した試験段階を完了した。

判断として、required command証跡の低頻度不足は別問題として残る。

提案として、この別問題を扱う場合はC30を変更せず、command実行と成功証跡保存の既存境界を対象にする。

提案として、case固有のcommand名による例外は追加しない。

## Evidence boundary

- targeted campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate30-runtime-owner-result-binding-owner-producer-v2-targeted5-global-m24-n5-20260717-v3-r1`
- expanded campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate30-runtime-owner-result-binding-owner-producer-v3-expanded12-global-m24-n5-20260717-v3-r1`
- continuous campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate30-runtime-owner-result-binding-owner-producer-v3-continuous-n5-b5-20260717`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/`
- 各resultはquality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
