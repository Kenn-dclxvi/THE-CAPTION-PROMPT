# Review location誤差の原因診断計画

## 結論

Candidate41 B18で観測したF10 location mismatchは、直ちにprompt境界へ変換しない。先に、findingの意味判断とlocation座標の確定がどのeventで行われたかを保存し、誤差の発生段階を識別する。

最初の変更predicateはprompt規則ではなく、model-visible入力を変えない診断記録`CLAIM_PROVENANCE`とする。

```text
CLAIM_PROVENANCE := path:line claimごとに、
finding確定event、location初出event、
claim前に観測されたrevision / path / line / line textの直接座標根拠、
terminal claimとの差を保存する。
```

この記録で原因段階を識別できない場合だけ、別互換条件の診断runでlocation確定checkpointを追加する。candidate bundle、評価profile、Layer 4 resultは、原因に対応するprompt変更predicateへユーザーが合意するまで作成しない。

## 既存traceから確認した事実

- Candidate41 B18のF10 monthly reviewは90件あり、score分布は`4 / 3 = 88 / 2`だった。
- score `3`の2件はfinding、severity、直接根拠、impactを正しく特定し、実変更行`:25`に対してlocationだけを`:24`とした。
- target sourceの`:25`を`nl -ba`などで直接表示した43件は43 / 43がscore `4`だった。
- target sourceの`:25`を直接表示しなかった47件も45 / 47がscore `4`だった。したがって、line番号付き表示の欠如はfailureの十分条件ではない。
- `monthly_engine.py`、target source、固定diffの順で最初に読んだ`ETD` traceは3件だった。3件の最初の3 outputはbyte単位で同一だった。
- `ETD`の失敗2件はfindingとimpactを確定した後、座標を再確認せず、terminal responseで初めて`:24`を生成した。
- `ETD`の成功1件は同じ分岐点から`nl -ba`でtarget sourceを再読し、`:25`をterminal responseへ出した。
- 同じv9条件のControlFreeRepositoryにも、`DTE`順、line番号付き表示なし、terminal responseで初めて`:24`を生成した1件がある。
- Candidate35の保存traceにも、別のcompound read順からterminal responseで初めて`:26`を生成した1件がある。
- 以上から、C41 label、owner経路、`ETD`順、特定toolの不使用のいずれも単独原因とは確認できない。

## 現時点の仮説

### 推論

最も狭い反証可能な仮説は次である。

> semantic findingを確定した時点で、locationがrevision上の直接参照可能な座標へまだ結び付いていない場合、terminal response生成時の座標再構成が隣接行へずれることがある。

この仮説はroot promptの境界を主張しない。誤差候補を、authority選択やfinding発見ではなく、findingからexact coordinateへの接続段階へ限定する。

### 未確認事項

- model内部で`:24`がfinding確定時に作られたのか、terminal response生成時に作られたのかは保存されていない。
- line番号付き表示が誤差を防いだのか、正確さを確認する実行姿勢と相関しただけなのかは確定していない。
- この誤差がF10 fixture固有か、exact coordinateを要求するreview一般に発生するかは、現evaluation setに別の`path:line` review caseがないため確認できない。

## 診断記録`CLAIM_PROVENANCE`

### 配置

新規runでは、Layer 2完了後かつseal前に次へ保存する。

```text
layer2/extensions/<run_id>/response-claim-trace/trace.json
```

compact済みrunはarchiveを変更しない。backfill結果は、source archiveのSHA-256と`run_id`へbindしたappend-onlyな外部diagnostic artifactとして保存する。

### 最小field

| field | 内容 |
| --- | --- |
| `schema_version` | 診断記録schema |
| `collector_revision` | 後処理実装identity |
| `run_id`、`case_id`、`iteration` | run binding |
| `source_artifacts` | 入力event、response、diffのkindとSHA-256 |
| `observations` | event順、operation、target path、`unified_diff / unnumbered_source / numbered_source`、line anchor、output SHA-256 |
| `response_claims` | intermediate / terminal、path、line、初出event、claim text SHA-256 |
| `claim_alignment` | 観測済みchanged lineとの`exact / adjacent / none`とdelta |

