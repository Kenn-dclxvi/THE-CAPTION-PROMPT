# Candidate76 final-state validation wave設計記録

## 結論

Candidate76はCandidate75を直接sourceとする。Candidate74の型付き状態機械とCandidate75のindependent validation fast pathを維持し、post-invocationの最終target versionを観測するvalidationだけを後続waveへ固定する。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-authority-bound-validation-fast-path-r1`（Candidate75）とする。最短正常経路は、相互非依存なfocused / full validationを最初の同一waveで発行し、その実行が生成・変更・削除し得る最終worktreeを観測するdiff / status / path-scope validationを次の同一waveで発行してterminalへ閉じる経路である。
2. 保存済み誤経路はCandidate75 F06 N=5の4 runである。focused / fullと同じwaveにdiff / path確認を入れ、required test完了後の最終worktree versionを観測する依存を失った。残る1 runはfocused / fullを同時発行し、test完了後にdiff / path確認を発行した。
3. TaskSpecはF06-C3として許可file以外の差分がないことを要求する。required testがreportや生成物を作り得るため、test前またはtestと同時のdiff / statusだけではpost-test final stateを証明できない。Candidate75の一般的なindependence条件だけではこのtarget version依存が5 / 5へ収束しなかった。
4. 追加する一つのpredicateは`final_state_observer := 他required invocation完了後のtarget / artifact / worktree versionをpass conditionが観測するvalidation`である。potential mutatorからobserverへdependency edgeをbindする。
5. 消す判断点は、diff / status / path-scope確認をtest waveへ入れるか、test後へ送るかというrunごとの解釈差である。
6. 増える判断点は、pass conditionがpost-invocation final versionを要求するかの一回の分類である。observer同士は同一waveへまとめ、先行resultをearly-stopへ読み替えない。
7. 成果品質はF06 revision `r2`、第12版採点、N=5でscore `4 = 5`を要求する。command protocol違反、workspace failure、excluded attemptは0件を要求する。
8. behavior gateは、focused / fullの同一waveが5 / 5、diff / status / path-scopeが両test完了後の同一waveであることが5 / 5、全required validation後の追加read / validationが0 / 5である。
9. 一件でも成果scoreが4未満、focused / fullの逐次化、final-state observerの先行または同時発行、成功後追加read、またはCandidate75までの状態構造欠落があれば標準14項目へ進めず停止する。

## 変更境界

- 維持: C74の6共通定義節と型付き状態軸
- 維持: C75のauthority-bound dependency、independent fast path、成功後response closure
- 追加: potential mutatorからfinal-state observerへのtarget-version dependency
- 非変更: evaluation foundation、TaskSpec、permission、rating、THE-CAPTION runtime

## 評価状態

- candidate number: Candidate76
- prompt identity: `the-caption-3ce91a4-final-state-validation-wave-r1`
- direct source: `the-caption-3ce91a4-authority-bound-validation-fast-path-r1`（Candidate75）
- changed target: root `AGENTS.md`だけ
- targeted evaluation: F06 N=5、score `4 = 5`、behavior gate 3項目を各`5 / 5`で通過
- standard14 evaluation: 70 / 70 valid、score `4 = 69 / 3 = 1`
- state: `stopped`。A02 iteration 2の`git diff --check`成功証拠欠落により品質gate不合格
- adoption / release / runtime projection: 未実施

## Evidence

- [Candidate75設計記録](candidate75-authority-bound-validation-fast-path-design.md)
- [Candidate74設計記録](candidate74-typed-execution-state-machine-design.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Candidate74 / 75 / 76評価](../evaluations/results/candidate74-candidate75-candidate76-validation-wave-v12_2026-07-23.md)
