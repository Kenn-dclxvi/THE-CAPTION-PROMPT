# Candidate69 model reentry decision boundary設計記録

## 結論

Candidate69はCandidate43を直接sourceとし、root `AGENTS.md`へ`DECISION_BOUNDARY`を一つ追加する。

この制御はpromptの文字数を減らさない。保存済みC43 traceでall-agent `total_tokens`と強く結び付いたtop-level tool cycleを減らすため、未発行invocationの選択を変えない既知の相互非依存invocationを、一つのmodel stepへまとめる。

`FIXED_READ`のようにtask種別やread-onlyを条件にしない。A02のauthority探索のように、受領resultが次のtarget、permission、method、stop conditionを変え得る区間はdecision boundaryとして逐次判断を残す。

## C43実traceから確認した対象

Candidate43標準14項目を18 batch、各`N=5`で実行した1,260 runは、all-agent `total_tokens`が`299,794,375`だった。内訳はinput `295,873,337`、output `3,921,038`で、inputが`98.69%`を占めた。child session由来は一件、`74,965 tokens`、全体の`0.025%`だった。

同一caseの中央値を差し引いたrun間比較では、all-agent tokenとのPearson相関はtop-level tool call `0.9148`、reasoning item `0.7237`、shell command数`0.2357`、required validation command数`0.0389`だった。command自体を減らすより、commandやreadの間でmodelへ戻る回数を減らす方が観測値へ直接対応する。

保存済みtraceには、shell command数とtool output量が近いままtool cycleだけが大きく異なる経路がある。

| case | run | shell command | tool call | tool output chars | all-agent tokens |
| --- | --- | ---: | ---: | ---: | ---: |
| F08 高cycle | `1bf2a0b4448541bebab8c09787f572ef` | 17 | 23 | 32,896 | 556,770 |
| F08 低cycle | `5ffceeda81ed4fb2aaa3ae4bf0de8791` | 17 | 5 | 36,644 | 119,158 |
| F10 monthly 高cycle | `27ca8fcf89934e519eab69de0aff97e9` | 10 | 15 | 27,815 | 330,270 |
| F10 monthly 低cycle | `ba109473fca34424b8dc6781b6c8a1ed` | 10 | 3 | 26,591 | 77,453 |

これらは必要なcommandやevidenceを省略する制御ではなく、既知の作業を何回のmodel stepへ分けるかを制御対象にする根拠である。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。最短正常経路は、TaskSpec、repository authority、repository stateから現時点で実行可能と分かる相互非依存invocationを一度に発行し、全resultを受領してから一度だけ次のinvocationまたはterminalを判断する経路である。
2. 保存済み誤経路はF08高cycle run `1bf2a0b4448541bebab8c09787f572ef`である。低cycle runと同じ17 shell command、近いtool output量でrequired outcomeを成立させたが、既知のread、edit、validation、diffを23 top-level tool callへ分割し、all-agent tokenは`556,770`だった。
3. TaskSpecはoutcome、permission、validation、停止条件を固定し、repository authorityとstateは正しい対象を制約する。一方、既知の相互非依存invocationのresultを個別に受領して、その都度同じ残作業を再判断するかどうかは固定しない。Candidate43の`METHOD`も手段選択とfailure fallbackを扱うだけで、model再入境界を定めない。
4. 追加する一つのpredicateは、`decision_boundary := 受領resultが未発行invocationのtarget / permission / method / stop conditionを変え得る`である。decision boundaryを持たない既知の相互非依存invocationは、分割せず同一model stepで発行する。
5. 消す判断点は、既知の独立read、validation、diffを一件受領するたびに、変更されていない残りのtarget、permission、method、stop conditionを再展開する中間判断である。必要なcommand、evidence、predicate判定、terminal判定は消さない。
6. 新たに増えるのは`DECISION_BOUNDARY`一labelと、未発行invocationの選択がresultで変わり得るかという一判断である。task種別、case label、read-only、対象file列挙、例外routeは追加しない。A02ではcanonical targetが解決するまでdecision boundaryが成立し、逐次探索を維持する。
7. 成果品質はCandidate43と同じ標準14項目、第10版quality rating、各`N=5`で判定する。70 / 70 valid・rateable、全件score `4`、zero driftを次の検討条件とする。単独caseや局所probeだけで判断しない。
8. 期待する変化は、shell commandとrequired evidenceを維持したままtop-level tool call、reasoning item、token_count event、all-agent `total_tokens`を減らすことである。A / Fはroot-onlyを維持する。3 KPIの`quality_score`、`total_tokens`、`elapsed_seconds`を省略しない。
9. score `4`以外、required commandまたはevidenceの欠落、A02でcanonical target確定前の探索batch、worker routing増加、zero drift不成立のいずれかがあれば停止する。品質を維持してもtool cycleとall-agent tokenの方向がC43より減らない場合、説明文を追加せずprompt制御として停止し、次はexecutor側の機械的なdependency materializationを別scopeで検討する。

