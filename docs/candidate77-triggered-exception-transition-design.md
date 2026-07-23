# Candidate77 triggered exception transition設計記録

## 結論

Candidate77はCandidate71を直接sourceとする。Candidate71の11 labelと最短正常経路を変更せず、型付き状態仕様は例外triggerが成立したoperationだけへ適用する。

R-01からR-14の定義本文は`docs/prompt-guide.md`へ置く。root `AGENTS.md`はtriggerと参照先だけを持ち、triggerがないtaskでは例外仕様を読まず、identity revision、result validity key、DAG、method budget、recovery budgetを追加でmaterializeしない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-closure-r1`（Candidate71）とする。最短正常経路は、TaskSpecとrepository authorityからoutcomeを固定し、一つのproducerで変更し、完全なrequired validation集合を同一waveで実行し、成功後の追加readなしでterminalへ閉じる経路である。
2. 保存済み誤経路はCandidate76の`TC-F10-MONTHLY-FORMAT-TEST-REVIEW`である。C71とC76はともにcommand中央値11、model response中央値4だったが、token中央値は`85,272 -> 294,159`（`+245.0%`）だった。C76のroot promptはC71の`4,987 byte`から`21,509 byte`へ増え、同じ正常経路へ例外状態定義のinput costだけを加えた。
3. TaskSpec、repository authority、repository stateはtaskの実行内容を制限できるが、runtimeがroot promptとして常時注入する制御文をtaskごとに除外できない。適用範囲はroot prompt側で閉じる必要がある。
4. 置換する一つのpredicateは`exception_transition_required := authority conflictまたはtyped field未固定 ∨ producer / execution contract / predicate contract / target version変更 ∨ stale result候補 ∨ invocation異常またはpermission禁止 ∨ independent producer / delegated result provenance ∨ validation dependency / shared-state / final-state observer / cycle / unexpected dependency ∨ methodまたはrecovery継続`である。
5. このpredicateは、triggerがないoperationでR-01からR-14の全状態を展開し、各model再入へ同じ定義を持ち回るcontext伝播を消す。該当triggerがある場合も`docs/prompt-guide.md`の対応節だけを一度読み、無関係な節を読まない。
6. 増える判断点は、operationごとの一回のtrigger分類と、triggerから六つの例外仕様節への対応だけである。通常経路へ新しいowner探索、identity照合、validation、worker、model stepを追加しない。
7. 非trigger品質はF10 Entry / Monthly reviewでscore `4 = 10 / 10`、開始・終了zero drift、C71と同じread-only routeを要求する。trigger品質はA02とF06でscore `4 = 10 / 10`、required validation完全性、独立validation同一wave、final-state observer後続waveを要求する。第8節A〜Qは構造testで対応を確認する。
8. 非triggerではC71と同じcommand / model-step分布と、C76より低いinput tokenを期待する。triggerでは例外仕様の一回のread costを許容するが、全仕様の常時inputと成功後再読は許容しない。worker routingはTaskSpecが独立producerを明示した場合だけとする。
9. C71の既存11 label変更、root `AGENTS.md`が`7,500 byte`超、R-01からR-14または受入A〜Qの意味欠落、非triggerで例外仕様read、triggerと無関係な節のread、required validation欠落、成功後追加read、score `4`未満のいずれかがあれば停止する。targeted gate通過前にstandard14へ進めない。

## 適用構造

```text
Candidate71 core
  -> triggerなし: C71の最短正常経路でterminal
  -> authority / preparation trigger: AUTHORITY_AND_TASKSPEC
  -> producer / version / stale trigger: IDENTITY_AND_LINEAGE
  -> invocation / predicate / terminal trigger: EXECUTION_STATE
  -> delegated producer trigger: PRODUCER_AND_DELEGATION
  -> dependency / shared-state trigger: SCHEDULING_AND_VALIDATION
  -> failed method / recovery trigger: METHOD_AND_RECOVERY
```

例外仕様は該当operationだけを精緻化する。C71のbind済みでcurrentなresultを無関係な例外triggerで失効させず、例外解決後はC71のterminal closureへ戻る。

## 変更境界

- direct source: Candidate71
- 維持: C71 root `AGENTS.md`の11 label全文
- 追加: rootの`EXCEPTION_TRANSITION`一label
- 追加: `docs/prompt-guide.md`の六つの条件付き例外仕様節
- 非変更: TaskSpec、evaluation set、rating、permission、executor parameter、THE-CAPTION runtime
- adoption / release / runtime projection: 未実施

## Candidate状態

- candidate number: Candidate77
- prompt identity: `the-caption-3ce91a4-triggered-exception-transition-r1`
- evaluation status: `standard14_evaluated_stopped`
- state: `stopped`
- result id: `748d799b3700433a9c8eac3870bd9439`
- standard14 N=5: 70 / 70 valid、score `4 = 70`
- Candidate71との差: quality中央値`0.000`、all-agent token中央値`+24.16%`、elapsed中央値`+17.77%`
- 判定: 品質は回復したが、Candidate71の最短正常経路よりcostが増えたため停止する。adoption、release、runtime projectionは未実施。

## Evidence

- [実行制御修正指示書](THE-CAPTION_execution-control_revision-instructions.md)
- [Candidate71設計](candidate71-validation-closure-design.md)
- [Candidate71 / Candidate74評価](../evaluations/results/candidate71-candidate74-typed-execution-state-machine-v12-standard14-n5_2026-07-23.md)
- [Candidate74 / 75 / 76評価](../evaluations/results/candidate74-candidate75-candidate76-validation-wave-v12_2026-07-23.md)
- [Candidate71 / Candidate77評価](../evaluations/results/candidate71-candidate77-triggered-exception-transition-v12-standard14-n5_2026-07-23.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
