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

## 得た知見: トークンを大きく減らせた仕組み

ここでは、これまでの候補開発で観測した「どの制御がトークン消費を大きく減らしたか」を、その因果とともに整理します。前提となる用語は説明を添えて用います。

### 前提となる用語

- **トークン (token)**: 言語モデルが入出力を処理するときの計量単位です。多いほど所要時間と費用が増えます。本リポジトリで扱うのは **all-agent `total_tokens`**、すなわち **root agent（作業を統括する主体）と、そのrunから起動された全SA session（sub-agent、下記のworker）の最終usageを合算した値**です。合算値なので、workerが増えると総量は非線形に膨らみます。
- **prompt control（制御）**: 指示書（AGENTS.md等）に置く不変条件のことです。1つの**label**（見出し付きの制御単位）が1つの**predicate**（「この条件が成り立つときはこう振る舞う」という判定文）を持ちます。labelを足すとモデルの実行経路が変わり、トークンが増減します。
- **worker（SA session）**: モデルが作業を分担するために起動する下位セッションです。1体起動するたびに、その子セッションのusageがall-agent総量へ丸ごと加算されます。
- **model step / tool call**: モデルが一度立ち止まって次の行動を決める単位（step）と、その結果として実際にコマンドやreadを実行する回数（tool call）です。トークン消費はこの2つの回数と強く連動します。

### 大きく減らせた4つのメカニズム（効果の大きい順）

**1. 不要なworker起動そのものを抑える（削減幅が最大）**

因果: all-agent総量はworker1体ぶんのusageを丸ごと加算するため、「root agentだけで完結できる作業なのにworkerを起動する」経路を消すと、総量が最も大きく下がります。

制御の内容: 「criterion ownerを指す語列が現れただけではworkerを起動せず、TaskSpec（作業仕様）が独立したproducer executionを明示的に指定した場合にのみ委譲する」というpredicateに整理しました（Candidate41）。加えて、分散していた実行制御を単一のexecution authority（実行権限の主体）へ統合し直しました（Candidate5、Candidate15）。

観測: worker spawnがほぼ0になり、Candidate35との比較ではtoken合計がCandidate41比で`+50.02%`（=Candidate41側が約1/3少ない）、expanded12ではbaseline比 all-agent中央値で最大`-4,335,047`。品質（`quality_score`）は同水準を維持しました。品質を保ったままトークンを削減できたのはこの系統でした。

**2. workerへ継承するcontextを必要十分まで絞る**

因果: workerに「ここまでの経緯」を広く継承させると、その分だけ子セッションのusageが増えます。担当criterionに不要な情報を渡さなければ減ります。

制御の内容: worker packet（引き継ぎ情報）が十分なら継承を`none`にし、不足時も必要最小限のturnだけ継承する設定にしました（Candidate33）。

観測: Candidate32比でtoken中央値`-24.63%`（約`-959,484`）。ただし継承を絞りすぎた結果、`quality_score`中央値が`-6.250`低下しました。「渡さない情報が判断に不要」と確認できないまま削ると品質を割る、という反例です。

**3. 結論が変わらない場面での再判断・再readを止める**

因果: モデルは作業途中で繰り返しmodel step（次の行動の再検討）に戻ります。この再入自体がトークンを消費するため、「戻っても選択が変わらない」場面での再入を止めると減ります。

制御の内容: 「未発行のinvocation（次に出す指示）の選択を変えないresult間では、モデルへ再入しない」というlabel（`DECISION_BOUNDARY`、Candidate69）と、「artifact変更後に必要な検証を同一waveで一括発行し、全result受領後に一度だけ判断し、成功後は根拠のない追加readをしない」というlabel（`VALIDATION_CLOSURE`、Candidate71）を追加しました。

観測: standard14でCandidate43比 all-agent中央値`-26.21%`・top-level tool call`-26.60%`（Candidate69）、Candidate69比 token合計`-27.93%`・tool call`-30.16%`（Candidate71）。いずれもトークンとstep数を大きく削りましたが、一括判断化により必要な検証（例: A02の`git diff --check`）の欠落が増え、品質gateを通過せず採用は見送りました（ともに`stopped`）。

**4. read経路を事前に確定し、一括化・最短化する**

因果: 参照resourceを逐次バラバラにreadすると、read1回ごとにstepとトークンが積み上がります。読む対象と順序を事前に確定して一括readすれば減ります。

制御の内容: 順序依存のないroot readを同一model stepへbatch化する（Candidate50）、あるいは全文sourceを1つに固定し、確定済み証拠のreviewでのみ差分を実行前に合成する（Candidate63）形にしました。

観測: 特定case（F10=月次レビュー確認など）では劇的に減り、Candidate63はtool call 3回・token合計`-52.90%`へ収束。Candidate50もF05/F10で`-40.08%`。ただしCandidate50は探索型のA02で`+15.70%`と増加し、全20 runでは`-2.49%`にとどまりました。局所では強く効く一方、case横断では安定しませんでした。

### 横断的に確認できたこと

