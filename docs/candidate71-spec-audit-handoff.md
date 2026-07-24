# Candidate71 `SPEC`監査 引継ぎ指示書

> [!IMPORTANT]
> この文書はCandidate71 `SPEC`監査の**完了済み引継ぎ指示書**であり、当時のbranch・HEAD・working tree・実行手順を含む履歴artifactである。監査結果は[`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)へ統合済みで、現在の結論と監査状況の分類はそちらを正とする。以下は引継ぎ当時の記述として保持する。

## 次タスクの目的

Candidate71のroot `AGENTS.md`にある`SPEC`一行だけを、表現ではなく制御機能へ分解して監査する。

目的は短文化ではない。各句が保存済みのどの誤経路を防ぎ、TaskSpec、repository authority、repository stateだけではなぜ防げないかを確認する。

監査結果から一つの削除または置換predicateを導けない場合は、Candidate74を作らず「変更根拠なし」で終了する。

## 作業開始位置

- repository: `/Users/kenn/repos/THE-CAPTION-PROMPT`
- branch: `main`
- 引継ぎ作成時HEAD: `2113ed247a0060f4b68846ced2188a420ff17ea8`

状態は変わり得るため、次タスクは最初に次を実行してlive値を使用する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

working treeには既存の未commit差分と未追跡artifactがある。これらは現在までの作業成果である。`reset`、`checkout`、削除、別worktreeへの移動を行わない。変更する場合は対象pathを限定する。

commit、push、PR、merge、release、THE-CAPTION本体反映は依頼されていないため実施しない。

## 現在の確定事項

1. Candidate71はCandidate69へ`VALIDATION_CLOSURE`一行だけを追加したcandidateである。
2. Candidate71のB18効率差は保存するが、A02のrequired validation欠落3件とA01の未確認実装1件があり、`standard14_b18_evaluated / stopped`である。
3. Candidate72はOPEN / CLOSED抽象へ置換したが、F06のmodel再入とtokenが増えて停止した。
4. Candidate73はterminal tool closureを残したが、F06の編集後model再入中央値が`2 -> 3`となり停止した。
5. `VALIDATION_CLOSURE`は次タスクで変更しない。
6. `OWNER_ROLE`監査は完了した。各句に実誤経路があり、Candidate49の広い圧縮もtoken増加で停止したため変更しない。
7. Candidate74は存在しない。`SPEC`監査が終わるまでbundle、profile、evaluation runを作らない。

## 正本prompt

- prompt identity: `the-caption-3ce91a4-validation-closure-r1`
- bundle SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- root prompt: `prompts/candidates/the-caption-3ce91a4-validation-closure-r1/files/AGENTS.md.txt`
- manifest: `prompts/candidates/the-caption-3ce91a4-validation-closure-r1/manifest.json`

監査対象は次の一行だけである。

```text
- SPEC: 実行前にrequired outcomeをoperation identityへ分け、`predicate / criterion owner / permission / constraint`をTaskSpecへ固定する。`spec_ready := TaskSpecへ固定する全値が、明示user inputまたはrequested outcome valueを直接要求する一意なrepository authorityへbind済み`。current value / option set / complement / test expectation / implementation convenienceはrequested outcome valueをbindしない。`spec_ready=false`の間はproducer binding / predicate実行 / artifact変更 / testを開始しない。repository authorityからbindできない未固定値だけをclarification resultにする。`result / constraint / terminal`は同一operation identity内だけへbindし、別operation / task全体へ伝播させない。
```

## 必ず先に読む文書

次の順で読む。

1. [`AGENTS.md`](../AGENTS.md)
2. [`Prompt制御の検討原則`](prompt-control-design-principles.md)
3. [`Candidate71 control abstraction分析`](candidate71-control-abstraction-analysis.md)
4. [`Candidate43 control element分類`](candidate43-control-element-classification.md)
5. [`Candidate42 A01 / A02結果`](../evaluations/results/candidate42-spec-readiness-boundary-ambiguity-targeted2-n5_2026-07-20.md)
6. [`Candidate43 A01 / A02結果`](../evaluations/results/candidate43-outcome-authority-boundary-ambiguity-targeted2-n5_2026-07-20.md)
7. [`Candidate61 atomic SPEC設計`](candidate61-atomic-spec-operation-gate-design.md)
8. [`Candidate43 / Candidate55 / Candidate61結果`](../evaluations/results/candidate43-candidate55-candidate61-atomic-spec-operation-gate-catalog-fixed-targeted-n5_2026-07-21.md)
9. [`Candidate34 result state separation`](../evaluations/results/candidate34-owner-result-state-separation-owner-producer-v5-targeted2-expanded12-n5_2026-07-18.md)
10. [`Candidate69 / Candidate71 v12 B18`](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)

非公開のraw run logはrepositoryへ取り込まない。既存のappend-only resultと圧縮済みevidenceで不足する場合だけ、外部archiveをread-onlyで確認する。

## `SPEC`の仮分解

以下は監査開始用の仮分類であり、結論ではない。

| ID | 句 | 現時点の意味 |
| --- | --- | --- |
| `S1` | required outcomeをoperation identityへ分け、predicate / owner / permission / constraintを固定 | 確定済みoperationの開始単位 |
| `S2` | user inputまたはrequested outcomeを直接要求する一意なauthorityだけで`spec_ready`を成立 | outcome authority |
| `S3` | current value、option set、complement、test expectation、implementation convenienceを根拠にしない | 誤った補完のnegative boundary |
| `S4` | `spec_ready=false`ではproducer、predicate、変更、testを開始しない | Strictな開始gate |
| `S5` | authorityから固定できない未固定値だけを質問する | clarification boundary |
| `S6` | result / constraint / terminalを同一operationへ閉じる | operation間の非伝播 |

監査では`S2 + S3 + S4 + S5`をauthority readiness、`S1 + S6`をfixed operationとして分けて検討する。一つの`SPEC`という名前を前提に結論を作らない。

## 既知の証拠

### Authority readiness

- Candidate42は開始禁止を追加したが、A01の5 / 5でcurrent valueの補集合を変更後値と推測し、質問前に編集と試験へ進んだ。
- Candidate43は変更後値をbindできるauthorityを直接要求する規則へ限定した。A01は5 / 5で編集・試験前に質問し、A02は5 / 5でrepositoryから正規targetを解決した。
- Candidate71 B18では、A01の1件が未固定modeを確認せず実装・試験へ進んだ。したがってStrictなauthority gateは解決済みとは扱わない。

### Fixed operation

- Candidate34は、あるcriterionの`false / failed`を別operationの成立済みresultへ伝播させる経路を分離した。
- Candidate61はCandidate55の`READINESS`と`OPERATION`をCandidate43のatomic `SPEC`へ戻した。A01 / A02は10 / 10 score `4`だったが、F10の短経路は戻らず、tool callとtokenがCandidate43を超えて停止した。
- したがって、`SPEC`を一つへまとめること自体をKPI改善の原因としない。反対に、分割すれば効率化すると仮定しない。

## 実施手順

### 1. Identityと差分scopeを確認する

- live branch、HEAD、statusを記録する。
- Candidate71 bundleを`verify_bundle`で検証する。
- 監査対象の`SPEC`一行が上記正本と一致することを確認する。

### 2. 六句を保存済み誤経路へ対応付ける

各`S1..S6`について次を表にする。

| 項目 | 必須内容 |
| --- | --- |
| 句 | 正本の対象部分 |
| 防ぐ誤経路 | 保存traceで起きた具体的事象 |
| TaskSpec等で防げない理由 | TaskSpec、repository authority、repository stateとの差分 |
| 増やす判断点 | identity、binding、negative list、clarificationなど |
| 観測結果 | quality、token、tool call、model step、routing |
| 判定 | `retain` / `merge` / `move` / `review` |

事実、推測、提案を列で混ぜない。

### 3. Strict制御と実行効率を分ける

- `S2..S5`は、未固定値を推測せず質問するStrict境界として評価する。
- `S1 / S6`は、operation bindingと失敗伝播の境界として評価する。
- A01の未確認実装をtoken削減と相殺しない。
- Candidate61のruntime不通過を、`S1 / S6`の意味が不要という証拠へ読み替えない。

### 4. 重複または移動候補を一つだけ探す

優先して確認する関係は次である。

- `S1`と`PRODUCER`のoperation / producer bindingの重複。
- `S6`と`TERMINAL`、`OWNER_ROLE`のresult state / 補完禁止の重複。
- `S2`と`S3`を一つのauthority predicateへ統合してもnegative boundaryを失わないか。
- criterion ownerを`SPEC`で常時固定する必要があるか。明示委譲時の`OWNER_ROLE`だけで足りるか。

移動して同じ判断を別labelで読むだけなら、削減候補としない。

### 5. 監査結果を正本へ追記する

[`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)へ`SPEC監査結果`を追記する。

