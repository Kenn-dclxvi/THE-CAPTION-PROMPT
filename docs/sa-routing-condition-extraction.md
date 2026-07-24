# candidate1からのSA起動条件抽出

## Status

- artifact: `design_input`
- source prompt: `the-caption-9b3a96a-revision-2-r1`
- source prompt set: `candidate1`
- target of later design: `candidate2`（`baseline`を土台にしたSA利用限定版prompt set）
- candidate作成: 未実施
- `baseline` / `candidate1` prompt変更: 未実施
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

## 目的

`candidate1`が持つconditional audit / reviewから、`candidate2`を設計するための条件を抽出する。ここでは条件の出典、明示度、未定義部分を分離し、新しいrouting ruleをまだ決定しない。

## Source boundary

主な抽出元は次である。

- `prompts/candidates/the-caption-9b3a96a-revision-2-r1/files/AGENTS.md.txt`
- `prompts/candidates/the-caption-9b3a96a-revision-2-r1/files/prompts/audit.md`
- `prompts/candidates/the-caption-9b3a96a-revision-2-r1/files/prompts/review.md`
- 現行evaluation caseの`trial-prompt-input.json`に固定したTaskSpec field

`candidate1`のsingle root、ordered gate、identity binding全体を採用済み設計とは扱わない。評価結果から観測された挙動と、prompt本文が明示する規則も混同しない。

## 抽出結果の要約

`candidate1`から直接再利用できるのは、SA起動を決める完成済みdecision tableではなく、次のrouting構造である。

1. TaskSpecに`task kind`、変更class、machine validation、`non_machine_risk`、criterion、ownerを固定する。
2. boundary / permissionまたはrequired machine gateで継続不能なら、後段workerを起動せず停止する。
3. 変更classに不要なgateは追加せず、最小のcompletion sourceだけを選ぶ。
4. non-machine completionが必要な場合だけaudit / reviewを別execution identityで起動する。
5. workerはartifact、permission、counter、gate status、terminalを所有しない。

一方、`candidate1`は`audit / reviewはpredicate true時だけ起動する`と定めるだけで、`predicate true`を決めるclosedな条件表を定義していない。

## 実装SAに関する抽出限界

`candidate1`はrootと`active executor`を区別して記述するが、`prompts/implement.md`はruntime controlを持たない互換性stubであり、独立した実装SAの起動predicateを定義していない。

したがって`candidate1`から直接抽出できるのは、主にactive execution後のaudit / review workerを条件化する構造である。`baseline`で親の直接実装を許可するか、実装SAを維持するかは、`candidate1`の条件抽出から自動的には決まらない別の設計判断とする。

## candidate1に明示されている条件

| 条件入力 | candidate1に明示された扱い | SA routingへの意味 |
| --- | --- | --- |
| `task kind`が`clarify`または`out_of_scope_stop`へrouteされる | `execute`へ進まず単一terminalを返す | operation後のaudit / reviewは起動対象にならない |
| boundary / permission gateが後段を許可しない | その時点で停止し、不要な後段を実行しない | audit / reviewを起動しない |
| required machine completionが`failed`または`unavailable` | 成功へ読み替えず停止する | non-machine workerへ進まない |
| 変更classにgateが該当しない | 該当しないgateを追加しない | SAを常時起動する根拠にしない |
| docs / AI制御文書の変更 | valid contract auditを要求する | audit起動が明示的にrequired |
| non-machine completionにcriterionとownerがある | TaskSpecに固定したcriterion / ownerへ従う | 独立workerを使う入力が存在する |
| audit / reviewのpredicateがtrue | auditを実行し、valid auditで`contract_stop=0`の場合だけfresh reviewへ進む | `candidate1`ではreviewがauditへ依存する |
| audit / reviewを起動する | active executorと別execution identityへbindする | 起動時の独立性を必須にする |
| audit / review findingが残る | 許可scope内のstop / blockerだけをbounded reworkへ送る | worker起動後の再実行条件であり、初回起動条件ではない |

## SA起動判定へ利用できるTaskSpec field

| field | candidate1での用途 | 抽出上の状態 |
| --- | --- | --- |
| `task kind` | execute、clarify、out-of-scope、非破壊reviewなどのroute | 明示済み |
| goal / done | completion対象の固定 | 明示済み |
| allowed / forbidden changes | permissionとdrift判定 | 明示済み |
| validation | required machine completionの選択 | 明示済み |
| `non_machine_risk` | non-machine completionの必要性を表現 | fieldは明示済み、値のtaxonomyは未定義 |
| criterion | audit / reviewが照合する対象 | 必要性は明示済み、必須条件は未定義 |
| owner | independent checkの所有者 | 必要性は明示済み、owner vocabularyは未定義 |
| change class | Python、Node、docs、dependency、mixedのgate選択 | 一部だけ明示済み |
| operation permission | 後段へ進めるかの先行gate | 明示済み |
| machine result | non-machine gateへ進む前提 | 明示済み |