rating、score、prompt identity、oracle、expected locationはLayer 2記録へ入れない。原因分析時に保存済みratingと別途joinする。

### 既存archiveから取得できる情報

- source、diff、line番号付きsourceのread順と表示形式
- findingを初めて明示したmessage
- locationを初めて明示したmessage
- claim前に同じ座標がmodel-visible outputへ存在したか
- claimとdiff changed lineのdelta
- tool call、model step、output byte、root / child構成

### 既存archiveから取得できない情報

- model内部のline計算過程
- modelが複数の観測のうち実際にどれを採用したか
- compact前に収集しなかったdescendantの全intermediate message

最初の2点を自己申告だけで補完しない。必要なら次の別診断条件で観測点を追加する。

## `CLAIM_PROVENANCE` backfill結果

### 実装と保存

- collector: `scripts/response_claim_trace.py`
- unit test: `tests/test_response_claim_trace.py`
- backfill対象: Candidate41 B18のF10 monthly review 90件
- diagnostic artifact: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/diagnostics/candidate41-f10-response-claim-trace-backfill-20260719-r2`
- 保存内容: 90 trace、source archive SHA-256、trace SHA-256、scoreを後段joinした分析view

最初の`r1` backfillは、revision prefix付き`git grep -n` output 5件をdirect coordinateとして認識しなかった。collectorを`response-claim-trace/v2`へ修正し、既存`r1`を変更せず`r2`をappend-onlyで追加した。

### 事実

| terminal claim前のtarget direct coordinate | score `4` | score `3` |
| --- | ---: | ---: |
| あり | 43 | 0 |
| なし | 45 | 2 |

| claimと観測済みchanged lineの関係 | score `4` | score `3` |
| --- | ---: | ---: |
| `exact` | 88 | 0 |
| `adjacent`、delta `-1` | 0 | 2 |

90件すべてを同じcollectorで再計算し、手作業で確認した43 / 47分類と一致した。collectorはraw command、raw output、raw responseを保存せず、それらのSHA-256、byte数、event順、representation、line anchor、path:line claimだけを保存する。rating、score、oracleは個別Layer 2 traceに含めず、外部analysisでjoinした。

### 推論

direct coordinateを観測した43件でmismatchがなかったことは、直接座標への接続が保護要因である仮説と整合する。ただし、direct coordinateなしでも45 / 47が正しいため、座標再確認の欠如を単独原因とは判断できない。

誤った2件はいずれもlocationがterminal responseで初めて観測された。既存traceだけでは、その値が非表示の内部判断ですでに`:24`だったのか、terminal response生成時に`:24`になったのかを区別できない。したがって、追加診断runの実施条件を満たす。

## 追加診断run

### 実施条件

`CLAIM_PROVENANCE`のbackfill後も、誤った座標がfinding確定時とterminal生成時のどちらで生じたか区別できない場合に限る。

### 変更する一変数

Candidate41 bundle、model、case、fixture、permissionは固定し、TaskSpecへ診断専用のlocation checkpointだけを追加する。

checkpointは、findingの意味を確定した後、terminal responseより前の独立messageとして、次だけを記録する。

```text
revision
path
line
line_text
```

oracle、expected line、scoreはmodelへ渡さない。この条件は既存v9とexecution compatibilityが異なるpartial diagnosticであり、Layer 4比較、採用判断、prompt改善の成果として扱わない。

### 識別方法

| checkpoint | terminal | 読み方 |
| --- | --- | --- |
| wrong line、correct line text | wrong line | coordinate変換段階の誤差候補 |
| correct line、correct line text | wrong line | terminal projection段階の誤差候補 |
| adjacent line、adjacent line text | wrong line | evidence選択段階の誤差候補 |
| correct | correct | checkpointが誤差を抑えた可能性があり、原因確定とはしない |

### 反証条件と停止条件

1. checkpointで直接座標を確認した後にもwrong locationが出た場合、直接座標への接続だけで防げるという仮説を反証する。
2. 最初のlocation mismatchを観測した時点で停止し、発生段階を分類する。
3. 最大30 valid runでmismatchが出なければ停止する。checkpoint追加が挙動を変えた可能性を残し、原因確定やcandidate化をしない。
4. checkpointが独立messageとして保存されない場合、そのrunを原因判断へ使わない。同じprotocol failureが3回続いた場合は診断方法を停止する。
5. 一つの診断結果からroot prompt predicateを作らない。F10固有でないことを確認できる別review evidenceが必要である。

## 追加診断run結果

### 実施条件

2026-07-19に、上記のlocation checkpointを別compatibilityのpartial diagnosticとして実施した。

- diagnostic root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/diagnostics/candidate41-f10-location-checkpoint-20260719-r1`
- prompt set: `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1`
- case: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3`
- fixed seed revision: `a53601614b41f52633f1d75e77c72861a0f0f1c8`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- frozen diagnostic set identity: `6bd7efd364f0ab7e28b675863e1eae27b69bbb29b0628b8691cd39e845061895`
- contract SHA-256: `e4d16145283fa7f95c545893df2c4d97f1fec35204c3353fc258da6608ac7285`

既存F10 r3 TaskSpecへ`diagnostic_location_checkpoint_protocol`だけをmodel-visible fieldとして追加した。C41 bundle、F10 fixture、model、Agent環境、permissionは既存B18と同じである。runnerは逐次実行と30 valid停止へ変更したため、既存v9 resultとはcompatibleではない。

preflight後のcollector reviewで、prepared input hashの再検証、同一finding確認、同一protocol failure signature、controller再開処理を補強した。補強中に開始していたiteration 2のpartial directoryは、bindingとexecutionが作成される前に停止した。これは削除せず保存し、attemptとvalid countへ含めていない。model-visible入力とfrozen capsuleは変更していない。

### 事実

| 観測 | 件数 |
| --- | ---: |
| Layer 2 valid | 30 / 30 |
| checkpoint protocol valid | 30 / 30 |
| checkpoint `path / line / line_text = changed line` | 30 / 30 |
| terminal location `monthly_main.py:25` | 30 / 30 |
| checkpointとterminalのlocation一致 | 30 / 30 |
| 同じF10 semantic findingをterminalで確認 | 30 / 30 |
| protocol failure | 0 |
| external failure | 0 |
| checkpoint前にtarget direct coordinateをtool outputで観測 | 11 / 30 |
| checkpoint前にtarget direct coordinateをtool outputで未観測 | 19 / 30 |

最初のlocation mismatchは発生せず、固定した停止条件`max_30_diagnostic_valid_without_location_mismatch`で停止した。Layer 3 ratingとLayer 4 resultは作成していない。

保存artifactは次である。

- `summary.json`: 30 runの停止結果とtoken、elapsed
- `manifest.json`: 30 runのbinding、execution、event、response、checkpoint、trace、usageのSHA-256
- `verification.json`: protocol、location、semantic finding、Layer 3 / 4不在の再検証
- `descriptive-comparison.json`: C41 B18 F10との非互換な記述的cost / event比較
- `batch-001/cycle/layer2/extensions/<run_id>/location-checkpoint/checkpoint.json`: checkpoint専用trace
- `batch-001/cycle/layer2/extensions/<run_id>/response-claim-trace/trace.json`: passive claim trace
- `batch-001/compact/execution-evidence.tar.zst`: lossless execution archive、SHA-256 `a01f193227160fb77982cbe23d6fcf83f345abe48fa982dbb21961bea7c452f9`

archive検証後、30個のvalid workspaceをpruneし、937,697,280 bytesを回収した。中断したpartial workspaceは削除せずarchiveとlocalの両方へ保存した。

同じC41 B18 F10 monthly reviewとの記述的cost比較は次である。

| 条件 | runs | all-agent token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: |
| C41 B18 F10、checkpointなし | 90 | 223,415.5 | 93.371秒 |
| C41 F10 checkpoint diagnostic | 30 | 238,926.5 | 90.560秒 |
| diagnostic - B18 | — | +15,511、+6.943% | -2.810秒、-3.010% |

平均では、B18が`192,151.26 tokens / 88.698秒`、diagnosticが`216,368.63 tokens / 91.101秒`だった。平均差は`+24,217.38 tokens / +2.402秒`であり、elapsedの中央値差と平均差は方向が逆である。

root event proxyの中央値は次である。これは保存event数であり、非表示の推論step数ではない。

| 条件 | completed agent message中央値 | intermediate agent message中央値 | command execution中央値 |
| --- | ---: | ---: | ---: |
| C41 B18 F10、checkpointなし | 4 | 3 | 11 |
| C41 F10 checkpoint diagnostic | 5 | 4 | 11 |
| diagnostic - B18 | +1 | +1 | 0 |

TaskSpecと反復条件が異なるため、これらはcheckpointの純粋なcost推定ではない。特にelapsedの差を高速化と判断しない。token増加とmessage 1件増加はcheckpoint追加と整合するが、`+15,511`をcheckpoint単独へ因果帰属しない。

### 推論

- checkpointで`:25`を記録した後にterminalだけが`:24`へ変わる例はなかった。したがって、terminal projectionだけで座標がずれる経路は今回観測していない。
- checkpoint時点ですでにwrong lineまたはadjacent line textを選ぶ例もなかった。したがって、evidence選択またはcoordinate変換の誤差段階も今回識別できていない。
- direct coordinateをtool outputで見なかった19件もcheckpointとterminalが正しかった。したがって、`nl -ba`など特定toolの使用を必要条件またはroot境界とは判断できない。
- 30 / 30 exactは、明示的な`revision / path / line / line_text` bindingが誤差を抑えた可能性と整合する。ただし、checkpointを要求したこと自体が注意や生成経路を変えた可能性を分離できない。
- 元の観測は2 / 90の低頻度誤差である。独立かつ同じ2 / 90発生率を仮定すると、30件で0件となる確率は約50.96%である。今回の0 / 30だけで保護効果や原因を確定しない。

### 次の提案

次に行うなら、prompt candidateではなく、同じF10条件で`line`だけをcheckpointから外すsemantic-only diagnosticを一つの変更predicateとする。

```text
SEMANTIC_LOCATION_CHECKPOINT := finding確定後、terminal前に
revision / path / line_textだけを独立messageへ記録し、
numeric lineはterminalで初めて生成させる。
```

この条件で隣接行誤差が再現すれば、numeric coordinateをterminal前にbindしたことが保護要因である可能性が上がる。再現しなければ、numeric bindingではなく、structured checkpointまたは注意の変化が誤差を抑えた可能性を残す。

この提案は別compatibilityの診断であり、ユーザー合意前にcase、profile、runを作成しない。結果が得られても、F10固有でないreview evidenceなしにroot prompt predicateへ昇格しない。

## 同一checkpoint診断の追加105件

### 結論

30件では低頻度誤差を識別できなかったため、model-visible checkpointを変更せず105 valid runを追加した。追加105件のうち1件でlocation mismatchを観測し、誤りがterminal responseより前のnumeric coordinate bindingで生じていたことを確認した。

上記のsemantic-only diagnostic案は実施していない。追加母数だけで発生段階を観測できたため、まず低確率でnumeric coordinateがずれる生成機構を分析する。症状を照合するだけのprompt predicateへ直結させない。

### 実施条件

- diagnostic root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/diagnostics/candidate41-f10-location-checkpoint-20260719-r2-parallel-n105`
- model-visible TaskSpec SHA-256: `e15969c1390dd576ca7f185b64f947631d60d1a2975675ab42d262cb1ace1d26`
- 既存30件と追加105件で、model-visible TaskSpec SHA-256は同一
- phase 1: 5並列で19 validを保存後、ユーザー指示により中断
- phase 2: 通常試験と同じ24並列で84 valid
- replacement: mismatchによるshard早期停止で不足した2 validを2並列で補完
- Layer 3 rating、Layer 4 result、candidate、profileは作成していない

