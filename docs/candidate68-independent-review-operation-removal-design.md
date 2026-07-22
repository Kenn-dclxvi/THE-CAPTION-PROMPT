# Candidate68 independent review operation removal設計記録

## 結論

Candidate68はCandidate43を直接sourceとし、root `AGENTS.md`の一層9 label、順序、残りの本文を保ったまま、`INDEPENDENCE`のF9一文だけを削除する。

削除対象は「先行result / artifactを対象とする別operationへ固有predicate / owner / producerを実行前に固定する。」である。同じlabelにある「同一predicateを別producerへ再割当てしない。」は残す。

`F5 / D6 / R1 / R2`、Candidate67で対象にしたcross-label duplicate 2文、表面表現、route、permissionは変更しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。最短正常経路は、TaskSpecで確定した一つのoperationへproducerを一度bindし、成果生成と必要な確認を同じproducerが完了する経路である。
2. 保存済みの誤経路は、同一predicateをrootとworkerへ重複割当てする経路、および既存成果の確認を理由にowner探索や別producerを追加する経路である。
3. 同一predicateのproducer再割当ては`PRODUCER`のsingle producer ruleと`INDEPENDENCE`の隣接文で制御する。独立した確認operationが必要かどうかはTaskSpecが対象、predicate、producerを明示する責務を持つ。そのためF9の常時適用だけを外しても既存境界が残る可能性がある。
4. 変更する一つのrelationは、`unconditionally predeclare independent review operation -> rely on TaskSpec and existing producer exclusivity`である。
5. 消す判断は、先行result / artifactを参照するたびに別operationを作るかどうかを共通promptから判定する処理である。
6. 新しい判断、参照、例外、permission、route、labelは追加しない。Candidate43の9 labelと順序を維持し、F9以外は逐語一致で残す。
7. 最初にF10-onlyを`N=5`で実行する。`quality_score`、all-agent `total_tokens`、`elapsed_seconds`をすべて記録し、root-only、zero drift、shell command、tool call、reasoning item、token_count eventも確認する。
8. F10-onlyが5 / 5 score `4`、root-only、zero drift、Candidate43と同じrequired command集合を満たし、Candidate43のtop-level tool call `40`、reasoning item `29`、all-agent token合計`811,578`を超えない場合だけA01 / A02、F05 / F10、D01を各`N=5`で実行する。`elapsed_seconds`は停止閾値に使わず、判断用KPIとして必ず併記する。
9. gate不通過時は停止し、補助predicateを追加しない。gate通過後もD01の指定worker境界、A / Fのroot-only、成果品質を満たさない場合は停止する。

九項目を定義済みであるため、Candidate68のbundle、4 profile、構造testを作成できる。構造testに合格した場合だけF10-only評価を開始する。

## 構築結果

Candidate68をCandidate43の直接childとして構築した。

- prompt identity: `the-caption-3ce91a4-independent-review-operation-removal-r1`
- bundle SHA-256: `d76a223819f36ee38ee9c4fdfa46a31b642cf981c65e55ef0061f7cdfb434a95`
- changed target: root `AGENTS.md`だけ
- root bytes: `3,980 -> 3,860`、`-120`、`-3.02%`
- label: 9 / 9を同じ順序で保持
- 削除: F9一文だけ

Candidate68の構築、評価、採用、release、本体反映は別状態とする。

## 評価結果

F10-only `N=5`は5 / 5でscore `4`、root-only、zero driftを維持した。登録済み3 KPIの中央値は`quality_score 100.0 -> 100.0`、all-agent `total_tokens 211,070 -> 213,525`、`elapsed_seconds 87.367 -> 110.118`だった。token合計も`811,578 -> 812,004`、`+0.05%`となり、事前上限を426 token超えた。

top-level tool callは`40 -> 40`、reasoning itemは`29 -> 28`、token_count eventは`46 -> 45`、shell commandは`50 -> 50`だった。F9削除による意味欠落はF10では観測しなかったが、経路とruntimeの削減も確認しなかった。

## 状態

Candidate68は`targeted_evaluated / stopped`とする。gateに従いA / F追加scope / Dは実行せず、standard14、採用、release、本体反映へ進めない。詳細は[`Candidate43 / Candidate68 F10 N=5`](../evaluations/results/candidate43-candidate68-independent-review-operation-removal-f10-n5_2026-07-22.md)を正本とする。
