# Candidate63 fixed evidence route projection設計記録

## 結論

Candidate63はCandidate43を唯一の共通prompt sourceとし、固定証拠reviewでだけ使う一つのmethod差分を実行前に合成する。

二つのroot `AGENTS.md`をauthoring sourceとして保守しない。route差分を見せないtaskではCandidate43をそのまま使い、固定証拠reviewだけがCandidate43と差分からmaterializeしたfull bundleを使う。modelが一回の実行で読むroot `AGENTS.md`は常に一枚である。

## Candidate作成前gate

1. 基準prompt setはCandidate43である。F10の最短正常経路は、固定済みworkspace identityを確認し、列挙済みの固定diff、authority、2 source fileを取得し、zero driftのreview resultを返す経路である。A02はCandidate43の通常経路でrepository authorityからcanonical targetを解決し、`run.sh`だけを変更して必要な検証を完了する。
2. 保存済み誤経路はCandidate62のA02である。同じ常時可視`AGENTS.md`へ固定read方法と非適用条件を置くと、5 run中4件でC56型の並行取得が変更taskへ流入した。F05も2 / 5で成果に不要なsource readを追加した。
3. TaskSpec、repository authority、repository stateはA02が変更task、F05がclarification taskであることを示していた。それでもmodel-visibleなmethod本文があると非適用条件を越えて利用された。既存三層だけでは、可視化済みmethodの意味伝播を防げない。
4. 追加する一つの制御はprompt内predicateではなく`FIXED_EVIDENCE_ROUTE_PROJECTION`である。task全体が、固定target identity、有限の列挙済みevidence set、そのevidenceだけを評価するterminal review output、scope expansion停止、edit / test / dependency禁止を持つ場合だけ、固定read method差分をCandidate43へ実行前合成する。
5. この制御が消すcontext伝播は、固定read method本文がA02、F05、A06など非対象taskへ流入する経路である。非対象taskのmodel-visible promptには差分bytes自体が存在しない。
6. 新たに増える判断点はmodel実行前のroute選択一つである。authoring sourceはCandidate43 full bundleと一つの小さなroute差分とし、解決済みfull bundle、base hash、route hash、合成後hashをmanifestへ固定する。case label、A / F分類、SA、TaskSpec method、prompt内否定条件は追加しない。
7. 成果品質はcatalog固定F10 `N=5`で判定する。5 / 5 score `4`、root-only、zero drift、正しいreview findingまたは根拠あるno-findings、固定read範囲維持を必須とする。非対象routeは機械契約でF05、A02、A06がCandidate43 identityを選び、route差分をmaterializeしないことを確認する。
8. 新しいF10-only Evaluation setでCandidate43とCandidate63を同時に各`N=5`実行する。Candidate63は5 runすべて3 top-level tool call以下、shell command合計55を維持し、同じ新条件のCandidate43 token合計を下回ることを必須とする。旧targeted2のCandidate43 `848,388`とCandidate56 `371,820`はfixture identityが異なるため参考値だけとする。route選択はmodel実行前なので、A02、F05、A06のmodel-visible promptはCandidate43から変化しない。
9. F10で1 runでも3 tool callを超える、score `4`を失う、read範囲を拡張する、合成物をbase + route差分から一意に再現できない、または非対象taskへroute差分を選ぶ場合は停止する。別predicateを足さず、standard14、A06、採用、release、本体反映へ進めない。

九項目を定義済みであるため、Candidate63のroute差分、materializer、解決済みfull bundle、F10 profileを作成できる。

## 構成

```text
Candidate43 full bundle                  fixed-evidence-review route delta
files/AGENTS.md                          one method line + placement identity
        \                                      /
         \                                    /
          +-- model実行前materialization ----+
                         |
                         v
             Candidate63 resolved full bundle
             files/AGENTS.mdは一枚
```

authoring sourceを二つの全文へ複製しない。一方、評価入力は[`prompt file bundle方式`](prompt-file-bundle.md)に従い、Candidate63単独で再現可能なfull bundleへ解決して保存する。

## Route境界

`fixed-evidence-review`は単なる`read=true`ではない。

- F10: fixed target identity、有限evidence set、terminal review、no expansion、no edit / testをすべて満たすため対象。
- F05: terminal outcomeが利用者へのclarificationであり、evidence readが成果生成の中核ではないため対象外。
- A02: repository authority探索、edit、testを必要とするため対象外。
- A06: read-only reviewだが、production surface、authority、test、分割方法が実行前に閉じていないため対象外。

route選択、candidate作成、対象評価、採用、release、本体反映は別状態である。

## 対象試験結果

2026-07-22にF10-onlyの同一Layer 1でCandidate43とCandidate63を各`N=5`実行した。両promptとも5 / 5がscore `4`、root-only、zero driftだった。

Candidate63は5 runすべて3 top-level tool call、4 model stepへ収束した。Candidate43のtool callは`11 / 3 / 11 / 11 / 4`、Candidate63は`3 / 3 / 3 / 3 / 3`だった。shell commandは両promptとも各run 11件、合計55件で、許可外readと禁止操作は0件だった。

all-agent token合計はCandidate43 `811,578`、Candidate63 `382,228`で、差は`-429,350`、`-52.90%`だった。token中央値は`211,070 -> 76,409`、elapsed中央値は`87.367秒 -> 54.086秒`だった。

route materializerはCandidate43と一行deltaからCandidate63をbit-for-bit再生成した。F05、A02、A06型の非一致factsはCandidate43 identityを選ぶ機械契約を通過した。

事前gateを満たしたため、Candidate63の状態を`targeted_evaluated / route_gate_passed`とする。この状態は採用、release、本体反映を意味しない。詳細は[`Candidate43 / Candidate63 F10 N=5`](../evaluations/results/candidate43-candidate63-fixed-evidence-route-projection-f10-n5_2026-07-22.md)に置く。
