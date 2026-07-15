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

最初の評価caseとして[`TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r1`](TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r1/README.md)を選定し、model-visible入力、model-invisibleな`seed.patch`、oracle / grader contractを取り込んだ。

固定commitからEvaluation set capsuleと自己完結したfixtureを準備し、prompt file bundleを適用してCodexを実行するところまで実装済みである。

`r1`のnull pilotでは、fixtureのseed済みdirty状態とmodel-visible TaskSpecのdrift停止条件が一致せず、両runが実装前に停止した。このため`r1`は`case_revision_not_qualified`である。詳細は[`TC-F01 r1 pilot`](../results/TC-F01-r1_identical-bundle-pilot_2026-07-15.md)に記録する。

`r2`は同じseedをdeterministic commitへ固定し、known-good `.venv`をself-contained fixtureへ含めた。bit-identical bundleによる`N=10`では20runすべてが同じ正解成果へ到達したが、token中央値に57.8%差が出てnull条件で機械的winnerが生じた。このためstatusは`execution_qualified_null_calibration_failed`である。詳細は[`TC-F01 r2 N=10 null calibration`](../results/TC-F01-r2_identical-bundle-n10_2026-07-15.md)に記録する。正式なprompt評価結果はまだ存在しない。

revision 2 candidateの最初の追加variationとして[`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`](TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1/README.md)をmaterializeした。F01にないmulti-file、cross-layer、test-contract risk、conditional audit対象を追加する。seeded focused gateは`10 failed / 14 passed`、reference postimageはfocused `24 passed`、full `326 passed / 3 skipped`で、fixtureはqualifiedである。prompt実行は未実施である。

同じsource catalogのF03〜F10もfile bundleへmaterializeした。変更を伴うcaseは`private/seed.patch`、preimage / postimage identity、決定的seed commitを持つ。変更を伴わないF05 / F10は`clean_checkout`として固定commit、source identity、absent path、zero driftを検証する。全caseでEvaluation set capsuleへ入るmodel-visible情報は`trial-prompt-input.json`だけである。

F09はcase artifactとfixtureの再現には成功しているが、seed対象の`tests/AGENTS.md`がbaseline / candidate双方のprompt targetでもある。bundle overlayでcase条件が消えるため、現revisionを実行setへ入れない。これは未materializeではなく、`prompt_target_collision`による明示的なexecution blockerである。

| family | case | 主なvariation | 状態 |
| --- | --- | --- | --- |
| F01 | `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r2` | single-source Python implementation | `execution_qualified_null_calibration_failed` |
| F02 | `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1` | multi-file cross-layer implementation + test-contract risk | `fixture_qualified_prompt_not_evaluated` |
| F03 | [`TC-F03-ATOMIC-CONTEXT-CLEANUP/r1`](TC-F03-ATOMIC-CONTEXT-CLEANUP/r1/README.md) | mocked-I/O cleanup + filesystem state | `fixture_qualified_prompt_not_evaluated` |
| F04 | [`TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r1`](TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r1/README.md) | React / TypeScript + conditional UI | `fixture_qualified_prompt_not_evaluated` |
| F05 | [`TC-F05-CLARIFY-UNITS-MODE/r1`](TC-F05-CLARIFY-UNITS-MODE/r1/README.md) | clarification + zero drift | `fixture_qualified_prompt_not_evaluated` |
| F06 | [`TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r1`](TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r1/README.md) | test-only contract restoration | `fixture_qualified_prompt_not_evaluated` |
| F07 | [`TC-F07-CANONICAL-V4-RUNNER/r1`](TC-F07-CANONICAL-V4-RUNNER/r1/README.md) | shell runner + semantic target | `fixture_qualified_prompt_not_evaluated` |
| F08 | [`TC-F08-CANONICAL-CLI-REFERENCE-SYNC/r1`](TC-F08-CANONICAL-CLI-REFERENCE-SYNC/r1/README.md) | docs-only source/reference sync | `fixture_qualified_prompt_not_evaluated` |
| F09 | [`TC-F09-SCOPED-TEST-AUTHORITY/r1`](TC-F09-SCOPED-TEST-AUTHORITY/r1/README.md) | scoped authority restoration | `fixture_qualified_execution_blocked_prompt_target_collision` |
| F10 | [`TC-F10-ENTRYPOINT-INVENTORY-REVIEW/r1`](TC-F10-ENTRYPOINT-INVENTORY-REVIEW/r1/README.md) | read-only inventory inspection | `fixture_qualified_prompt_not_evaluated` |