phase間でdispatch条件が異なるため、location outcomeだけを既存30件と記述的に合算する。tokenとelapsedをv3 compatible KPI比較へ使わない。

### 事実

| 観測 | 追加105件 | 既存30件との累計135件 |
| --- | ---: | ---: |
| `valid_exact` | 104 | 134 |
| `valid_mismatch` | 1 | 1 |
| checkpointとterminalのlocationが同じ | 105 | 135 |
| protocol failure | 0 | 0 |
| external failure | 0 | 0 |

追加105件のautomatic semantic signatureは`matched=103`、`review_required=2`だった。後者2件は、短いflag名または別表現により語句patternを満たさなかった。terminal responseを個別確認し、どちらも同じF10 finding、engine effect、user-visible impactを含むことをappend-onlyな`semantic-review.json`へ記録した。

唯一のmismatchはrun `3fd716da89b64324bde76ea244d5aaa1`である。

| field | 観測値 |
| --- | --- |
| checkpoint `path` | `src/app/entrypoints/monthly_main.py` |
| checkpoint `line` | `24` |
| checkpoint `line_text` | `format_test=args.force,` |
| `line_text`が固定revisionで実在する行 | `25` |
| terminal location | `src/app/entrypoints/monthly_main.py:24` |
| checkpointとterminalのdelta | `0`、`same` |
| changed lineに対するdelta | `-1`、`adjacent` |
| semantic finding | `matched` |

