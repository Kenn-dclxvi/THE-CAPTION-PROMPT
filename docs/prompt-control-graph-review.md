# Prompt制御graph棚卸し

## 結論

F05 clarificationとF10 monthly reviewは、ControlFreeRepositoryの三層、すなわちTaskSpec、path-scoped repository authority、repository evidenceだけで最終成果まで到達できる。

C35は、operation、producer、owner、terminal、contextを結ぶ九つのlabelをrootへ持つ。C38は、このgraphへresult unit、evidence、invalidationの関係を追加した。C40はresult unitをoperation terminal resultのprojectionへ限定したが、F10の実行経路を短縮せず、正しいchild findingをowner identity不一致として省略した。

次の変更候補は、result unit条件の追加ではない。TaskSpecの`owner`語列をworker起動条件へ自動変換するC35以降の`OWNER`関係を、明示された独立実行だけを委譲条件とする一つのpredicateへ置換することである。

本書は棚卸しと変更提案までを扱う。candidate、profile、評価run、release、THE-CAPTION本体反映は作成または実施しない。

## Evidence境界

### 事実

- 基準prompt setは`the-caption-3ce91a4-control-free-repository-r1`である。root `AGENTS.md`だけが0-byteであり、`src/AGENTS.md`などのpath-scoped authorityは残る。
- ControlFreeRepositoryのexpanded 12 case N=5はscore `4 / 3 = 59 / 1`、quality中央値`100.000`だった。
- ControlFreeRepositoryのF10 entrypoint inventoryは5 / 5がscore `4`であり、各runはroot sessionだけで完了した。
- C35のroot `AGENTS.md`本文はdirect sourceであるC34と同一である。C35で変更されたのはlegacy role / process 7 targetの0-byte化である。
- root制御のdirect source chainは、ControlFreeRepository → C23 → C24 → C28 → C29 → C30 → C31 → C32 → C33 → C34 → C35である。
- C38のdirect sourceはC35である。C38は`SPEC`、`CONTEXT`、`OWNER`をresult unit単位へ変更した。
- C40のdirect sourceはC38である。C39はC40のdirect sourceではない。
- C35とC38のv9 targeted N=5は、どちらもF05 / F10の10 / 10がscore `4`だった。
- C38 - C35の10 run token合計差は`+255,767`だった。その99.34%はinput tokenであり、90.50%はF10に集中した。
- F10では、C38がC35より`exec +8`、`wait +3`、model step `+10`だった。
- C40のscore分布は`4 / 1 = 9 / 1`だった。F10のtool call、model step、token合計はC38から減らなかった。

### 推論

- F05 / F10では、TaskSpecの`owner`語列が成果生成者を指定する情報ではなく、評価上のnon-machine risk ownerとして記載されている可能性が高い。
- この語列をnon-root producerの必須指定へ変換すると、ControlFreeRepositoryでは存在しなかったworker起動、runtime identity照合、wait、root / childの重複readが生じる。
- C38 / C40のresult unit関係は、F05 / F10のTaskSpecが既に分けているrequired fieldとevidence条件をroot promptで再定義している。
- C40はresult unitとoperationを論理上分離したが、`OWNER`、`PRODUCER`、`TERMINAL`との参照関係を残したため、実行時の判断点を減らせなかった。

数値は記載したcaseと反復条件に限定する。個別labelとtoken差の決定的な因果は断定しない。

## 最短正常経路

### F05 clarification

#### 事実

| 段階 | 内容 |
| --- | --- |
| 入力 | `daily`または`strict`の選択と、`strict`時のlive CSV fallback policyが未指定である。readだけが許可され、edit、test、外部operationは禁止される。 |
| 必要なread | `pwd`、branch、`HEAD`、`git status --short`で開始identityとzero driftを確認する。TaskSpec自身が不足する2点を列挙しているため、成果生成のためのsource readは必須ではない。必要なら許可済みの`src/domain/universal_ingester.py`だけを読む。 |
| 判断 | user policyが二つ不足しているため、repositoryから既定値を推測せず実装を開始しない。 |
| terminal output | `daily` / `strict`の選択と、`strict`時にlive CSV fallbackを許可するかを一つのclarificationで質問し、single terminal outcomeとして終了する。 |

#### 推論

この経路にはoperation分割、worker起動、criterion ownerとruntime identityの照合、result unit分割が不要である。TaskSpecだけで質問内容、禁止操作、停止条件が確定しているためである。

### F10 monthly review

#### 事実

