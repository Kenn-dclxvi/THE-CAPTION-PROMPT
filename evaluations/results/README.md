# Results

固定済みprofileで得た再現可能な結果を置く。raw logを無条件にcommitせず、必要なprovenance、集計、比較情報、除外理由を残す。

このdirectoryの既存文書はv1 / v2の履歴resultである。v3の一次結果は1 prompt setごとのappend-only registry resultであり、旧A / B resultをin-place変換しない。sanitized resultをrepositoryへ公開する場合もruntime registryからの別artifact単位として扱う。

v3で2026-07-16までに保存した`prompt-set-result/v1`の`total_tokens`はroot agentだけを数えていた。現行値は[`v3 all-agent token再集計`](v3-all-agent-token-reaccounting_2026-07-16.md)の`prompt-set-result/v2`を使用する。以下から参照する旧v3 standalone resultとcomparison viewのtoken値はroot-onlyの履歴であり、all-agent値として使用しない。qualityとelapsedの履歴は変更していない。

root-only履歴のv3 resultは[`baseline N=5`](baseline-expanded12-global-m24-n5_2026-07-15.md)、[`candidate1 N=5`](candidate1-expanded12-global-m24-n5_2026-07-15.md)、[`candidate2 N=5`](candidate2-expanded12-global-m24-n5_2026-07-15.md)、[`candidate3 N=5`](candidate3-expanded12-global-m24-n5_2026-07-15.md)、[`candidate4 N=5`](candidate4-expanded12-global-m24-n5_2026-07-15.md)、[`candidate5 N=5`](candidate5-expanded12-global-m24-n5_2026-07-16.md)、[`candidate6 N=5`](candidate6-expanded12-global-m24-n5_2026-07-16.md)である。C6の設計対象に合わせ、同じ旧compatibility keyを持つBase、C1、C5、C6から[`4-result N=5 comparison view`](baseline-candidate1-candidate5-candidate6-expanded12-global-m24-n5_2026-07-16.md)を生成した。既存viewは履歴として変更せず、winner、採用、release判断は行っていない。

Candidate9の[`expanded 12-case staged N=5 result`](candidate9-expanded12-global-m24-n5_2026-07-16.md)は、F03 / F06先行stageとremaining 10 case stageの60 runを1つのcampaign summaryへまとめた。2つのEvaluation set identityとappend-only一次resultは変更せず、既存expanded resultとのKPI comparison view、winner、採用、release判断は生成していない。

Candidate1直接派生のCandidate10は[`expanded 12-case global M=24 N=5 result`](candidate10-c1-counter-boundary-expanded12-global-m24-n5_2026-07-16.md)として60 runを単一のappend-only resultへ登録した。既存expanded 12-case all-agent resultと互換なfixture identityを使い、winner、採用、release判断は行っていない。

Baseline、C1、C5、C1直接派生C10の[`4-result N=5 comparison view`](baseline-candidate1-candidate5-candidate10-c1-derived-expanded12-global-m24-n5_2026-07-16.md)は、all-agentの3 KPI中央値、反復値、quality分布、C10から各setを引いた数値差だけを記録する。winnerや採用判断は出力しない。

C10直接派生のCandidate11は[`expanded 12-case global M=24 N=5 result`](candidate11-sa-context-boundary-expanded12-global-m24-n5_2026-07-16.md)として60 runを単一のappend-only resultへ登録した。Baseline、C1、C5、C11の[`4-result N=5 comparison view`](baseline-candidate1-candidate5-candidate11-expanded12-global-m24-n5_2026-07-16.md)は、互換なall-agentの3 KPI、quality分布、case token、SA context境界の補助観測を記録し、winnerや採用判断は出力しない。