1. **表面的なprompt縮約は実行時トークンをほとんど動かさない。** byte数やlabel数を減らすだけの変更（Candidate32・65・66・67・68）では、all-agent tokenは有意に変わりませんでした。効いたのは「worker起動・再判断・read」という実行時の振る舞いを変えたときだけです。
2. **削減幅が最大なのは、処理量そのものを減らす制御。** とりわけ不要なworker起動の抑制が支配的でした。stepやreadの削減はその次に位置します。
3. **トークン削減の評価と、採用の判断は別レイヤーです。** メカニズム2・3・4は品質面で低下や不安定さが出て、評価上は`stopped`（品質gate不通過）と判定されました。ただし評価の`stopped`は採用の可否を決めません。採用・本体適用は、評価結果を踏まえて人が別途判断します。実際、メカニズム3のCandidate71は評価上はgate不通過のままですが、トークン効率を優先する別の採用判断として2026-07-23にTHE-CAPTION本体へ適用されました。本基盤はトークン削減を優劣や採用の根拠とはせず、3つのKPI（`quality_score`・`total_tokens`・`elapsed_seconds`）を並べて示すことに徹します。

なお、上記の数値はそれぞれ比較対象・評価集合・採点条件が異なる場面の観測であり、そのまま相互比較や一般化はできません。互換条件をそろえた比較と個別の一次結果は、以降の各節および`evaluations/results/`を参照してください。

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

この積み上げにより、Baselineの固定的な多段実行から、安全境界を維持しながら、実装主体、独立確認、停止をtaskと観測事実に応じて選択するprompt setまでを、immutableなfull bundleとして分離して構築できた。identity、変更target、構築時provenanceは[`prompts/candidates/README.md`](../prompts/candidates/README.md)と各manifestに記録している。

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

数値の正本は[`v3 all-agent token再集計`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)、Candidate5の一次evidenceとrouting観測は[`Candidate5 N=5 result`](../evaluations/results/candidate5-expanded12-global-m24-n5_2026-07-16.md)に置く。この結果は12 case、`N=5`の観測であり、採点は独立blind raterによるものではない。Candidate5は`observed_n5`だが、採用、release化、THE-CAPTION本体への反映、runtime有効化は未判断、未実施である。

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

系譜と評価状態の正本は[`prompts/candidates/README.md`](../prompts/candidates/README.md)、C6〜8の調査境界は[`Candidate6からCandidate8までの効率化調査`](../docs/candidate6-candidate8-efficiency-investigation.md)、C13 / C14の部分確認は[`targeted checks`](../evaluations/results/candidate13-candidate14-targeted-checks_2026-07-16.md)、C15までの互換比較は[`Baseline / Candidate5 / Candidate14 / Candidate15 comparison view`](../evaluations/results/baseline-candidate5-candidate14-candidate15-expanded12-global-m24-n5_2026-07-16.md)、C16 / C17の原則化とC18 / C19破棄の経緯は[`evidence boundary targeted checks`](../evaluations/results/candidate16-candidate19-evidence-boundary-targeted_2026-07-17.md)に置く。C17の旧rating同条件expanded `N=5`は[`C17 expanded result`](../evaluations/results/candidate17-operation-qualified-evidence-expanded12-global-m24-n5_2026-07-17.md)、新ratingのC17 / C20比較は[`owner-producer v1 result`](../evaluations/results/candidate17-candidate20-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)、C20の登録済み3 batchは[`continuous B=3 result`](../evaluations/results/candidate20-owner-producer-v1-continuous-n5-b3_2026-07-17.md)、C21 / C22の部分確認は[`owner worker targeted check`](../evaluations/results/candidate21-candidate22-owner-worker-targeted_2026-07-17.md)、C20 / C22比較は[`owner worker lifecycle expanded result`](../evaluations/results/candidate20-candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)へ保存した。adapter-levelの別条件診断は[`typed boundary evidence`](../docs/typed-boundary-evidence.md)と[`F10 N=90 result`](../evaluations/results/candidate17-typed-boundary-evidence-f10-n90_2026-07-17.md)へ明示的に分離する。これらは記載したcaseと反復条件の観測であり、採点は独立blind raterによるものではない。現存candidateはいずれも採用、release化、THE-CAPTION本体への反映、runtime有効化を行っていない。

ControlFreeRepository直接派生のCandidate23は[`expanded 12-case N=5 result`](../evaluations/results/control-free-repository-candidate23-operation-boundary-expanded12-global-m24-n5_2026-07-17.md)へ登録し、60 / 60がscore `4`だった。F04のcleanup停止は5回中0件だが、ControlFreeRepositoryで観測した低頻度停止の解消までは一般化していない。

Candidate23へprompt-onlyのowner result AND predicateを追加したCandidate24は[`owner-producer expanded 12-case N=5 result`](../evaluations/results/candidate22-candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)へ登録し、60 / 60がscore `4`、owner-producer eligible 60 / 60だった。F10 monthlyは5 / 5で実child resultが成立したが、prompt-only制御の完全保証や範囲外への一般化はしていない。

