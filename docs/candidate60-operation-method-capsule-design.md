# Candidate60 operation method capsule設計記録

## 結論

Candidate60はCandidate55を直接sourceとし、root `AGENTS.md`一枚の`OPERATION`だけを置換する。

共通promptが固定するのは、`method / result / constraint / failure / terminal`を同一operationへ閉じ、別operationへはTaskSpecが明示したterminal resultだけを渡す境界である。固定readの取得方法そのものはroot `AGENTS.md`へ置かず、対象operationのTaskSpec capsuleだけへ提示する。

## Candidate作成前gate

1. 基準prompt setはCandidate55である。control-freeな最短正常経路は、F10の固定差分review operationだけが列挙済みreadを3 model stepで取得し、findingをterminal resultとして返す経路である。A02では開始identity operationのterminal resultだけを次のcanonical target探索へ渡し、read grouping方法を持ち越さない。
2. 保存済みの誤経路はCandidate56のA02である。global `FIXED_READ`はF10を5 / 5で3 tool callへ収束させた一方、A02 commandをCandidate43の47から70へ増やし、1 runで必須`git diff --check`を欠いた。
3. Candidate57はTaskSpec列挙条件、Candidate59はoperation全体のno-edit / no-test条件へ適用範囲を狭めたが、global `AGENTS.md`にmethod本文が残るためA02の実行方法へ影響した。TaskSpec、repository authority、repository stateだけでは、model-visibleなglobal method本文の別operationへの意味伝播を防げない。
4. 置換する一つの不変条件は、operation固有の`method / failure`を既存の`result / constraint / terminal`と同じbindingへ加え、別operationが受け取れる情報を明示されたterminal resultへ限定する境界である。
5. この境界が消す判断点は、先行operationのtool grouping、invocation状態、raw outputを後続operationのmethodとして再利用してよいかという再判断である。後続operationは、自身のTaskSpec、permission、authority、入力だけからmethodを選ぶ。
6. 増える読解costは`OPERATION`一文への局所binding対象とexport境界の追加だけである。新しいcase名、A / F分類、read適用predicate、worker、session分離は追加しない。
7. 診断setではF10 review operationへ固定read methodを提示する。A02では開始identity operationだけへ同じmethodを提示し、そのterminal後にmethod未指定のcanonical target探索operationへ移る。同じTaskSpec revisionをCandidate55とCandidate60へ渡す。
8. route probeは各promptのF10 / A02を1回実行する。F10は正しいfinding、zero drift、3 execution groupを必須とする。A02は正しい1 path変更、required validation、`git diff --check`、scope維持を必須とし、開始identity capsule後のmethod持越しをtraceで確認する。
9. probeを通過した場合だけ同じ新TaskSpec revisionで各`N=5`へ進む。旧C43 / C55 / C56 resultはTaskSpec条件が異なるため互換KPI比較へ混ぜない。

九項目を定義済みであるため、Candidate60 bundleと同条件profileの作成を許可する。

## 変更するgraph

```text
global operation invariant
  bind purpose / predicate / permission / constraint
  bind method / result / failure / terminal locally
  export only declared terminal result

F10 review capsule
  fixed read method -> findings

A02
  start identity capsule
    fixed read method -> start identity
  canonical target capsule
    no inherited method -> resolved target
  implementation / validation
```

## 非目標

- F系またはA系というcase labelをruntime条件にすること。
- 未知のユースケースを列挙すること。
- 固定read方法をglobal `AGENTS.md`へ戻すこと。
- workerまたは別sessionをカプセル化の必須手段にすること。
- 新TaskSpec resultを旧TaskSpec resultと互換比較すること。

candidate作成、対象試験、採用、release、本体反映は別状態である。

## N=1 route probe結果

同一の新TaskSpec revision、fixture、model、catalog identity、executor parameterでCandidate55とCandidate60を各F10 / A02へ1回実行した。4 runはすべてvalidである。

| case | C55 tokens / seconds / command | C60 tokens / seconds / command | 観測 |
| --- | ---: | ---: | --- |
| F10 | `73,775 / 73.049 / 11` | `72,476 / 53.468 / 11` | 両方とも3 command phase、正しい`monthly_main.py:25` finding、zero drift |
| A02 | `226,746 / 81.871 / 18` | `426,947 / 158.999 / 26` | 両方とも正しい1行修正、`326 passed / 3 skipped`、`git diff --check`成功、scope維持 |

A02では両promptとも、`start-identity`を4つの個別commandで完了し、後続のcanonical target探索を別operationとして開始した。先行operationのtool grouping、invocation状態、raw outputを後続methodへ流用したtraceは観測しなかった。

Candidate60だけに観測した追加実行は、authority readの拡張、routing harness、harnessの引数分割誤りによる再試行、追加wrapper確認である。A02の差は`+200,201 tokens`（`+88.29%`）、`+77.128秒`（`+94.20%`）、`+8 command`だった。

したがって、TaskSpecに明示したmethod expirationだけで今回の境界は成立した。共通`AGENTS.md`のCandidate60置換による固有効果は観測できず、追加costが大きいため事前gateは不通過とする。N=5、採用、release、本体反映へ進めない。