| 段階 | 内容 |
| --- | --- |
| 入力 | review対象は`a536016^..a536016`の`src/app/entrypoints/monthly_main.py`差分である。read-only review、allowed read、禁止操作、required output fieldがTaskSpecへ明記されている。 |
| 必要なread | `pwd`、branch、`HEAD`、開始`git status --short`、固定commit存在確認、root / `src/AGENTS.md`、固定diff、`monthly_main.py`、`monthly_engine.py`を読む。終了時に`git status --short`でzero driftを確認する。 |
| 判断 | 変更行の`format_test=args.force`を、parserの`args.format_test`と`MonthlyEngine`のformat-test early-returnへ照合する。`-t`が無視され、`-F`がformat-test挙動も有効にするため、behaviorへ影響するmajor findingと判断する。 |
| terminal output | `review_findings`へmajor、`src/app/entrypoints/monthly_main.py:25`、直接根拠、`-t` / `-F`へのuser-visible impactを記載し、finding countを返す。artifactは変更しない。 |

#### 推論

この経路はroot一つで完結できる。ControlFreeRepositoryのF10 entrypoint inventoryが5 / 5でrootだけにより完了した事実は、少なくともrepository authorityの読解にchildが必須ではないことを示す。ただし、monthly review r3そのもののControlFreeRepository同条件N=5は保存されていないため、root-only経路の再現性は未測定である。

## C35制御graph

C35のroot本文はC34から継承されている。表の「実測結果」は、そのpredicateを導入したdirect childの観測またはC35全体の観測であり、C35内の単独ablationではない。

