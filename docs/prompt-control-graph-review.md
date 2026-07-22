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

-  task identityを生成する判断。
- owner語列、spawn `task_name`、`FINAL_ANSWER.Sender`を三重照合する判断。
- TaskSpecが独owner語列からruntime立executionを明示しないF05 / F10でworkerを起動する判断。
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

candidate作成前gate、targeted試験gate、expanded 12-case N=5試験gateは`passed`とする。targeted結果は[`Candidate41 targeted N=5`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-targeted2-n5_2026-07-19.md)、expanded結果は[`Candidate41 expanded 12-case N=5`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-expanded12-n5_2026-07-19.md)へ分離した。expandedは60 / 60 score `4`、全run root-onlyだった。その後のrelease候補指定は独立したrelease artifactへ記録し、採用と本体反映は未判断のまま保持する。

## Candidate41 B18後の再検討

### 結論

Candidate41 B18で観測したF10 location mismatch 2件は未解決riskとして対策対象に残す。ただし、この観測から新しいroot prompt境界は導かない。

line番号付きsourceによるexact location確認は、F10の1行ずれを直接対象にしたCandidate37 `LOCATION`規則として既に試行されている。これをCandidate41へ足すことは、owner metadataとdelegationを分離するC41の変更軸へ、case固有のreview方法を混ぜることになる。

Candidate37の`LOCATION`、`EVIDENCE_PRECISION`、`RESULT_SOURCE`はいずれもF10の試験構造から逆算した案である。名前を一般化しても、repository-wideな誤分岐を消す境界にはならないため変更候補から外す。

### 責務配置

| 情報 | このrepositoryでの配置 | 今回の扱い |
| --- | --- | --- |
| repository-wideな実行境界 | prompt bundleのroot `AGENTS.md` | C41の`OWNER_ROLE`を維持し、location mismatchを理由とする規則を追加しない |
| path固有のauthority | bundle内の`src/AGENTS.md`など | ControlFreeRepositoryからC41まで同一であり、今回の変更対象にしない |
| task固有のrequired output | `evaluations/cases/.../trial-prompt-input.json` | F10 r3は既に`path:line`を要求している |
| model-invisibleな期待値と採点条件 | case private dataとrating contract | changed-line locationの不一致をscore `3`として記録する |
| 観測された低頻度事象 | `evaluations/results/` | C41 B18の2 / 90をcase別riskとして保持する |
| prompt変更判断 | 本design review | repository-wideな原因が未確認なのでcandidate作成gateを開かない |

### 事実

- C41 B18のscore `3`は2件とも、finding内容、severity、直接根拠、impactは正しく、locationだけが実変更行`monthly_main.py:25`に対して`:24`だった。
- 同じv9互換条件のControlFreeRepository N=5でも、F10 monthly reviewのlocation mismatchが1件あった。
- Candidate41のdirect sourceはCandidate35であり、変更targetはroot `AGENTS.md`だけである。
- Candidate37はCandidate36をdirect sourceとし、F10のlocation mismatchを理由に`LOCATION`をrootへ追加した別枝である。
- Candidate37 expanded N=5は60 / 60 score `4`だったが、Candidate41 B18とはrating revisionが異なり、B18も実施していない。
- C41 B18のscore `3` 2件は、どちらも`monthly_engine.py`、`monthly_main.py`、固定diffの順で読み、固定diffの確認後にfinding内容を確定した。中間messageにはlocationがなく、追加readなしでterminal responseへ`:24`を付けた。
- C41 B18のF10 90 runには、line番号付きsourceまたは`git grep -n`を使わず`:25`を返したscore `4` runも複数ある。番号付き表示の不使用だけではfailureを説明できない。
- 保存したcommand sequenceの分類では、behavior reference、target source、diffの順で読む経路は上記2件だけであり、2件ともscore `3`だった。他の88件はscore `4`だった。この相関だけからread順序を決定的原因とは断定しない。
- C35 B18で`:26`を返したworkerも、固定diff、target source、behavior referenceを一つのcompound outputとして番号なしで受け取り、terminal responseで初めてlocationを付けた。

