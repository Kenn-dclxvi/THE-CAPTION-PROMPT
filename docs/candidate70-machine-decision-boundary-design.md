# Candidate70 machine decision boundary設計記録

## 結論

Candidate70はCandidate69を直接sourceとし、root `AGENTS.md`へ`MACHINE_BOUNDARY`を一つ追加する。

この制御はpromptの文字数を減らさない。Candidate69 B18に残ったall-agent `total_tokens`と`elapsed_seconds`の両方に結び付くmodel再入を対象とする。

変更するのはAGENTS.mdだけである。評価runner、executor parameter、TaskSpec、repository authority、permission、required command、command evidence protocolは変更しない。

## Candidate69 B18から確認した対象

Candidate69の標準14項目18 Batch、1,260 runは、all-agent `total_tokens = 260,811,498`、top-level tool call `9,040`だった。Candidate43比ではtoken合計`-13.00%`、tool call `-15.29%`だった一方、shell commandは`+1.54%`、90反復全体のelapsed中央値は`+2.84%`だった。

Candidate69内でcaseごとの平均を差し引いたrun間比較では、all-agent tokenとtop-level tool callのPearson相関は`0.9185`だった。編集を行った810 runでは、編集後tool callとall-agent tokenの相関は`0.8143`、elapsedとの相関は`0.4469`だった。単回帰の記述値は、編集後tool call一回当たり`+36,131 tokens`、`+5.85秒`だった。これは因果効果の推定値ではなく、制御対象を選ぶためのtrace診断である。

保存済みF06 traceには、発行するcommand集合が同じままmodel再入数が異なる経路がある。

| 経路 | run | `exec_command` invocation | top-level tool call | all-agent tokens | elapsed |
| --- | --- | ---: | ---: | ---: | ---: |
| 低cycle | `6d62a8f493cc4bb1a70f8164a198e5bd` | 18 | 9 | 274,229 | 138.4秒 |
| 高cycle | `f0fad420eaf54773a559aa619e90840d` | 18 | 22 | 578,340 | 174.0秒 |