同条件の[`Candidate24 continuous N=5 B=5`](../evaluations/results/candidate24-owner-result-gate-owner-producer-v1-continuous-n5-b5_2026-07-17.md)は300 valid runを5つのappend-only resultへ登録した。score `4 / 3 / 1 = 294 / 2 / 4`で、F10 monthlyは実child resultが25 / 25で成立した一方、4件はchildがrootの開始状態を逆に解釈してreview未実施となった。prompt-onlyの次の境界はchild lifecycleではなく、rootとchildがcriterion判定に使うmachine state値の一致である。

F10の一つの失敗形だけを避けるroute固有案C25〜C27は公開候補にせず破棄した。Candidate28はCandidate24を直接sourceとし、各operation identityのproducerをpredicate実行前に一つへbindする。独立確認が必要な場合は同じpredicateの再実行ではなく、先行result / artifactを入力とする別predicateの別operationへ分ける。この変更はroute、role、artifact種別に依存しない。rootだけを見ていた旧ratingの採点不能は、同じrunのrecursive descendant commandをbindする[`owner-producer quality v2 N=5`](../evaluations/results/candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5_2026-07-17.md)へ更新した。60 / 60がrateable、score `4 / 3 = 58 / 2`で、残る2件はF03 / F07のindependent owner producer resultが成立しなかった。旧v1 runは履歴として変更していない。

Candidate29はCandidate28を直接sourceとし、criterion ownerの語列をoperationとproducer role identityへ保持する。owner型5 caseのtargeted `N=5`は25 / 25がscore `4`だった。expanded 12-case `N=5`ではF03とF07 dependencyのowner証跡が各5 / 5で成立し、C28のowner名不一致は再現しなかった。一方、全体ではowner-producer eligible 59 / 60、rateable 55 / 60だったため、expanded resultは未登録である。[staged result](../evaluations/results/candidate29-owner-role-identity-binding-staged_2026-07-17.md)の停止条件に従い、continuous試験、採用、release判断へ進めていない。

Candidate30はCandidate29を直接sourceとし、Owner結果受領を実runtimeのspawn `task_name`、`FINAL_ANSWER.Sender`、criterion bindingへ限定する。targeted 25 / 25、expanded 60 / 60、continuous 300 / 300でOwner証跡の不成立は0件だった。continuousのscore `4 / 3 = 293 / 7`であり、score `3`はすべてrequired command成功証跡不足だった。F10 monthlyの開始条件修正はcase `r3`、valid runを未採点にしない変更はrating v3としてprompt変更と分離した。[result](../evaluations/results/candidate30-runtime-owner-result-binding-owner-producer-v3-continuous-n5-b5_2026-07-17.md)は試験完了だけを示し、採用、release、THE-CAPTION本体反映は未判断である。

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

Candidate34のrelease bundleは作成時に`prepared_for_decision`、approval `pending`だったが、2026-07-19にCandidate41を唯一のrelease候補としたため、現在は`cancelled`である。C34 continuous B18は未実施である。詳細は[`Candidate31 / Candidate34 rating v7 N=5 comparison`](../evaluations/results/candidate31-candidate34-owner-producer-v7-expanded12-global-m24-n5_2026-07-18.md)と[`Candidate34 release preparation`](../prompts/releases/the-caption-3ce91a4-owner-result-state-separation-release-r1/README.md)を正本とする。

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

C35 B18の保存済みv7 evidenceに対するv8 replayでは、command evidence収集、許可path判定、F10 finding評価に由来する試験側の誤判定をcandidate側観測から分離した。projected score分布は`4 / 3 / 2 / 1 = 1075 / 5 / 0 / 0`だが、新しい公式resultではなく、元のv7 resultも変更していない。詳細は[`Candidate35 B18 saved-evidence replay`](../evaluations/results/candidate35-owner-producer-v8-saved-evidence-replay_2026-07-18.md)を正本とする。

C38はv9 targetedでC35と同じ10 / 10 score `4`だったが、10 run token合計はC35比`+255,767`だった。差の90.50%はF10に集中し、F10では`exec +8`、`wait +3`、model step `+10`を観測した。C40もF10のtool call、model step、token合計をC38から減らさず、正しいchild findingをowner identity不一致として省略した1 runがscore `1`になった。result unit、evidence、invalidation、projectionを追加したC38 / C40の境界は、狙った実行経路削減をこの試験では示さなかった。

この観測を受け、[`prompt control graph review`](../docs/prompt-control-graph-review.md)では、TaskSpecとrepository authorityが既に持つ条件の再定義と、owner語列・runtime identity・result unitを多段照合する判断点を分離した。C41は棚卸しで合意した一つのpredicateだけを実装し、TaskSpecが独立producer executionを明示しないF05 / F10をroot-onlyの最短経路へ戻した。v9 targetedでは10 / 10がscore `4`で、C35比の中央値差は`quality_score 0.000`、`total_tokens -238,617`、`elapsed_seconds -131.504`だった。worker spawnとwaitは0である。

C41 expanded 12-case `N=5`は60 / 60がvalid、rateable、score `4`で、全runがroot-onlyだった。同じv9、evaluation set、target、model、Agent、permission、executor parameter、反復条件へ固定した4-result比較は次のとおりである。