### 推論

location mismatchはC41のowner / delegation境界に固有のfailureではない。TaskSpecに既に存在する`path:line`要件を、line番号付きsourceという方法指定に変換してrootへ再掲しても、repository-wideな判断分岐は減らない。

Candidate37の結果は、その方法指定がN=5で成果を壊さなかったことを示す。一方で、低頻度誤りを消したこと、追加readや確認costを上回る正味効果があること、他のreview taskへ一般化できることは示していない。

保存traceで共通する実行形は、個別line番号を持たないsource / diff textからterminal responseのlocationを生成したことである。再構成結果がC35では`:26`、C41では`:24`になった。

番号なしでも正解したrunがあるため、line番号の欠落はfailureの十分条件ではない。read順序もC41の2件とは相関したが、C35の`:26`は別順序で発生している。したがって、保存traceから特定のread順序、owner経路、C41 labelを決定的原因にはできない。

現時点で確認できるのは、exact coordinateを非構造化textから生成する経路に確率的な誤差が残ることまでである。これは実行evidenceの表現またはmodelの事実抽出精度の問題候補だが、repository-wideなprompt制御の誤分岐とは確認できない。

### 対策の責務

- Evaluation: score `3`を有効な観測として保持し、中央値やscore `4`多数で隠さない。
- Prompt design: repository-wideな原因が確認できないため、location mismatchからcandidateを作らない。
- Release: C41にはF10 exact locationの低頻度riskが残ると記録し、risk受容なしに採用またはrelease済みとしない。
- Execution interface: exact coordinateの決定的保証が必要なら、実運用と評価で共通する構造化evidenceを入力として提供する別要件を検討する。評価adapterだけへline情報を足して本caseを通す変更はしない。

### 判断

- C41へCandidate37の`LOCATION`を統合しない。
- `EVIDENCE_PRECISION`案は撤回する。
- `RESULT_SOURCE`案も試験依存のため撤回する。
- location mismatchから新しいprompt変更predicateを導かない。
- C41 B18 resultへcase別の残存review精度riskとして保持する。
- candidate bundle、profile、追加評価runを作成しない。

## 追加135件診断による判断更新

### 結論

上記の「location mismatchから新しい変更predicateを導かない」という判断は、原因段階を観測できなかった時点の判断として保持する。追加診断によりterminal前のnumeric bindingで誤りが生じたことは確認したが、症状を照合するだけの指示は低確率で発生する理由を説明しない。

一度提案した`REVIEW_LOCATION_TEXT_LINE_CONSISTENCY`はcandidate候補から撤回する。新しい分析対象はprompt boundaryではなく、同じevidenceが持つ複数coordinate frameの取り違えである。

### 事実

- 同一のmodel-visible checkpointで既存30件に105件を追加し、累計135 validを得た。
- 累計分布は`valid_exact=134`、`valid_mismatch=1`だった。
- 追加105件はcheckpointとterminalのlocationが105 / 105で同じだった。
- 唯一のmismatchは、checkpointで正しい完全なline text `format_test=args.force,`を記録しながら、numeric lineを`24`とした。固定revisionでそのline textが存在する行は`25`だった。
- terminal responseはcheckpointの`:24`を変更せず返した。
- mismatch前に、変更行25を示すunified diffはmodel-visibleだった。
- 同じ変更行は、new-file 1-based座標では`25`、source sequenceのzero-based indexでは`24`、削除行を含むdiff表示順では`26`になる。
- 既知のC41 mismatch 3件は`:24`、Candidate35の別mismatch 1件は`:26`だった。
- C41 B18 90件とcheckpoint 135件をcoordinate provenanceだけで記述的に並べると、terminal前に明示的direct coordinateがあった90件は90 / 90 exactだった。implicit reconstruction側は132 / 135 exact、3 mismatchだった。
- 詳細は[`Review location誤差の原因診断計画`](review-location-cause-diagnostic-plan.md)と外部diagnostic rootの`summary.json`へ保存した。