このrunはcheckpoint前に、変更行を25行目として含むunified diffと、同じsource line textをmodel-visible outputで観測していた。checkpointでは正しいline textを保持したまま、numeric lineだけを24と記録した。terminalはその誤ったnumeric lineを変更せず出力した。

追加105件のall-agent token中央値は`225,620`、合計は`19,418,718`だった。run別elapsed中央値は`94.148秒`だった。これらは並列host contentionと反復条件が異なる記述値であり、逐次30件またはB18との増減判断に使わない。

24並列phaseのcontroller wall-clock windowは84 validで`460.556秒`、補完2並列は2 validで`108.466秒`だった。最初の5並列phase開始から補完完了までの全windowは、並列度変更と再準備を含め`1,270.430秒`だった。これは運用時間の記録であり、run別elapsed KPIまたは逐次条件とのcompatible比較ではない。

135件中1件のmismatch率は`0.741%`、Wilson 95%区間は約`0.131%..4.076%`である。固定発生率を元の`2 / 90`と仮定したとき、135件で0件となる確率は約`4.813%`である。実際には1件を観測したため、この計算は効果差の検定ではなく、30件から母数を増やす根拠の確認に限定する。

### 推論

- terminal projectionが唯一の原因という仮説は、今回のmismatchに当てはまらない。誤った`:24`はterminal前のcheckpointですでに存在した。
- evidence lineの選択誤りでもない。checkpointの`line_text`は実変更行25の完全なsource lineと一致した。
- 観測した誤経路は、正しいevidence textをnumeric coordinateへ結び付ける段階のoff-by-oneである。
- exact coordinate情報がrepository outputに存在するだけでは十分でない。今回のmismatchは、25行目を示すunified diffを観測した後にも発生した。
- structured checkpointは誤差を完全には抑止しない。104 / 105 exactは保護効果と整合するが、効果量や因果はこの非互換診断だけでは判断しない。
- 内部でどの表現から`24`を生成したかはevent traceから特定できない。したがって、特定tool、read順、diff形式を原因と断定しない。