| label / predicate | 入力となる状態 | 消そうとした誤経路 | 追加した判断点 | 基本三層との重複 | 実測結果 | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| `SPEC` | required outcome、criterion owner、permission、constraint | 個別commandの拒否や一つのresultを別operationまたはtask全体へ伝播し、許可済み成果を未完了停止する経路 | operation分割、operation identity、predicate binding、伝播範囲 | outcome、permission、constraintはTaskSpecと重複する。operation-localな失効範囲は一部だけ追加情報である | C23はControlFreeRepository比でF04 score `4`が1件増え、F04 token中央値`-82,794`だった。C35内での単独効果は未分離である | **提案: 置換候補。** operation identityの全面再定義を外し、個別手段の失敗をtask terminalへ伝播させない条件だけを`METHOD`側へ残す |
| `PRODUCER` | operation、criterion owner、root / worker identity | 同じpredicateをrootとworkerが重複実行する経路、worker不成立後にroot resultへ差し替える経路 | producer選択、execution identity、owner語列の正規化、producer変更時の旧binding失効 | TaskSpecはownerを持つがproducer runtime identityを定めない | C28はexpanded N=5でscore `4 / 3 = 58 / 2`だった。残る2件はowner producer不成立であり、単独で全経路を閉じなかった | **提案: `OWNER`へ統合。** 明示的に委譲したoperationだけをsingle producerへbindする。root / worker選択を全operationの事前判断にしない |
| `TERMINAL` | operation内の全predicate、producer terminal result、worker / session state | 非同期処理が継続中またはresult欠落でも、root final responseで完了を補完する経路 | 全predicate列挙、各terminal result確認、上位operationのclosure | TaskSpecのdone condition、required validationと重複する。開始済み非同期処理のnonterminal状態は追加情報である | C31 targetedは15 / 15がscore `4`だった。ただしprompt変更とcollector変更を同じcampaignで評価しており寄与率は未分離である。expanded v5は60 / 60がscore `4`だった | **提案: 狭く維持。** 「開始済みoperationがnonterminalの間は完了宣言しない」という直接記述へ置換する |
| `CONTEXT` | criterion、owner、TaskSpec範囲、target、diff / result、evidence、allowed read、forbidden input | 十分なworker packetがあるのに親の全contextを継承し、反復inputを増やす経路 | packet完全性判定、9 field確認、`fork_turns`選択、最小turn数判断 | TaskSpecとallowed readに既にある情報をpacketへ再列挙する部分がある。context流入境界自体は基本三層にない | C11のF07は必要な2 workerを維持し、10 spawnすべて`none`、C10比case token中央値`-1,009,985`だった。C33は55 spawnすべて`none`でC32比token中央値`-959,484`だったがquality中央値も低下した。C34は同境界を維持して必須responseを回復した | **提案: 狭く維持。** packetとallowed readが十分なら親履歴を継承しない。TaskSpec fieldの再定義は減らす |
| `OWNER` | criterion owner語列、spawn `task_name`、`FINAL_ANSWER.Sender`、result binding | child session / final resultなしでowner result受領を自己申告する経路、存在しないruntime fieldを要求して正しいresultを捨てる経路、criterion falseを別operationへ伝播する経路 | owner語列正規化、task identity生成、worker起動要否、runtime path照合、Sender照合、result binding、`false / failed / unavailable`分岐、失効範囲 | TaskSpecのowner語列をruntime worker必須条件へ拡張している。成果fieldと失効範囲はTaskSpec内で既に別criterionとして記載される | C24は60 / 60 owner-producer eligibleだった。C30のF10 2 caseはcontinuous 50 / 50がscore `4`だった。C34はC33のresponse欠落を回復した。一方、C40は正しいchild findingをowner identity不一致と解釈しscore `1`にした | **提案: 置換優先。** `owner`語列だけをworker起動条件へ変換せず、TaskSpecが独立executionを明示した場合だけruntime identityを使う |
| `ROOT` | producer binding、worker packet、producer result | non-root producerのpredicateをrootが再実行または再構成する経路 | rootが実行可能な行為をpacket構築、binding、集約へ限定する判断 | TaskSpecのallowed operationと一部重複する。委譲後の再実行禁止は追加情報である | C38 / C40のF10ではrootとchildのauthority / source重複readが残り、このlabelだけでは再取得を止めなかった | **提案: `PRODUCER`へ統合。** 明示的に委譲したoperationだけ、rootはterminal resultを再生成しない |
| `INDEPENDENCE` | 先行result / artifact、別criterion、owner / producer | 同じpredicateを別producerへ再割当てし、独立確認を元operationと混ぜる経路 | 新operation作成、固有predicate、owner、producerの再固定 | TaskSpecが独立確認を明示した場合はTaskSpecと重複する。明示しない場合の追加operationは基本三層を超える | このlabel単独の互換ablationは保存結果から分離できない | **提案: 削除候補。** TaskSpecが独立operationを明示した場合だけ、そのTaskSpecに従う |
| `METHOD` | TaskSpec明示手段、permission、個別invocation status | 一つの未固定手段がfailed / unavailableになっただけでpermission否定またはtask terminalへ変換する経路 | 手段が明示済みか、代替手段がpermission内か、同じpredicateかの判断 | permissionと明示手段はTaskSpecと重複する。個別invocationとoperation terminalの分離は追加情報である | C23のF04は5 / 5がscore `4`で、ControlFreeRepositoryのcleanup未完了1件を同じN=5では再現しなかった | **提案: 維持。** 観測済み誤経路一つに対応し、実行前の選択肢ではなく誤った早期停止を減らす |
| `RECOVERY` | environment-only repair、same required command rerun、counter上限 | 未固定手段の選択をenvironment recoveryとして数え、不要に上限を消費する経路 | repairとrerunの組判定、counter消費時点、method変更との区別 | TaskSpecのcounter値は基本三層にある。消費単位の定義は追加情報である | C23 manifestはC10観測を由来にするが、F05 / F10ではcounterが`not_applicable`であり本棚卸しのtargeted実測はない | **提案: 本見直しでは維持保留。** F05 / F10の変更predicateへ混ぜず、counter対象caseで別判断する |

## C38差分graph

C38はC35を直接sourceとし、`SPEC`、`CONTEXT`、`OWNER`だけを変更した。他の六labelはC35から継承した。

| label / predicate | 入力となる状態 | 消そうとした誤経路 | 追加した判断点 | 基本三層との重複 | 実測結果 | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| `SPEC`: result unit | required outcome、evidence差、invalidation条件 | C34 F05で成立済みclarificationを別read constraint失敗により省略した経路。C35 F10でfinding内容とlocationを一括passedにした経路 | 最小unit分割、unitごとのpredicate / owner / permission / constraint、unit-local失効 | F05 / F10 TaskSpecはrequired fieldと判定条件を既に分けている | v9 targetedはC35 / C38とも10 / 10 score `4`だった。C38は10 run token合計`+255,767`だった | **提案: 削除して直接記述へ置換。** TaskSpec-required fieldを、根拠がある限り他criterion失敗で省略しない |
| `CONTEXT`: unit別direct evidence | result unit、direct evidence、invalidation、allowed read | locationなどunit固有evidenceなしでpassedにする経路 | unitごとのevidence取得、packetへのdirect evidence固定、unit値確定、context十分性 | allowed readとrequired evidenceはTaskSpecにある。unitごとの再取得は重複する | F10 traceではrootがpacket前にevidenceを取得し、childがauthority / sourceを再取得した。C38のF10はC35比`exec +8`、`wait +3`、model step `+10`だった | **提案: 置換。** evidence selectorだけをproducerへ渡し、取得済みevidenceをrootとchildで二重生成しない |
| `OWNER`: unit-local state | owner result、unitの`false / failed`、別unit result | 一つのcriterion失敗で成立済みfieldを省略する経路 | owner readinessとunit値の直積、unit間失効判定 | TaskSpecが別criterionとrequired outputを明記しており重複が大きい | v8 targetedでは内容要件10 / 10を満たしたが、F10 1件でrootをproducerへbindし既存`OWNER`と競合してscore `3`だった | **提案: `TERMINAL`へ統合。** 成立済みrequired fieldを無関係な失敗で省略しないという一条件だけを残す |