C11直接派生のCandidate12は[`expanded 12-case global M=24 N=5 result`](candidate12-route-cardinality-expanded12-global-m24-n5_2026-07-16.md)として60 runを単一のappend-only resultへ登録した。Baseline、C1、C5、C12の[`4-result N=5 comparison view`](baseline-candidate1-candidate5-candidate12-expanded12-global-m24-n5_2026-07-16.md)は、互換なall-agentの3 KPI、quality分布、case elapsed、route cardinalityの補助観測を記録し、winnerや採用判断は出力しない。

Candidate13のreview role接続とCandidate14のvalidation authority接続は[`targeted check`](candidate13-candidate14-targeted-checks_2026-07-16.md)へ分離した。C13はF03 / F04、C14はF06だけを確認し、partial set resultをexpanded comparisonへ混ぜていない。

C13直接派生のCandidate14は[`expanded 12-case global M=24 N=5 result`](candidate14-validation-authority-expanded12-global-m24-n5_2026-07-16.md)として60 runを単一のappend-only resultへ登録した。Baseline、C1、C5、C14の[`4-result N=5 comparison view`](baseline-candidate1-candidate5-candidate14-expanded12-global-m24-n5_2026-07-16.md)は、互換なall-agentの3 KPI、quality分布、case elapsed、validation authorityの補助観測を記録し、winnerや採用判断は出力しない。

C14直接派生のCandidate15は[`expanded 12-case global M=24 N=5 result`](candidate15-selected-role-control-input-expanded12-global-m24-n5_2026-07-16.md)として60 runを単一のappend-only resultへ登録した。Baseline、C5、C14、C15の[`4-result N=5 comparison view`](baseline-candidate5-candidate14-candidate15-expanded12-global-m24-n5_2026-07-16.md)は、互換なall-agentの3 KPI、quality分布、case elapsed、selected-role control input境界の補助観測を記録し、winnerや採用判断は出力しない。

制御promptなし・repository情報ありとC15は、独立した[`ambiguity boundaries 5-case global M=10 N=3 comparison`](control-free-repository-candidate15-ambiguity-boundaries-global-m10-n3_2026-07-17.md)として各15 runをappend-only resultへ登録した。互換な3 KPI、case別のclarify / execute / stopped境界、semanticな成果同等性を記録し、winner、採用、release判断は出力しない。

C15連続試験のF04 / F10低scoreに対するCandidate16 / 17の原則化、および明示合意なく診断中に追加され後に破棄したC18 / C19の経緯は[`evidence boundary targeted checks`](candidate16-candidate19-evidence-boundary-targeted_2026-07-17.md)へ分離した。expanded 12 case resultへ混ぜず、観測値と破棄理由を履歴として保持する。

Candidate17のpromptを維持し、実行adapterへtyped boundary evidenceを追加したF10 `N=90`は[`Candidate17 typed boundary evidence F10 N=90`](candidate17-typed-boundary-evidence-f10-n90_2026-07-17.md)へ分離した。execution compatibilityが異なるため既存Candidate17 resultへ混ぜず、90 / 90のscore `4`相当、450 / 450のtyped observation pass、開始identity誤認0件を記録する。

Candidate23を直接sourceとし、prompt-onlyのowner result AND predicateを追加したCandidate24の[`expanded 12-case N=5 result`](candidate22-candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)は60 / 60がscore `4`、owner-producer eligible 60 / 60となった。F10 monthlyは5 / 5で実child resultが成立し、Candidate22で残ったscore `3`の2 / 5はこのN=5では0件だった。runtime強制や範囲外への一般化は行わない。

同じCandidate24と互換条件を固定して継続した[`continuous N=5 B=5 result`](candidate24-owner-result-gate-owner-producer-v1-continuous-n5-b5_2026-07-17.md)は5つのappend-only result、300 valid runをまとめる。score `4 / 3 / 1 = 294 / 2 / 4`で、F07 / F04のscore `3`は実child result欠落、F10 monthlyのscore `1` 4件は実child resultがrootの開始状態を逆に解釈してreviewを開始しなかった。child lifecycle成立とmachine state一致が別境界であることを記録し、winner、採用、release判断は行っていない。

