# Candidate59 read-only operation batch設計記録

## 結論

Candidate59はCandidate56を直接sourceとし、root `AGENTS.md`一枚の`FIXED_READ`一文だけを置換する。

A系routeは指定しない。operation全体がno-edit / no-test / no-dependencyで、実行前TaskSpecが許可read path / commandとread-only validationを有限列挙した場合だけ、F系batchを適用する。

## Candidate作成前gate

1. F10の最短正常経路はTaskSpec列挙済みの開始identity、固定authority / diff / source、終了statusを3 top-level tool callで取得する経路である。Candidate56は5 / 5 runで再現した。
2. Candidate56は条件をlocal read単位で解釈し、edit / testを伴うA02のauthority探索にもbatchを適用した。A02 commandは`47 -> 70`、1 runはscore `3`となった。
3. Candidate57はTaskSpec明示列挙へ狭めてもA02 parallel readを止めなかった。Candidate58はA routeを逐次化し、A02 tokenを`+29.30%`、model stepを`+56.86%`とした。
4. 既存TaskSpecはoperation全体のedit / test permissionを明示する。repository authority / stateだけでなく、このpermission境界をmethod適用へbindする必要がある。
5. 置換後の一つの不変条件は、F batchをoperation全体が`edit=false ∧ test=false ∧ dependency=false ∧ read target有限列挙 ∧ read-only validation有限列挙`の場合だけへ限定することである。
6. 一条件でも未明示またはfalseなら非適用とする。非適用時のA route、探索順、batch禁止は追加せず、C43から継承した通常判断へ委ねる。
7. 消す判断点はF系列挙済みreadの再決定とcontext再送だけである。A系へ新しい判断、確認、逐次化を追加しない。
8. 最初にA02を1件probeする。開始identity以外で、authority探索readを複数commandの同一model stepへ置くtraceがあれば停止する。
9. probe通過時だけF05 / F10各`N=5`を先に実行し、F10各run5 tool call以下、5 / 5 score `4`、token合計Candidate43以下を必須とする。F系通過後にA01 / A02各`N=5`を実行し、10 / 10 score `4`、A02のcommand / model step / tool call / token / elapsed中央値がCandidate43以下であることを必須とする。

九項目を定義済みであるため、Candidate59 bundleとA / F profileの作成を許可する。

## Graph

```text
operation permissions
  edit=false + test=false + dependency=false
    + TaskSpec enumerates read targets and read-only validation
      -> F batch

  otherwise
      -> inherited C43 route
      -> no added A method control
```

candidate作成、probe、対象試験、採用、release、本体反映は別状態である。