### 原因仮説

最も一般的な説明は`coordinate-frame leakage`である。modelは通常、implicitな位置表現をrequested one-based `path:line`へ正規化する。低確率で、sourceのzero-based indexまたはdiff表示順など、別frameの未正規化値がterminal valueへ漏れると推測する。

これは既知4件を`:24 / :26`の両方向を含めて説明する。一方、model内部のselected frameまたはtoken probabilityは保存eventから見えないため、まだ推論である。

checkpoint mismatchだけはroot authority outputがdiffより後に完了した唯一のrunだった。これはsalience増幅要因候補である。ただし、元B18の2 mismatchはdiffが最後であり、共通原因ではない。

### control graph上の扱い

- `SPEC`、`CONTEXT`、`OWNER`、`ROOT`へlocation条件を追加しない。
- C41の`OWNER_ROLE`へ統合しない。
- Candidate37の`LOCATION`を再採用しない。
- output照合postconditionも、原因仮説の反証前にはcandidate化しない。
- 次の対象は、unnumbered sourceとraw diffを渡す`multi-frame`条件と、atomic one-based recordだけを渡す`single-frame`条件の外部mechanism diagnosticである。

### Gate状態

この時点では低確率原因の仮説を定義したが、反証可能なmechanism diagnosticは未実行だった。candidate作成gateは`closed`のままとし、candidate bundle、profile、Layer 3、Layer 4 resultを作成しなかった。

## Coordinate representation診断後の更新

multi-frameとsingle-frameを各135件、24並列で実施した。multi-frameはunnumbered sourceとraw unified diff、single-frameはatomic one-based recordをmodel-visible evidenceとした。semantic code内容、review要求、model、reasoning effortは固定した。

両条件とも135 / 135が正しい`:25`を返し、`:24 / :26`は発生しなかった。tool use、retry、schema failureも0だった。

この結果により、複数coordinate frameが同じevidenceに存在することだけをroot causeとする仮説は支持されなかった。したがって、evidenceをsingle-frameへ変える制御またはinterface変更も、現時点では変更predicateへしない。

実Agentの135 checkpoint traceでは、checkpoint前のagent messageへnumeric coordinateを保持したrunが0件だった。134件は完全なchanged line textも保持せず、semantic findingだけを確定した後、別turnでcoordinateを再構成した。縮小mechanism diagnosticは同じturnでevidenceからcoordinateを直接出力していた。

次の原因候補は、coordinate representation単独ではなく、`semantic compression後のdelayed coordinate reconstruction × competing coordinate frames`の相互作用である。これはboundary labelではない。Agent stateをまたぐevidence identity保持の問題候補である。

次の一変数診断は、同じevidence representationについて、turn 1でcoordinateなしのsemantic findingへ圧縮し、turn 2でevidenceを再掲せずcoordinateを返すdelayed条件である。ユーザー合意を2026-07-19に受領し、各条件135件、24並列で実施した。

## Delayed coordinate reconstruction診断後の更新

### 事実

- delayed multi-frameは135 / 135が`:25`で、`:24 / :26`は0件だった。
- delayed single-frameも135 / 135が`:25`で、`:24 / :26`は0件だった。
- valid 270 sessionのturn 1 / turn 2でtool使用は0だった。
- 即時条件に対するdelayed条件のtoken中央値差は、multi-frameが`+28,425`、single-frameが`+30,933`だった。
- 即時条件に対するelapsed中央値差は、multi-frameが`+12.910秒`、single-frameが`+14.289秒`だった。
- semantic validatorは自然な日本語同義語を43 attemptで偽陰性にした。最終1 slotは、最小attempt番号の既存sessionを固定ruleで再分類して補った。

### 推論

