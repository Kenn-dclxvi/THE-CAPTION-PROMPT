# Candidate73 terminal closure preserving compression設計記録

## 結論

Candidate73はCandidate71を直接sourceとし、root `AGENTS.md`の`VALIDATION_CLOSURE`一行だけを、terminal closureの機能を残した短い表現へ置換する。

Candidate72は継承しない。他の10 label、TaskSpec、permission、required validation、executor parameter、rating contractは変更しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-closure-r1`（Candidate71）とする。最短正常経路は、artifact変更後にrequired validation全件を同一model stepから発行し、全result成功後は追加read / validationなしでterminalを判断する経路である。
2. Candidate72のF06はrequired pytestを同時発行したが、その前にdiffを単独受領し、全成功後に最終行を追加readした。編集後model再入中央値はCandidate71の`2`から`3`、token中央値は`157,863`から`198,552`へ増えた。
3. TaskSpecとCandidate71の他labelだけでは、required validationを同時発行した後に追加readせずterminalへ進むことを固定しない。Candidate72はOPEN/CLOSEDという抽象だけではterminal closureを保持できないことを示した。
4. 置換する一つのpredicateは、Candidate71の`VALIDATION_CLOSURE`が持つ次の四機能を一行で保持する条件である。入口の完全性、個別invocationの同時発行、全成功後の追加readなしterminal、欠落・失敗・unexpected時のnonterminalである。
5. 消すのは`validation_set_ready`という補助変数、`=true`の再記述、`bind済み`の反復、`TaskSpec-required`の重複だけである。required validation identity、command、pass / stop condition、result有効性、非適用域は消さない。
6. 新しいlabelと判断点は追加しない。Candidate71と同じ適用域を、同じ一行・同じlabel順で表面圧縮する。
7. F06は正の適用例、F05はartifact変更なし、A01は未固定仕様、A02はauthority探索中と編集後の境界を確認する。既存`the-caption-closure-abstraction-targeted4-r1`を各5回使用する。
8. Candidate71比でF06の編集後model再入中央値`2`、20 runのquality、all-agent `total_tokens`、`elapsed_seconds`、required validation、root-onlyを維持することを期待する。prompt byte削減自体をKPI改善としない。
9. 実質的な品質低下、required validation欠落、F06編集後model再入増加、全成功後の追加read、A01確認前edit / test、A02 authority確定前batch、不要worker、またはall-agent token増加を観測した場合は停止する。結果後に補助文を追加しない。

九項目を定義済みであるため、Candidate73 bundleと対象4項目profileを作成できる。

## 変更する一行

```text
- VALIDATION_CLOSURE: artifact変更後、TaskSpec-required validationのidentity / command / pass / stop conditionが全件確定した場合だけ、各validationを個別invocationとして同一model stepで発行し、全resultを一度だけ受領する。全件successかつresult有効で追加要求がなければ、追加read / validationなしでterminalを判断する。欠落 / non-success / unexpected stateはnonterminalとする。探索 / 変更前 / review / 未固定method / recoveryには適用しない。
```

Candidate73の構築、対象試験、標準14項目、B18、採用、release、本体反映は別状態として扱う。

## 対象試験結果

Candidate73を`the-caption-closure-abstraction-targeted4-r1`のF06、F05、A01、A02で各5回実行した。20 / 20件がvalid・rateable・score `4`で、required validation欠落、workspace drift、command protocol違反、child sessionは0件だった。

保存resultの中央値では、Candidate71比で`quality_score`は同じ、all-agent `total_tokens`は`552,025 -> 534,349`、`elapsed_seconds`は`265.696秒 -> 243.610秒`だった。一方、20 run token合計は`2,737,443 -> 2,943,149`へ増えた。

F06では、全成功後の追加read / validationは観測しなかった。しかし編集後agent message中央値は`2 -> 3`だった。3 / 5 runが編集後に3回modelへ再入し、そのうち2 runは全criterion成功を述べた後に、toolを追加実行せず完了説明をもう一度生成した。残る1 runは集約出力に構造化exit codeがなく、定義どおりnonterminalとしてrequired pytestを再実行した。

terminal closureのtool境界は保持したが、事前gate 9の「F06編集後model再入増加」に該当する。Candidate73を`targeted_evaluated / stopped`とし、補助文の追加、標準14項目、B18、採用、release、本体反映へ進めない。
