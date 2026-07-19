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

候補41は同じ曖昧性評価集合からA01とA02だけを選び、[`各5回の結果`](candidate41-owner-metadata-delegation-boundary-ambiguity-targeted2-n5_2026-07-20.md)として10件を追記専用で登録した。A01は5回すべてで方針を推測して編集と試験へ進み点数`0`だった。A02は5回すべてで正規の起動先へ修復したが、非公開条件の`main_verify.sh`を実行せず点数`3`だった。この結果は候補作成前の記録である。旧3回試験との互換比較、優劣、採用、公開判断は行わない。

候補42の[`各5回の結果`](candidate42-spec-readiness-boundary-ambiguity-targeted2-n5_2026-07-20.md)は、A01の5回すべてで現在値と選択肢から`strict`を推測し、編集と試験へ進んだことを記録した。候補43の[`各5回の結果`](candidate43-outcome-authority-boundary-ambiguity-targeted2-n5_2026-07-20.md)は、A01の5回すべてで変更せず確認し、A02の5回すべてで正規の起動先を解決した。ただし旧採点条件が非公開で定めた動作方式と代替取得方針を同時に質問できたのは1回だった。候補44の[`各5回の結果`](candidate44-complete-spec-readiness-boundary-ambiguity-targeted2-n5_2026-07-20.md)は、A01で旧採点条件どおりの質問が2回に留まり、A02の1回で不要な確認を発生させたため停止した。4結果は同じ互換条件へ登録し、優劣、採用、公開判断は行っていない。

実行役に提示していない質問項目と試験コマンドを必須にしない第10版で、候補41と候補43を新規実行した[`A01 / A02各5回の結果`](candidate41-candidate43-outcome-boundary-v10-targeted2-n5_2026-07-20.md)は、両候補の20件すべてを有効かつ採点可能として登録した。候補41はA01の5件が点数`0`、A02の5件が点数`4`だった。候補43は10件すべて点数`4`だった。第2版の提示入力は第1版と同一であり、質問項目、正解値、特定コマンドを追加していない。採用、公開、本体反映は未判断である。

候補43を既存F項目12件とA01・A02で構成する標準14項目へ展開した[`各5回の結果`](candidate43-outcome-authority-boundary-v10-standard14-n5_2026-07-20.md)は、70 / 70件を有効かつ採点可能な追記専用の結果として登録した。点数は全件`4`、品質点中央値は`100.000`、全実行使用量中央値は`3,647,298`、所要時間中央値は`1,353.458`秒だった。旧12項目の結果とは評価集合が異なるため互換比較へ混ぜず、採用、公開、本体反映は未判断である。

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

Candidate17を現行のF10 monthly `r3`、`owner-producer-quality-v5`、command evidence v3へ固定して新規実行した[`expanded 12-case N=5 result`](candidate17-operation-qualified-evidence-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)は、60 / 60 valid runをappend-only resultへ登録した。score `4 / 3 / 1 = 49 / 10 / 1`で、低score 11件のうち10件は主要成果を満たしたがOwner producer resultが成立しなかった。Candidate31 rating v5 resultと同じcompatibility keyの比較viewを外部evidenceへ保存し、winner、採用、release判断は行っていない。

Candidate31を直接sourceとし、root `AGENTS.md`を8つの制御規則へ縮約したCandidate32の[`expanded 12-case N=5 result`](candidate32-compact-execution-control-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)は、60 / 60 valid runをappend-only resultへ登録した。score `4 / 2 / 1 = 58 / 1 / 1`だった。Candidate31比のall-agent `total_tokens`中央値差は`+235,955`、60 run合計差は`+1,012,750`、`elapsed_seconds`中央値差は`-321.557`秒だった。F01 score `2`は固定rating側allowlistの不整合、F10 inventory score `1`は必須inventoryを返さなかった実失敗として分離して記録し、winner、採用、release判断は行っていない。

Candidate32を直接sourceとし、十分なworker packetでは親履歴を継承しないCandidate33の[`expanded 12-case N=5 result`](candidate33-worker-context-sufficiency-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)は、60 / 60 valid runをappend-only resultへ登録した。score `4 / 3 / 1 = 56 / 1 / 3`だった。Candidate32比のall-agent `total_tokens`中央値差は`-959,484`（`-24.63%`）、60 run合計差は`-4,455,048`（`-22.89%`）だった。一方、`quality_score`中央値差は`-6.250`であり、token抑制とquality低下を分離して記録し、winner、採用、release判断は行っていない。

