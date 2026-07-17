# Profiles

比較開始前にmodel、Agent、environment、実行policy、repetition、成功基準、停止条件を固定する。結果確認後の変更は新revisionとして扱う。

実行順は再現用provenanceとして保存するが、A / Bの実行環境を揃える補正には使わない。global queueでは処理時間短縮のために過去の所要時間が長いslotから投入し、空いたworkerへ次のslotを渡す。実測tokenと時間は環境補正せずKPIへ渡す。

v3の現行token仕様は[`token-accounting-all-agents-v1`](token-accounting-all-agents-v1.json)である。`total_tokens`はroot agentと全descendant SA sessionの最終usageを合算する。新しいRun capsuleはこのprofileの`accounting` objectを`comparison_conditions.executor_parameters.token_accounting`へ固定する。root-onlyで実行した既存profileは履歴として保持し、all-agentへの再集計をin-place変更として扱わない。

[`candidate17-operation-qualified-evidence-f10-boundary-v1-global-m5-n5-r1`](candidate17-operation-qualified-evidence-f10-boundary-v1-global-m5-n5-r1.json)はCandidate17のpromptを変更せず、実行adapterのtyped boundary evidenceを独立したcompatibility条件として検証するF10限定profileである。既存のraw shell outputをAgentが対応付けるresultとは互換比較しない。

[`candidate17-operation-qualified-evidence-expanded12-global-m24-n5-r1`](candidate17-operation-qualified-evidence-expanded12-global-m24-n5-r1.json)はCandidate17をexpanded 12 case、`1..5`、`M=24`、all-agent token accountingへ固定する。adapter、quality audit、Evaluation set、fixture、TaskSpec、permissionをCandidate15連続試験時点から変更せず、prompt identityだけをC17へ替える。

owner-producerをscore `4`の必要条件にする新rating revisionは、[`C17`](candidate17-operation-qualified-evidence-owner-producer-v1-expanded12-global-m24-n5-r1.json)、[`C20`](candidate20-criterion-owner-evidence-binding-owner-producer-v1-expanded12-global-m24-n5-r1.json)、[`C22`](candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5-r1.json)の別profileへ固定する。3 profileはprompt identity以外の条件と`quality_rating=owner-producer-quality-v1`を同一にする。旧rating revisionのC15 / C17 resultは変更せず、新profileとの互換比較へ混ぜない。C22の[`expanded result`](../results/candidate20-candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)はC20との保存済みcomparison viewへ3 KPIの数値差だけを出力する。

最新のv3 profileは[`baseline N=5`](baseline-expanded12-global-m24-n5-r1.json)、[`candidate1 N=5`](candidate1-expanded12-global-m24-n5-r1.json)、[`candidate2 N=5`](candidate2-expanded12-global-m24-n5-r1.json)、[`candidate3 N=5`](candidate3-expanded12-global-m24-n5-r1.json)、[`candidate4 N=5`](candidate4-expanded12-global-m24-n5-r1.json)、[`candidate5 N=5`](candidate5-expanded12-global-m24-n5-r1.json)、[`candidate6 N=5`](candidate6-expanded12-global-m24-n5-r1.json)である。各prompt setをexpanded 12 case、`1..5`、`M=24`の同一互換条件へ固定し、単独resultとして登録した。既存`N=1` profileとresultは変更していない。

Candidate9のN=5は、[`F03 / F06先行stage`](candidate9-f03-f06-global-m24-n5-r1.json)と[`remaining 10 case stage`](candidate9-remaining10-global-m24-n5-r1.json)を同じprompt identity、固定環境、`1..5`、`M=24`で実行し、[`expanded 12-case campaign result`](../results/candidate9-expanded12-global-m24-n5_2026-07-16.md)へまとめた。各stageのEvaluation set identityと一次resultは分離したまま保持する。

