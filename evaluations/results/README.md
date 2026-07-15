# Results

固定済みprofileで得た再現可能な結果を置く。raw logを無条件にcommitせず、必要なprovenance、集計、比較情報、除外理由を残す。

最新のv2 full-set comparisonは[`revision 2 expanded 12-case global M=24 N=1`](revision-2-expanded12-global-m24-n1_2026-07-15.md)である。3 KPIと`B - A`差分だけを出力し、winner、改善・悪化、採用判断は行わない。

最新の完了済みcore comparisonは[`revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md`](revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)である。これはv1のwinnerを含む履歴resultであり、v2では3 KPIと観測事項を判断材料として読む。`M=4`の事前確認は[`global-m4-qualification-f01-f04-n2_2026-07-15.md`](global-m4-qualification-f01-f04-n2_2026-07-15.md)、最小負荷確認は[`M=6`](global-m6-minimal-load-f01-n3_2026-07-15.md)、[`M=8`](global-m8-minimal-load-f01-n4_2026-07-15.md)、[`M=24`](global-m24-minimal-load-f01-n12_2026-07-15.md)に分離する。

control coverage追加の最初のstandalone comparisonは[`TC-F05 out-of-scope production deploy r1 N=3`](TC-F05-out-of-scope-production-deploy-r1-n3_2026-07-15.md)である。

2番目のstandalone comparisonは[`TC-F07 dependency provenance pair r1 N=3`](TC-F07-dependency-provenance-pair-r1-n3_2026-07-15.md)である。

3番目のstandalone comparisonは[`TC-F10 monthly format-test review r2 N=3`](TC-F10-monthly-format-test-review-r2-n3_2026-07-15.md)である。r1のprompt-overlay-relative diff blockerも同resultへ記録する。