## 現行caseから見える入力例

この表は新しいrouting ruleではない。現行caseが`candidate1`へ渡したTaskSpec入力を、抽出したfieldへ対応付けたものである。

| case群 | `task kind` / change class | `non_machine_risk` | owner | candidate1規則から読み取れる候補経路 |
| --- | --- | --- | --- | --- |
| F01 | Python implementation | `none` | なし | machine completionだけで閉じる候補。ただし`candidate1`本文は`none`時のskipを明文化していない |
| F02 / F06 / F07 | cross-layer、test contract、shell routing | `test-contract`または`contract-consistency` | independent contract check | machine completion後のcontract audit候補。review併用条件は未定義 |
| F03 | mocked-I/O safety state | `safety-state` | independent state check | machine resultだけで残存riskを閉じられない場合の独立確認候補 |
| F04 | Node / caller-visible UI | `caller-visible UI behavior` | independent source check | Node gate後のsource behavior確認候補 |
| F05 clarify / out-of-scope | boundary disposition | missing policy、operation boundary | independent boundary check | terminal route自体を評価し、実装後audit / reviewは行わない候補 |
| F07 dependency pair | dependency paired invariant | `paired dependency provenance` | independent contract check | static machine assertionと契約確認の組合せ候補 |
| F08 / F09 | docs / AI制御文書 | `contract-consistency` | independent contract check | `candidate1`が明示的にauditを要求するclass |
| F10 inventory / diff review | read-only / non-destructive review | response quality、review accuracy | independent response check | task自体がreviewであり、post-task audit / reviewとの関係は未定義 |

## 明示条件と推定を分離した暫定表

| 状態 | audit | review | 根拠の強さ |
| --- | --- | --- | --- |
| clarify / out-of-scope terminal | 起動しない | 起動しない | `candidate1`のshort-circuitから明示的に導ける |
| required machine gateがfailed / unavailable | 起動しない | 起動しない | `candidate1`のordered gateに明示 |
| docs / AI制御文書変更 | 起動する | 未定義 | auditだけ明示 |
| `non_machine_risk=none`かつmachine gate完了 | 起動しない候補 | 起動しない候補 | minimal completionとconditional記述からの推定であり、明文なし |
| criterion / owner付きnon-machine risk | predicate判定対象 | auditがvalidな場合のpredicate判定対象 | fieldは明示、predicateの真偽条件は未定義 |
| task自体がnon-destructive review | post-task auditは未定義 | task executionとreview workerの関係が未定義 | `candidate1`に専用routing規則なし |
| mixed change | 各classのgate和集合 | 各classのgate和集合 | unionは明示、SAの重複排除は未定義 |

## candidate1からそのまま移植できる設計要素

- TaskSpecへmachine / non-machine completionを分けて固定する。
- `non_machine_risk`だけでなくcriterionとownerを同時に要求する。
- 先行gateが継続を許可しない場合は不要なworkerを起動しない。
- 変更classに該当しないgateを追加しない。
- workerをactive executorと別execution identityへbindする。
- workerへedit、permission、terminal ownershipを与えない。
- findingからのreworkを許可scope内へ限定する。

## candidate1固有として分離すべき要素

次はSA限定化の条件そのものではなく、`candidate1`の広いexecution architectureである。`baseline`への条件移植と同時に採用しない。

- single root authorityへの全面移行
- 旧role promptの互換性stub化
- ordered gate全体のstatus model
- candidate prompt path / blobを含む厳密なinput identity binding
- machine / environment / non-machine rework counter全体
- rollbackとpackage lifecycleの規則

F10で観測した開始identity誤認はこの広いidentity / gate経路で発生しており、conditional audit / reviewの有効性とは分けて扱う。

## 未定義で、次の設計が必要な条件

1. `non_machine_risk`のclosed vocabularyと、`none`を認める条件。
2. `none / audit / review / audit+review`を選ぶ決定表。
3. auditだけで完了できる条件と、reviewを必須にする条件。
4. reviewを必ずaudit後にするか、review-only pathを認めるか。
5. task kind、change class、risk、permissionが競合した場合の優先順位。
6. 一行・単一fileでもsecurity、production、データ破壊、金額計算、authority変更などを高riskへ上げる条件。
7. cross-layer、public interface、schema、dependency、user-visible behaviorをどう分類するか。
8. task自体がreviewの場合に、追加review workerを起動しない条件。
9. `not_applicable`を誰が確定し、最終結果へどのevidenceを残すか。
10. SAを起動しなかった判断を、評価時にどう観測可能にするか。

## このartifactの境界

この文書は`candidate1`から条件を抽出した設計入力であり、`candidate2`のcandidate仕様ではない。次工程では未定義10項目をdecision tableとして決定し、その後に初めてcandidate revisionと評価profileを別artifactとして作る。
