# Explicit producer monthly review D01 r1

## 結論

Candidate43とCandidate64のdelegated producer pathを、同じ明示的なproducer bindingで比較する単一case setである。

F10 monthly review r3のreview対象、read範囲、seed、oracleを維持し、model-visible TaskSpecへoperation identityと指定producer identityだけを追加した。

## 固定条件

- set ID: `tc-d01-explicit-producer-monthly-review-r1`
- revision: `r1`
- case: `TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1`
- source case: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3`
- operation identity: `monthly-format-review`
- canonical producer identity: `/root/monthly_format_review_producer`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- Layer 1 identity: `4b36be3a9fd5c89bb7ea3cf9e1b150e9cd5d83eab632db055ec6044161ee998e`
- fixture identity: `a99d551dbd6113886d7b13a141e22f1947c744df7f5de2cd78ab4e2287e4ef48`

## 状態

Evaluation setのmaterializeとfreezeを完了した。同じLayer 1でCandidate43とCandidate64を各`N=5`実行し、両resultのLayer 4登録とcomparison view生成を完了した。

両promptとも5 / 5がscore `4`だった。保存rolloutでは指定workerの起動、worker terminal resultの受信、rootによるreview非再実行を5 / 5で確認した。標準owner-producer collectorは両promptでproducer candidateを取得できなかったため、この経路確認は診断証拠として扱う。詳細は[`Candidate43 / Candidate64 catalog固定 N=5`](../../results/candidate43-candidate64-self-contained-execution-paths-catalog-fixed-n5_2026-07-22.md)に置く。

Candidate64の採用、release、本体反映は未判断、未実施である。
