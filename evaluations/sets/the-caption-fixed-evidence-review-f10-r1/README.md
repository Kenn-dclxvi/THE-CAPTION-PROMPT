# Fixed evidence review F10 r1

## 結論

Candidate43共通promptとfixed-evidence route projectionを、同じ一つの固定証拠reviewだけで比較するF10-only setである。

既存`the-caption-prompt-fixes-f05r1-f10r3-r1`からF10だけをprofile選択すると、Layer 4は未実行のF05を欠落としてfail-closedする。このためF10 `r3`のmodel-visible TaskSpecとseedを変更せず、単一caseの新しいEvaluation setとしてfreezeした。

## 固定条件

- set ID: `tc-f10-monthly-format-test-review-r3`
- revision: `r3`
- case: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- Layer 1 identity: `98da7e8c9ea12d91be50bb4d66ac15926b53a4ddee4d2035bc61bace13b01507`
- fixture identity: `a99d551dbd6113886d7b13a141e22f1947c744df7f5de2cd78ab4e2287e4ef48`

新しい単一case setはCandidate43とCandidate63の両方へ同じものを渡す。case集合とfixture identityが既存F05 / F10 resultとは異なるため、旧resultをstrict compatibility comparisonへ混ぜない。

## 状態

Evaluation setのmaterializeとfreezeを完了した。同じLayer 1でCandidate43とCandidate63を各`N=5`実行し、両resultのLayer 4登録とcomparison view生成を完了した。

5 / 5 score `4`を維持し、Candidate63のall-agent token合計はCandidate43比`-52.90%`だった。詳細は[`Candidate43 / Candidate63 F10 N=5`](../../results/candidate43-candidate63-fixed-evidence-route-projection-f10-n5_2026-07-22.md)に置く。採用、release、本体反映は未判断である。
