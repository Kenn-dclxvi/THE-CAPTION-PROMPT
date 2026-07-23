# Candidate72 closed validation state設計記録

## 結論

Candidate72はCandidate71を直接sourceとし、root `AGENTS.md`の`VALIDATION_CLOSURE`一行だけを短いclosed-state表現へ置換する。

他の10 label、TaskSpec、permission、required validation、executor parameter、rating contractは変更しない。標準14項目やB18へ進む前に、F06、F05、A01、A02の対象4項目だけで適用域とmodel再入を確認する。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-closure-r1`（Candidate71）とする。最短正常経路は、artifact変更後にrequired validation集合が確定した場合だけ全件を同一model stepから発行し、全result受領後に一度だけterminalを判断する経路である。
2. 保存済みBatch 12 traceでは、F06の編集後model再入中央値がCandidate69からCandidate71で`4 -> 2`、A02が`3 -> 2`となった。F06 token中央値は`311,773 -> 177,460`、A02は`372,648 -> 247,354`だった。
3. F06とA02ではrequired commandを維持したまま、closed validation集合内の中間model再入だけが減った。F05は両条件とも5 / 5で同じ2 response、4 command経路であり、非validation caseのKPI差をこの制御の直接効果としない。A01はCandidate71の1 / 5で未固定仕様を早くclosedへ移したため、非適用域の保持を独立に確認する。
4. 置換する一つのpredicateは、artifact変更後にrequired validationの全commandとpass / stop conditionが確定した場合だけvalidation集合をclosedとする条件である。
5. 消す判断点は、closed集合内の各validation result受領ごとの中間判断である。required command、個別invocation、result、terminal判断は消さない。
6. 新しいlabelは追加しない。Candidate71の`VALIDATION_CLOSURE`から、同じclosed-stateを説明する重複したidentity、success、unexpected-state、追加read条件を削り、適用域と一括発行だけを残す。
7. F06は正の適用例、F05はartifact変更なしの非適用例、A01は未固定仕様のOPEN維持、A02はauthority探索中のOPENと編集後のCLOSEDを確認する。各caseを5回実行する。
8. F06とA02ではrequired validationを維持し、編集後model再入、all-agent `total_tokens`、`elapsed_seconds`がCandidate71から増えないことを期待する。F05とA01では不要なread、edit、testを増やさない。
9. 実質的な品質低下、required validation欠落、A01の確認前編集・test、A02のauthority確定前batch、不要worker、またはF06の編集後model再入増加を観測した場合は停止する。結果後に補助文を追加しない。

九項目を定義済みであるため、Candidate72 bundleと対象4項目profileを作成できる。

## 変更する一行

```text
- VALIDATION_CLOSURE: artifact変更後、TaskSpec-required validationの全commandと各pass / stop conditionが確定した場合だけvalidation集合をclosedとし、個別invocationを同一model stepで発行する。全result受領後に一度だけterminalを判断し、探索 / 変更前 / review / 未固定method / recoveryはclosedにしない。
```

Candidate72の構築、対象試験、標準14項目、B18、採用、release、本体反映は別状態として扱う。

## 構築結果

Candidate71を直接sourceとし、`VALIDATION_CLOSURE`一行だけを置換した。

- prompt identity: `the-caption-3ce91a4-closed-validation-state-r1`
- bundle SHA-256: `4e6931afd00c6281f529ebb267f9a6b8b8d0be98de1cc1b2a1a3c36bf8d3dea9`
- changed target: root `AGENTS.md`だけ
- root bytes: `4,987 -> 4,652`、`-335`、`-6.72%`
- Candidate71の他10 labelと残り18 targetは同一

構造testは3 / 3件が通過した。

## 対象4項目試験の結果

Candidate71 / Candidate72を第12版採点、F06、F05、A01、A02の各`N=5`で実行した。両条件とも20 / 20 valid・rateable・score `4`、zero drift、protocol違反0、root-onlyだった。

保存resultの中央値差はCandidate72 - Candidate71で、quality `0.000`、all-agent `total_tokens = +92,810`、`elapsed_seconds = +2.523秒`だった。20 run合計tokenは`2,737,443 -> 3,190,427`、`+16.55%`である。

F06では、Candidate71が編集後model再入中央値`2`を維持したのに対し、Candidate72は`3`へ増えた。token中央値は`157,863 -> 198,552`、token合計は`755,968 -> 1,051,125`だった。Candidate72もrequired pytestを同一model stepから発行したが、その前にdiffを一度受領し、全成功後に最終行を追加readしてからterminalにしたrunが残った。

A02の編集後model再入中央値は`3 -> 3`で、token中央値は`219,690 -> 252,895`だった。F05はCandidate72の5 / 5で2 response、4 commandを維持した。A01は両条件とも確認前のedit / testを0件に保ったが、Candidate72のmodel response中央値は`3 -> 4`だった。

全20 runのagent messageは`81 -> 92`、attempted shell commandは`136 -> 168`、failed commandは`3 -> 4`だった。required validation欠落とcommand protocol違反は0件である。

## 判定

Candidate72は`targeted_evaluated / stopped`とする。

OPEN/CLOSED抽象だけではCandidate71の効率を保持しなかった。Candidate71から削った「全required validation成功後、新要求またはresult失効がなければ追加read / validationを行わずterminalを判断する」という明示条件が、validationの同時発行だけでなく、その後のterminal closureを固定していた。

短いclosed-state表現は成果品質を維持したが、F06の編集後model再入とall-agent tokenを増やし、事前停止条件に該当した。Candidate72へ補助文を追加せず、標準14項目、B18、採用、release、本体反映へ進めない。

詳細は[`Candidate71 / Candidate72対象4項目結果`](../evaluations/results/candidate71-candidate72-closed-validation-state-v12-targeted4-n5_2026-07-23.md)へ保存する。