Candidate10のN=5は[`candidate10-c1-counter-boundary-expanded12-global-m24-n5-r1.json`](candidate10-c1-counter-boundary-expanded12-global-m24-n5-r1.json)でCandidate1直接派生のidentity、expanded 12 case、`1..5`、`M=24`、all-agent token accountingを固定した。[`result`](../results/candidate10-c1-counter-boundary-expanded12-global-m24-n5_2026-07-16.md)は既存のexpanded 12-case all-agent resultと同じcompatibility keyへ登録した。

Candidate11のN=5は[`candidate11-sa-context-boundary-expanded12-global-m24-n5-r1.json`](candidate11-sa-context-boundary-expanded12-global-m24-n5-r1.json)でC10直接派生のidentity、expanded 12 case、`1..5`、`M=24`、all-agent token accountingを固定した。[`result`](../results/candidate11-sa-context-boundary-expanded12-global-m24-n5_2026-07-16.md)は既存のexpanded 12-case all-agent resultと同じcompatibility keyへ登録した。

Candidate12のN=5は[`candidate12-route-cardinality-expanded12-global-m24-n5-r1.json`](candidate12-route-cardinality-expanded12-global-m24-n5-r1.json)でC11直接派生のidentity、expanded 12 case、`1..5`、`M=24`、all-agent token accountingを固定した。[`result`](../results/candidate12-route-cardinality-expanded12-global-m24-n5_2026-07-16.md)は既存のexpanded 12-case all-agent resultと同じcompatibility keyへ登録した。

Candidate14のN=5は[`candidate14-validation-authority-expanded12-global-m24-n5-r1.json`](candidate14-validation-authority-expanded12-global-m24-n5-r1.json)でC13直接派生のidentity、expanded 12 case、`1..5`、`M=24`、all-agent token accountingを固定した。C13のF03 / F04とC14のF06は[`targeted check`](../results/candidate13-candidate14-targeted-checks_2026-07-16.md)としてN=5 resultへ混ぜず、C14の[`expanded result`](../results/candidate14-validation-authority-expanded12-global-m24-n5_2026-07-16.md)だけを既存resultと同じcompatibility keyへ登録した。

Candidate15のN=5は[`candidate15-selected-role-control-input-expanded12-global-m24-n5-r1.json`](candidate15-selected-role-control-input-expanded12-global-m24-n5-r1.json)でC14直接派生のidentity、expanded 12 case、`1..5`、`M=24`、all-agent token accountingを固定した。[`result`](../results/candidate15-selected-role-control-input-expanded12-global-m24-n5_2026-07-16.md)は既存のexpanded 12-case all-agent resultと同じcompatibility keyへ登録した。

曖昧性・競合境界の独立setは、[`control-free repository N=3`](control-free-repository-ambiguity-boundaries-global-m10-n3-r1.json)と[`C15 N=3`](candidate15-ambiguity-boundaries-global-m10-n3-r1.json)へ分けた。両profileは[`the-caption-ambiguity-boundaries-r1`](../sets/the-caption-ambiguity-boundaries-r1/README.md)の5 case、`1..3`、`M=10`、all-agent token accountingを固定し、prompt identity以外の比較条件を同一にする。各15 runをappend-only resultへ登録し、[`comparison`](../results/control-free-repository-candidate15-ambiguity-boundaries-global-m10-n3_2026-07-17.md)へ3 KPIとcase別境界観測を記録した。採用判断は未実施である。

制御プロンプトなしの2条件は、[`repository固有指示なし`](control-free-generic-expanded12-global-m24-n5-r1.json)と[`repository固有指示あり`](control-free-repository-expanded12-global-m24-n5-r1.json)へ分け、expanded 12 case、`1..5`、`M=24`、all-agent token accountingを固定した。両[`result`](../results/control-free-generic-repository-expanded12-global-m24-n5_2026-07-16.md)は既存のexpanded 12-case all-agent resultと同じcompatibility keyへ独立登録した。

[`candidate23-control-free-operation-boundary-expanded12-global-m24-n5-r1`](candidate23-control-free-operation-boundary-expanded12-global-m24-n5-r1.json)はControlFreeRepositoryを直接sourceとするCandidate23をexpanded 12 case、`1..5`、`M=24`、all-agent token accountingへ固定する。ControlFreeRepositoryの既存resultからprompt identityだけを替え、Evaluation set、fixture、TaskSpec、permission、executor parameter、旧rating条件を維持する。

