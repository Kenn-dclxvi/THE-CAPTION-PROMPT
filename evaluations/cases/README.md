# Evaluation set overview

## 目的

THE-CAPTIONで開発作業を行うAgent向けpromptを、少ない手間で繰り返し比較する。

CONTEXT、CHRONICLEなどruntime内の生成promptは対象にしない。

## 評価セット

評価セットには、THE-CAPTIONで実際に発生した代表的な開発タスクを使う。短時間で繰り返せる小さなセットから始め、評価対象promptのcontrol coverageをcase variationとして段階的に追加する。

1 caseで基盤が必要とするのは次だけとする。

- case ID
- 開始時のrepository fixture
- adapterへ渡すopaqueなpayload

task、期待する目的、model-visible入力などの可変fieldはpayload内へカプセル化する。基盤はpayloadを解釈しない。exact postimageや細かな採点項目は必須にせず、test結果、diff、変更path、最終応答など、取得できる実行結果を採点材料にする。

## 採点

quality raterが成果全体を見て、caseごとに1つのscoreを付ける。

| score | 意味 |
| ---: | --- |
| 4 | 目的を十分に達成している |
| 3 | ほぼ達成している |
| 2 | 一部を達成している |
| 1 | わずかな進展だけがある |
| 0 | 目的を達成していない |

複数観点への分解、重み付け、機械的な合否判定は行わない。quality raterにはprompt identityとA / Bの名称を見せない。

全caseのscoreを0から100へ正規化した値を`quality_score`とする。quality raterはscoreと短い事実根拠だけを返す。

prompt set A / Bのwinnerは、`quality_score`、`total_tokens`、`elapsed_seconds`の3 KPIだけで決める。

quality raterは改善提案、修正、再実行、A / Bの選択を行わない。

## 増やし方

評価セットへcaseを追加する根拠は、既存セットでは見えない失敗が実際に見つかった場合、または評価対象promptの変更controlが既存caseで観測できない場合とする。

revision 2 candidateの初期coverage sourceには、`ai-development-research`の`the-caption-case-catalog-v1`にある`core-10`を使う。catalog上のcase specが存在することを、fixture qualified、evaluation ready、known-good、prompt評価済みと扱わない。各caseはこのrepositoryのfile bundle方式へ変換し、seed / reference behaviorと実行環境を個別にqualificationする。

日常の改善では同じ小さなセットを使う。このセットでpromptを調整した結果を、そのまま未使用caseでの最終確認結果とは扱わない。

## 現在の状態

F01 r1のnull pilotでseed済みdirty fixtureとTaskSpecのdrift停止条件の不一致を検出し、r2でdeterministic commitとknown-good `.venv`を持つself-contained fixtureへ修正した。F01 r2のbit-identical bundle `N=10`では全20 runが正解成果へ到達した一方、null条件でもtoken中央値が揺れた。詳細は[`TC-F01 r1 pilot`](../results/TC-F01-r1_identical-bundle-pilot_2026-07-15.md)と[`TC-F01 r2 N=10 null calibration`](../results/TC-F01-r2_identical-bundle-n10_2026-07-15.md)に記録する。

F01〜F10をfile bundleへmaterializeし、F09を除く9 caseでbaseline / candidate比較を実施済みである。最初のcore9 r1、`M=2`、`N=3`比較は`winner: b`だった。その結果で観測したTaskSpec外の周辺risk、未定義のcleanup恒久失敗、required gate重複、既存default routingを未完了理由にする揺れに対し、F01 r3、F03 r2、F06 r2、F07 r2を新しいprofile revisionとして作成した。

core9 r2はglobal queue、`M=4`、staged N=1→N=3で54 runを実行した。最終結果は`winner: a`であり、candidateはこのsetと反復条件では改善ではない。詳細は[`core9 r2 global M=4 staged N=3`](../results/revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)に記録する。artifactの存在、比較済み、採用、release、本体反映は別状態である。

F09はcase artifactとfixtureの再現には成功しているが、seed対象の`tests/AGENTS.md`がbaseline / candidate双方のprompt targetでもある。bundle overlayでcase条件が消えるため、現revisionを実行setへ入れない。これは未materializeではなく、`prompt_target_collision`による明示的なexecution blockerである。

| family | case | 主なvariation | 状態 |
| --- | --- | --- | --- |
| F01 | [`TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r3`](TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r3/README.md) | single-source Python implementation | `evaluated_in_core9_r2_n3` |
| F02 | [`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`](TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1/README.md) | multi-file cross-layer implementation + test-contract risk | `evaluated_in_core9_r2_n3` |
| F03 | [`TC-F03-ATOMIC-CONTEXT-CLEANUP/r2`](TC-F03-ATOMIC-CONTEXT-CLEANUP/r2/README.md) | mocked-I/O cleanup + filesystem state | `evaluated_in_core9_r2_n3` |
| F04 | [`TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r1`](TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r1/README.md) | React / TypeScript + conditional UI | `evaluated_in_core9_r2_n3` |
| F05 | [`TC-F05-CLARIFY-UNITS-MODE/r1`](TC-F05-CLARIFY-UNITS-MODE/r1/README.md) | clarification + zero drift | `evaluated_in_core9_r2_n3` |
| F06 | [`TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r2`](TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r2/README.md) | test-only contract restoration | `evaluated_in_core9_r2_n3` |
| F07 | [`TC-F07-CANONICAL-V4-RUNNER/r2`](TC-F07-CANONICAL-V4-RUNNER/r2/README.md) | shell runner + semantic target | `evaluated_in_core9_r2_n3` |
| F08 | [`TC-F08-CANONICAL-CLI-REFERENCE-SYNC/r1`](TC-F08-CANONICAL-CLI-REFERENCE-SYNC/r1/README.md) | docs-only source/reference sync | `evaluated_in_core9_r2_n3` |
| F09 | [`TC-F09-SCOPED-TEST-AUTHORITY/r1`](TC-F09-SCOPED-TEST-AUTHORITY/r1/README.md) | scoped authority restoration | `fixture_qualified_execution_blocked_prompt_target_collision` |
| F10 | [`TC-F10-ENTRYPOINT-INVENTORY-REVIEW/r1`](TC-F10-ENTRYPOINT-INVENTORY-REVIEW/r1/README.md) | read-only inventory inspection | `evaluated_in_core9_r2_n3` |
