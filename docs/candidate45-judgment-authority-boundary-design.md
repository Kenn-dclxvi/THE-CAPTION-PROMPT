# Candidate45 判断成立責任境界の設計記録

## 位置付け

Candidate45はCandidate43を直接sourceとし、producer制御を「同一operationを別producerへ割り当てない」という手続きから、「一つの判断結果の成立責任を同時に複数のroleへまたがせない」という境界へ置換する候補である。

Candidate44はcomplete spec readiness boundaryとして既に保存済みであるため変更しない。Candidate45の作成、A06診断、採用、release、本体反映は別状態として扱う。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。最短正常経路は、各producerが担当判断を成立させ、rootが必要なsourceを確認して各resultを採用または棄却し、採用resultから監査結論を構成する経路である。
2. 保存済みのTHE-CAPTION-DEV監査traceでは、12の初期監査workerの後に15のvalidatorが起動され、同じfindingの成立判断が別producerで再構成された。A06のCandidate43再試験ではこの段は再現しなかったが、rootによるsource確認と3件の候補棄却は有効なadmissionとして観測した。
3. TaskSpec、repository authority、repository stateは監査対象、permission、正しい製品挙動を制約するが、一つのfindingを誰の判断結果として成立させるか、およびproducer resultとroot admissionの責任分離を定めない。
4. 置換するpredicateは、各judgment resultの内容と成立根拠を確定するproducer execution identityを一つに保ち、同じ情報、対象、predicateを用いる別roleの判断を別result identityとして扱う境界である。
5. この置換は、「同じpredicateを他roleが読むこと自体を禁止するか」「rootのsource確認をpredicate再実行とみなすか」という二つの解釈判断を消す。同一resultの暗黙の共同生成だけを禁止対象として残す。
6. 新たに必要になる判断は、二つの出力が同一resultの補完なのか、独立resultまたはadmissionなのかの区別である。worker数、担当file、tool、読取り順、再検証方法は固定しない。
7. 成果はA06の最終監査について、適用authority、到達可能な不適合、重大な見落とし、既知false positive、現物適合性と製造履歴の分離、no-driftで確認する。単一runはdiagnosticであり、範囲外へ一般化しない。
8. 想定する実行変化は、rootのsource確認と採否判断を維持しつつ、同一findingを別producerが暗黙に補完または再生成する段を要求しないことである。all-agent token、tool call、model step、worker routingは固定せず観測する。
9. rootがproducer resultの不足を暗黙に補完した場合、独立確認まで抑止して重大findingを失った場合、既知false positiveを採用した場合、またはC43より判断点と再取得だけが増えた場合は、追加candidateへ進まず境界を再検討する。

## 変更単位

Candidate43のroot `AGENTS.md`だけを変更する。

- `PRODUCER`をoperation割当ての禁止からjudgment resultの成立責任境界へ置換する。
- `ROOT`をpredicate実行禁止からproducer resultに対するadmission責任へ置換する。
- 同一predicateの別producer割当てを一律禁止する`INDEPENDENCE`を削除する。

三つの文面変更は、producerとadmissionの判断責任を分離する一つの判断を表す。`SPEC`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`METHOD`、`RECOVERY`は変更しない。