追記には次を必須とする。

- 一文の結論。
- `S1..S6`の証拠対応表。
- 何が構造で、何が表現上の過積載か。
- Candidate74を作る根拠があるか。
- 根拠がない場合、次に監査するlabel。

## Candidate74を作成できる条件

次の九項目をすべて定義できた場合だけ、別タスクで作成前gateを検討する。

1. 基準prompt identity。
2. control-freeまたはCandidate71での最短正常経路。
3. 保存traceで確認した一つの誤経路。
4. TaskSpec、repository authority、repository stateだけでは防げない理由。
5. 削除または置換する一つのpredicate。
6. そのpredicateが消す具体的な判断点。
7. 新しく増える判断、参照、例外。
8. quality、token、elapsed、tool call、model step、routingの期待。
9. 期待と逆なら補助文を追加せず停止する条件。

一つでも未定義ならCandidate74 bundle、profile、evaluation set、runを作らない。

## やらないこと

- `VALIDATION_CLOSURE`、`OWNER_ROLE`、評価基盤v3の固定点を変更しない。
- Candidate72 / 73を修正または再評価しない。
- 既存result、profile、bundle、ratingをin-place変更しない。
- A01のStrict境界を「現在値の反対を選ぶ」などのcase固有規則へ置換しない。
- prompt byte数だけを削減効果としない。
- quality中央値で低scoreまたはrequired validation欠落を隠さない。
- 新しい評価caseやrating revisionを同じ変更単位へ混ぜない。
- 明示依頼なしにcommit、push、PR、merge、release、本体反映を行わない。

## 完了条件

次タスクは次の状態で完了する。

1. Candidate71 bundle identityが確認済み。
2. `S1..S6`が保存済み根拠へ対応付けられている。
3. Strict境界とruntime効率が別々に判定されている。
4. [`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)へ`SPEC監査結果`が追記されている。
5. Candidate74について`作成根拠あり`または`作成根拠なし`を一つだけ結論にしている。
6. `git diff --check`が通っている。

文書だけを変更した場合はrepository全testを必須にしない。bundle、profile、scriptへ触れた場合は、変更scopeに応じたtestと全体testを実行する。

## 最初に返すべき進捗

次タスク開始時は、次の一文を先に示す。

> Candidate71の`SPEC`だけを監査します。まず六つの句をStrictなauthority readinessとfixed operationへ分け、保存済み誤経路との対応がない句はCandidate化せず報告します。
