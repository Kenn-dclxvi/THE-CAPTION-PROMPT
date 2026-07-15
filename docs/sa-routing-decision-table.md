# candidate2 SA routing decision table

## Status

- artifact: `design_draft`
- design input: [`sa-routing-condition-extraction.md`](sa-routing-condition-extraction.md)
- prompt set identity: `candidate2`
- identity meaning: `baseline`を土台にしたSA利用限定版prompt set
- baseline responsibility model: `the-caption-3ce91a4-current-r2`
- scope: 実装完了後のaudit / review SA起動条件
- implementation SA routing: 変更しない
- candidate作成: 未実施
- evaluation profile変更: 未実施
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

## 設計目的

`candidate2`は`baseline`が持つpermission、作業単位、実装SA、独立worker、完了判定の境界を維持したまま、成果全体の確認に不要なaudit / review SAを起動しないprompt setとする。

狙う変更はSA利用回数の削減であり、required machine validation、変更scope、禁止操作、drift確認を弱めることではない。

prompt setの呼称は`baseline`、`candidate1`、`candidate2`とする。評価基盤のcondition labelは実行時の比較条件を表す別の識別子であり、将来の比較profileでは各condition labelへ固定したprompt identityをbindする。

## 非対象

- 親へ直接実装を許可すること
- 実装SAの起動条件を変更すること
- `candidate1`のsingle root、ordered gate、identity model、stub構造を移植すること
- test commandやrequired validationを削減すること
- audit / reviewの指摘分類やrework上限を変更すること
- evaluation foundationのLayer、KPI、schemaを変更すること

## Routing output

実装後のnon-machine completion routeは次の4つだけとする。

| route | 必要なSA | 意味 |
| --- | --- | --- |
| `none` | なし | machine evidenceとdrift確認だけで今回のdoneを判定できる |
| `audit` | audit SA | 契約、authority、scope、invariantの独立照合が必要 |
| `review` | review SA | runtime correctness、利用者影響、state safetyなどの独立品質確認が必要 |
| `audit+review` | audit SAの後にreview SA | 契約riskとquality riskの両方がある |

`review`は単独routeとして認める。`candidate1`のように常にaudit成功をreviewの前提にはしない。`audit+review`の場合だけ、auditの停止指摘0件をreview起動条件とする。

## 固定入力

routingは実装開始前にTaskSpecへ次を固定して決める。

| input | 値 |
| --- | --- |
| `task_kind` | `implementation` / `boundary_disposition` / `non_destructive_review` |
| `change_class` | `python` / `node` / `test` / `shell` / `docs` / `ai_control` / `dependency` / `config` / `mixed` |
| `machine_coverage` | `direct` / `partial` / `not_applicable` |
| `contract_risk_flags` | 下記C1からC4の集合、または空集合 |
| `quality_risk_flags` | 下記Q1からQ5の集合、または空集合 |
| `explicit_independent_check` | `none` / `audit` / `review` / `audit+review` |
| criterion | 各SAが判定する固定criterion。routeが`none`なら不要 |
| owner | `independent_contract_check` / `independent_quality_check`。routeが`none`なら不要 |

`line_count`や単純な変更file数はrouting inputにしない。一行変更でもrisk flagがあればSAを起動し、複数fileでもrisk flagがなくmachine coverageが`direct`なら`none`を選択できる。

## Contract risk taxonomy

| flag | 条件 | 主な例 |
| --- | --- | --- |
| `C1_authority_permission` | authority、permission、許可operation、scope boundaryを変更または解釈する | `AGENTS.md`、deploy permission、write boundary |
| `C2_public_contract_invariant` | public interface、schema、CLI routing、dependency provenance、paired invariantを変更する | shell alias、`.in / .txt`、serialized schema |
| `C3_test_validation_contract` | test、required gate、assertion、expected resultの妥当性が成果の一部になる | regression test修復、test scope変更 |
| `C4_reference_control_consistency` | docs、AI制御文書、正規command、referenceとsourceの整合を扱う | command reference、prompt control文書 |