Candidate33を直接sourceとし、owner result未取得とbind済みcriterionのfalse / failedを分離したCandidate34の[`targeted 2-case / expanded 12-case N=5 result`](candidate34-owner-result-state-separation-owner-producer-v5-targeted2-expanded12-n5_2026-07-18.md)は、targeted 10 / 10とexpanded 60 / 60をappend-only resultへ登録した。Candidate33で必須response欠落を観測したF05 out-of-scopeとF10 inventoryは、targetedとexpandedの合計20 / 20でscore `4`だった。expandedの公式scoreは`4 / 1 = 58 / 2`、`quality_score`中央値は`100.000`だった。Candidate31比のall-agent `total_tokens`中央値差は`-460,026`（`-12.57%`）、60 run合計差は`-2,431,654`（`-13.18%`）だった。score `1`の2件はTaskSpecを満たす日本語の「フォールバック」を固定ratingの英字markerが認識しなかった偽陰性として分離し、公式resultは変更していない。

上記の偽陰性をresponse evidenceのsemantic marker groupで修正した`owner-producer-quality-v6`により、C31とC34を同条件で新規実行した[`expanded 12-case N=5 comparison`](candidate31-candidate34-owner-producer-v6-expanded12-global-m24-n5_2026-07-18.md)は、各60 / 60をappend-only resultへ登録した。F05 clarifyは両方とも5 / 5 score `4`だった。今回の10応答はすべて英字`fallback`を使ったため、日本語「フォールバック」の受理は固定回帰試験の証拠と分離した。両setのscore分布は`4 / 3 = 59 / 1`、quality中央値は`100.000`だった。C31のscore `3`はrequired validation未完了、C34のscore `3`はmarkdown-heading形式の成功証跡をcommand evidence v3がbindできなかったcollector偽陰性だった。後者はcommand evidence v4とrating v7で修正し、実rollout replayで確認したが、v6 resultは変更していない。C34比のall-agent `total_tokens`中央値差は`-833,631`（`-20.90%`）、60 run合計差は`-3,993,229`（`-19.84%`）で、C34のtoken合計は5 / 5反復で小さかった。採用、release承認、本体反映は行っていない。

command evidence v4と`owner-producer-quality-v7`へ揃えて新規実行した[`Candidate31 / Candidate34 expanded 12-case N=5 comparison`](candidate31-candidate34-owner-producer-v7-expanded12-global-m24-n5_2026-07-18.md)は、各60 / 60をappend-only resultへ登録した。両setとも全60件がscore `4`で、quality中央値は`100.000`だった。Candidate34のall-agent `total_tokens`中央値差はCandidate31比`-625,986`（`-15.98%`）、60 run合計差は`-2,779,489`（`-14.39%`）で、5 / 5反復、12 case中10 caseで小さかった。`elapsed_seconds`中央値差は`-18.304`秒だったが、反復別でCandidate34が短いのは1 / 5だった。v6の保存済みresultは変更せず、採用、release承認、本体反映は行っていない。

[`Candidate35 B18 v8 saved-evidence replay`](candidate35-owner-producer-v8-saved-evidence-replay_2026-07-18.md)は、保存済みv7 evidence 1,080 runに対する診断である。試験側のcollector、path policy、F10 ratingを修正するとprojected scoreは`4 / 3 / 2 / 1 = 1075 / 5 / 0 / 0`、全run合算qualityは`99.8843%`になる。F04 r1のcleanup条件は履歴として維持し、新規F04 r2ではadapter-owned teardownへ移管する。このreplayは新しい公式resultではなく、v7 resultを変更しない。

Candidate37の[`F05 clarify / F10 monthly review targeted N=5 result`](candidate37-exact-evidence-location-owner-producer-v8-targeted2-n5_2026-07-18.md)は、10 / 10 valid runをappend-only resultへ登録し、全件がscore `4`だった。F05は5 / 5で2点のclarificationを返し、F10は5 / 5でmajor findingを実変更行`monthly_main.py:25`へ結び付けた。初回dispatchで発見したF04非対象時のcleanup診断例外は試験側で修正し、例外終了attemptをprompt qualityへ算入せず、修正後の10 runだけを公式resultにした。採用、release、本体反映は行っていない。