`semantic compression後の別turn再構成`も、観測した隣接line errorの十分条件として支持されなかった。これにより、coordinate representation単独とturn delay単独の二つを、変更predicateから外す。

残る原因候補は、delayed reconstructionとreal-Agent固有のcontext pressureの相互作用である。ただし、長いmulti-tool context、task switch、evidence距離、完了順のどれが必要条件かは未識別である。

lexical retry filteringがあったため、今回の0 / 135をsummary wordingから独立な結果として一般化しない。

### 提案

事前gateを満たさないため、evidence完了順の新規runへ進まない。まず既存real-Agent traceのmismatch / exactを、evidence距離、競合数値の直近性、tool / authority完了順、context量proxy、task switch数でpassiveに比較する。

これは新しいprompt labelではない。C35 / C38 / C40 / C41の既存labelへ条件を追加しない。candidate作成gateは引き続き`closed`である。

## Implicit coordinate passive case-control後の更新

### 事実

保存済みC41 traceのimplicit reconstruction 135件を、B18 terminal 47件とcheckpoint first binding 88件へ分けて再抽出した。exactは132件、mismatchは3件だった。

3 mismatchすべてで、first coordinate binding前に最後に完了したexact line text付きevidenceがunified diffだった。同じdiff-last状態のexactは11件だった。最後のline-bearing evidenceがtarget sourceだった121件はすべてexactだった。

| group | diff-last exact / mismatch | target-source-last exact / mismatch |
| --- | ---: | ---: |
| B18 terminal | 7 / 2 | 38 / 0 |
| checkpoint first binding | 4 / 1 | 83 / 0 |

context output byteとevidence距離は、3 mismatchをexact分布の一方の端へ共通して分離しなかった。cumulative input tokenは3件とも低い側だったが、追加model stepと再読数に交絡し、同じ帯域にもexactがあった。

### 推論

最も狭い共通条件は、完了順全体ではなく、first coordinate binding時点の`latest line-bearing evidence representation`である。direct coordinateがない状態では、直近のrepresentationが座標frame選択へ影響する可能性がある。

ただしdiff-lastは十分条件ではない。real-Agentで11件がexactで、縮小mechanism diagnosticでも誤差を再現していない。この関連だけをprompt制御へ昇格させない。

### 提案

次に分離する一変数は、通常のreal-Agent review経路を保持したまま、first coordinate binding前の最後のline-bearing evidenceを`unified diff`または`unnumbered target source`にする条件差である。

これは外部原因診断のproposalである。新規runはユーザー合意前に開始しない。C35 / C38 / C40 / C41のlabelは変更せず、candidate作成gateも`closed`のままとする。

## Real-Agent representation recency診断後の更新

### 事実

通常のC41 repository review経路を保持し、turn 1でrepository inspectionとsemantic finding確定を行った。turn 2直前に追加する最後のline-bearing evidenceだけを、full-context unified diffまたはfull unnumbered target sourceへ変えた。

| 最後のevidence | valid | exact `:25` | mismatch | all-Agent token中央値 | elapsed中央値 | turn 1 tool中央値 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| unified diff | 135 | 135 | 0 | 163,845 | 123.773秒 | 6 |
| target source | 135 | 135 | 0 | 150,307 | 105.799秒 | 6 |

270 sessionすべてroot 1 sessionで完了した。turn 1のpath / coordinate / exact-line output leakは0だった。turn 2のtool callと追加workerも0だった。

初期validatorは`sed`後方のshell代入`=`を誤検出し、23 turn 1を偽陽性にした。修正版で23件を同じsessionからresumeした補足監査も23 / 23 exactだった。

### 推論

`latest line-bearing evidence = unified diff`は、隣接line errorの十分条件として支持されなかった。passive traceのpost-hoc関連は、通常repository readを含む二条件操作で再現しなかった。

したがって、diff-last回避、source-last強制、座標のための再読をC35 / C38 / C40 / C41の制御graphへ追加しない。これらはrepository-wideな分岐を消さず、今回のdiagnostic methodだけへ適合する。