Candidate15と同じcompatibilityで実行したCandidate17の[`expanded 12-case global M=24 N=5 result`](candidate17-operation-qualified-evidence-expanded12-global-m24-n5_2026-07-17.md)は60 runをappend-only resultへ登録した。adapterとquality auditもC15連続試験時点の版へ固定し、60 / 60がscore `4`だった。winner、採用、release判断は行っていない。

ControlFreeRepositoryを直接sourceとするCandidate23の[`expanded 12-case global M=24 N=5 comparison`](control-free-repository-candidate23-operation-boundary-expanded12-global-m24-n5_2026-07-17.md)は、旧rating条件の同一compatibilityへ60 runをappend-onlyで登録した。Candidate23は60 / 60がscore `4`で、ControlFreeRepositoryのF04 score `3`はこのN=5では再現しなかった。保存済みviewは3 KPIの数値差だけを出力し、低頻度停止の解消、winner、採用、release判断へ一般化しない。

owner-producer証跡をscore `4`の必要条件にする新rating revisionで新規実行した[`Candidate17 / Candidate20 expanded 12-case N=5 comparison`](candidate17-candidate20-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)は、各60 runを同じcompatibility keyへ登録した。C17はscore `4 / 3 = 49 / 11`、C20はscore `4 / 3 / 1 = 49 / 10 / 1`で、F10 monthlyのowner producer resultは両方とも0 / 5だった。旧rating revisionのresultは変更せず、本comparisonへ混ぜていない。

同じCandidate20とrating revisionで継続した[`continuous N=5 B=3 result`](candidate20-owner-producer-v1-continuous-n5-b3_2026-07-17.md)は、登録・compactまで完了した3 result、180 runだけをまとめる。score `4 / 3 / 1 = 148 / 31 / 1`で、score `3`の全31件は成果未達ではなくowner producer result不足だった。F05 clarificationとF10 monthlyが各14 / 15を占め、必要なowner worker起動とresult生成がgate flowへ未接続という課題を記録する。未登録のbatch 4と未実施のbatch 5〜18は集計へ含めない。

Candidate20のscore `3`原因に対するCandidate21 / 22の[`4-case targeted N=5 check`](candidate21-candidate22-owner-worker-targeted_2026-07-17.md)は、partial-set diagnostic evidenceとしてLayer 4へ登録しない。C21はowner producer eligible `19 / 20`、C22は`20 / 20`であり、C22の別原因によるscore `1`をowner evidence不足へ読み替えない。

Targeted gate後に同じ互換条件へ展開した[`Candidate20 / Candidate22 expanded 12-case N=5 comparison`](candidate20-candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)は、C22の60 runをappend-only resultへ登録した。C22はscore `4 / 3 = 58 / 2`で、残る2件はいずれもF10 monthlyにおけるreceiver未確定waitとroot自己申告だった。保存済みviewはC22 - C20の3 KPI数値差だけを出力し、winner、採用、release判断は行わない。

Candidate24を直接sourceとし、各operationへproducerを一つだけbindするCandidate28の[`expanded 12-case N=5 incomplete rating result`](candidate28-single-producer-operation-binding-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)は60 / 60 runとowner-producer eligible 60 / 60を完了した。固定済みquality auditがdescendant sessionで成功したrequired validationを採点入力に含めないため、55 runだけがscore `4`、5 runはunrateableとなった。60 run全体のquality、Layer 4 result、KPI comparison、winner、採用、release判断は生成していない。

上記evidence scopeを別rating revisionとして更新したCandidate28の[`owner-producer quality v2 expanded 12-case N=5 result`](candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5_2026-07-17.md)は60 / 60をrateableとしてappend-only登録した。required command不足は0件、score `4 / 3 = 58 / 2`で、2件はいずれも所定成果を満たしたがindependent ownerのproducer resultが成立しなかった。旧v1 resultは変更せず、winner、採用、release判断は行わない。