[`candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5-r1`](candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5-r1.json)はCandidate23を直接sourceとするCandidate24をexpanded 12 case、`1..5`、`M=24`、`owner-producer-quality-v1`へ固定する。Candidate22の保存済みowner-producer resultと同じcompatibility条件を維持し、prompt identityだけを替える。

[`candidate28-single-producer-operation-binding-owner-producer-v1-expanded12-global-m24-n5-r1`](candidate28-single-producer-operation-binding-owner-producer-v1-expanded12-global-m24-n5-r1.json)はCandidate24を直接sourceとするCandidate28をexpanded 12 case、`1..5`、`M=24`、`owner-producer-quality-v1`へ固定する。Candidate24 profileからprompt identityだけを替え、Evaluation set、fixture、TaskSpec、permission、executor parameter、rating条件を維持した。[N=5 result](../results/candidate28-single-producer-operation-binding-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)は60 runを完了したが、descendant sessionで実行したvalidationを固定済みquality auditが採点入力に含めない5 runがrateableにならず、Layer 4へ登録していない。

[`candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5-r1`](candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5-r1.json)は、上記v1試験で再現したevidence scope不足を別rating revisionとして修正する。prompt、Evaluation set、fixture、TaskSpec、permission、executor parameter、反復条件は維持し、`quality_rating`だけを`owner-producer-quality-v2`へ替える。v2は同一runのrootから到達できるdescendant command evidenceを採点可能にし、v1 resultを変更しない。[N=5 result](../results/candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5_2026-07-17.md)は60 / 60をrateableとしてLayer 4へ登録し、score `4 / 3 = 58 / 2`だった。

[`candidate29-owner-role-identity-binding-owner-producer-v2-targeted5-global-m24-n5-r1`](candidate29-owner-role-identity-binding-owner-producer-v2-targeted5-global-m24-n5-r1.json)は、Candidate29のowner語列保持をF03、F04、F05 clarification、F07 dependency、F10 inventoryの5 case、`1..5`、`M=24`、`owner-producer-quality-v2`へ固定する。25 runはscore `4`かつowner-producer eligibleとして別Evaluation set resultへ登録した。

[`candidate29-owner-role-identity-binding-owner-producer-v2-expanded12-global-m24-n5-r1`](candidate29-owner-role-identity-binding-owner-producer-v2-expanded12-global-m24-n5-r1.json)は、Candidate29をexpanded 12 case、`1..5`、`M=24`、`owner-producer-quality-v2`へ固定する。60 runは実行したが、owner-producer eligibleが59 / 60、rateableが55 / 60だったためLayer 4へ登録していない。[staged result](../results/candidate29-owner-role-identity-binding-staged_2026-07-17.md)の停止条件に従い、continuous試験へ進めていない。

[`candidate30-runtime-owner-result-binding-owner-producer-v2-targeted5-global-m24-n5-r1`](candidate30-runtime-owner-result-binding-owner-producer-v2-targeted5-global-m24-n5-r1.json)は、Candidate29 targeted profileからprompt identityだけをCandidate30へ替える。25 / 25 runがscore `4`かつowner-producer eligibleとなり、Layer 4へ登録した。

[`candidate30-runtime-owner-result-binding-owner-producer-v3-expanded12-global-m24-n5-r1`](candidate30-runtime-owner-result-binding-owner-producer-v3-expanded12-global-m24-n5-r1.json)は、Candidate30をexpanded 12 case、`1..5`、`M=24`へ固定する。F10 monthlyは開始条件を修正した`r3`、quality ratingはvalid runを未採点にしない`owner-producer-quality-v3`を使う。expanded 60 runと同条件continuous 300 runはすべてrateableかつowner-producer eligibleとして登録した。[result](../results/candidate30-runtime-owner-result-binding-owner-producer-v3-continuous-n5-b5_2026-07-17.md)はprompt変更、case revision、rating revisionを別artifactとして明示する。