いずれかのcontract risk flagがあれば、少なくとも`audit`を要求する。

## Quality risk taxonomy

| flag | 条件 | 主な例 |
| --- | --- | --- |
| `Q1_high_impact_behavior` | security、credential、production、外部送信、金額計算、report内容、データ破壊へ影響し得る | send flag、financial total、secret handling |
| `Q2_state_failure_recovery` | persistence、atomicity、cleanup、failure path、concurrency、retry、state transitionを変更する | atomic save、rollback、partial failure |
| `Q3_cross_layer_interface` | 複数layer、caller / callee、public interfaceを跨ぐruntime behaviorを変更する | appからdomainへのdate伝播 |
| `Q4_user_visible_uncovered` | user-visible behaviorを変更し、required machine gateがその意味を直接検証しない | UI表示条件、message、formatting |
| `Q5_machine_coverage_gap` | implementation taskだが、doneの中核behaviorに対するmachine coverageが`partial`または存在しない | generic buildだけが通る意味的変更 |

いずれかのquality risk flagがあれば、少なくとも`review`を要求する。

## `machine_coverage`の定義

| 値 | 条件 |
| --- | --- |
| `direct` | required machine commandが変更対象の中核behaviorと主要regressionを直接検証する |
| `partial` | syntax、build、広いtestは通るが、変更した意味またはfailure pathを直接検証しない |
| `not_applicable` | boundary disposition、read-only review、docsなど、実行可能なmachine behavior gateを要求しない |

runtime behaviorを変更する`python`、`node`、`shell`、`dependency`、`config`、またはそれらを含む`mixed`で、`machine_coverage=partial`の場合はQ5を自動付与する。これらのclassで`not_applicable`を使う場合もQ5を自動付与する。

`docs`と`ai_control`はmachine behavior gateが`not_applicable`でもよいが、既定のcontract riskによるauditを省略しない。

## Decision table

### 先行route

| 条件 | route | 理由 |
| --- | --- | --- |
| `task_kind=boundary_disposition` | `none` | clarificationまたはout-of-scope terminal自体が成果であり、実装後workerは存在しない |
| `task_kind=non_destructive_review` | `none` | task自体がreviewであり、同一成果への追加reviewを既定で重ねない |
| boundary / permissionが未確定または否定 | 実装開始前に停止 | SA routingで不足や禁止を補完しない |
| required machine validationがfailed / unavailable | audit / reviewを起動せず停止 | non-machine確認でmachine failureを代替しない |

`non_destructive_review`へ独立したsecond opinionが明示要求された場合だけ、`explicit_independent_check=review`としてreview SAを追加できる。

### Implementation route

machine coverageからQ5を導出した後、最終的なrisk flagの有無でrouteを一意に決める。

| contract risk | quality risk | route |
| --- | --- | --- |
| なし | なし | `none` |
| あり | なし | `audit` |
| なし | あり | `review` |
| あり | あり | `audit+review` |

runtime behaviorを変更するclassでmachine coverageが`partial`または`not_applicable`ならQ5が付くため、最終表で`none`にはならない。

`explicit_independent_check`は表のrouteを同じ方向または強い方向へ上書きできるが、既存riskが要求するaudit / reviewを削除できない。

## Precedence

routing conflictは次の順に解決する。

1. boundary、permission、禁止operation。実行不可なら停止する。
2. `task_kind`の先行route。
3. 明示されたindependent check要求。
4. contract risk flags。
5. quality risk flagsとmachine coverage gap。
6. change classの既定flag。

下位条件は上位条件が要求したSAを削除できない。複数条件がある場合は和集合を取り、`audit+review`を上限とする。

## Change classの既定flag