### 撤回した症状照合案

最初に、次のpostconditionを変更predicate候補とした。

```text
REVIEW_LOCATION_TEXT_LINE_CONSISTENCY :=
review findingへpath:lineを付ける場合、terminal response前に、
直接根拠として採用した完全なline textが固定revisionのそのnumeric lineに存在することを照合する。
一致しない場合は、line textが存在するnumeric lineへlocationを修正してから返す。
```

これは観測された`:24`を検出する方法であり、なぜ低確率で`:24`が生成されるかを説明しない。2026-07-19の再検討でcandidate候補から撤回した。candidate bundle、profile、評価runは作成しない。

### 低確率で発生する理由の追加分析

#### 事実

同じ変更行は、model-visible evidence内で次の三つの数値へ対応し得る。

| 座標frame | 同じ`format_test=args.force,`の値 |
| --- | ---: |
| new fileの1-based `path:line` | 25 |
| unnumbered sourceをsequenceとして扱ったzero-based index | 24 |
| unified diff hunk内で削除行も1表示行として数えた追加行の表示順 | 26 |

既知のC41 mismatch 3件はすべて`:24`だった。Candidate35の別mismatch 1件は`:26`だった。いずれもsemantic findingとevidence line textは正しく、numeric coordinateだけがずれた。

