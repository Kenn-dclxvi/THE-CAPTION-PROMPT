# Candidate75 authority-bound validation fast path設計記録

## 結論

Candidate75はCandidate74を直接sourceとし、型付き実行状態機械を維持したまま、`SCHEDULING_AND_VALIDATION`のvalidation partition規則だけを置換する。

Candidate71への全面的な復元は行わない。Candidate74で導入したfield-specific authority、identity / lineage、result validity、invocation / predicate / lifecycleの状態分離、producer境界、dependency DAG、METHOD / RECOVERY closureは変更しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-typed-execution-state-machine-r1`（Candidate74）とする。最短正常経路は、finalized artifactに対する無条件requiredかつ相互非依存なvalidationを一つのwaveで発行し、全result受領後の一度の判断でterminalへ閉じる経路である。
2. 保存済み誤経路はCandidate74標準14項目N=5のF06である。5 / 5 runすべてがfocused test、full test、diff / path確認を別model stepへ逐次化した。run `b3ba8fca24d74bbfb800b636c78af6d5`では全required validation成功後にline再読も追加した。
3. F06 TaskSpecはfocused testとfull testを両方requiredとし、coverage重複も許可する。TaskSpec、repository authority、repository stateだけでは、modelがfocused / fullという名称や慣例的fail-fastをdependencyへ読み替えることを防げない。
4. 置換する一つのpredicateは`validation_fast_path_ready := validation_set_ready ∧ 全required validationがindependent ∧ decision boundaryなし`である。dependency edgeは`dependency_authority`が直接固定したものだけを認め、focused / full、coverage包含、cost、executor preferenceから作らない。
5. 消す判断点は、独立validationを一件実行するたびにresultをmodelへ戻し、後続validationを発行するか再判断する境界である。全成功後のstatus再確認、line再読、根拠再取得も消す。
6. 増える判断点は、`validation_independence_policy`による一回の独立分類と`validation_fast_path_ready`判定である。既存のDAG / wave例外は削除せず、明示dependencyがある場合だけ使用する。
7. 成果品質はF06 revision `r2`、第12版採点、N=5でscore `4 = 5`を要求する。command protocol違反、workspace failure、excluded attemptは0件を要求する。
8. 期待するbehaviorは、focused test、full test、diff / path確認を同一model stepから発行するrunが5 / 5、全required validation成功後の追加read / validationが0 / 5である。F06のmodel step、tool call、all-agent tokenはCandidate74保存traceより減る方向を期待するが、KPI閾値として採用判断へ使用しない。
9. 一件でも成果scoreが4未満、required validation欠落、independent validationの逐次化、成功後追加read、またはCandidate74の型付き状態構造の欠落があれば、標準14項目へ拡張せずcandidateを停止する。

## 変更境界

```text
Candidate74 typed execution state machine
  AUTHORITY_AND_TASKSPEC       維持
  IDENTITY_AND_LINEAGE         維持
  EXECUTION_STATE              維持
  PRODUCER_AND_DELEGATION      維持
  SCHEDULING_AND_VALIDATION
    dependency authority       維持
    validation DAG / wave      維持
    independent fast path      置換
    success response closure   直接化
  METHOD_AND_RECOVERY          維持
```

## 評価状態

- candidate number: Candidate75
- prompt identity: `the-caption-3ce91a4-authority-bound-validation-fast-path-r1`
- direct source: `the-caption-3ce91a4-typed-execution-state-machine-r1`（Candidate74）
- changed target: root `AGENTS.md`だけ
- targeted evaluation: F06 N=5実施、score `4 = 5`
- behavior: focused / full同一wave `5 / 5`、final-state確認post-test wave `1 / 5`、成功後追加readなし`5 / 5`
- state: `stopped`。post-test target version dependencyを一貫して保持できなかったため標準14へ進めない
- standard14 / adoption / release / runtime projection: 未実施

## Evidence

- [Candidate74設計記録](candidate74-typed-execution-state-machine-design.md)
- [Candidate71 control abstraction分析](candidate71-control-abstraction-analysis.md)
- [Candidate71 / Candidate74標準14項目N=5](../evaluations/results/candidate71-candidate74-typed-execution-state-machine-v12-standard14-n5_2026-07-23.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Candidate74 / 75 / 76評価](../evaluations/results/candidate74-candidate75-candidate76-validation-wave-v12_2026-07-23.md)
