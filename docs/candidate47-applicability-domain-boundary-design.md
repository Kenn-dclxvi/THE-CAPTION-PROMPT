# Candidate47 適用域境界の設計記録

## 位置付け

Candidate47はCandidate46を直接sourceとし、解決済みpremiseの適用域を対象の列挙ではなく、required outcomeとの関係を判定する適用predicateと、result成立に必要なevidence conditionで閉じる候補である。

変更対象は`CONTEXT`と`ROOT`だけとする。worker数、担当file、tool、読取り順、探索深度は固定しない。新しい対象の探索も禁止しない。

Candidate47の作成、A06診断、採用、release、本体反映は別状態として扱う。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-resolved-premise-input-boundary-r1`（Candidate46）とする。最短正常経路は、rootがrequired outcomeに対する適用predicateとevidence conditionを解決済みpremiseとして固定し、producerが発見した対象をその条件で判定し、rootがterminal resultを再探索なしでadmitする経路である。
2. 保存済みA06のCandidate46 strict traceでは、authority本文の再取得は減ったが、scope membershipの列挙は収束しなかった。`rg --files`の参照sessionは`30 → 40`、workerは`31 → 42`へ増え、rootは高重要度候補へ8本の独立反証workerを追加した。最終報告は週次legacy ledger依存を含めず、Web Editor findingを適用scope不明として主結論から除外した。
3. TaskSpec、repository authority、repository stateは、対象ごとの適否と証拠を制約する。しかし、新しく見つかった対象を既存の適用基準で判定する場合と、その適用基準自体を変更しなければ判定できない場合を区別しない。そのため、新しい対象が見つかるたびにscopeを再解決する経路と、十分なproducer resultへ確信を追加するための別検証経路を防げない。
4. 置換する一つのpredicateは、解決済みpremiseの適用predicateとevidence conditionで判定できる新しい対象または証拠を同じ適用域の入力として扱い、その条件自体を変更する反証だけでpremiseを再開する境界である。
5. このpredicateは、新しい対象ごとのscope再解決、同じevidence conditionを満たしたresultへの確信追加だけを目的とする別検証、および対象列挙を完了条件とするcontext伝播を消す。新しい対象の探索、既存条件による判定、条件を変更する反証の報告は消さない。
6. 新たに必要になる判断は、観測した対象または証拠を既存の適用predicateとevidence conditionで判定できるか、その条件自体の変更が必要かという一つの区別である。新しいlabel、packet field、worker数制限、tool制限は追加しない。
7. 成果はA06の最終監査について、適用authority、到達可能な不適合、重大な見落とし、既知false positive、現物適合性と製造履歴の分離、no-driftで確認する。Candidate46が報告した主要findingに加え、週次legacy ledger依存とWeb Editorの到達可能な挙動を既存の適用predicateで判定できるかを観測する。blind ratingがないため、score `4`は公式値として保存しない。
8. 想定する実行変化は、広い対象探索を維持しつつ、新対象ごとのscope再解決、rootの確信追加validator、同じ適用域を再列挙するnested operation、child token、tool call、model step、durationが減ることである。worker数やtokenの減少だけを成功としない。
9. 主要findingを失った場合、既知false positiveを採用した場合、Web Editorまたは週次処理を探索抑止によって見落とした場合、rootのauthority再取得が再発した場合、または適用predicateとevidence conditionの判定自体が新しいworker waveを生んだ場合は、追加candidateへ進まず境界を再検討する。

## 変更単位

Candidate46のroot `AGENTS.md`だけを変更する。

- `CONTEXT`を、不足、失効、矛盾、または新しい対象範囲を一律に別resultとする境界から、既存の適用predicateとevidence conditionで判定できる対象を同じ適用域の入力として扱う境界へ置換する。
- `ROOT`を、不足またはscope extensionを別resultとする境界から、既存の適用predicateとevidence conditionを満たすresultを追加探索なしでadmitし、その条件自体を変える反証だけをpremise再解決へ送る境界へ置換する。

二つの文面変更は、解決済みpremiseの適用域を判定基準で閉じる一つのpredicateを表す。`SPEC`、`PRODUCER`、`TERMINAL`、`OWNER_ROLE`、`METHOD`、`RECOVERY`は変更しない。