Candidate41 B18 90件とcheckpoint 135件を、実行互換比較ではなくcoordinate provenanceだけで記述的に並べると次になる。

| terminal前の明示的direct coordinate | exact | mismatch |
| --- | ---: | ---: |
| あり | 90 | 0 |
| なし、unnumbered source / raw diffから再構成 | 132 | 3 |

direct coordinateなしでも132 / 135は正しい。したがって、direct coordinateの欠如はfailureの十分条件ではない。一方、観測した3 mismatchはすべてimplicit reconstruction側で発生した。

checkpoint 135件の唯一のmismatchは、5つの並列evidence readの完了順が`src authority → target source → behavior source → diff → root authority`だった。root authorityがdiffより後に完了したrunは135件中この1件だけだった。ただし、元B18の2 mismatchは`behavior source → target source → diff`であり、共通する完了順ではない。

#### 推論

現時点の最も一般的な説明は`coordinate-frame leakage`である。

```text
coordinate-frame leakage :=
modelは通常、implicitな位置表現をnew-file 1-based path:lineへ正規化する。
ただし低確率で、同時に利用できる別frameの未正規化値をそのまま出力する。
```

`:24`は正しい行のzero-based indexと一致し、`:26`は削除行を含むdiff表示順と一致する。この対応は、単なる隣接数のrandom errorより、複数座標frameの取り違えで既知4件を一つに説明できる。

低確率なのは、implicit reconstruction自体が通常は成功するためである。生成は決定的なparserではないため、同じsemantic evidenceでも、まれに正規化前のframeが出力へ漏れると推測する。

並列完了順はsalienceを変える増幅要因候補だが、既知mismatchに共通しないためroot causeとはしない。read順、C41 owner制御、terminal projection、隣接line textの選択も共通原因から外す。

この推論はmodel内部の選択frameまたはtoken確率を直接観測したものではない。`:24 / :26`と別frame値の一致が偶然である可能性は残る。

#### 次の診断proposal

次に必要なのはprompt指示の試験ではなく、coordinate representationだけを変える小さいmechanism diagnosticである。

1. semantic code内容、review要求、model、reasoning effortを固定する。
2. `multi-frame`条件では、現在と同じunnumbered sourceとraw unified diffを渡す。
3. `single-frame`条件では、同じ内容を`revision / path / one-based line / line text`のatomic recordだけで渡す。
4. numeric resultが`24 / 25 / 26`のどのframeへ一致したかを記録する。
5. `multi-frame`でmismatchを再現できた場合だけ、diff last、authority last、target source lastの順序条件を追加する。

これは外部の原因診断であり、candidate、profile、Layer 3、Layer 4を作らない。ユーザー合意を2026-07-19に受領し、次の条件で実施した。

### Coordinate representation mechanism diagnostic結果

