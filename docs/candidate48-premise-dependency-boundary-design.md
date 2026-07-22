# Candidate48 前提依存境界の設計記録

## 位置付け

Candidate48はCandidate47を直接sourceとし、先行premiseへ依存するjudgmentを、そのpremiseがterminal inputになる前に独立operationとして分散しない境界を追加する候補である。

変更対象はroot `AGENTS.md`への`DEPENDENCY`追加だけとする。Candidate47の適用域境界を維持し、worker数、担当file、tool、読取り順、探索深度、実行順序は固定しない。未解決5の`TERMINAL`は変更しない。

Candidate47の停止条件は、rootのauthority再取得とnested waveを観測したため発動した。Candidate48は、その観測を受けてuserが明示的に指定した未解決2だけを再検討するものであり、Candidate47の採用、release、本体反映へ進めるものではない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-applicability-domain-boundary-r1`（Candidate47）とする。最短正常経路は、required outcomeに共通するpremiseを担当producerがterminal resultとして成立させ、そのpremiseへ依存するjudgmentだけがresultを入力として受け、各producerが対象固有の未解決predicateを判定する経路である。共通premiseへ依存しないjudgmentと、premise成立に必要な独立evidence取得は並行できる。
2. 保存済みA06のCandidate47 strict traceでは、rootがauthorityの適用関係を担当すると宣言しながら`authority_adr` producerを起動し、そのterminal result前にrootもReferenceとADRを読んだ。同時に17 workerを起動し、初期inventoryは深さ4まで再分割された。共通authority premiseがterminal inputになる前に、それへ依存するjudgmentを独立operationとして分散した経路を一つの誤経路とする。
3. TaskSpec、repository authority、repository stateは正しいpremiseとjudgmentを制約するが、先行premiseへ依存するjudgmentが独立operationとして成立する時点を定めない。既存`PRODUCER`は一つのjudgment resultの成立責任を定め、`CONTEXT`は解決済みpremiseの適用域を定めるが、premise解決前の依存関係を閉じない。
4. 追加する一つのpredicateは、先行premiseに依存するjudgmentは、そのpremiseのterminal resultが入力へbindされるまで独立operationとして成立しないという依存境界である。
5. このpredicateは、同じ共通premiseをrootと別producerが並行して解決する経路、および依存producerがtask definitionを再構成するために共通authorityを再取得するcontext伝播を消す。独立evidence、対象固有の実装確認、反証、新対象の探索は消さない。
6. 新たに必要になる判断は、あるjudgmentが先行premiseへ依存するかという一つだけである。packet field、worker数、tool、読取り回数、固定順序、探索深度の条件は追加しない。
7. 成果はA06の最終監査について、適用authority、到達可能な不適合、重大な見落とし、既知false positive、現物適合性と製造履歴の分離、no-driftで確認する。Candidate47が報告した主要finding、Web Editor、週次経路を観測し、blind ratingがないためscore `4`を公式値として保存しない。
8. 想定する実行変化は、共通premiseのproducerと依存producerの責任重複、task-definition再探索、全履歴継承、nested depth、thread-limit失敗、child input token、tool call、model stepが減ることである。worker数または経過時間の減少だけを成功としない。
9. 主要findingを失った場合、既知false positiveを採用した場合、独立evidence取得まで直列化した場合、terminal premiseを受けた後も同じtask definitionを再解決した場合、または依存判定のための新しいworkerやauthority再読が増えた場合は、未解決5または別candidateへ進まず、この境界を再検討する。

## 変更単位

Candidate47のroot `AGENTS.md`へ、次の一文だけを追加する。

```text
DEPENDENCY: 先行premiseに依存するjudgmentは、そのpremiseのterminal resultが入力へbindされるまで独立operationとして成立しない。
```

既存`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`METHOD`、`RECOVERY`は変更しない。
