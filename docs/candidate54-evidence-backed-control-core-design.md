# Candidate54 evidence-backed control core設計記録

## 結論

Candidate54はCandidate43を直接sourceとし、root `AGENTS.md`一枚だけを変更する。

常時読む制御を、A系readiness、F系fixed operation、明示委譲時だけのD系へ分ける。Candidate43の各文を短く言い換えるのではなく、保存済み実績で必要性を確認できた関係だけを残す。

## Candidate作成前gate

1. control-freeな最短正常経路は、TaskSpecでrequired outcomeが確定していればrootが一つのproducerとしてrequired predicateを実行し、全terminal resultが揃った時点で完了する経路である。未確定値がある場合だけ、その値を質問して停止する。
2. 保存済みの誤経路は、C42がA01で未固定値を補集合から推測したこと、C30以前がchild resultのruntime identityを誤認したこと、C31以前がrequired command result不足のまま完了を宣言したこと、C33が`false / failed`を別resultの失効へ伝播したことである。
3. TaskSpecはrequired outcome、permission、allowed path、required validation、停止条件を定める。一方、result欠落をfinal responseで補わないこと、同一operationを別producerへ再割当てしないこと、委譲resultを実runtime identityへbindすることはTaskSpecだけでは固定しない。
4. C43の`F1 / F5 / F9`、9項目packet、`R1 / R2`には、それぞれを単独変更した互換比較がない。既存caseのTaskSpecはoperation対象とpermissionを既に列挙し、recoveryは`0`または`not_applicable`であり、正のrecovery cycleを観測していない。これらを常時制御として残す根拠は不足している。
5. C30では実runtimeの`task_name`と`FINAL_ANSWER.Sender`へ合わせた後、targeted 25件、expanded 60件、continuous 300件でowner証跡不成立が0件だった。D系ではこのprovenance predicateを保持する。
6. C11では明示packetとcontext sufficiency境界を追加したF07で、10 / 10 spawnが`fork_turns=none`となり、score `4`を維持した。ただし後の9項目すべての単独効果は未確認である。Candidate54は未解決predicate、target、required evidence、allowed read、forbidden inputだけを最小packetとする。
7. C53は目的見出しを分けたが、F10のtool callとmodel stepがC43より増えた。同じcall数のtokenは同等だったため、次の変更対象は文量ではなく、常時評価するpredicate数である。

このgateにより、Candidate54の作成を許可する。recovery制御の必要性は否定せず、正のrecovery caseを作る別変更へ分離する。

## 変更するgraph

```text
A readiness
  authority -> unresolvedならclarification / resolvedならFへ

F fixed operation
  TaskSpec outcome -> one producer -> all terminal results -> terminal
                         |                    |
                         +-- no reassignment +-- no response fill
  result stateはoperation内に閉じる
  method failureとpermission denialを分ける

D explicit delegation only
  explicit producer requirement -> minimal packet -> runtime provenance
                                         |              |
                                         + context      + rootは補完しない
```

## 保持・統合・除外

| 対象 | Candidate54の処置 | 根拠 |
| --- | --- | --- |
| `A1..A4` | `Readiness`へ保持・統合 | A01 / A02で開始可否の差を観測済み |
| `F2 / F3 / F6 / F7 / F8` | `Fixed operation`へ保持 | C28、C31、C34の誤経路へ直接対応 |
| `F1` | TaskSpecで確定したoutcome単位という入口だけ残す | predicate / owner / permission / constraintの再列挙はTaskSpecと重複 |
| `F5` | `F3`の再割当て禁止へ統合 | 新TaskSpec化の単独効果は未確認 |
| `F9` | 常時制御から除外 | 独立確認を追加する条件自体はTaskSpecに委ね、同一operationの再割当ては`F3`で禁止 |
| `D1..D5 / D7` | 明示委譲時だけ保持・統合 | C30のruntime provenanceとC11のcontext sufficiencyを保持 |
| `D6` | 5項目packetへ縮小 | 9項目すべての単独効果は未確認 |
| `M1..M4` | `Fixed operation`へ保持・統合 | C23が対象にしたinvocation failureとpermission denialの分離 |
| `R1 / R2` | Candidate54から除外し別caseへ送る | 正のrecovery cycleが現Evaluation setにない |

## 静的差分

変更対象はroot `AGENTS.md`だけである。残り18 targetはCandidate43とbit identityを保つ。

- Candidate43 root: `3,980 bytes`
- Candidate54 root: `2,525 bytes`
- 差: `-1,455 bytes`、`-36.56%`

byte数はtoken数や実行効率を意味しない。成果判定には使わない。

## 評価gate

1. bundle identity、単一target差分、必要graph、除外predicateを構造testで確認する。
2. capability catalog固定済みのF05 / F10を各`N=5`でC43と比較する。
3. F05 / F10でscore `4`、root-only、zero driftを維持し、F10のmodel step、tool call、token合計がC43以下ならA01 / A02へ進む。
4. A01は未確定値を質問して変更しないこと、A02はrepository authorityから解決して不要な質問をしないことを確認する。
5. 明示委譲の正のcaseは現行standard caseにない。新caseを作る場合はCandidate54評価と混ぜず、TaskSpec revisionを別にする。

F系で停止条件に該当した場合、Candidate54へ文を追加しない。候補は停止し、route traceから次の一つの誤経路を特定する。

## 対象試験結果

2026-07-21にcapability catalog固定済みのF05 / F10を各`N=5`で実行した。Candidate54は10 / 10でscore `4`、root-only、zero driftだった。

Candidate43比でF05 token合計は`-16.46%`だった。一方、F10はmodel step `48 -> 53`、tool call `43 -> 48`、token合計`+9.44%`、elapsed中央値`+18.31%`だった。10 run全体のtoken合計も`+2.18%`だった。

停止条件に従い、Candidate54は`catalog_fixed_targeted_n5 / stopped`とする。A01 / A02、standard14、A06、採用、release、本体反映へ進めない。Candidate54へ補助文を追加しない。詳細は[`Candidate43 / Candidate54対象試験`](../evaluations/results/candidate43-candidate54-evidence-backed-control-core-catalog-fixed-targeted-n5_2026-07-21.md)に記録する。
