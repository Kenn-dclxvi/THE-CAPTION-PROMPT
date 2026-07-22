# Candidate71 validation closure設計記録

## 結論

Candidate71はCandidate69を直接sourceとし、root `AGENTS.md`へ`VALIDATION_CLOSURE`を一つ追加する。

Candidate70の`MACHINE_BOUNDARY`は継承しない。対象を、artifact変更が完了し、TaskSpec-required validationの完全な集合が発行前に確定した検証段階だけへ限定する。

変更するのはroot `AGENTS.md`だけである。評価runner、executor parameter、TaskSpec、permission、required command、command evidence protocolは変更しない。

## 保存済み結果から確認した対象

Candidate70 B18はCandidate69比で、all-agent `total_tokens`合計`-16.52%`、`elapsed_seconds`合計`-9.16%`、top-level tool call`-19.41%`、model step`-17.08%`だった。model再入を減らす方向はtokenと時間の両方に対応した。

一方、Candidate70のA02はshell commandが`880 -> 1,198`へ増え、2 runでTaskSpec-required validationの`git diff --check`を欠いた。広いmachine boundaryは、検証集合の完全性を入口条件にせず、探索や意味判断を含むoperationへ適用範囲を広げた。

同じ1,260組のC70 - C69差では、top-level tool call差とall-agent token差のPearson相関は`0.911`、elapsed差との相関は`0.593`だった。shell command差との相関はそれぞれ`0.172`、`0.278`である。減らす対象はrequired command数ではなく、完全に確定したvalidation間のmodel再入とする。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-model-reentry-decision-boundary-r1`（Candidate69）とする。最短正常経路は、artifact変更後にTaskSpec-required validationの完全な集合を一度だけ確定し、各commandを個別invocationとして同じmodel stepから発行し、全result受領後に一度だけterminalまたは継続を判断する経路である。
2. 保存済み誤経路はCandidate70 B18のA02である。全体ではmodel stepを減らしたが、2 runで`git diff --check`を欠き、同caseのshell commandを318件増やした。検証集合の完全性を固定しない広いmachine boundaryは、必要なvalidationを保った収束にならなかった。
3. TaskSpecはrequired validationと成功条件を固定する。Candidate69の`DECISION_BOUNDARY`は独立invocationの分割を抑える。一方、artifact変更後に全required validationを完全な一集合としてbindしてから発行することと、全件成功後に追加readまたは再validationを開始しないことは固定しない。
4. 追加する一つのpredicateは、`validation_set_ready := artifact変更完了 ∧ TaskSpec-required validationのidentity / command / individual pass condition / stop conditionが全件bind済み`である。成立時だけ全validationを個別invocationとして同一model stepから発行し、全resultを一度だけmodelへ返す。
5. 消す判断点は、成功したrequired validationを一件受領するたびに、未変更の残りvalidation、permission、stop conditionを再展開する中間判断と、全件成功後に根拠なくreadまたはvalidationを追加する判断である。required command、個別exit、failure result、unexpected diff、terminal completenessは消さない。
6. 新たに増えるのは`VALIDATION_CLOSURE`一labelと、完全なvalidation集合がbind済みかという一判断である。target探索、artifact変更前、review finding、未固定method、意味判断を要するrecoveryへ適用しない。case名、固定path、worker、shell command結合は追加しない。
7. 成果品質はCandidate69 / Candidate70と同じ対象4項目、第11版quality rating、各`N=5`で確認する。20 / 20 valid・rateable、実質的な品質後退0、required validation欠落0、protocol違反0、zero drift、root-onlyを必須とする。
8. F04、F06、F07 canonicalでは、Candidate69比でtop-level tool call、model step、all-agent `total_tokens`を減らすことを期待する。A02ではcanonical target確定前に適用せず、確定後は全required validationを保持する。`elapsed_seconds`は必ず記録し、減らない場合は時間短縮を主張しない。
9. required validation欠落、unexpected command増加、target探索への流入、不要worker、実質的な品質後退、または正の3 caseでtool call・model step・tokenがCandidate69から減らない場合は停止する。Candidate71へ補助predicateを追加せず、standard14、B18、採用、release、本体反映へ進めない。

九項目を定義済みであるため、Candidate71のbundle、Candidate69と同条件の対象4項目profile、構造testを作成できる。

## 変更する関係

```text
Candidate69 DECISION_BOUNDARY
  -> artifact変更完了
  -> validation_set_ready=false
       -> 通常のmodel判断を維持
  -> validation_set_ready=true
       -> required validationを個別invocationとして同一model stepから発行
       -> 全resultを一度だけmodelへ返す
       -> 全件successなら追加read / validationなしでterminal判断
       -> 欠落 / non-success / unexpected stateならnonterminal