[`candidate31-operation-terminal-closure-owner-producer-v4-targeted3-global-m15-n5-r1`](candidate31-operation-terminal-closure-owner-producer-v4-targeted3-global-m15-n5-r1.json)は、C30 continuous試験でscore `3`が残ったF06とF07の3 caseだけを`1..5`、`M=15`、`owner-producer-quality-v4`へ固定する。C31はC30のoperation bindingへ全predicateのterminal closureだけを追加する。case revision、fixture、TaskSpec、permissionは変更しない。rating v4はstructured command arrayと完了済みcontinuationを収集するcommand evidence v2を使い、既存v3 resultを変更しない。[targeted result](../results/candidate31-operation-terminal-closure-owner-producer-v4-targeted3-global-m15-n5_2026-07-17.md)は15 / 15 runをscore `4`としてLayer 4へ登録した。

[`candidate31-operation-terminal-closure-owner-producer-v4-expanded12-global-m24-n5-r1`](candidate31-operation-terminal-closure-owner-producer-v4-expanded12-global-m24-n5-r1.json)は、C31をexpanded 12 case、`1..5`、`M=24`、`owner-producer-quality-v4`へ固定する。[expanded result](../results/candidate31-operation-terminal-closure-owner-producer-v4-expanded12-global-m24-n5_2026-07-18.md)は60 / 60 valid runをLayer 4へ登録し、score `4 / 3 = 59 / 1`だった。score `3`はcustom `exec` wrapperの集約結果をcommand evidence v2が各required commandへ対応付けられなかった評価証跡不足として記録した。

[`candidate31-operation-terminal-closure-owner-producer-v5-expanded12-global-m24-n5-r1`](candidate31-operation-terminal-closure-owner-producer-v5-expanded12-global-m24-n5-r1.json)は、上記の再現済みcollector不具合を修正したcommand evidence v3と`owner-producer-quality-v5`へ固定する。prompt、Evaluation set、fixture、TaskSpec、permission、executor parameter、反復条件は維持した。[rating v5 result](../results/candidate31-operation-terminal-closure-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)は別campaignの60 / 60 valid runをLayer 4へ登録し、score `4 / 3 = 60 / 0`、quality audit failure count `0`だった。旧v4 resultは変更せず、互換比較へ混ぜない。

最初のv3 standalone profileは[`candidate2-expanded12-global-m24-n1-r1.json`](candidate2-expanded12-global-m24-n1-r1.json)である。candidate2の12 caseを`N=1`、`M=24`で実行し、[`result`](../results/candidate2-expanded12-global-m24-n1_2026-07-15.md)へ単一prompt setの3 KPIを記録した。

比較用baselineも固定A / B profileへ戻さず、[`baseline-expanded12-global-m24-n1-r1.json`](baseline-expanded12-global-m24-n1-r1.json)として単独実行した。candidate2 profileとの互換条件key一致を確認し、保存済み2 resultから比較viewを生成した。

candidate1も[`candidate1-expanded12-global-m24-n1-r1.json`](candidate1-expanded12-global-m24-n1-r1.json)として単独実行し、同じcompatibility keyを持つ3つの保存resultから比較viewを生成した。

最新の完了済みv2 profileは[`revision-2-expanded12-global-m24-n1-r1.json`](revision-2-expanded12-global-m24-n1-r1.json)である。12 case、A / B各1回、合計24 slotを`M=24`で実行し、[`result`](../results/revision-2-expanded12-global-m24-n1_2026-07-15.md)へ3 KPIと`B - A`差分を記録した。

直前の[`revision-2-core9-global-m4-r2.json`](revision-2-core9-global-m4-r2.json)はv1のwinnerによりN=1 screenからN=3 confirmationへ進む履歴profileであり、新しいv2 cycleへ再利用しない。

v2の新しい比較は、winnerやKPI優先順位を持たない新revisionを作り、実行前に`N`を固定する。v3ではA / B pairをprofile identityにせず、1 prompt set単位でprofileを固定する。

expanded profileにF09 r1とF10 review r1はexecution blockerのため含めない。