残る候補は、representation単独ではなく、terminal response構築、prior coordinate pressure、または未記録stateとの高次相互作用である。今回のturn 2は固定JSON schemaへの直接bindingであり、元のterminal / checkpoint constructionと同一ではない。

### 提案

新しいmodel runへ続けて進まない。保存traceから残る相互作用を一つに限定できるまで、location mismatchをprompt変更predicateへ使わない。

candidate作成gateは`closed`である。candidate、profile、Layer 3、Layer 4を作らない。

## Recorded-state collision受動監査後の更新

### 事実

新しいmodel runを行わず、implicit reconstruction 135件の保存済みfeatureを再比較した。3 mismatchが共有する記録済みfeatureは17個あった。しかし、その17個すべてが同じexact runも4件あった。

B18の2 mismatchは同じrelevant completion orderを共有した。一方、checkpointの1 mismatchは別のorderだった。checkpoint mismatchの`root_authority_after_diff=true`もcheckpoint exact 1件と衝突した。したがって、group内で見つけた完了順やauthority順は3 mismatch全体を分離しない。

先行するreal-Agent representation interventionでは、unified-diff-lastとtarget-source-lastが各135 / 135 exactだった。保存済みtraceの外部状態と、実施済み介入のどちらからも、mismatchだけを選ぶ決定的なpredicateは得られなかった。

### 推論

残る事象は、semantic line textを正しく選んだ後にnumeric coordinateだけを隣接値`:24`へ正規化する低確率誤差と整合する。ただしmodel内部stateは記録していないため、これは原因の証明ではない。

少なくとも、read order、diff-last回避、source再読、owner labelのいずれも、観測した3 mismatchをexactから分離するprompt predicateにはならない。これらをC41へ追加すると、消すことを確認できない分岐のために方法costだけを増やす。

### 提案

- prompt candidate作成gateは`closed`のままとする。
- exact coordinateの低頻度riskはrelease判断へ残す。
- exact coordinateがhard requirementなら、選択済みのexact line textをdeterministicなsource indexでone-based coordinateへ解決するevidence interface要件を、prompt制御とは別に定義する。
- このinterface要件を検討範囲へ入れるかはユーザー合意を次gateとする。合意前にcandidate、profile、追加run、runtime実装を作らない。

詳細と証拠hashは[`Review location誤差の原因診断計画`](review-location-cause-diagnostic-plan.md)へ記録した。

candidate作成gateは引き続き`closed`である。C35 / C38 / C40 / C41の既存labelへ条件を追加しない。

## 参照

- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Prompt制御見直し 引き継ぎ](prompt-control-review-handoff.md)
- [Control-free repository N=5](../evaluations/results/control-free-generic-repository-expanded12-global-m24-n5_2026-07-16.md)
- [Candidate11 worker context sufficiency N=5](../evaluations/results/candidate11-sa-context-boundary-expanded12-global-m24-n5_2026-07-16.md)
- [ControlFreeRepository / Candidate23 operation boundary N=5](../evaluations/results/control-free-repository-candidate23-operation-boundary-expanded12-global-m24-n5_2026-07-17.md)
- [Candidate35 / Candidate38 v9 targeted N=5](../evaluations/results/candidate35-candidate38-outcome-quality-owner-diagnostic-v9-targeted2-n5_2026-07-19.md)
- [Candidate35 / Candidate38 token trace analysis](../evaluations/results/candidate35-candidate38-v9-targeted2-n5-token-trace-analysis_2026-07-19.md)
- [Candidate40 targeted N=5](../evaluations/results/candidate40-operation-result-projection-boundary-v9-targeted2-n5_2026-07-19.md)
- [Candidate37 exact evidence location expanded N=5](../evaluations/results/candidate37-exact-evidence-location-owner-producer-v8-expanded12-n5_2026-07-18.md)
- [Candidate41 continuous B18](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-continuous-n5-b18_2026-07-19.md)