```

Candidate71の構築、対象試験、採用、release、本体反映は別状態として扱う。

## 構築と対象試験の結果

Candidate71をCandidate69の直接childとして構築した。

- prompt identity: `the-caption-3ce91a4-validation-closure-r1`
- bundle SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- changed target: root `AGENTS.md`だけ
- label: Candidate69の10 labelを逐語一致で保持し、`VALIDATION_CLOSURE`一labelだけを追加
- profile: 保存済みCandidate69とCandidate71を対象4項目、各`N=5`、`M=24`、第11版quality ratingへ固定し、profile差をprompt identityだけに限定

Candidate71の20 runは全件valid・rateable・score `4`だった。required validation欠落、command protocol違反、workspace drift、worker起動は0件である。

保存済みCandidate69比で、all-agent `total_tokens`中央値は`1,391,860 -> 814,513`、`-41.48%`、elapsed中央値は`506.732 -> 396.946秒`、`-21.67%`だった。20 run合計はtokenが`-39.65%`、elapsedが`-19.97%`である。

正の3 case合計ではtop-level tool callが`153 -> 93`、model stepが`168 -> 108`、token合計が`-44.49%`、elapsed合計が`-20.88%`だった。F04、F06、F07 canonicalは、4指標がcase別でもすべて小さかった。

A02はrequired validationを5 / 5で保持し、変更前のvalidation流入を観測しなかった。shell commandは`47 -> 48`だったが、tool call、model step、token、elapsedはすべて小さく、増加した1 commandは探索ばらつきである。command数はKPIへ昇格させず、route failureの診断としてのみ保持する。

## 標準14項目試験の結果

保存済みCandidate69 v10と同じ標準14項目、各`N=5`、`M=24`でCandidate71を実行した。profile差は`profile_id`と`prompt_set_identity`だけであり、Candidate69は再実行していない。

Candidate71の70 runは全件valid・rateable・score `4`だった。required validation欠落、command protocol違反、workspace drift、worker起動は0件である。

Candidate69比で、all-agent `total_tokens`中央値は`2,691,522 -> 1,923,837`、`-28.52%`、elapsed中央値は`1,104.860 -> 1,031.401秒`、`-6.65%`だった。70 run合計はtokenが`-28.48%`、elapsedが`-5.59%`である。

tokenは14 case中13 case、5反復中5反復で小さかった。elapsedは14 case中10 case、5反復中4反復で小さかった。elapsedが増えた4 caseの最大値はF06の`+5.64%`であり、全体中央値と合計は削減した。

top-level tool callは`469 -> 338`、model stepは`539 -> 408`、shell commandは`689 -> 670`だった。70個の対応run差ではtool call差とtoken差のPearson相関が`0.869`、elapsed差との相関が`0.543`だった。shell command差との相関はtokenが`0.185`、elapsedが`0.276`であり、狙ったmodel再入削減とKPI削減が対応した。

## B18前の採点契約是正

C69 / C70の保存済み結果で、成果成功を低得点にした採点偽陰性を4パターン、11観測へ分類した。内訳は、C69 A01の「明示してください」1件、C69 / C70 F10 Monthlyの数値line mismatch 3件、C70 A02の引用符付き成功command 6件、C70 F10 Monthlyの意味的に正しい誤binding説明1件である。数値lineは第11版で診断へ分離済みである。

第12版`outcome-semantic-evidence-normalized-owner-diagnostic-v12`は、残り3パターンをsemantic evidence normalizationとして追加する。A01は確認要求の意味、A02は`exit_code=0`にbindされたshell token列、F10は二つのCLI optionと誤接続関係を採点する。疑問符、quoteの有無、`args.force`という字面だけではscoreを決めない。

C70 B18で`git diff --check`を実行しなかった2件は採点偽陰性ではない。第12版でも`a02_missing_successful_command:diff_check`としてscore `3`を維持する。既存v10 / v11 resultは変更せず、第12版のC69 / C71 profileを新しいB18 comparison identityとする。

## 現在の状態

Candidate71は`standard14_evaluated / gate_passed`とする。

対象4項目と標準14項目では、Candidate70で観測したrequired validation欠落を再現しなかった。標準14項目では品質を維持し、tokenと全体elapsedの両方を削減した。

採用、release、本体反映は未判断、未実施である。Candidate69とCandidate43の比較では、標準14項目`N=5`とB18でelapsed差の方向が反転した履歴がある。次の評価段階はCandidate69 / Candidate71の両方を新しい第12版採点へ固定した標準14項目B18とする。既存v10 / v11 resultは再採点せず、比較へ混ぜない。

## Evidence

- [Candidate69設計記録](candidate69-model-reentry-decision-boundary-design.md)
- [Candidate70設計記録](candidate70-machine-decision-boundary-design.md)
- [Candidate69 / Candidate70 B18](../evaluations/results/candidate69-candidate70-machine-decision-boundary-v10-standard14-continuous-n5-b18_2026-07-22.md)
- [Candidate69 / Candidate71対象4項目結果](../evaluations/results/candidate69-candidate71-validation-closure-targeted4-n5_2026-07-22.md)
- [Candidate69 / Candidate71標準14項目結果](../evaluations/results/candidate69-candidate71-validation-closure-v10-standard14-n5_2026-07-22.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