## C40差分graph

C40はC38を直接sourceとし、`SPEC`、`CONTEXT`、`ROOT`を変更した。C38で競合が観測された`OWNER`は変更していない。

| label / predicate | 入力となる状態 | 消そうとした誤経路 | 追加した判断点 | 基本三層との重複 | 実測結果 | 判定 |
| --- | --- | --- | --- | --- | --- | --- |
| `SPEC`: operation terminal resultのprojection | operation、producer terminal result、result unit | result unitの論理分割を固有operation / command分割として解釈する経路 | operationとunitの対応、projection、unit固有operation / producer / invocationの不存在確認 | TaskSpecのrequired output fieldとproducer resultから自然に決まる関係を再定義する | C40 F10のtool callはC38の74から75、model stepは84から85、token合計は`+49,106`だった | **提案: 削除。** 狙った実行経路削減を観測せず、projection判断だけを追加した |
| `CONTEXT`: operation packetとmulti-unit binding | operation、required evidence、producer terminal result、複数unit | unit別commandとroot / childの重複evidence取得 | operation単位packet、terminal evidenceからのunit確定、same evidenceのmulti-bind | required evidenceとoutput fieldはTaskSpecにある | C40でもroot / childのauthority / source重複readが残った | **提案: 削除してproducer read ownershipへ統合。** unit mappingを作らずterminal resultをTaskSpec outputへ集約する |
| `ROOT`: producer terminal resultだけを受領 | producer binding、terminal result、evidence | rootがpacket用evidenceを先に取得し、producerが再取得する経路 | producer resultの受領元確認、rootによるevidence生成禁止 | 委譲したoperationの所有権としては追加情報だが、root自身がproducerの最短経路には不要である | F10の重複readとtool turnを減らさなかった。さらに継承した`OWNER`が正しいchild resultをidentity不一致で省略した | **提案: 単独labelとしては削除。** 明示的な委譲時だけ「rootはproducer resultを再生成しない」へ統合する |

## 分類

### 事実に基づく分類

| 分類 | predicate |
| --- | --- |
| repository / TaskSpecで既に成立するためrootで重複している | C38 / C40のresult unit分割、evidence / invalidation mapping、projection mapping。C35 `SPEC`のoutcome / permission / constraint再固定。明示済み独立確認に対する`INDEPENDENCE` |
| 観測済みの誤経路を一つ消すため必要である | `METHOD`の個別invocationとoperation terminalの分離。`TERMINAL`の開始済みnonterminal operationに対する早期完了禁止。`CONTEXT`の十分なpacketに対する親履歴流入遮断 |
| 成果後の確認だけを増やし、実行前の分岐を減らしていない | C38のunit別direct evidence、C40のprojection / multi-bind、C35 `OWNER`のruntime identity三重照合 |
| 複数labelを結合し、解釈のブレまたは最短経路の阻害を生んでいる | `SPEC` → `PRODUCER` → `OWNER` → `TERMINAL` → `ROOT`。C38 / C40ではこのchainへresult unit、evidence、invalidation、projectionが加わる |
| 効果を判断する証拠が不足している | C35 `INDEPENDENCE`単独。F05 / F10に対する`RECOVERY`。ControlFreeRepository条件でのF10 monthly review r3 root-only同条件N=5 |

### 推論

維持価値が比較的明確なのは、実行前にcontext流入を減らす`CONTEXT`のsufficiency部分と、個別手段の失敗を早期terminalへ変換しない`METHOD`である。

圧縮対象は、成果後にowner、runtime identity、result unit、evidence、invalidation、projectionを多段照合するchainである。このchainはF10でworkerを必須化し、root / childの重複readと正しいresultの省略を生んだ。

## 次の変更predicate案

### 提案

次の一つへ`OWNER`のworker起動条件を置換する。

