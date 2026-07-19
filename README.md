# THE-CAPTION-PROMPT

THE-CAPTION向けプロンプトを設計、比較、評価し、反映可能な形へまとめるための専用リポジトリです。

## 目的

- 現行プロンプトの参照元とidentityを固定する
- 候補プロンプトを本体から分離して構築する
- 同一条件で比較できる評価caseとprofileを管理する
- 評価済み候補をrelease単位でまとめる
- THE-CAPTION本体への反映を明示的な承認作業として扱う

## 現在の状態

`evaluation_foundation_v3`。1つのimmutableなprompt set identityごとに3 KPIをappend-onlyで保存し、互換条件を満たす任意個のresultを後から取得・比較できます。現行の`total_tokens`はroot agentと全descendant SA sessionを合算するall-agent値です。root-onlyで保存したv3 `prompt-set-result/v1`は履歴として保持し、再集計値を`prompt-set-result/v2`へ追記します。固定A / B pair、winner、改善・悪化は保存・出力しません。v1 / v2 evaluation foundation resultも履歴として保持し、migrationや再解釈は行っていません。候補の採用、THE-CAPTION本体への反映、runtime有効化も行っていません。

## BaselineからCandidate5までの成果

固定したBaselineの役割別surfaceと一律の実装後確認を起点に、1つのcandidateで1つの制御境界を扱い、保存した観測を次の変更理由へ接続した。Candidate5の直接の系譜は`Baseline → Candidate2 → Candidate3 → Candidate4 → Candidate5`である。Candidate1はBaselineから直接派生したcompact構造の比較枝であり、Candidate5の親ではない。

| prompt set | 由来 | 固定した変更単位 |
| --- | --- | --- |
| Baseline | `the-caption-3ce91a4-current-r2` | 19 pathの比較元。専用実装SAへの委任と、実装後のAudit / Reviewを既定とする |
| Candidate1 | Baselineの直接child（比較枝） | rootを単一execution authorityへ統合し、JIT Context、ordered gate、変更class別completion、conditional Audit / Review、bounded rework、single terminalを同じ契約へまとめる |
| Candidate2 | Baselineの直接child（Candidate5本流） | 実装SA、permission、required validation、rework境界を維持したまま、riskとmachine coverageから`none` / `audit` / `review` / `audit+review`を選ぶ |
| Candidate3 | Candidate2の直接child | validationにtestを使うだけのtaskをtest変更とみなさないよう、test contract riskとchange classの導出境界を限定する |
| Candidate4 | Candidate3の直接child | 専用実装SAへの必須委任を外し、親直接、SA委任、分担の選択をモデル判断へ戻す |
| Candidate5 | Candidate4の直接child | 実行開始後は、完了条件または明示済み停止条件が観測事実として成立するまで継続する一般的な完了志向を加える |

この積み上げにより、Baselineの固定的な多段実行から、安全境界を維持しながら、実装主体、独立確認、停止をtaskと観測事実に応じて選択するprompt setまでを、immutableなfull bundleとして分離して構築できた。identity、変更target、構築時provenanceは[`prompts/candidates/README.md`](prompts/candidates/README.md)と各manifestに記録している。

expanded 12 case、`N=5`、global queue `M=24`の互換条件で保存した現行all-agent再集計値は次のとおりである。`total_tokens`は12 caseのiteration合計の中央値、`elapsed_seconds`も各iterationで12 caseを合計した値の中央値である。