同じCandidate37を12 caseへ展開した[`expanded N=5 result`](candidate37-exact-evidence-location-owner-producer-v8-expanded12-n5_2026-07-18.md)は、60 / 60 valid runをappend-only resultへ登録し、全件がscore `4`だった。F04 r2は5 / 5でadapter-owned teardownが完了し、candidate cleanup試行は0件だった。command collectorは9 run、26件の非required commandに関するprotocol violationを診断として保持したが、全required command groupは成功証跡へ結び付いたためqualityへ算入していない。採用、release、本体反映は行っていない。

Candidate35へresult unit別のevidenceとinvalidation範囲を追加したCandidate38の[`targeted N=5 result`](candidate38-result-unit-evidence-binding-owner-producer-v8-targeted2-n5_2026-07-18.md)は、成果内容を10 / 10で満たし、score分布は`4 / 3 = 9 / 1`だった。残るscore `3`はF10でrootがnon-root ownerのproducerを担当し、independent owner evidenceが成立しなかったものである。

Candidate38のproducerをcriterion ownerと同一role identityへ固定したCandidate39の[`targeted N=5 result`](candidate39-owner-aligned-result-unit-owner-producer-v8-targeted2-n5_2026-07-18.md)も、成果内容を10 / 10で満たした一方、score分布は`4 / 3 = 9 / 1`だった。F05の1 runがworkerを起動せず正しいclarificationを直接返したため、追加文言で独立owner経路の欠落は解消しなかった。同原因のprompt追記とexpanded試験には進めていない。

成果品質とowner経路診断を分離するv9で新規実行した[`Candidate35 / Candidate38 targeted N=5 comparison`](candidate35-candidate38-outcome-quality-owner-diagnostic-v9-targeted2-n5_2026-07-19.md)は、両setとも成果score `4`が10 / 10、owner evidence eligibleが10 / 10だった。Candidate38 - Candidate35の中央値差は`quality_score = 0.000`、`total_tokens = +41,659`、`elapsed_seconds = +7.357`で、10 run token合計差は`+255,767`だった。winner、採用、release判断は出力していない。

同じ20 runの[`token trace analysis`](candidate35-candidate38-v9-targeted2-n5-token-trace-analysis_2026-07-19.md)は、token差`+255,767`の`99.34%`がinput tokenで、`90.50%`がF10に集中したことを記録する。F10のsession数とspawn数は同じだったが、Candidate38は`exec +8`、`wait +3`、model step `+10`だった。result unitの論理分割を個別証拠取得の実行分割として扱い、root / childが重複確認したことを主要因として分離した。

Candidate38のresult unitをoperation terminal resultのprojectionへ限定したCandidate40の[`targeted N=5 result`](candidate40-operation-result-projection-boundary-v9-targeted2-n5_2026-07-19.md)は、score分布`4 / 1 = 9 / 1`だった。F10のtool callはCandidate38の74から75、model stepは84から85、token合計は`+49,106`で、境界修正による実行分割抑制は観測しなかった。F10 score `1`のrunではchildの正しいfindingをrootがowner identity不一致と解釈して省略した。winner、採用、release判断は出力していない。

TaskSpecのcriterion owner語列と明示的なproducer delegationを分離したCandidate41の[`targeted N=5 result`](candidate41-owner-metadata-delegation-boundary-v9-targeted2-n5_2026-07-19.md)は、F05 / F10の10 / 10がscore `4`だった。全runはroot sessionだけで完了し、worker spawnとwaitは0だった。Candidate41 - Candidate35の中央値差は`quality_score = 0.000`、`total_tokens = -238,617`、`elapsed_seconds = -131.504`で、10 run token合計差は`-1,077,725`だった。F10はtool call `63 → 27`、model step `74 → 32`、token合計`1,380,966 → 671,053`だった。winner、採用、release判断は出力していない。

