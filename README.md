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

## Candidate6からCandidate15までの成果

Candidate5以降は、C5の完了志向を維持してcontext効率化を調べる系列と、C1のcompact構造を維持してTaskSpec、worker、role、validationの接続境界を収束させる系列に分けた。直接の系譜は`C5 → C6`、`C5 → C7 → C8`、`C1 → C9`、`C1 → C10 → C11 → C12 → C13 → C14 → C15`であり、candidate番号の順番をそのまま単一の親子関係として扱わない。

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

C6〜8では、prompt上のcontext参照や投影formatを狭めるだけでは、C5の品質特性を維持しながらall-agent tokenを減らす根拠にならないことを確認した。C9ではTaskSpecとdefaultの優先順位を導入した一方、適用外counterの解釈が分岐したため、その境界だけをC1へ加えたC10を別の直接childとして構築した。C10以降は、各観測で残ったcontext継承、worker cardinality、role起動条件、validation authority、control inputの境界を、原則1 targetずつ追加してC15まで接続した。

expanded 12 case、`N=5`、global queue `M=24`で保存したall-agent値は次のとおりである。C6、C10〜12、C14、C15はBaseline、C1、C5と同じ互換条件のresultである。C9は同じ実行条件で12 caseを完了したが、先行2 caseと残り10 caseを異なるEvaluation set capsuleへ固定したstaged campaignであり、strict compatibilityの同一comparisonへ混ぜない。C7、C8はF02 `N=1`の診断、C13はF03 / F04各`N=3`のtargeted checkまでである。

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

Candidate15とBaselineの中央値差は、`quality_score`が`0.000`、`total_tokens`が`-4,335,047`、`elapsed_seconds`が`-1,104.046`だった。Candidate5との差は順に`0.000`、`-1,149,690`、`+9.072`秒、Candidate14との差は`0.000`、`-58,058`、`-29.172`秒だった。Candidate15ではCandidate14のF10 inventory未完了停止は再現せず、60 runすべてscore 4を記録した。

系譜と評価状態の正本は[`prompts/candidates/README.md`](prompts/candidates/README.md)、C6〜8の調査境界は[`Candidate6からCandidate8までの効率化調査`](docs/candidate6-candidate8-efficiency-investigation.md)、C13 / C14の部分確認は[`targeted checks`](evaluations/results/candidate13-candidate14-targeted-checks_2026-07-16.md)、C15までの互換比較は[`Baseline / Candidate5 / Candidate14 / Candidate15 comparison view`](evaluations/results/baseline-candidate5-candidate14-candidate15-expanded12-global-m24-n5_2026-07-16.md)に置く。これらは記載したcaseと反復条件の観測であり、採点は独立blind raterによるものではない。Candidate6〜15はいずれも採用、release化、THE-CAPTION本体への反映、runtime有効化を行っていない。

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
v3のall-agent token補正結果は[`evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md`](evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)に記録します。Candidate5の評価整理と次candidateの設計方向は[`docs/candidate5-token-efficiency-direction.md`](docs/candidate5-token-efficiency-direction.md)、Candidate6からCandidate8までの効率化調査と設計結論は[`docs/candidate6-candidate8-efficiency-investigation.md`](docs/candidate6-candidate8-efficiency-investigation.md)に記録します。両設計文書のtoken由来の旧解釈はroot-only履歴であり、補正結果を現行値として扱います。

## 初期作業

1. THE-CAPTIONの対象commitと現行prompt identityを固定する
2. 現行promptを`prompts/baselines/`へ取り込む
3. 最初の候補が解く問題と非目標を定義する
4. 比較前にevaluation profileを固定する
5. 評価結果と承認を分けて記録する