| change class | 既定flag | 補足 |
| --- | --- | --- |
| `python` | なし | behaviorに応じてQ1からQ5を付与する |
| `node` | なし | user-visible意味をbuild / lintが直接検証しない場合はQ4またはQ5 |
| `test` | C3 | test自体が契約になるためaudit |
| `shell` | C2 | launcher、alias、operation routingをcontractとして扱う |
| `docs` | C4 | source / reference整合をauditする |
| `ai_control` | C1とC4 | authorityとcontrol consistencyをauditする |
| `dependency` | C2 | constraint、pin、provenanceのinvariantをauditする |
| `config` | なし | permission、external side effect、public contractに応じてC1、C2、Q1を付与する |
| `mixed` | 含まれるclassとrisk flagの和集合 | SAは種類ごとに最大1つとし、同種workerを重複起動しない |

## 一行・局所変更の扱い

一行または単一fileという事実だけでは`none`にしない。次をすべて満たす局所implementationだけが`none`候補になる。

- `machine_coverage=direct`
- contract risk flagが空
- quality risk flagが空
- authority、permission、test、schema、dependency、CLI/public interfaceを変更しない
- production、外部送信、security、credential、金額、永続化、failure recovery、user-visible未検証behaviorへ影響しない
- required validation成功と許可外driftなしを確認できる

この条件を満たさない場合は変更行数に関係なくrisk tableへ従う。

## 実装後のescalation

実装開始前にrouteを固定するが、実際のdiffまたはmachine resultから定義済みrisk flagが新たに確認された場合はrouteを強い方向へだけ変更できる。

- `none`から`audit`、`review`、`audit+review`
- `audit`または`review`から`audit+review`

実装後にriskを再解釈してSAを削除してはならない。route変更時は追加したflag、根拠artifact、criterion、ownerを最終結果へ残す。

## Worker sequencing

| route | sequence |
| --- | --- |
| `none` | implementation SA → required machine validation → drift確認 → parent completion |
| `audit` | implementation SA → required machine validation → audit SA → drift確認 → parent completion |
| `review` | implementation SA → required machine validation → review SA → drift確認 → parent completion |
| `audit+review` | implementation SA → required machine validation → audit SA停止指摘0件 → review SA → drift確認 → parent completion |

audit / reviewのblocking findingが許可scope内で最小修正可能な場合のreworkは`baseline`の既存規則へ従う。SAを省略したことを理由に親がauditまたはreviewを代行しない。

## Case mappingによるdesign check

この対応はevaluation resultではなく、decision tableが既存caseをどのrouteへ分類するかの設計確認である。

| case | flags / coverage | route |
| --- | --- | --- |
| F01 duplicate asset key | direct、flagなし | `none` |
| F02 cross-layer date bound | C3、Q3、direct | `audit+review` |
| F03 atomic cleanup | Q2、direct | `review` |
| F04 UI visibility | Q4、partial | `review` |
| F05 clarification | boundary disposition | `none` |
| F05 out-of-scope deploy | boundary disposition | `none` |
| F06 regression test restoration | C3、direct | `audit` |
| F07 shell runner | C2、direct | `audit` |
| F07 dependency provenance pair | C2、direct | `audit` |
| F08 CLI reference sync | C4、not applicable | `audit` |
| F10 entrypoint inventory | non-destructive review | `none` |
| F10 monthly diff review | non-destructive review | `none` |

## Required routing evidence

親は最終結果へ次を残す。

- selected route
- `task_kind`と`change_class`
- `machine_coverage`
- contract / quality risk flags
- 起動したSAと起動しなかったSA
- `none`または`not_applicable`の根拠
- 実装後escalationの有無と根拠
- required machine resultとfinal drift identity

このrouting evidenceは実行artifactであり、評価基盤のKPIやLayerを増やすものではない。

## Design acceptance

このdecision tableがcandidate仕様へ進む前に、少なくとも次を確認する。

- 4 routeが相互排他的に一つへ決まる。
- `none`が変更量だけで選ばれない。
- machine failureをaudit / reviewで代替しない。
- auditとreviewの責務が混ざらない。
- task自体がreviewの場合に重複reviewを既定起動しない。
- `baseline`の実装SA、permission、required validation、rework、terminal境界を変更していない。

## このartifactの境界

この文書はSA routingの設計draftである。prompt bundle、candidate identity、評価profile、採用判断を生成しない。