Candidate28を直接sourceとし、criterion owner語列をproducer role identityへ保持するCandidate29の[`staged result`](candidate29-owner-role-identity-binding-staged_2026-07-17.md)は、owner型5 caseのtargeted `N=5`を25 / 25 score `4`としてappend-only登録した。続くexpanded 12-case `N=5`はF03とF07 dependencyのowner証跡が各5 / 5で成立したが、全体ではowner-producer eligible 59 / 60、rateable 55 / 60だった。expandedはLayer 4へ登録せず、continuous `N=5 B=5`も開始していない。

Candidate29を直接sourceとし、Owner結果受領を実runtimeのspawn `task_name`と`FINAL_ANSWER.Sender`へ結び付けたCandidate30の[`targeted、expanded、continuous result`](candidate30-runtime-owner-result-binding-owner-producer-v3-continuous-n5-b5_2026-07-17.md)は、targeted 25 / 25、expanded 60 / 60、continuous 300 / 300をrateableかつOwner証跡 eligibleとして登録した。continuousのscore `4 / 3 = 293 / 7`で、score `3`はすべてrequired command成功証跡不足だった。F10 monthlyは新case revision `r3`、採点は新rating revision `owner-producer-quality-v3`としてprompt変更と分離した。採用、release、THE-CAPTION本体反映は行っていない。

最初のv3 standalone resultは[`candidate2 expanded 12-case global M=24 N=1`](candidate2-expanded12-global-m24-n1_2026-07-15.md)である。candidate2だけをimmutableな`prompt_set_identity`へ結び付けて保存し、比較、winner、採用判断は行っていない。

同じ互換条件で新規実行した[`baseline standalone result`](baseline-expanded12-global-m24-n1_2026-07-15.md)とcandidate2から、[`baseline / candidate2 comparison view`](baseline-vs-candidate2-expanded12-global-m24-n1_2026-07-15.md)を生成した。差分方向は`candidate2 - baseline`であり、3 KPIの数値差だけを記録する。

さらに[`candidate1 standalone result`](candidate1-expanded12-global-m24-n1_2026-07-15.md)を同じ互換条件で追記し、[`baseline / candidate1 / candidate2 comparison view`](baseline-candidate1-candidate2-expanded12-global-m24-n1_2026-07-15.md)を生成した。既存の2-result viewは履歴として変更しない。

最新のv2 full-set comparisonは[`revision 2 expanded 12-case global M=24 N=1`](revision-2-expanded12-global-m24-n1_2026-07-15.md)である。3 KPIと`B - A`差分だけを出力し、winner、改善・悪化、採用判断は行わない。

最新の完了済みcore comparisonは[`revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md`](revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)である。これはv1のwinnerを含む履歴resultであり、v2では3 KPIと観測事項を判断材料として読む。`M=4`の事前確認は[`global-m4-qualification-f01-f04-n2_2026-07-15.md`](global-m4-qualification-f01-f04-n2_2026-07-15.md)、最小負荷確認は[`M=6`](global-m6-minimal-load-f01-n3_2026-07-15.md)、[`M=8`](global-m8-minimal-load-f01-n4_2026-07-15.md)、[`M=24`](global-m24-minimal-load-f01-n12_2026-07-15.md)に分離する。

control coverage追加の最初のstandalone comparisonは[`TC-F05 out-of-scope production deploy r1 N=3`](TC-F05-out-of-scope-production-deploy-r1-n3_2026-07-15.md)である。

2番目のstandalone comparisonは[`TC-F07 dependency provenance pair r1 N=3`](TC-F07-dependency-provenance-pair-r1-n3_2026-07-15.md)である。

3番目のstandalone comparisonは[`TC-F10 monthly format-test review r2 N=3`](TC-F10-monthly-format-test-review-r2-n3_2026-07-15.md)である。r1のprompt-overlay-relative diff blockerも同resultへ記録する。