| prompt set | `quality_score` | all-agent `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| Baseline | 100.000 | 8,925,798 | 2,828.032 |
| Candidate1 | 97.917 | 5,732,480 | 1,932.971 |
| Candidate2 | 100.000 | 7,381,355 | 2,477.185 |
| Candidate3 | 100.000 | 6,240,246 | 2,465.865 |
| Candidate4 | 100.000 | 5,909,205 | 1,676.820 |
| Candidate5 | 100.000 | 5,740,441 | 1,714.914 |

Candidate5とBaselineの数値差は、`quality_score`が`0.000`、`total_tokens`が`-3,185,357`、`elapsed_seconds`が`-1,113.118`だった。qualityの内訳では、Baselineがscore 4を58 run、score 3を2 run、Candidate4がscore 4を57 run、score 3を1 run、score 1を2 run記録したのに対し、Candidate5は60 runすべてscore 4だった。Candidate5の40 implementation runはすべて親直接を選び、選択した独立Audit / Review workerはすべて実際に起動された。

数値の正本は[`v3 all-agent token再集計`](evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)、Candidate5の一次evidenceとrouting観測は[`Candidate5 N=5 result`](evaluations/results/candidate5-expanded12-global-m24-n5_2026-07-16.md)に置く。この結果は12 case、`N=5`の観測であり、採点は独立blind raterによるものではない。Candidate5は`observed_n5`だが、採用、release化、THE-CAPTION本体への反映、runtime有効化は未判断、未実施である。

## Candidate6からCandidate22までの成果

Candidate5以降は、C5の完了志向を維持してcontext効率化を調べる系列と、C1のcompact構造を維持してTaskSpec、worker、role、validationの接続境界を収束させる系列に分けた。現存する直接の系譜は`C5 → C6`、`C5 → C7 → C8`、`C1 → C9`、`C1 → C10 → C11 → C12 → C13 → C14 → C15 → C16 → C17 → C20 → C21 → C22`であり、candidate番号の順番をそのまま単一の親子関係として扱わない。

| prompt set | 由来 | 固定した変更単位 |
| --- | --- | --- |
| Candidate6 | Candidate5の直接child | 正本のJIT節参照、SA packet最小化、最終結果の再掲抑制を追加する |
| Candidate7 | Candidate5の直接child | required commandの完全evidence保存と、次工程へ渡すmodel-visible outputを分離する |
| Candidate8 | Candidate7の直接child | command単位のprojectionを工程間result全体へ一般化する |
| Candidate9 | Candidate1の直接child（診断枝） | invariant、TaskSpec明示値、change-class defaultの優先順位を解決し、解決済み契約をworkerへbindする |
| Candidate10 | Candidate1の直接child（C15本流） | machine reworkとenvironment recoveryのcounter domainを、責務が適用対象の場合だけ評価する |
| Candidate11 | Candidate10の直接child | workerのcontext継承を、担当criterionに必要十分な最小範囲へ収束させる |
| Candidate12 | Candidate11の直接child | TaskSpecのcriterion / ownerとrequired non-machine workerを必要十分な一対一対応へ収束させる |
| Candidate13 | Candidate12の直接child | review-onlyとaudit+reviewで異なる起動前提をreview role promptへ接続する |
| Candidate14 | Candidate13の直接child | TaskSpecが明示したrequired machine commandを変更class別defaultより優先する |
| Candidate15 | Candidate14の直接child | manifest-boundなselected roleのcontrol inputと、TaskSpecが制限するrepository evidence readを分離する |
| Candidate16 | Candidate15の直接child | bind済みevidenceだけがgate statusを変更できる原則へ既存記述を再編する |
| Candidate17 | Candidate16の直接child | constraint / terminalもoperation identityごとに限定する |
| Candidate20 | Candidate17の直接child | criterion ownerとproducer execution identityが一致するresultだけをevidenceとする |
| Candidate21 | Candidate20の直接child | owner固定criterionを全routeのrequired worker起動とcompleted resultへ接続する |
| Candidate22 | Candidate21の直接child | worker成立をruntimeが返すchild execution identity、そのidentityへのwait、child final resultへ限定する |

C6〜8では、prompt上のcontext参照や投影formatを狭めるだけでは、C5の品質特性を維持しながらall-agent tokenを減らす根拠にならないことを確認した。C9ではTaskSpecとdefaultの優先順位を導入した一方、適用外counterの解釈が分岐したため、その境界だけをC1へ加えたC10を別の直接childとして構築した。C10〜15は各観測で残ったcontext継承、worker cardinality、role起動条件、validation authority、control inputの境界を原則1 targetずつ接続した。C16 / C17はC15連続試験のF04 / F10低scoreを入口に、operation identityとevidenceの既存記述を再編したtargeted diagnostic系列である。C18 / C19は明示的に合意された候補ではなく、実施指示を広く解釈して診断中に追加された効果のない派生案だったため、経緯と観測値だけを履歴recordへ残してcandidate artifactを破棄した。C20は番号を再利用せずC17から直接派生し、criterion ownerをevidenceのproducer identity条件へ接続する。C21 / C22はC20連続試験のscore `3`原因に対し、required owner resultと実child lifecycleを順に接続する。

expanded 12 case、`N=5`、global queue `M=24`で保存したall-agent値は次のとおりである。C6、C10〜12、C14、C15、C17はBaseline、C1、C5と同じ互換条件のresultである。C9は同じ実行条件で12 caseを完了したが、先行2 caseと残り10 caseを異なるEvaluation set capsuleへ固定したstaged campaignであり、strict compatibilityの同一comparisonへ混ぜない。C7、C8はF02 `N=1`の診断、C13はF03 / F04各`N=3`のtargeted checkまでである。

| prompt set | 評価状態 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | score 4 / 3 / 1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Candidate6 | `observed_n5` | 100.000 | 5,951,457 | 1,715.486 | 58 / 1 / 1 |
| Candidate7 | `observed_f02_n1` | — | — | — | — |
| Candidate8 | `observed_f02_n1` | — | — | — | — |
| Candidate9 | `observed_n5`（staged campaign） | 93.750 | 8,331,893 | 2,353.169 | 53 / 2 / 5 |
| Candidate10 | `construction_complete / observed_n5` | 100.000 | 6,798,932 | 2,359.190 | 60 / 0 / 0 |
| Candidate11 | `observed_n5` | 100.000 | 5,726,760 | 2,301.432 | 60 / 0 / 0 |
| Candidate12 | `observed_n5` | 97.917 | 4,757,900 | 1,777.127 | 57 / 3 / 0 |
| Candidate13 | `construction_complete / observed_targeted` | — | — | — | — |
| Candidate14 | `observed_n5` | 100.000 | 4,648,809 | 1,753.159 | 59 / 1 / 0 |
| Candidate15 | `observed_n5` | 100.000 | 4,590,751 | 1,723.986 | 60 / 0 / 0 |
| Candidate17 | `observed_n5` | 100.000 | 4,422,933 | 1,388.239 | 60 / 0 / 0 |

Candidate15とBaselineの中央値差は、`quality_score`が`0.000`、`total_tokens`が`-4,335,047`、`elapsed_seconds`が`-1,104.046`だった。Candidate5との差は順に`0.000`、`-1,149,690`、`+9.072`秒、Candidate14との差は`0.000`、`-58,058`、`-29.172`秒だった。Candidate15ではCandidate14のF10 inventory未完了停止は再現せず、60 runすべてscore 4を記録した。

Candidate17とCandidate15は同じcompatibility keyを持つ。Candidate17 - Candidate15の中央値差は、`quality_score`が`0.000`、`total_tokens`が`-167,818`、`elapsed_seconds`が`-335.747`秒だった。Candidate17も60 runすべてscore 4を記録した。

owner-producer証跡をscore `4`の必要条件にする新rating revisionは、旧resultを変更せずC17とC20を新規実行した。この2 resultだけが相互に互換であり、上表の旧rating revisionとは混ぜない。

| prompt set | 評価状態 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | score 4 / 3 / 1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Candidate17 | `observed_n5_owner_producer_v1` | 95.833 | 4,510,093 | 1,635.175 | 49 / 11 / 0 |
| Candidate20 | `observed_n5_owner_producer_v1` | 95.833 | 4,404,154 | 1,613.670 | 49 / 10 / 1 |
| Candidate22 | `observed_n5_owner_producer_v1` | 100.000 | 4,904,017 | 1,746.454 | 58 / 2 / 0 |

C20 - C17の中央値差は`quality_score 0.000`、`total_tokens -105,939`、`elapsed_seconds -21.506`秒だった。F10 monthlyのowner producer resultはC17 / C20とも0 / 5で、C20では1件が開始identity誤認によりreview未実施のscore `1`となった。このN=5ではC20の狙いの挙動は観測できなかった。

C22 - C20の中央値差は`quality_score +4.167`、`total_tokens +499,863`、`elapsed_seconds +132.784`秒だった。C22はscore `4 / 3 = 58 / 2`で、F05 clarification、F05 out-of-scope、F07 dependency provenanceを含む11 caseは各5 / 5でscore `4` eligibleだった。F10 monthlyの2件はreceiver未確定のwait後にrootがchild result受領を自己申告しており、owner producer evidence不足としてscore `3`に残した。

C20の同条件連続試験は登録済み3 batch、180 runで中止した。score `4 / 3 / 1 = 148 / 31 / 1`で、score `3`の31件はすべて所定成果を満たした一方、criterion ownerに対応する別execution identityのproducer resultが成立しなかった。特にF05 clarificationとF10 monthlyが各14 / 15であり、owner evidenceの流用禁止だけでなく、必要なowner workerの起動とresult生成をgate flowへ接続する課題が残った。未登録のbatch 4と未実施batchは集計へ含めない。

C21 / C22の4-case targeted `N=5`では、owner producer eligibleがC21の19 / 20からC22の20 / 20になった。続くC22 expanded 12-case `N=5`は60 valid runをappend-onlyで登録し、C20とのcomparison viewを生成した。targeted resultとexpanded resultを混ぜず、Step 5の連続試験は実施していない。

系譜と評価状態の正本は[`prompts/candidates/README.md`](prompts/candidates/README.md)、C6〜8の調査境界は[`Candidate6からCandidate8までの効率化調査`](docs/candidate6-candidate8-efficiency-investigation.md)、C13 / C14の部分確認は[`targeted checks`](evaluations/results/candidate13-candidate14-targeted-checks_2026-07-16.md)、C15までの互換比較は[`Baseline / Candidate5 / Candidate14 / Candidate15 comparison view`](evaluations/results/baseline-candidate5-candidate14-candidate15-expanded12-global-m24-n5_2026-07-16.md)、C16 / C17の原則化とC18 / C19破棄の経緯は[`evidence boundary targeted checks`](evaluations/results/candidate16-candidate19-evidence-boundary-targeted_2026-07-17.md)に置く。C17の旧rating同条件expanded `N=5`は[`C17 expanded result`](evaluations/results/candidate17-operation-qualified-evidence-expanded12-global-m24-n5_2026-07-17.md)、新ratingのC17 / C20比較は[`owner-producer v1 result`](evaluations/results/candidate17-candidate20-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)、C20の登録済み3 batchは[`continuous B=3 result`](evaluations/results/candidate20-owner-producer-v1-continuous-n5-b3_2026-07-17.md)、C21 / C22の部分確認は[`owner worker targeted check`](evaluations/results/candidate21-candidate22-owner-worker-targeted_2026-07-17.md)、C20 / C22比較は[`owner worker lifecycle expanded result`](evaluations/results/candidate20-candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)へ保存した。adapter-levelの別条件診断は[`typed boundary evidence`](docs/typed-boundary-evidence.md)と[`F10 N=90 result`](evaluations/results/candidate17-typed-boundary-evidence-f10-n90_2026-07-17.md)へ明示的に分離する。これらは記載したcaseと反復条件の観測であり、採点は独立blind raterによるものではない。現存candidateはいずれも採用、release化、THE-CAPTION本体への反映、runtime有効化を行っていない。

ControlFreeRepository直接派生のCandidate23は[`expanded 12-case N=5 result`](evaluations/results/control-free-repository-candidate23-operation-boundary-expanded12-global-m24-n5_2026-07-17.md)へ登録し、60 / 60がscore `4`だった。F04のcleanup停止は5回中0件だが、ControlFreeRepositoryで観測した低頻度停止の解消までは一般化していない。

Candidate23へprompt-onlyのowner result AND predicateを追加したCandidate24は[`owner-producer expanded 12-case N=5 result`](evaluations/results/candidate22-candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)へ登録し、60 / 60がscore `4`、owner-producer eligible 60 / 60だった。F10 monthlyは5 / 5で実child resultが成立したが、prompt-only制御の完全保証や範囲外への一般化はしていない。

同条件の[`Candidate24 continuous N=5 B=5`](evaluations/results/candidate24-owner-result-gate-owner-producer-v1-continuous-n5-b5_2026-07-17.md)は300 valid runを5つのappend-only resultへ登録した。score `4 / 3 / 1 = 294 / 2 / 4`で、F10 monthlyは実child resultが25 / 25で成立した一方、4件はchildがrootの開始状態を逆に解釈してreview未実施となった。prompt-onlyの次の境界はchild lifecycleではなく、rootとchildがcriterion判定に使うmachine state値の一致である。

F10の一つの失敗形だけを避けるroute固有案C25〜C27は公開候補にせず破棄した。Candidate28はCandidate24を直接sourceとし、各operation identityのproducerをpredicate実行前に一つへbindする。独立確認が必要な場合は同じpredicateの再実行ではなく、先行result / artifactを入力とする別predicateの別operationへ分ける。この変更はroute、role、artifact種別に依存しない。rootだけを見ていた旧ratingの採点不能は、同じrunのrecursive descendant commandをbindする[`owner-producer quality v2 N=5`](evaluations/results/candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5_2026-07-17.md)へ更新した。60 / 60がrateable、score `4 / 3 = 58 / 2`で、残る2件はF03 / F07のindependent owner producer resultが成立しなかった。旧v1 runは履歴として変更していない。

Candidate29はCandidate28を直接sourceとし、criterion ownerの語列をoperationとproducer role identityへ保持する。owner型5 caseのtargeted `N=5`は25 / 25がscore `4`だった。expanded 12-case `N=5`ではF03とF07 dependencyのowner証跡が各5 / 5で成立し、C28のowner名不一致は再現しなかった。一方、全体ではowner-producer eligible 59 / 60、rateable 55 / 60だったため、expanded resultは未登録である。[staged result](evaluations/results/candidate29-owner-role-identity-binding-staged_2026-07-17.md)の停止条件に従い、continuous試験、採用、release判断へ進めていない。

Candidate30はCandidate29を直接sourceとし、Owner結果受領を実runtimeのspawn `task_name`、`FINAL_ANSWER.Sender`、criterion bindingへ限定する。targeted 25 / 25、expanded 60 / 60、continuous 300 / 300でOwner証跡の不成立は0件だった。continuousのscore `4 / 3 = 293 / 7`であり、score `3`はすべてrequired command成功証跡不足だった。F10 monthlyの開始条件修正はcase `r3`、valid runを未採点にしない変更はrating v3としてprompt変更と分離した。[result](evaluations/results/candidate30-runtime-owner-result-binding-owner-producer-v3-continuous-n5-b5_2026-07-17.md)は試験完了だけを示し、採用、release、THE-CAPTION本体反映は未判断である。

## Candidate17からCandidate34までの要約

Candidate17以降は、operation単位のevidence境界を起点に、owner resultの実行identity、child lifecycle、単一producer、terminal closureを順に接続した。その後、制御意味を維持したprompt縮約、worker context継承の最小化、owner result状態の分離を行った。

Candidate17からCandidate34までは単一の親子系譜ではない。owner evidenceを既存compact promptへ接続した系列は`C17 → C20 → C21 → C22`である。root制御なしの対照から必要な制御だけを積み上げた系列は`ControlFreeRepository → C23 → C24 → C28 → C29 → C30 → C31 → C32 → C33 → C34`である。C22とC24は同じ試験で比較したが親子ではない。C18 / C19とC25〜C27は診断中の不採用案であり、現行candidate chainへ含めない。

| prompt set | 直接source | 追加または変更した制御境界 | 主な保存evidence |
| --- | --- | --- | --- |
| Candidate17 | Candidate16 | `constraint / terminal`をoperation identity内へ限定 | 旧rating expanded 60 / 60 score `4`。owner-producer rating v5ではscore `4 / 3 / 1 = 49 / 10 / 1` |
| Candidate20 | Candidate17 | criterion ownerとproducer execution identityが一致するresultだけをevidence化 | continuous B=3のscore `3` 31件から、owner worker起動とresult生成の未接続を特定 |
| Candidate21 | Candidate20 | owner固定criterionをrequired worker起動とcompleted resultへ接続 | 4-case targetedでowner-producer eligible 19 / 20 |
| Candidate22 | Candidate21 | producer成立をruntime child identity、wait、child final resultへ限定 | targeted 20 / 20 eligible。expanded score `4 / 3 = 58 / 2` |
| Candidate23 | ControlFreeRepository | operation-scoped constraint / terminal、手段選択、recovery counterだけを復元 | expanded 60 / 60 score `4` |
| Candidate24 | Candidate23 | owner resultをchild identity、completed wait、final result、criterion bindingのAND predicateへ固定 | expanded 60 / 60 score `4`。continuous B=5はscore `4 / 3 / 1 = 294 / 2 / 4` |
| Candidate28 | Candidate24 | operationごとにproducerを一つだけbindし、独立確認を別operation化 | rating v2 expanded score `4 / 3 = 58 / 2` |
| Candidate29 | Candidate28 | criterion owner語列を短縮・言換えずproducer role identityへ保持 | owner型targeted 25 / 25 score `4`。expandedは停止条件により未登録 |
| Candidate30 | Candidate29 | Owner result受領をspawn `task_name`、`FINAL_ANSWER.Sender`、criterion bindingへ接続 | targeted 25 / 25、expanded 60 / 60、continuous 300 / 300でOwner証跡成立 |
| Candidate31 | Candidate30 | 全predicateのbind済みproducer terminal resultが揃うまでoperationをnonterminalに保持 | rating v5 expanded 60 / 60 score `4` |
| Candidate32 | Candidate31 | rootの見出し、説明、重複表現を8つの制御規則へ縮約 | root promptは32.6%縮約したが、C31比token中央値は`+6.45%`。score `4 / 2 / 1 = 58 / 1 / 1` |
| Candidate33 | Candidate32 | worker packetが十分なら`fork_turns=none`、不足時も必要最小turnだけ継承 | C32比token中央値`-24.63%`、quality中央値`-6.250`。score `4 / 3 / 1 = 56 / 1 / 3` |
| Candidate34 | Candidate33 | owner result未取得とbind済みcriterionの`false / failed`を分離し、別operationへの失効伝播を禁止 | targeted 10 / 10 score `4`。現行rating v7 expanded 60 / 60 score `4` |

Candidate32ではprompt表面の縮約だけではtoken削減を確認できなかった。Candidate33ではworker継承contextを削減し、C32比でall-agent token中央値が`-959,484`となったが、quality中央値も`-6.250`となった。Candidate34はC33で欠けたF05 out-of-scopeとF10 inventoryの必須responseをtargetedとexpandedの合計20 / 20で成立させ、owner result未取得とcriterionの`false / failed`を別状態へ戻した。

Candidate34のv5 expandedで残ったF05 clarifyのscore `1` 2件は、日本語の「フォールバック」を英字`fallback`と同義に扱わないrating偽陰性だった。rating v6でsemantic markerを修正した。v6で残ったCandidate34 F07 dependencyのscore `3` 1件は、markdown-heading形式の成功commandをcollectorがbindできない別の偽陰性だった。command evidence v4とrating v7でこの形式を修正し、保存済みv5 / v6 resultは再採点せず履歴として保持した。

現行のC31 / C34比較は、同じrating v7、expanded 12 case、`N=5`、global queue `M=24`で新規実行したresultである。

| KPI中央値 | Candidate31 | Candidate34 | Candidate34 - Candidate31 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| all-agent `total_tokens` | 3,916,601 | 3,290,615 | -625,986（-15.98%） |
| `elapsed_seconds` | 1,485.419 | 1,467.115 | -18.304（-1.23%） |

両setとも60 / 60がscore `4`で、retryとexcluded attemptは0件だった。Candidate34のtoken合計は5 / 5反復、12 case中10 caseでCandidate31より小さかった。elapsedは反復別でCandidate34が小さい回が1 / 5のため、安定した短縮とは判断しない。

C31とC34の19 target中18 targetは同一で、prompt差分はroot `AGENTS.md`だけである。C34はC31の主要制御境界をlabel化し、root promptを`3,785 bytes`から`3,235 bytes`へ`550 bytes`（`14.53%`）縮約したうえで、worker context最小化とowner result状態分離を追加した。静的なprompt縮約だけで実行時token差の因果を証明しない。

Candidate34のrelease bundleは作成時に`prepared_for_decision`、approval `pending`だったが、2026-07-19にCandidate41を唯一のrelease候補としたため、現在は`cancelled`である。C34 continuous B18は未実施である。詳細は[`Candidate31 / Candidate34 rating v7 N=5 comparison`](evaluations/results/candidate31-candidate34-owner-producer-v7-expanded12-global-m24-n5_2026-07-18.md)と[`Candidate34 release preparation`](prompts/releases/the-caption-3ce91a4-owner-result-state-separation-release-r1/README.md)を正本とする。

## Candidate35からCandidate41までの要約

Candidate35以降は、C34のroot execution controlを残してlegacy role / process surfaceだけをstub化したC35を共通の起点とした。F05のrequired output省略とF10のfinding location誤差に対する診断枝を作った後、C35 / C38 / C40の制御graphを棚卸しし、criterion owner語列をworker起動条件へ変換しないC41をC35から直接派生させた。

この範囲もcandidate番号順の一本道ではない。直接の系譜は`C34 → C35 → C36 → C37`、`C35 → C38 → C39`、`C38 → C40`、`C35 → C41`である。C36はartifactだけを保持した未評価candidateである。C39は停止条件に従ってexpanded試験へ進めていない。

| prompt set | 直接source | 追加または変更した制御境界 | 主な保存evidence |
| --- | --- | --- | --- |
| Candidate35 | Candidate34 | root execution controlとpath-scoped repository authorityを残し、legacy role / process 7 targetを0-byte stubへ置換 | B18保存evidence 1,080 runのv8診断replayはprojected score `4 / 3 = 1075 / 5`。v9 expandedは60 / 60 score `4` |
| Candidate36 | Candidate35 | 同じproducer final内でbind可能なrequired outputを、別criterion / constraintの`false / failed`から分離してproject | `not_evaluated` |
| Candidate37 | Candidate36 | findingの`path:line`をtarget revisionのline番号付きsourceによる直接確認へbind | v8 expanded 60 / 60 score `4` |
| Candidate38 | Candidate35 | evidenceまたはinvalidation条件が異なるrequired outputを最小result unitへ分割 | v8 targetedはscore `4 / 3 = 9 / 1`。v9 targetedは10 / 10 score `4` |
| Candidate39 | Candidate38 | operation producerをcriterion ownerと同一role identityへ固定 | v8 targetedは成果内容10 / 10、score `4 / 3 = 9 / 1`。expanded未実施 |
| Candidate40 | Candidate38 | result unitをoperation terminal resultのprojectionへ限定し、non-root evidenceをproducer terminal resultへbind | v9 targetedはscore `4 / 1 = 9 / 1` |
| Candidate41 | Candidate35 | owner語列だけではworkerを起動せず、TaskSpecが独立producer executionを明示した場合だけ委譲 | v9 targeted 10 / 10、expanded 60 / 60がscore `4` |

C35 B18の保存済みv7 evidenceに対するv8 replayでは、command evidence収集、許可path判定、F10 finding評価に由来する試験側の誤判定をcandidate側観測から分離した。projected score分布は`4 / 3 / 2 / 1 = 1075 / 5 / 0 / 0`だが、新しい公式resultではなく、元のv7 resultも変更していない。詳細は[`Candidate35 B18 saved-evidence replay`](evaluations/results/candidate35-owner-producer-v8-saved-evidence-replay_2026-07-18.md)を正本とする。

C38はv9 targetedでC35と同じ10 / 10 score `4`だったが、10 run token合計はC35比`+255,767`だった。差の90.50%はF10に集中し、F10では`exec +8`、`wait +3`、model step `+10`を観測した。C40もF10のtool call、model step、token合計をC38から減らさず、正しいchild findingをowner identity不一致として省略した1 runがscore `1`になった。result unit、evidence、invalidation、projectionを追加したC38 / C40の境界は、狙った実行経路削減をこの試験では示さなかった。

この観測を受け、[`prompt control graph review`](docs/prompt-control-graph-review.md)では、TaskSpecとrepository authorityが既に持つ条件の再定義と、owner語列・runtime identity・result unitを多段照合する判断点を分離した。C41は棚卸しで合意した一つのpredicateだけを実装し、TaskSpecが独立producer executionを明示しないF05 / F10をroot-onlyの最短経路へ戻した。v9 targetedでは10 / 10がscore `4`で、C35比の中央値差は`quality_score 0.000`、`total_tokens -238,617`、`elapsed_seconds -131.504`だった。worker spawnとwaitは0である。

C41 expanded 12-case `N=5`は60 / 60がvalid、rateable、score `4`で、全runがroot-onlyだった。同じv9、evaluation set、target、model、Agent、permission、executor parameter、反復条件へ固定した4-result比較は次のとおりである。

| prompt set | score 4 / 3 | `quality_score`中央値 | all-agent `total_tokens`中央値 | token合計 | `elapsed_seconds`中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 58 / 2 | 100.000 | 10,826,033 | 60,750,594 | 3,705.409 |
| ControlFreeRepository | 59 / 1 | 100.000 | 2,808,523 | 14,877,979 | 1,135.178 |
| Candidate35 | 60 / 0 | 100.000 | 4,565,773 | 22,035,738 | 1,841.107 |
| Candidate41 | 60 / 0 | 100.000 | 2,861,019 | 14,688,469 | 1,172.182 |

C35とC41は12 caseすべてで5 / 5がscore `4`だった。C35のtoken合計はC41より`7,347,269`、`50.02%`多く、case別では11 / 12 caseで多かった。C35の`elapsed_seconds`中央値はC41より`668.926`秒、`57.07%`長かった。ControlFreeRepositoryはC41と近いtoken量だったが、F10 monthly reviewでlocation mismatchが1件あった。N=5の1件対0件から低頻度誤経路の解消を一般化しない。

数値と互換条件の正本は[`Candidate41 targeted N=5`](evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-targeted2-n5_2026-07-19.md)、[`Candidate41 expanded 12-case N=5`](evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-expanded12-n5_2026-07-19.md)、[`Candidate41 continuous B18`](evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-continuous-n5-b18_2026-07-19.md)、[`Baseline / ControlFreeRepository / Candidate35 / Candidate41 comparison`](evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md)に置く。C41は唯一のrelease候補として`prepared_for_decision`、approvalは`pending`である。C34のrelease候補状態は一旦`cancelled`とした。これはC41の採用承認、THE-CAPTION本体への反映、runtime有効化、またはC34の不採用を意味しない。

## 構成

| Path | 役割 |
| --- | --- |
| `docs/` | リポジトリ契約、設計判断、反映手順 |
| `prompts/baselines/` | 比較元プロンプトと取得元identity |
| `prompts/candidates/` | 構築中の候補プロンプト |
| `prompts/releases/` | 承認可能な単位へ固定したprompt bundle |
| `evaluations/cases/` | 評価caseとmodel-visible / private境界 |
| `evaluations/profiles/` | model、Agent、環境、反復条件、比較条件 |
| `evaluations/results/` | 公開済みの履歴評価結果。v3 runtime registryとは分離 |

運用境界は[`docs/repository-contract.md`](docs/repository-contract.md)を正本とします。
評価基盤のLayerと境界は[`docs/prompt-comparison-workflow.md`](docs/prompt-comparison-workflow.md)に定義します。実行方法は[`docs/evaluation-loop-manual.md`](docs/evaluation-loop-manual.md)、検証cloneの容量維持は[`docs/evaluation-storage-maintenance.md`](docs/evaluation-storage-maintenance.md)を参照します。
v3のall-agent token補正結果は[`evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md`](evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)に記録します。今後の制御追加、置換、削除は[`docs/prompt-control-design-principles.md`](docs/prompt-control-design-principles.md)を検討原則とします。Candidate5の評価整理と次candidateの設計方向は[`docs/candidate5-token-efficiency-direction.md`](docs/candidate5-token-efficiency-direction.md)、Candidate6からCandidate8までの効率化調査と設計結論は[`docs/candidate6-candidate8-efficiency-investigation.md`](docs/candidate6-candidate8-efficiency-investigation.md)に記録します。両設計文書のtoken由来の旧解釈はroot-only履歴であり、補正結果を現行値として扱います。

## 初期作業

1. THE-CAPTIONの対象commitと現行prompt identityを固定する
2. 現行promptを`prompts/baselines/`へ取り込む
3. 最初の候補が解く問題と非目標を定義する
4. 比較前にevaluation profileを固定する
5. 評価結果と承認を分けて記録する
