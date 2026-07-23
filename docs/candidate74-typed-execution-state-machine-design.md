# Candidate74 typed execution state machine設計記録

## 結論

Candidate74はCandidate71を直接sourceとし、root `AGENTS.md`の実行制御を型付き状態機械へ改訂する。

変更根拠は[`THE-CAPTION execution control 修正指示書`](THE-CAPTION_execution-control_revision-instructions.md)である。これは既存traceから導く一つの効率化predicateではなく、R-01からR-11を同時に満たす明示的な仕様改訂である。

変更targetはroot `AGENTS.md`だけとする。Candidate72 / Candidate73は継承しない。評価基盤、TaskSpec、permission、executor parameter、rating contract、THE-CAPTION本体は変更しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-closure-r1`（Candidate71）とする。最短正常経路は、fieldを型に対応するauthorityへbindし、一つのproducerでpredicateを実行し、current resultだけを集約し、依存DAGの同一waveを同時発行してterminalへ閉じる経路である。
2. 保存済み誤経路はCandidate71 B18のA01である。未固定modeを確認せず実装・testへ進んだ1件があり、readinessと実行状態の境界が破れた。A02にはrequired validation欠落3件があり、validation集合の完全性だけでは実行状態機械が閉じなかった。
3. 既存TaskSpec、repository authority、repository stateは入力値と証拠を供給するが、authority型、execution identity改訂、invocation / predicate二軸、stale result、validation dependency wave、method / recovery枯渇後の遷移を定義しない。C71の11 labelだけでは修正指示書の受入条件を一意に判定できない。
4. 置換する一つの制御artifactは、C71のflatな11 labelを、`AUTHORITY_AND_TASKSPEC / IDENTITY_AND_LINEAGE / EXECUTION_STATE / PRODUCER_AND_DELEGATION / SCHEDULING_AND_VALIDATION / METHOD_AND_RECOVERY`の6共通定義節へ再編した型付き実行状態機械である。
5. 消す判断点は、authorityを一種類として解釈する判断、nonzero exitをpredicate falseへ変換する判断、旧producer / 旧artifact resultを再利用する判断、validation依存を実行後に推測する判断、method / recovery枯渇後も継続する判断、rootがworker resultを補完する判断である。
6. 増える判断点はauthority type、二種類のoperation identity、predicate contract version、result validity key、状態の二軸、validation DAG / wave、method / recovery budgetである。これは明示要件であり、prompt短縮やtoken削減を目的にしない。
7. 構造受入は修正指示書第8節A〜Qを対象とする。runtime qualityは将来の同一互換条件の評価で確認し、candidate構築だけをquality維持の証拠にしない。
8. 想定効果は誤った状態変換、stale result利用、validation競合、無期限method探索を減らすことである。prompt byte、tool call、model step、worker routingの削減は事前主張しない。
9. R-01〜R-11の欠落、requested outcome推測禁止の弱化、producer / criterion ownerの混同、operation-local stateの伝播、root補完、DAG cycle許容、unavailability reason消失のいずれかがあればcandidateを修正または停止し、profileやrunを作らない。

明示的な仕様改訂として九項目を定義したため、Candidate74 bundleと構造testを作成できる。評価profileとevaluation runは別状態として扱う。

## 変更構造

```text
AUTHORITY_AND_TASKSPEC
  -> field-specific authority
  -> control-plane preparation / spec_ready / clarification

IDENTITY_AND_LINEAGE
  -> lineage / execution / TaskSpec revision / predicate contract version
  -> operation partition / result validity / stale propagation

EXECUTION_STATE
  -> invocation / process exit / predicate / lifecycleの独立軸
  -> terminal readiness / outcome + stop reason / task aggregation

PRODUCER_AND_DELEGATION
  -> single producer / canonical delegated result binding
  -> nonproducer root / enforced-advisory context / nullable owner

SCHEDULING_AND_VALIDATION
  -> decision boundary / authority-bound acyclic DAG
  -> dependency wave / runtime undeclared dependency rebuild

METHOD_AND_RECOVERY
  -> finite method stop / budget
  -> one repair + one rerun / exhaustion closure
