# Candidate5評価整理と次の方向性

> [!IMPORTANT]
> この文書のtoken数値とtoken由来の設計解釈はroot-only履歴であり、現行のall-agent再集計によって置き換えられた。現行値は[`v3 all-agent token再集計`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)を参照する。特に、root-onlyではBaselineがCandidate5より615,701少なく見えたが、all-agentではBaselineが3,185,357多く、SA利用setほどtokenが少ないという読みは成立しない。以下は当時の判断経緯として保持する。

## 位置づけ

この文書は、Baseline、Candidate1、Candidate5のexpanded 12 case、`N=5`結果を整理し、次candidateの設計方向を固定するdesign preparationである。Candidate5の採用、release化、THE-CAPTION本体への反映は判断しない。

比較対象は同じcompatibility key `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`を持ち、evaluation set、target repository ref、model、Agent環境、TaskSpec、permission、fixture、executor parameter、case、iteration、反復条件が一致する。

## N=5比較

| 指標 | Baseline | Candidate1 | Candidate5 |
| --- | ---: | ---: | ---: |
| `quality_score`中央値 | 100.000 | 97.917 | 100.000 |
| score 4 / 3 / 1 | 58 / 2 / 0 | 57 / 3 / 0 | 60 / 0 / 0 |
| `total_tokens`中央値 | 3,888,115 | 4,338,633 | 4,503,816 |
| `elapsed_seconds`中央値 | 2,828.032秒 | 1,932.971秒 | 1,714.914秒 |
| runner wall time | 733.867秒 | 635.451秒 | 426.528秒 |
| valid runs | 60 / 60 | 60 / 60 | 60 / 60 |
| excluded attempts | 0 | 0 | 0 |

差分はcandidateからBaselineを引いた値である。

| set | `quality_score` | `total_tokens` | `elapsed_seconds` | runner wall time |
| --- | ---: | ---: | ---: | ---: |
| Candidate1 - Baseline | -2.083 | +450,518 | -895.062秒 | -98.416秒 |
| Candidate5 - Baseline | 0.000 | +615,701 | -1,113.118秒 | -307.339秒 |

runner wall timeは60 runを`M=24`で並列実行した実時間であり、Layer 4のKPIではない。`elapsed_seconds`中央値は、各iterationで12 caseの実行時間を合計した値の中央値である。

## Prompt設計の差

| set | 実装主体 | Audit / Review | 停止制御 |
| --- | --- | --- | --- |
| Baseline | 専用実装SAへ委任 | AuditとReviewを要求 | Baseline既定 |
| Candidate1 | active executorに委ね、専用実装SAを持たない | TaskSpec predicateによるconditional実行 | Candidate1既定 |
| Candidate5 | 親直接 / SA委任 / 分担をモデル判断 | riskとmachine coverageによる4 route | 実行開始後の停止を明示済み条件と観測事実へ限定 |

Candidate5の保存evidenceでは、40 implementation runすべてが親直接を選び、実装目的のSA委任は0件だった。selected routeは`none` 24、`audit` 20、`review` 11、`audit+review` 5で、要求された独立workerはすべて起動された。

## 観測の整理

Candidate5は60 runすべてscore 4だった。一方、`total_tokens`中央値はBaselineより615,701（15.8%）、Candidate1より165,183（3.8%）多い。

ただしCandidate4からCandidate5への差は`total_tokens`が-75,660である。Candidate5で追加した完了志向そのものがtoken増加を生んだとは読めない。token量は、Candidate4から継続する実行時のcontext読取り、複数workerへのcontext投影、確認結果とrouting情報の反復出力を含む挙動として切り分ける。

case別の5回中央値では、Candidate5とCandidate1のtoken差は特に以下へ集中した。これはLayer 4 KPIではなく、保存済みcase resultを使った補助観測である。

| case | Candidate1 | Candidate5 | C5 - C1 |
| --- | ---: | ---: | ---: |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 549,123 | 978,822 | +429,699 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 348,757 | 539,593 | +190,836 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 167,566 | 258,506 | +90,940 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 345,031 | 427,131 | +82,100 |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 259,140 | 317,484 | +58,344 |

個別case名をprompt ruleへ持ち込まず、複数の実装・独立確認経路に共通するcontext処理を次の変更対象とする。

## 次candidateの設計方向

次candidateはCandidate5を直接のprompt parentとし、目的をmodel-visible contextの重複削減に限定する。

変更候補は以下である。

1. 親が常に長い正本文書全体を読むのではなく、固定済み作業単位とselected routeに必要な節だけを参照できるindexを用意する。
2. Audit / Reviewへ渡す情報は現在の分離条件を維持し、同じauthority、routing定義、経緯説明を重複して投影しない。
3. 最終出力は、固定済み定義の再掲を避け、選択値、直接根拠、validation、drift、停止指摘 / 重大指摘だけを返す。
4. prompt bundle内の同義説明を統合し、`AGENTS.md`、正本、guide、role promptの責務境界を崩さずにmodel-visibleな重複を減らす。

この方向で維持する不変条件は以下である。

- 実装主体は親直接 / SA委任 / 分担からモデルが選ぶ。
- Audit / Reviewの4 route、risk taxonomy、独立性、起動順序を変更しない。
- Candidate5の完了志向と、停止条件を観測事実へ結び付ける原則を変更しない。
- required validation、permission、allowed / forbidden path、drift確認を弱めない。
- case ID、fixture、既知の失敗文言に固有の例外を追加しない。
- Evaluation set、quality rating、KPI、評価基盤v3の固定点を変更しない。

## 次の比較単位

次candidateを作る場合は、prompt変更をcontext効率化だけに限定し、Candidate5と同じexpanded 12 case、`N=5`、`M=24`条件で独立resultを保存する。比較viewでは3 KPI、quality score分布、selected route、実装主体、worker起動数を観測するが、閾値、winner、採用判断は評価基盤へ追加しない。

Candidate5の一次結果は[`evaluations/results/candidate5-expanded12-global-m24-n5_2026-07-16.md`](../evaluations/results/candidate5-expanded12-global-m24-n5_2026-07-16.md)、6-result比較viewは[`evaluations/results/baseline-candidate1-candidate2-candidate3-candidate4-candidate5-expanded12-global-m24-n5_2026-07-16.md`](../evaluations/results/baseline-candidate1-candidate2-candidate3-candidate4-candidate5-expanded12-global-m24-n5_2026-07-16.md)に置く。