高cycle runは、対象test成功後にmodelへ戻り、`git status`を再確認してから全testを発行した。全test成功後も、差分確認を複数のmodel stepへ分けた。F06 TaskSpecはrequired commandと停止条件を固定するが、bind済みmachine resultだけで後続発行または停止が一意に決まる区間をmodelへ戻さず処理するかどうかは固定しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-model-reentry-decision-boundary-r1`（Candidate69）とする。最短正常経路は、target、permission、method、stop conditionが固定済みで、直前のbind済み`machine_result`だけで後続または停止が一意に決まる場合、各commandを個別 invocationとして同一tool invocation内で実行し、最初の非successまたは全success後に一度だけmodelへresultを返す経路である。
2. 保存済み誤経路はF06高cycle run `f0fad420eaf54773a559aa619e90840d`である。18 `exec_command` invocationを22 top-level tool callへ分け、all-agent tokenは`578,340`、elapsedは`174.0秒`だった。
3. TaskSpec、repository authority、repository stateはrequired command、許可path、成功条件、停止条件を固定する。一方、bind済みexit codeだけで次が一意な場合にもmodelへ戻って残作業を再判断するかどうかは固定しない。Candidate69の`DECISION_BOUNDARY`はstop conditionを変え得るresultをdecision boundaryにするため、このmachine-only分岐にもmodel再入を残す。
4. `machine_result`はstructured exit code、status、booleanと定義する。追加する一つの不変条件は、`machine_boundary := decision_boundary ∧ bind済みmachine_resultだけで後続invocationまたはstopが一意 ∧ 後続のidentity / command / permission / stop conditionが発行前にbind済み`である。
5. 消す判断点は、成功したcheckout確認、required command、diff check、変更path確認を一件受領するたびに、変更されていない後続identity、command、permission、stop conditionをmodelが再展開する中間判断である。command、structured exit、失敗result、terminal判定は消さない。
6. 新たに増えるのは`MACHINE_BOUNDARY`一labelと、decision boundaryがmachine-onlyかという一判断である。case名、task種別、read-only条件、固定path、並列実行、shell command結合は追加しない。target、permission、method、recoveryの意味判断が残るresultはmachine boundaryにしない。
7. 成果品質はF04、F06、F07 canonicalを正のcase、A02を非trigger caseとして、第11版quality rating、各`N=5`で確認する。Candidate70は20 / 20 valid・rateable・score `4`、zero drift、required command protocol違反0を次の検討条件とする。A02はcanonical target確定前のmachine boundary適用0を要求する。
8. 期待する変化は、required commandとevidenceを維持したまま、正の3 caseの編集後top-level tool call、token count event、all-agent `total_tokens`、`elapsed_seconds`をCandidate69より減らすことである。全caseはroot-onlyを維持する。prompt byte数を効果判定へ使わない。
9. score `4`以外、required commandまたはevidenceの欠落、command結合によるstructured exit喪失、A02でcanonical target確定前の適用、worker routing、zero drift不成立のいずれかがあれば停止する。正の3 caseで編集後tool callまたはall-agent tokenがCandidate69より減らない場合も停止する。elapsedが減らない場合は時間短縮を主張せず、同時間帯の追加反復前に原因を再診断する。

九項目を定義済みであるため、Candidate70のbundle、Candidate69 / Candidate70 targeted profile、構造testを作成できる。

Candidate70の構築、評価、採用、release、本体反映は別状態とする。

## 構築と評価の結果

Candidate70をCandidate69の直接childとして構築した。

- prompt identity: `the-caption-3ce91a4-machine-decision-boundary-r1`
- bundle SHA-256: `65397c3b2a589d5de37e7d616cfc620d36fda32a4a6b33fbb0f53c3da3b0f840`
- changed target: root `AGENTS.md`だけ
- label: Candidate69の10 labelを逐語一致で保持し、`MACHINE_BOUNDARY`一labelだけを追加
- profile: C69 / C70とも対象4項目、各`N=5`、`M=24`、第11版quality ratingへ固定し、両profile差をprompt identityだけに限定
- targeted Layer 1 identity: `1d438e885f5300bc177b3409a14044e206199c1e23a114f9b2d3f2ac3a17e8c5`
- comparison conditions SHA-256: `8433bcac8fbc98cb2ff27ae56d1194d983af937594b18abe044dde9e900e3d7b`

Candidate70構造testは`6 passed`、全repository testは`255 passed, 132 subtests passed`だった。

初回の各20 runは、容量確保時に削除したnpm cacheの不足でF04の`npm ci`が両promptとも5 / 5失敗した。初回resultはappend-onlyの環境診断として保持し、quality gateの判定には使わない。C43以前のraw runとC41診断生成物を削除し、同一F04 lockfileからローカルnpm cacheを復元した。外部volumeは使っていない。

復元後にC69 / C70を同時刻、同一条件で各20 run再実行した。40 / 40がvalid・rateable、root-only、zero drift、command protocol違反0だった。C69は20 / 20 score `4`、C70の公式scoreは`4 / 3 = 19 / 1`だった。

C70のscore `3`はA02 iteration 1である。保存済みtraceには`'bash' '-n' 'run.sh'`と`'git' 'diff' '--check'`がいずれもexit 0で存在する。一方、固定auditは引用符を除去せず連続文字列`bash -n run.sh`と`git diff --check`を探すため、2 commandを認識しなかった。これは成果欠落ではなく採点偽陰性であるが、公式resultは変更しない。

登録済みcomparison viewの中央値はC70 - C69で、`quality_score = 0.0`、all-agent `total_tokens = -319,714`、`elapsed_seconds = -19.116秒`だった。20 run token合計は`6,884,512 -> 5,540,899`、`-1,343,613`、`-19.52%`である。正の3 case合計のtop-level tool callは`153 -> 125`、token count eventは`168 -> 140`だった。

ただしF06単独ではtop-level tool callが`39 -> 49`、all-agent token合計が`1,352,287 -> 1,625,042`、`+20.17%`、elapsed合計が`602.230 -> 654.645秒`、`+8.70%`だった。F07の大幅減少が全体差を作っており、machine boundaryの効果は正のcase間で安定していない。

## 標準14項目の追加結果

事前gateは不通過だったが、ユーザー指定の診断としてCandidate70を標準14項目、各`N=5`で実行した。Candidate69は再実行せず、第10版採点条件の保存済み正本resultを比較に使った。両resultのcompatibility keyは`4948b6b613f3d5a809774ba29fa5cc82d0244fd6e1340e618b7b5f5abfaf6236`で一致した。

Candidate70は70 / 70 valid・rateable・root-only・score `4`、zero drift、required command protocol違反0だった。Candidate70からCandidate69を引いたKPI中央値差は、quality `0.000`、all-agent token `-278,878`、elapsed `+7.058秒`である。70 run token合計は`-14.86%`、elapsed合計は`+2.20%`だった。

top-level tool callは`469 -> 392`、model stepは`539 -> 462`へ減った。一方、shell commandは`689 -> 753`へ増えた。token合計は14 case中12 caseで減ったが、A01は`+4.03%`、F06は`+1.69%`だった。elapsed中央値は7 caseで減り、7 caseで増えた。

Candidate69 B18はCandidate43比でtoken合計`-13.00%`、tool call`-15.29%`だった一方、elapsed中央値は`+4.12%`だった。今回もtokenとtool callは減り、elapsedは減らなかった。machine boundaryをall-agent tokenの制御候補として保持できるが、処理時間短縮の制御とは判断しない。

## 標準14項目B18の追加結果

ユーザー指定の長期診断として、Candidate70を標準14項目、各`N=5`、18 Batch、合計1,260 runで実行した。Candidate69は再実行せず、同じ互換条件の保存済みB18を比較に使った。Candidate70は1,260 / 1,260 valid・rateable、除外0、command protocol違反0、workspace drift 0だった。18 resultはすべて登録・圧縮済みである。

Candidate70はCandidate69比で、18結果token中央値`-18.64%`、1,260 run token合計`-16.52%`、18結果elapsed中央値`-9.47%`、elapsed合計`-9.16%`だった。token合計は18 / 18 Batch、14 / 14 caseで小さく、elapsed中央値も18 / 18 Batchで小さかった。N=5で観測した時間増加はB18で再現せず、token削減と時間増加の固定的なtrade-offは確認しなかった。

top-level tool callは`9,040 -> 7,285`、model stepは`10,311 -> 8,550`へ減った。一方、shell commandは`12,691 -> 13,077`へ増えた。A02は`880 -> 1,198`へ増えたのに、2 runで必須の`git diff --check`を省略した。F02の1 runでは子sessionを1件起動し、Candidate69のroot-onlyも維持しなかった。

公式点数は`4 / 3 / 2 = 1,250 / 9 / 1`だった。trace確認ではA02の5件とF10の1件を採点偽陰性と判断した。一方、A02の2件は必須validationを実際に欠き、F10の2件はfinding位置を1行誤った。実質分布は`4 / 3 = 1,256 / 4`であり、既知偽陰性を除いたCandidate69の`1,259 / 1`より低い。

B18はtokenと時間の長期条件を通過したが、実質的な品質後退なし、不要command増加なし、worker routing維持の採用条件を満たさない。効率値だけで停止状態を変更しない。

## 現在の状態

Candidate70は`standard14_evaluated / stopped`とする。

対象4 caseの事前gate不通過は変更しない。B18ではtokenと時間の両方が改善したが、実質的な品質後退4件、A02のcommand増加、root-only非維持が残る。Candidate70へ補助predicateを追加せず、採用、release、本体反映へ進めない。

## Evidence

- [Candidate69 B18](../evaluations/results/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-continuous-n5-b18_2026-07-22.md)
- [Candidate69設計記録](candidate69-model-reentry-decision-boundary-design.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [F06 TaskSpec](../evaluations/cases/TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r2/trial-prompt-input.json)
- [C69 / C70対象4項目結果](../evaluations/results/candidate69-candidate70-machine-decision-boundary-targeted4-n5_2026-07-22.md)
- [C69 / C70標準14項目結果](../evaluations/results/candidate69-candidate70-machine-decision-boundary-v10-standard14-n5_2026-07-22.md)
- [C69 / C70標準14項目B18結果](../evaluations/results/candidate69-candidate70-machine-decision-boundary-v10-standard14-continuous-n5-b18_2026-07-22.md)