```

既存の`SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / DECISION_BOUNDARY / VALIDATION_CLOSURE / METHOD / RECOVERY`は削除扱いにせず、末尾の参照表から6共通定義節へ対応させる。

## R-12からR-14の判定

| ID | 判定 | 理由 |
| --- | --- | --- |
| R-12 | 採用 | nonproducer rootがTaskSpec構築、DAG / wave管理、result binding、terminal集約を行える範囲を列挙し、predicate実行とresult補完は禁止した。control planeとproducer実行を分離するために必要である。 |
| R-13 | 採用 | `fork_turns=none`が会話履歴だけを遮断する事実と、filesystem等を遮断しない限界を分けた。context指示をsecurity boundaryと誤認しないために必要である。 |
| R-14 | 採用 | pure machine predicateだけ`criterion_owner=none`を明示固定できる。owner不在とowner未固定を区別し、owner語列をproducer指定へ流用しないために必要である。 |

## 受入シナリオの対応

| Scenario | 一意にする定義 |
| --- | --- |
| A outcome authority | `outcome_authority`、negative bind list、競合時clarification |
| B producer変更 | lineage / execution分離、new execution、旧result invalidation |
| C worker provenance | canonical task / Sender / validity key、root補完禁止 |
| D invocation failure | `process_exit`と`invocation_status`とpredicate評価の分離 |
| E validation dependency | authority-bound acyclic DAG、wave、unexpected-state rebuild |
| F recovery exhaustion | attempt単位、有限max、証跡有無によるevaluated / unavailable |
| G task-wide constraint | 元policy authorityからoperation-localに個別materialize |
| H stale result | 6-field `result_validity_key`、revision-only例外、下流stale |
| I root非producer | control-plane許可一覧、predicate実行 / 再生成禁止 |
| J zero predicate | terminal時invalid、明示`no_op_allowed`だけsatisfied |
| K authority群 | policy優先順位、runtime canonical binding、method control readiness |
| L outcome / stop | `operation_evaluation_outcome`と`operation_stop_reason`の二軸 |
| M operation / wave | 最終artifactの独立評価は別operation、中間依存は別wave |
| N single producer | producer変更で旧独立predicate resultも再利用禁止 |
| O control-plane改訂 | predicate contract変更分と下流だけstale、contract変更はnew execution |
| P delegated binding | canonical binding relation採用、表示名 / wait / root要約不採用 |
| Q task aggregate | 全operationの`satisfied + none`だけoverall success |

## 構築状態

- candidate number: Candidate74
- prompt identity: `the-caption-3ce91a4-typed-execution-state-machine-r1`
- direct source: `the-caption-3ce91a4-validation-closure-r1`（Candidate71）
- changed target: root `AGENTS.md`だけ
- evaluation status: `standard14_evaluated`
- adoption / release / runtime projection: 未実施

## 標準14項目N=5結果

Candidate74を第12版採点、標準14項目、各`N=5`、global queue `M=24`で実行した。70 / 70件がvalidかつrateableで、全件score `4`だった。excluded attempt、workspace failure、command protocol違反、quality audit failureは0件である。

5反復中央値は`quality_score = 100.000`、all-agent `total_tokens = 3,366,548`、`elapsed_seconds = 1,140.329秒`だった。互換なCandidate71 Batch 1比で、中央値差は`quality_score = 0.000`、token `+58.88%`、elapsed `+9.28%`である。

成果品質は維持したが、今回の互換1 result比較ではtokenとelapsedが増えた。Candidate74を`standard14_evaluated`とし、採用、release、本体反映には進めない。詳細は[`Candidate71 / Candidate74標準14項目N=5`](../evaluations/results/candidate71-candidate74-typed-execution-state-machine-v12-standard14-n5_2026-07-23.md)へ保存する。

## Evidence

- [修正指示書](THE-CAPTION_execution-control_revision-instructions.md)
- [Candidate71設計記録](candidate71-validation-closure-design.md)
- [Candidate71第12版B18](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)
- [Candidate71 / Candidate74標準14項目N=5](../evaluations/results/candidate71-candidate74-typed-execution-state-machine-v12-standard14-n5_2026-07-23.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
