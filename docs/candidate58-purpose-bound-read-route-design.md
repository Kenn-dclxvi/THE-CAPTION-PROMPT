# Candidate58 purpose-bound read route設計記録

## 結論

Candidate58はCandidate57を直接sourceとし、root `AGENTS.md`一枚の`FIXED_READ`一文だけを`READ_ROUTE`へ置換する。

F系はTaskSpec明示列挙済みreadを同一model stepで取得する。A系はrepository authority / stateを解決するまで、各result後に次のreadを一つ決める。目的ごとのrouteを同じlabel内の排他的な二分岐として固定する。

## Candidate作成前gate

1. F10の最短正常経路は、TaskSpec列挙済みの開始identity、固定authority / diff / source、終了statusを3 top-level tool callで取得する経路である。
2. Candidate56 A02はmodel step / tool callを減らさずcommandを`47 -> 70`へ増やし、1 runで必須diff checkを欠いた。
3. Candidate57 A02 probeはTaskSpec明示列挙へ狭めても、`rg --files`後のauthority探索readを`3 / 3 / 3` commandの並列groupにした。非適用条件だけでは一般的なparallel read routeを止めなかった。
4. repository authority / stateだけでは次のreadが前のresultへ依存することを実行方法へbindしない。A系routeを明示する必要がある。
5. 置換する一つの不変条件は、read集合を固定したauthorityに応じてrouteを選ぶことである。TaskSpec列挙済みF readは同一model step、repository resultが対象を決めるA readは一result一decisionとする。
6. 消す判断点はF系の固定read再決定とcontext再送である。A系では探索集合の先読みと並列拡大を禁止し、前resultなしに次targetを選ばない。
7. 新しいlabelやphaseは追加しない。`FIXED_READ`を`READ_ROUTE`へ置換し、他のA / F / D、terminal、method predicateは変更しない。
8. 最初にA02を1件probeする。開始identityとTaskSpec列挙済みvalidationを除き、authority探索readの複数command同一model stepが1件でもあれば停止する。
9. probe通過時だけA01 / A02各`N=5`へ進み、10 / 10 score `4`、A02 command / model step / tool call / token / elapsed中央値がCandidate43以下を必須とする。A系通過時だけF05 / F10各`N=5`へ進み、F10各run5 tool call以下、合計25以下、5 / 5 score `4`、token合計Candidate43以下を必須とする。

九項目を定義済みであるため、Candidate58 bundleと既存条件をprompt identityだけ変更したA / F profileの作成を許可する。

## Graph

```text
who fixed the read set?
  TaskSpec before execution
    -> finite + independent + read-only
    -> same model step

  repository authority / state result
    -> one result
    -> choose one next read
    -> repeat until authority resolved
```

candidate作成、probe、対象試験、採用、release、本体反映は別状態である。
