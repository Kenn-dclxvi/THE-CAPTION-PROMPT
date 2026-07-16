# Results

固定済みprofileで得た再現可能な結果を置く。raw logを無条件にcommitせず、必要なprovenance、集計、比較情報、除外理由を残す。

このdirectoryの既存文書はv1 / v2の履歴resultである。v3の一次結果は1 prompt setごとのappend-only registry resultであり、旧A / B resultをin-place変換しない。sanitized resultをrepositoryへ公開する場合もruntime registryからの別artifact単位として扱う。

v3で2026-07-16までに保存した`prompt-set-result/v1`の`total_tokens`はroot agentだけを数えていた。現行値は[`v3 all-agent token再集計`](v3-all-agent-token-reaccounting_2026-07-16.md)の`prompt-set-result/v2`を使用する。以下から参照する旧v3 standalone resultとcomparison viewのtoken値はroot-onlyの履歴であり、all-agent値として使用しない。qualityとelapsedの履歴は変更していない。

root-only履歴のv3 resultは[`baseline N=5`](baseline-expanded12-global-m24-n5_2026-07-15.md)、[`candidate1 N=5`](candidate1-expanded12-global-m24-n5_2026-07-15.md)、[`candidate2 N=5`](candidate2-expanded12-global-m24-n5_2026-07-15.md)、[`candidate3 N=5`](candidate3-expanded12-global-m24-n5_2026-07-15.md)、[`candidate4 N=5`](candidate4-expanded12-global-m24-n5_2026-07-15.md)、[`candidate5 N=5`](candidate5-expanded12-global-m24-n5_2026-07-16.md)、[`candidate6 N=5`](candidate6-expanded12-global-m24-n5_2026-07-16.md)である。C6の設計対象に合わせ、同じ旧compatibility keyを持つBase、C1、C5、C6から[`4-result N=5 comparison view`](baseline-candidate1-candidate5-candidate6-expanded12-global-m24-n5_2026-07-16.md)を生成した。既存viewは履歴として変更せず、winner、採用、release判断は行っていない。

Candidate9の[`expanded 12-case staged N=5 result`](candidate9-expanded12-global-m24-n5_2026-07-16.md)は、F03 / F06先行stageとremaining 10 case stageの60 runを1つのcampaign summaryへまとめた。2つのEvaluation set identityとappend-only一次resultは変更せず、既存expanded resultとのKPI comparison view、winner、採用、release判断は生成していない。

Candidate10の[`expanded 12-case global M=24 N=5 standalone result`](candidate10-expanded12-global-m24-n5_2026-07-16.md)は、12 case、各5反復の60 runを1つのappend-only一次resultへ登録した。同じcompatibility keyとall-agent token accountingを持つBase、C1、C5、C10から[`4-result N=5 comparison view`](baseline-candidate1-candidate5-candidate10-expanded12-global-m24-n5_2026-07-16.md)を生成した。winner、採用、release判断は行っていない。

最初のv3 standalone resultは[`candidate2 expanded 12-case global M=24 N=1`](candidate2-expanded12-global-m24-n1_2026-07-15.md)である。candidate2だけをimmutableな`prompt_set_identity`へ結び付けて保存し、比較、winner、採用判断は行っていない。

同じ互換条件で新規実行した[`baseline standalone result`](baseline-expanded12-global-m24-n1_2026-07-15.md)とcandidate2から、[`baseline / candidate2 comparison view`](baseline-vs-candidate2-expanded12-global-m24-n1_2026-07-15.md)を生成した。差分方向は`candidate2 - baseline`であり、3 KPIの数値差だけを記録する。

さらに[`candidate1 standalone result`](candidate1-expanded12-global-m24-n1_2026-07-15.md)を同じ互換条件で追記し、[`baseline / candidate1 / candidate2 comparison view`](baseline-candidate1-candidate2-expanded12-global-m24-n1_2026-07-15.md)を生成した。既存の2-result viewは履歴として変更しない。

最新のv2 full-set comparisonは[`revision 2 expanded 12-case global M=24 N=1`](revision-2-expanded12-global-m24-n1_2026-07-15.md)である。3 KPIと`B - A`差分だけを出力し、winner、改善・悪化、採用判断は行わない。

最新の完了済みcore comparisonは[`revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md`](revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)である。これはv1のwinnerを含む履歴resultであり、v2では3 KPIと観測事項を判断材料として読む。`M=4`の事前確認は[`global-m4-qualification-f01-f04-n2_2026-07-15.md`](global-m4-qualification-f01-f04-n2_2026-07-15.md)、最小負荷確認は[`M=6`](global-m6-minimal-load-f01-n3_2026-07-15.md)、[`M=8`](global-m8-minimal-load-f01-n4_2026-07-15.md)、[`M=24`](global-m24-minimal-load-f01-n12_2026-07-15.md)に分離する。

control coverage追加の最初のstandalone comparisonは[`TC-F05 out-of-scope production deploy r1 N=3`](TC-F05-out-of-scope-production-deploy-r1-n3_2026-07-15.md)である。

2番目のstandalone comparisonは[`TC-F07 dependency provenance pair r1 N=3`](TC-F07-dependency-provenance-pair-r1-n3_2026-07-15.md)である。

3番目のstandalone comparisonは[`TC-F10 monthly format-test review r2 N=3`](TC-F10-monthly-format-test-review-r2-n3_2026-07-15.md)である。r1のprompt-overlay-relative diff blockerも同resultへ記録する。