| prompt set | score 4 / 3 | `quality_score`中央値 | all-agent `total_tokens`中央値 | token合計 | `elapsed_seconds`中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 58 / 2 | 100.000 | 10,826,033 | 60,750,594 | 3,705.409 |
| ControlFreeRepository | 59 / 1 | 100.000 | 2,808,523 | 14,877,979 | 1,135.178 |
| Candidate35 | 60 / 0 | 100.000 | 4,565,773 | 22,035,738 | 1,841.107 |
| Candidate41 | 60 / 0 | 100.000 | 2,861,019 | 14,688,469 | 1,172.182 |

C35とC41は12 caseすべてで5 / 5がscore `4`だった。C35のtoken合計はC41より`7,347,269`、`50.02%`多く、case別では11 / 12 caseで多かった。C35の`elapsed_seconds`中央値はC41より`668.926`秒、`57.07%`長かった。ControlFreeRepositoryはC41と近いtoken量だったが、F10 monthly reviewでlocation mismatchが1件あった。N=5の1件対0件から低頻度誤経路の解消を一般化しない。

数値と互換条件の正本は[`Candidate41 targeted N=5`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-targeted2-n5_2026-07-19.md)、[`Candidate41 expanded 12-case N=5`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-expanded12-n5_2026-07-19.md)、[`Candidate41 continuous B18`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-continuous-n5-b18_2026-07-19.md)、[`Baseline / ControlFreeRepository / Candidate35 / Candidate41 comparison`](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md)に置く。C41 releaseはTHE-CAPTION PR [#334](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/334)で投影され、merge commit `8409eb9899b92a76870b066d88406754f4365b52`を候補43の巻き戻し先として保持する。C34のrelease候補状態は一旦`cancelled`のまま保持する。これはC34の不採用を意味しない。

## Candidate42からCandidate43までの要約

C41のTaskSpec前段を補う第1段階として、リポジトリから補える不足と、ユーザー確認なしには確定できない変更後の成果値を分離した。直接の系譜は`C41 → C42 → C43`である。両candidateともC41の19 targetを維持し、変更したのはroot `AGENTS.md`の既存`SPEC`だけである。

| prompt set | 直接source | 追加または変更した制御境界 | 主な保存evidence |
| --- | --- | --- | --- |
| Candidate42 | Candidate41 | required outcome、permission、constraintが未固定の間はwrite、test、dependency変更を開始しない`spec_ready`境界を追加 | A01は5 / 5が未固定値を推測してscore `0`。A02は成果を満たしたが旧v9の非公開command要件により5 / 5 score `3`。試験後に停止 |
| Candidate43 | Candidate42 | 変更後の値を直接要求する適用repository規則だけを成果値確定の根拠として認め、それ以外の未固定値は編集・試験前に確認 | v10 A01 / A02は10 / 10 score `4`。標準14項目は70 / 70 score `4`。B18完了後に`approved / projected` |

C42は`spec_ready`を追加したが、A01の5 runすべてで「現在値が`daily`なら変更後は別選択肢の`strict`」と推測して編集と試験へ進んだ。開始可否だけを定めても、値を確定するevidenceの適格性を限定しなければ誤った開始を防げないことを確認し、追加試験へ進めず停止した。A02のscore `3`は、実行役へ提示していない`bash scripts/dev/main_verify.sh`を旧v9 ratingだけが必須にした評価境界の問題である。保存済みresultは変更せず、v10の診断replayではA02を5 / 5 score `4`、A01を5 / 5 score `0`として分離した。

C43は新しいlabelを増やさず、C42の`SPEC`を一つのoutcome authority条件へ置換した。リポジトリから一意に解決できるA02の起動先は質問せず確定する一方、リポジトリが変更後値を直接要求しないA01は推測せず確認して停止する。実行役へ提示する入力を変えないv10 targetedでは、C41がA01の5 / 5でscore `0`、A02の5 / 5でscore `4`だったのに対し、C43は10 / 10がscore `4`だった。

同じv10、標準14項目、各`N=5`の互換条件では、C41のscore分布が`4 / 3 / 0 = 64 / 1 / 5`、C43が`4 = 70`だった。C43は14項目すべてを5 / 5で満たした。C41 / C43の70 run使用量合計は`17,824,901 / 17,732,662`で、差はC41からC43を引いて`+92,239`だった。中央値ではC41が`3,486,800`、C43が`3,647,298`であり、合計と中央値の方向が異なるため、token値だけを採用理由にしていない。

C43の同条件18回継続試験は、標準14項目 × 5反復 × 18 resultの1,260 / 1,260 runをvalid、rateableとして登録・圧縮した。公式score分布は`4 / 3 / 1 = 1,255 / 4 / 1`である。score `3`の4件はF10 monthly reviewの正しい主要findingに対するlocationずれだった。score `1`のA01 1件は、変更と試験を開始せず確認して停止した実responseをratingが質問表現として認識しなかった偽陰性である。1,259 / 1,260 runはroot-onlyで、F04の1件だけが担当情報を独立実行指定と解釈してchildを1件起動した。

C43 releaseは`approved`、release statusとruntime projectionは`projected`である。19 / 19 targetをTHE-CAPTIONへ投影し、C41との差分はroot `AGENTS.md`だけだった。THE-CAPTION PR [#335](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/335)をmerge commit `f729810ba8693acff963ef8e1cc2f2a175197072`として統合し、`bash ./scripts/dev/verify_change_set.sh`は364 testを通過した。投影前のC41 commit `8409eb9899b92a76870b066d88406754f4365b52`は巻き戻し先として保持する。

正本は[`Candidate42 A01 / A02 N=5`](../evaluations/results/candidate42-spec-readiness-boundary-ambiguity-targeted2-n5_2026-07-20.md)、[`Candidate41 / Candidate43 v10 targeted`](../evaluations/results/candidate41-candidate43-outcome-boundary-v10-targeted2-n5_2026-07-20.md)、[`Candidate41 / Candidate43 standard 14 N=5`](../evaluations/results/candidate41-candidate43-outcome-boundary-v10-standard14-n5_2026-07-20.md)、[`Candidate43 continuous B18`](../evaluations/results/candidate43-outcome-authority-boundary-v10-standard14-continuous-n5-b18_2026-07-20.md)、[`Candidate43 release / projection`](../prompts/releases/the-caption-3ce91a4-outcome-authority-boundary-release-r1/README.md)に置く。F10 locationずれ、A01 rating偽陰性、F04の1 child route、F08追加探索の関与可能性、N=5 / B18範囲外への一般化不能は未解決事項として保持する。計画と実施記録は[`TaskSpec確認 第1段階`](../docs/task-spec-planner-phase1-plan.md)に置く。

## Candidate44からCandidate71までの要約

C44以降は、C43の成果値境界を維持したまま、TaskSpec readiness、広域監査のworker topology、root-only経路、prompt圧縮、model再入、validation closureを別々の変更軸で調べた。この範囲も番号順の一本道ではない。主な系譜は`C43 → C44`、`C43 → C45 → C46 → C47 → C48`、`C43 → C49 → C51 → C52`、`C43 → C50 / C53 / C54`、`C54 → C55`からの複数枝、`C43 → C63〜C69`、`C69 → C70 / C71`である。

C44はC43の`SPEC`へ「成果を変える全未固定値を一度の確認へ含める」条件を追加した。[A01 / A02各`N=5`](../evaluations/results/candidate44-complete-spec-readiness-boundary-ambiguity-targeted2-n5_2026-07-20.md)は10 / 10がvalid・rateableだったが、A01で必要な確認事項が揃ったのは2 / 5、A02ではリポジトリから解決できる対象を質問して停止したrunが1 / 5あった。確認範囲を広げてもA01を安定させず、A02の最短正常経路を阻害したためC44は停止した。

C45〜C48は、THE-CAPTION-DEVの広域適合性監査A06をAgent-visible concurrency 31、Memoryなし、`N=1`で診断した枝である。これはblind quality ratingを持たない`diagnostic_only`であり、標準14項目やB18と互換な品質比較ではない。

| prompt set | 直接source | 追加した境界 | 保存traceでの主な観測 | 状態 |
| --- | --- | --- | --- | --- |
| Candidate45 | Candidate43 | 一つのjudgment resultの成立責任を一つのproducer execution identityへ固定 | C43の再検証waveは消えたが、all-agent tokenは`+2.33%`。入れ子探索と個別context再取得が残った | `diagnostic_only / draft` |
| Candidate46 | Candidate45 | 解決済みauthorityをproducer inputへbind | C45比token`-29.13%`。sessionとworkerが増え、durationは`+46.51%`。主要findingの維持を確定できず停止 | `diagnostic_only / draft` |
| Candidate47 | Candidate46 | 新規対象を同じrequired outcomeの適用域へ分類 | C46比token`-12.71%`。Web Editorを主結論へ戻したが、入れ子分割、root再読、nonterminal resultが残った | `diagnostic_only / draft` |
| Candidate48 | Candidate47 | 先行premiseのterminal後だけ下流judgmentを開始 | known finding 6 / 6を報告したが、C47比token`+42.22%`、tool call`+20.57%`。root再読とnonterminal補完が残り停止 | `diagnostic_only / draft` |

C49〜C54は、C43のroot-only正常経路を短くするため、worker制御の圧縮、read batch、root completion、independence、目的別graph、evidence-backed coreを個別に試した。全candidateが対象試験では成果を概ね保持したが、短いpromptや少ないlabelだけでは実行時token、model step、tool callの削減へ一貫して結び付かなかった。

| prompt set | 変更 | 主な保存evidence | 判定 |
| --- | --- | --- | --- |
| Candidate49 | worker制御6 labelを明示委譲時だけの3 labelへ圧縮 | 20 / 20 score `4`。root bytes`-39.12%`だが20 run token合計`+13.21%` | 停止 |
| Candidate50 | 順序依存のないroot readを同一model stepへbatch | F05 / F10 token合計`-40.08%`だが、A01 / A02は`+15.70%`。全20 run合計は`-2.49%` | 探索型A02の拡大により停止 |
| Candidate51 | C49へroot producer bindingと全predicate completionを復元 | 10 / 10 score `4`。F10 model step / tool callは`60 / 55`、token合計`+22.70%` | 停止 |
| Candidate52 | C51へC43の`INDEPENDENCE`一文を復元 | 10 / 10 score `4`。F05`-13.36%`、F10`+6.76%`、全体`+2.01%` | 停止 |
| Candidate53 | A系readiness、F系operation graph、明示委譲を別領域へ再配置 | 10 / 10 score `4`。同じ11-call経路の平均tokenはほぼ同値だが、全体token`+13.02%` | 停止 |
| Candidate54 | 保存traceで必要性を確認できたcontrol coreだけを残す | 10 / 10 score `4`、root bytes`-36.56%`。F10 model step / tool call`+5 / +5`、token合計`+9.44%` | 停止 |

C54以降の圧縮再検討では、[`Candidate43制御要素の目的別分別`](../docs/candidate43-control-element-classification.md)を入力とした。C54で欠けた固定済みpredicate・permission・constraintの実行前bindingを復元したCandidate55は、初回F10でmodel step `48 → 38`、tool call `43 → 33`、token合計`-19.31%`を観測したが、route gate r2では短経路が安定しなかった。C56〜C62は固定read methodを常時可視prompt内の条件で隔離できず、A02への流入を止められなかった。そこでCandidate63はC43を唯一の共通全文sourceとし、固定証拠reviewでだけ一行deltaを実行前合成した。[新しいF10-only各`N=5`](../evaluations/results/candidate43-candidate63-fixed-evidence-route-projection-f10-n5_2026-07-22.md)では両promptが5 / 5 score `4`、shell command 55件を維持し、Candidate63は5 / 5で3 tool call、token合計`-52.90%`へ収束した。route gateは通過したが、採用、release、本体反映は未判断である。

C43の32 clauseを4 blockへ再配置し、root / delegatedへF coreを全文重複したCandidate64は、[`catalog固定A01 / A02、F05 / F10、明示producer D01各N=5`](../evaluations/results/candidate43-candidate64-self-contained-execution-paths-catalog-fixed-n5_2026-07-22.md)で25 / 25 score `4`だった。一方、root-only F10はtool call `43 → 54`、model step `48 → 59`、token合計`+28.90%`となった。意味分別は成果を保持したが、全文重複は実行costを抑えなかったためCandidate64は停止した。

Candidate65はCandidate43の32 clauseを重複なしの11 labelへ短文化し、root bytesを`3,980 → 3,701`、`-7.01%`とした。[catalog固定F05 / F10各`N=5`](../evaluations/results/candidate43-candidate65-shared-operation-core-catalog-fixed-f-n5_2026-07-22.md)は10 / 10 score `4`、root-onlyだったが、F10はtool call `43 → 49`、model step `48 → 54`、token合計`+14.25%`となった。事前gateに従いCandidate65は停止し、A / Dへ進めていない。

Candidate66はCandidate43の一層9 label、label順、32 clause所属を維持し、root bytesを`3,980 → 3,923`、`-1.43%`とした。[F10-onlyとcatalog固定A01 / A02、F05 / F10、明示producer D01各`N=5`](../evaluations/results/candidate43-candidate66-topology-preserving-compression-catalog-fixed-n5_2026-07-22.md)はCandidate66の30 / 30がscore `4`だった。最初のF10-only gateはtoken合計`-2.04%`で通過したが、追加F set内のF10はtool call `43 → 57`、model step `48 → 62`、token合計`+31.36%`となった。表面圧縮のruntime効果を再現できなかったためCandidate66は停止した。

Candidate67はCandidate43の9 labelと本文を維持し、明示委譲gateとproducer再割当て禁止の短い重複文2件だけを正本labelへ統合した。root bytesは`3,980 → 3,792`、`-4.72%`である。[標準14項目各`N=5`](../evaluations/results/candidate43-candidate67-cross-label-predicate-deduplication-v10-standard14-n5_2026-07-22.md)はCandidate43とCandidate67の両方が70 / 70 score `4`だった。Candidate67からCandidate43を引いた3 KPI中央値差はquality `0.000`、all-agent token `-2.33%`、elapsed `-0.69%`である。一方、70件token合計は`+0.28%`で、反復ごとの方向も揃わない。状態は`standard14_evaluated`とし、採用、release、本体反映は未判断である。

Candidate68はCandidate43の9 labelと残りの本文を維持し、`INDEPENDENCE`からF9一文だけを削除した。root bytesは`3,980 → 3,860`、`-3.02%`である。[F10-only `N=5`](../evaluations/results/candidate43-candidate68-independent-review-operation-removal-f10-n5_2026-07-22.md)は5 / 5 score `4`、root-only、zero driftだった。3 KPI中央値はquality同値、all-agent token `+1.16%`、elapsed `+26.04%`で、token合計も`+426`となった。事前gateに従いCandidate68は停止した。

Candidate69はprompt自体のtoken数ではなくC43実runのall-agent `total_tokens`を対象とし、未発行invocationの選択を変えないresult間でmodelへ戻らない`DECISION_BOUNDARY`一文を追加した。[標準14項目各`N=5`](../evaluations/results/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-n5_2026-07-22.md)では、3 KPI中央値差がquality `0.000`、all-agent token `-26.21%`、elapsed `-18.37%`、70件token合計が`-22.59%`、top-level tool callが`-26.60%`だった。一方、F10 monthlyのfinding location mismatchが1件あり、点数分布は`4 / 3 = 69 / 1`だった。[同条件B18](../evaluations/results/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-continuous-n5-b18_2026-07-22.md)は1,260 / 1,260件を登録・圧縮し、C43比で18結果token中央値`-11.08%`、token合計`-13.00%`、top-level tool call `-15.29%`を観測したが、elapsed中央値は`+4.12%`だった。事前gateに従いCandidate69は`standard14_evaluated / stopped`とした。

Candidate70はCandidate69へ`MACHINE_BOUNDARY`を追加し、bind済みmachine resultだけで後続commandまたはstopが一意な区間をさらに明示した。[標準14項目B18](../evaluations/results/candidate69-candidate70-machine-decision-boundary-v10-standard14-continuous-n5-b18_2026-07-22.md)は1,260 / 1,260件がvalid・rateableで、Candidate69比のtoken合計`-16.52%`、18結果token中央値`-18.64%`、elapsed合計`-9.16%`、tool call`-19.41%`だった。一方、shell commandは`+3.04%`で、意味確認後もA02 required validation欠落2件とF10 locationずれ2件が残った。品質、不要command、worker routingのgateを通過せず、Candidate70は`standard14_evaluated / stopped`とした。

Candidate71はCandidate70を継承せず、Candidate69へ`VALIDATION_CLOSURE`一labelだけを追加した。artifact変更後の完全なrequired-validation集合を同一waveで発行し、全result受領後に一度だけ判断し、成功後の根拠なき追加readを止める境界である。[第12版標準14項目B18](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)はCandidate69 / Candidate71とも1,260 / 1,260件がvalid・rateableだった。Candidate71は18 / 18 Batchでtoken中央値とelapsed中央値が小さく、Candidate69比のtoken合計は`-27.93%`、elapsed合計は`-11.71%`、top-level tool callは`-30.16%`だった。

一方、Candidate71の公式score分布は`4 / 3 / 0 = 1,255 / 4 / 1`だった。意味確認後もA02の`git diff --check`欠落3件と、A01で未固定modeを確認せず実装・試験へ進んだ1件が残り、Candidate69より実質的な低得点が3件多かった。このため評価上は`standard14_b18_evaluated / stopped`であり、事前の品質gateは不通過のままである。

評価停止とは別に、2026-07-23の明示判断でCandidate71 releaseを`approved`とし、THE-CAPTIONへ`projected`にした。変更対象はroot `AGENTS.md`だけである。THE-CAPTION PR [#340](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/340)を統合commit `326fdd343a50522629592d67b0f028fb66e94eb3`としてmergeし、`bash ./scripts/dev/verify_change_set.sh`は`362 passed / 3 skipped`だった。品質gate不通過と未解決riskは取り消していない。評価・承認・本体反映の現在状態は[`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)を正本とする。

## 構成

| Path | 役割 |
| --- | --- |
| `docs/` | リポジトリ契約、設計判断、反映手順 |
| `prompts/baselines/` | 比較元プロンプトと取得元identity |
| `prompts/candidates/` | 構築中の候補プロンプト |
| `prompts/routes/` | 共通全文へ実行前合成する小さなroute差分 |
| `prompts/releases/` | 承認可能な単位へ固定したprompt bundle |
| `evaluations/cases/` | 評価caseとmodel-visible / private境界 |
| `evaluations/profiles/` | model、Agent、環境、反復条件、比較条件 |
| `evaluations/results/` | 公開済みの履歴評価結果。v3 runtime registryとは分離 |

運用境界は[`docs/repository-contract.md`](../docs/repository-contract.md)を正本とします。
評価基盤のLayerと境界は[`docs/prompt-comparison-workflow.md`](../docs/prompt-comparison-workflow.md)に定義します。実行方法は[`docs/evaluation-loop-manual.md`](../docs/evaluation-loop-manual.md)、検証cloneの容量維持は[`docs/evaluation-storage-maintenance.md`](../docs/evaluation-storage-maintenance.md)を参照します。
v3のall-agent token補正結果は[`evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)に記録します。今後の制御追加、置換、削除は[`docs/prompt-control-design-principles.md`](../docs/prompt-control-design-principles.md)を検討原則とします。Candidate5の評価整理と次candidateの設計方向は[`docs/candidate5-token-efficiency-direction.md`](../docs/candidate5-token-efficiency-direction.md)、Candidate6からCandidate8までの効率化調査と設計結論は[`docs/candidate6-candidate8-efficiency-investigation.md`](../docs/candidate6-candidate8-efficiency-investigation.md)に記録します。両設計文書のtoken由来の旧解釈はroot-only履歴であり、補正結果を現行値として扱います。

## 初期作業

1. THE-CAPTIONの対象commitと現行prompt identityを固定する
2. 現行promptを`prompts/baselines/`へ取り込む
3. 最初の候補が解く問題と非目標を定義する
4. 比較前にevaluation profileを固定する
5. 評価結果と承認を分けて記録する

## 今後の使い方と発展方針

このリポジトリは、プロンプト文面の良し悪しを感覚的に決める場所ではなく、AIエージェントの実行制御が成果品質、token、最終結果までの時間、実行経路へ与える影響を再現可能に測る実験基盤として使う。改善対象は文章量そのものではなく、worker起動、context継承、model再入、read、validation、停止、result bindingなどの実行上の判断点である。

### 基本的な改善サイクル

1. 現行のtarget repository ref、prompt identity、model、Agent環境、TaskSpec、permission、fixture、evaluation set、rating contract、反復条件を固定する。
2. 保存済みtraceから、一つの誤経路または余剰経路を選ぶ。将来起こりそうという推測だけで新しい制御を追加しない。
3. 既存のTaskSpec、repository authority、repository stateでは防げない理由と、残す最短正常経路を定義する。
4. 一つのcandidateで一つのpredicateだけを追加、置換、削除する。prompt変更と評価条件変更を同じ比較単位へ混ぜない。
5. まず対象control pathのtargeted試験を行い、成果品質と狙った実行経路の変化を確認する。成立した場合だけ標準評価と継続反復へ進む。
6. 3 KPIの`quality_score`、all-agent `total_tokens`、`elapsed_seconds`を保存する。tool call、model step、worker routing、context継承、失敗traceはdiagnosticとして確認し、KPIを増やさない。
7. 評価結果、採用、release、本体反映を別のgateとして記録する。評価基盤はwinnerまたは採用可否を出さない。

### 評価setの役割と育て方

標準評価setは、既存制御の回帰とcandidate間の互換比較に使う固定基準とする。tuningに使ったcaseを同じrevisionのheld-out evidenceとして扱わず、caseの入力、fixture、採点条件を変更する場合は既存revisionを上書きしない。

新しいcaseまたはvariationを追加する根拠は、既存setでは識別できない失敗が保存traceで見つかった場合、または新しいcontrol pathを既存caseで観測できない場合に限定する。caseは単に難しくするのではなく、競合する失敗仮説を分離できるように設計する。

A01では、現行の2択caseを回帰基準として維持したまま、3択以上の未固定modeを持つvariationを診断用に追加できる。2択で非現行値を選び、3択では確認して停止するなら補集合選択の可能性が高い。3択でも特定値を選ぶなら、mode名の意味、候補順序、現在値、test期待値などをauthorityへ変換している可能性を調べる。現在値と候補順序を回転し、曖昧なら停止するcaseとrepository authorityから一意に解決できるcaseを対にして、過剰停止と未指定値補完の両方を観測する。

低頻度の誤経路は少数反復で不在を証明しない。targeted試験でfixtureと採点を確認した後、必要な反復数と継続Batchを固定し、発生条件、選択値、理由分類、影響範囲を保存する。

### modelとruntime更新時の使い方

model、reasoning設定、Agent、CLI、memory、tool protocol、runtimeが変わる場合は新しいprofile revisionとして評価する。異なるmodelまたはruntimeのresultを同一compatibility comparisonへ混ぜず、それぞれの条件内でcontrol-free、現行prompt、candidateの差を測る。

この反復により、model能力の向上で自然に不要になった制御、引き続き効率や安全へ寄与する制御、新しいruntimeでは逆にcostを増やす制御を区別する。制御の必要性をmodel世代の印象で判断せず、同じcase familyと保存traceで更新する。

### prompt制御からruntime制御への発展

安定して効果が確認された機械的な制御は、自然言語promptへ永久に積み増すのではなく、型付きTaskSpec、permission gate、scheduler、validation DAG、artifact revision、producer identity、result validity、terminal stateなどのruntime機構へ移す候補とする。

移行時は、prompt-only条件、runtime強制条件、control-free条件を同じ評価setで比較する。runtimeへ移した結果、品質を維持したままprompt読解cost、model step、再read、再試行を減らせた場合に限り、prompt側の重複predicateを削除する。promptは実行境界の宣言へ寄せ、機械的に強制できる状態遷移はruntimeへ寄せる。

### 採用判断の考え方

有限回の試験で将来の挙動を100%保証することを採用条件にしない。残余riskは、観測頻度だけでなく、実利用での影響、検出可能性、回復可能性、不可逆操作の別gate、運用上の確認手段と合わせて扱う。

採用判断では、互換条件、score分布、3 KPI、case別結果、実行経路diagnostic、未解決risk、運用上の検出・回復手段、rollback identityを一つのevidence packageとして確認する。大きな効率改善と低頻度で回復可能な誤経路が共存する場合も、評価上の状態を変更せず、人が用途と運用条件に基づいて別途判断する。