- diagnostic root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/diagnostics/c41-f10-coordinate-frame-mechanism-20260719-r1`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- parallelism: 24
- 各条件: 135 valid
- tool use: 禁止、実測0
- oracle / expected coordinate: multi-frameのmodel-visible入力へ不在
- output: `path / line / line_text / reason`の固定JSON schema

| 条件 | valid | line `25` | line `24` | line `26` | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| multi-frame、unnumbered source + raw diff | 135 | 135 | 0 | 0 | 13,330 | 13.934秒 |
| single-frame、atomic one-based record | 135 | 135 | 0 | 0 | 14,460 | 10.465秒 |

270件すべてdiagnostic validで、retry、tool call、schema failureはなかった。multi-frameに期待座標`25`の直接記載がないことをprepare時に確認した。

固定発生率を既存implicit reconstructionの`3 / 135`と仮定すると、135件で0 mismatchとなる確率は約`4.813%`である。0 / 135から得るmismatch率のone-sided 95%上限は約`2.195%`である。この結果はrepresentation単独で同じ誤差を再現しなかったことを示すが、発生率0を証明しない。

#### 仮説の更新

`multi-frame evidenceが存在するだけでframe leakageが起きる`という単独原因仮説は支持されなかった。

実Agentのcheckpoint 135 traceを再集計すると、checkpoint前のagent messageへnumeric coordinateを保持したrunは0 / 135だった。完全なchanged line textを保持したrunも1 / 135だけだった。通常のrunは、raw evidenceをいったんcoordinateなしのsemantic findingへ圧縮し、別turnでcheckpoint coordinateを再構成していた。

縮小mechanism diagnosticは、evidenceとcoordinate出力を同じturnで直接接続した。この条件ではmulti-frameでも135 / 135 exactだった。したがって、次の原因候補は次である。

```text
delayed coordinate reconstruction after semantic compression :=
raw evidenceからsemantic findingを確定する際にcoordinate bindingを状態へ保持せず、
別turnで過去evidenceからnumeric coordinateを再構成する。
この再構成時に低確率で別coordinate frameの値が漏れる。
```

複数frameは誤った値が`:24 / :26`になる理由を説明する。semantic compression後の遅延再構成は、その漏れが低確率でだけ発生する条件候補である。どちらか一方だけをroot causeとはしない。

#### 次の診断proposal

coordinate representationを固定し、即時抽出と遅延抽出の差を一変数にする。

1. turn 1で固定evidenceを渡し、coordinateと完全なline textを含まないsemantic findingだけを返す。
2. turn 2ではevidenceを再掲せず、conversation stateから`path / line / line_text`を返す。
3. delayed multi-frameとdelayed single-frameを各135件、24並列で実施する。
4. delayed multi-frameでmismatchを再現した場合だけ、evidence完了順の診断へ進む。

これは新しい外部mechanism diagnosticである。candidate、profile、Layer 3、Layer 4は作らない。実施前gateは未承認とする。

### Mechanism diagnosticの保存と検証

- `summary.json` SHA-256: `86e0e0faf74160c4466cd369ce1fc6ab47889d0473726403c8d6044a06d33c67`
- `analysis.json` SHA-256: `6683c35520c50ca982ddad3de614f054ff6fd1696991ab31528667c951727f69`
- `manifest.json` SHA-256: `cf93aa1d2f70f30d4297dc5e663b3bec150fe46bd40238b75fd3f8be4057ffb3`
- `verification.json` SHA-256: `d5e87b748e9619b04f4d4b6da5a6f60ee00988206ec8d8219faa5917bdaa73b4`
- lossless archive SHA-256: `c7375546a86326ebe71e885a1455c76897f3d6edc57db11fec7b93dc4dcee268`

### 保存と検証

- `summary.json` SHA-256: `15f64c9826e5c3b04d9573f9a9f273c0cbe60c9d2a97688f01d62ee9421136df`
- `manifest.json` SHA-256: `881b60f5dc930e095fd8d855b2aaaf4bedaecaaefb0c187a798c5c34de4bce89`
- `verification.json` SHA-256: `d65679dcecd7bbe8aee8b5822c66cad64e5941ce8808eb9b0c624e484a580b0b`
- `seal-index.json` SHA-256: `3cdab36744425f34087f87d3d2e16577efe00d623dff28c7cda01cc1be8fb804`
- lossless archive: 31 batch、合計680,125,870 bytes
- archive後に105 valid workspaceをpruneし、3,281,940,480 bytesを回収
- 中断時のpartial workspace 5件は、lossless archiveとlocalの両方へ保存

## 対策判断への接続

原因段階が識別できた後に、次を別々に判断する。

- prompt制御で消せるrepository-wideな誤経路か。
- TaskSpecが所有するtask固有の方法条件か。
- 実運用と評価に共通するevidence interface要件か。
- modelの残存精度riskとしてrelease判断で扱うか。

診断試験のためだけに追加したcheckpoint、line表示、adapter情報を、そのままprompt candidateまたは実運用要件へ昇格させない。