九項目を定義済みであるため、Candidate69のbundle、標準14 profile、構造testを作成できる。構造testに合格した後だけ実行を開始する。

Candidate69の構築、評価、採用、release、本体反映は別状態とする。

## 構築結果

Candidate69をCandidate43の直接childとして構築した。

- prompt identity: `the-caption-3ce91a4-model-reentry-decision-boundary-r1`
- bundle SHA-256: `76e6c86fa4cf107ee660d79598e034c384545935982da4983f65d67f65423e87`
- changed target: root `AGENTS.md`だけ
- root bytes: `3,980 -> 4,291`、`+311`、`+7.81%`
- label: Candidate43の9 labelを逐語一致で保持し、`DECISION_BOUNDARY`一labelだけを追加
- profile: Candidate43標準14 profileからidentityだけを変更

構造testと全repository testは`242 passed, 132 subtests passed`だった。

## 評価結果

標準14項目各`N=5`、合計70件を実行した。70 / 70 valid・rateable、excluded attempt 0、zero drift 70 / 70だった。

- 公式score分布: Candidate43 `4 = 70`、Candidate69 `4 / 3 = 69 / 1`
- 3 KPI中央値差: quality `0.000`、all-agent token `-955,776`、elapsed `-248.598秒`
- 70件token合計: `17,732,662 -> 13,726,510`、`-22.59%`
- top-level tool call: `639 -> 469`、`-26.60%`
- reasoning item: `548 -> 499`、`-8.94%`
- token_count event: `710 -> 539`、`-24.08%`
- shell command: `705 -> 689`、`-2.27%`
- A02: 5 / 5 score `4`、canonical target確定前の探索batchなし

score `3`はF10 monthlyのfinding locationを`monthly_main.py:24`と返し、期待する`:25`に一致しなかった一件である。finding内容と影響分析は成立していたが、行番号付きsource確認を行わなかった。

## 状態

Candidate69は`standard14_evaluated / stopped`とする。事前gateの全70件score `4`を満たさなかったため、結果後に基準を変更して通過扱いにしない。

一方、prompt bytesが`+7.81%`増えた状態でtool callとinput tokenが約23〜27%減り、tokenとelapsedも5 / 5反復でCandidate43より小さかった。model再入境界は、AGENTS.md使用tokenではなく実all-agent `total_tokens`へ結び付く制御対象として保持する。

Candidate69へ補助説明を追加しない。次へ進む場合は、global proseを増やすのではなく、executor側でdependencyとterminal evidence addressを機械的にmaterializeする別scopeとして検討する。詳細は[`Candidate43 / Candidate69標準14 N=5`](../evaluations/results/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-n5_2026-07-22.md)を正本とする。

## Evidence

- [Candidate43標準14 continuous N=5 B18](../evaluations/results/candidate43-outcome-authority-boundary-v10-standard14-continuous-n5-b18_2026-07-20.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