> `OWNER_ROLE`: TaskSpecの`owner`語列だけではworker operationを作らない。TaskSpecが独立したproducer executionを明示した場合だけworkerへ委譲し、それ以外はrequired outcomeを実行するagentをproducerとする。

この提案はcandidateではない。ユーザー合意前にbundle、profile、runを作成しない。

### 残す最短正常経路

- F05はrootが開始identityを確認し、一つのclarificationを返して終了する。
- F10はrootが許可されたauthority、固定diff、2 source fileを読み、根拠付きmajor findingを返して終了する。
- TaskSpecが独立worker executionを明記したcaseでは、委譲自体を禁止しない。

### 消す一つの誤経路

TaskSpecのrisk owner語列をruntime worker identityへ変換し、正しいproducer resultをtask name / Sender / runtime path表記差で`unavailable`にしてuser-visible outputから省略する経路を消す。

### 削除される判断点

- owner語列からruntime task identityを生成する判断。
- owner語列、spawn `task_name`、`FINAL_ANSWER.Sender`を三重照合する判断。
- TaskSpecが独立executionを明示しないF05 / F10でworkerを起動する判断。
- root / childの双方が同じauthorityとsourceを再取得する経路。

### quality不変条件

- F05 5 / 5が、2点を一回で質問し、zero driftでscore `4`となる。
- F10 5 / 5が、major、正確なpath:line、直接根拠、impactを返し、zero driftでscore `4`となる。
- score `1..3`を中央値で隠さず、10 / 10 score `4`を必要条件とする。

### 期待する実行経路

- F05 / F10でTaskSpecが独立executionを明示しない限り、worker routingは0になる。
- F10の`spawn_agent`と`wait`は0になる。
- root / childの重複authority / source readがなくなるため、F10のtool call、model step、case tokenはC35 / C38 / C40の同条件観測より減ることを期待する。
- exactな減少量は固定しない。prompt変更だけでなく実行経路のばらつきがあるためである。

### targeted試験と停止条件

合意後にcandidateを作る場合は、F05 clarification r1とF10 monthly review r3だけを同一v9条件、各N=5で確認する。

次のいずれかで停止し、別predicateを追加しない。

1. 一件でもscore `4`を満たさない。
2. F05またはF10でTaskSpecにないworker起動が残る。
3. F10の正しいfindingまたはlocationが省略される。
4. F10のtool call、model step、case tokenがC35の同条件観測から減らない。
5. quality維持のためにresult unit、owner identity、evidence mappingの追加条件が必要になる。

## Gate状態

最短正常経路、観測済み誤経路、基本三層との重複、変更predicate、削除する判断点、quality不変条件、期待する実行経路、停止条件は本書で定義した。

ユーザー合意は2026-07-19に受領した。Candidate41として`OWNER_ROLE` predicateを実装し、F05 / F10 v9 targeted N=5を実行した。結果は10 / 10 score `4`で、定義した停止条件は発火しなかった。

candidate作成前gate、targeted試験gate、expanded 12-case N=5試験gateは`passed`とする。targeted結果は[`Candidate41 targeted N=5`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-targeted2-n5_2026-07-19.md)、expanded結果は[`Candidate41 expanded 12-case N=5`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-expanded12-n5_2026-07-19.md)へ分離した。expandedは60 / 60 score `4`、全run root-onlyだった。release、採用、本体反映は未判断のまま保持する。

## 参照

- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Prompt制御見直し 引き継ぎ](prompt-control-review-handoff.md)
- [Control-free repository N=5](../evaluations/results/control-free-generic-repository-expanded12-global-m24-n5_2026-07-16.md)
- [Candidate11 worker context sufficiency N=5](../evaluations/results/candidate11-sa-context-boundary-expanded12-global-m24-n5_2026-07-16.md)
- [ControlFreeRepository / Candidate23 operation boundary N=5](../evaluations/results/control-free-repository-candidate23-operation-boundary-expanded12-global-m24-n5_2026-07-17.md)
- [Candidate35 / Candidate38 v9 targeted N=5](../evaluations/results/candidate35-candidate38-outcome-quality-owner-diagnostic-v9-targeted2-n5_2026-07-19.md)
- [Candidate35 / Candidate38 token trace analysis](../evaluations/results/candidate35-candidate38-v9-targeted2-n5-token-trace-analysis_2026-07-19.md)
- [Candidate40 targeted N=5](../evaluations/results/candidate40-operation-result-projection-boundary-v9-targeted2-n5_2026-07-19.md)