同じCandidate41を12 caseへ展開した[`expanded N=5 result`](candidate41-owner-metadata-delegation-boundary-v9-expanded12-n5_2026-07-19.md)は、60 / 60 valid runをscore `4`としてappend-only resultへ登録した。全runはroot-onlyで、child sessionは0だった。all-agent token合計は`14,688,469`、中央値は`2,861,019`だった。C35 expanded v8とはquality rating revisionが異なるため互換比較viewを作らず、採用、release、本体反映は未判断として保持する。

同じCandidate41 v9条件を18 batch反復した[`continuous N=5 B18 result`](candidate41-owner-metadata-delegation-boundary-v9-continuous-n5-b18_2026-07-19.md)は、18個のappend-only result、1,080 / 1,080 valid runを登録・compactした。score分布は`4 / 3 = 1,078 / 2`で、2件はいずれもF10 monthly reviewのlocation mismatchだった。1,079 runはroot-onlyで、F02の1 runだけが2 childを起動した。保存済みC35 B18はrating revisionが異なるため互換比較へ混ぜない。

Candidate41 expanded resultと同じv9互換条件でbaseline、ControlFreeRepository、Candidate35を新規実行した[`4-result expanded N=5 comparison`](baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md)は、各60 / 60 valid runをappend-only登録した。score分布はbaseline `4 / 3 = 58 / 2`、ControlFreeRepository `4 / 3 = 59 / 1`、Candidate35とCandidate41は各`4 = 60`だった。Candidate35のall-agent token合計はCandidate41比`+7,347,269`、`+50.02%`で、12 case中11 caseで大きかった。`elapsed_seconds`中央値はCandidate41比`+668.926`秒、`+57.07%`だった。winner、採用、release、本体反映は未判断、未実施である。

最初のv3 standalone resultは[`candidate2 expanded 12-case global M=24 N=1`](candidate2-expanded12-global-m24-n1_2026-07-15.md)である。candidate2だけをimmutableな`prompt_set_identity`へ結び付けて保存し、比較、winner、採用判断は行っていない。

同じ互換条件で新規実行した[`baseline standalone result`](baseline-expanded12-global-m24-n1_2026-07-15.md)とcandidate2から、[`baseline / candidate2 comparison view`](baseline-vs-candidate2-expanded12-global-m24-n1_2026-07-15.md)を生成した。差分方向は`candidate2 - baseline`であり、3 KPIの数値差だけを記録する。

さらに[`candidate1 standalone result`](candidate1-expanded12-global-m24-n1_2026-07-15.md)を同じ互換条件で追記し、[`baseline / candidate1 / candidate2 comparison view`](baseline-candidate1-candidate2-expanded12-global-m24-n1_2026-07-15.md)を生成した。既存の2-result viewは履歴として変更しない。

最新のv2 full-set comparisonは[`revision 2 expanded 12-case global M=24 N=1`](revision-2-expanded12-global-m24-n1_2026-07-15.md)である。3 KPIと`B - A`差分だけを出力し、winner、改善・悪化、採用判断は行わない。

最新の完了済みcore comparisonは[`revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md`](revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)である。これはv1のwinnerを含む履歴resultであり、v2では3 KPIと観測事項を判断材料として読む。`M=4`の事前確認は[`global-m4-qualification-f01-f04-n2_2026-07-15.md`](global-m4-qualification-f01-f04-n2_2026-07-15.md)、最小負荷確認は[`M=6`](global-m6-minimal-load-f01-n3_2026-07-15.md)、[`M=8`](global-m8-minimal-load-f01-n4_2026-07-15.md)、[`M=24`](global-m24-minimal-load-f01-n12_2026-07-15.md)に分離する。

control coverage追加の最初のstandalone comparisonは[`TC-F05 out-of-scope production deploy r1 N=3`](TC-F05-out-of-scope-production-deploy-r1-n3_2026-07-15.md)である。

2番目のstandalone comparisonは[`TC-F07 dependency provenance pair r1 N=3`](TC-F07-dependency-provenance-pair-r1-n3_2026-07-15.md)である。

3番目のstandalone comparisonは[`TC-F10 monthly format-test review r2 N=3`](TC-F10-monthly-format-test-review-r2-n3_2026-07-15.md)である。r1のprompt-overlay-relative diff blockerも同resultへ記録する。
