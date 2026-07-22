# Candidate59 read-only operation batch A02 probe

## 結論

Candidate59はA02 probe 1件で停止した。

`FIXED_READ`をoperation全体がno-edit / no-test / no-dependencyの場合だけへ限定したが、edit / testを伴うA02でもauthority探索readがshell command結合へ流入した。条件を満たさないA operationへbatch方法の表現自体が波及した。

残り9 slot、F05 / F10、standard14、A06へ進めない。

## 観測

- run ID: `9f4c442c419a4714a15cb79d2954aa19`
- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` / iteration 1
- Layer 2 status: `valid`
- total tokens: `314,879`
- elapsed: `96.870秒`
- top-level tool call: `9`
- command execution group: `7`
- group内shell subcommand: `22`
- catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`

開始identityは4 subcommandを一つのshellへ結合した。authority探索では`run.sh`と全域`rg`、entrypoint inventoryとauthority / README / source、root / tests authorityとtest sourceをそれぞれ複数subcommandのshellへ結合した。個別exit evidenceを保つF methodとは異なる形だが、A系read集合のbatch化は止まっていない。

このprobeは2 case × `N=5`を満たさず、Layer 4 resultへ登録していない。互換KPI比較へ使わない。

## 判断

Candidate56、57、59は、A系を明示的に逐次化しない限り、global `AGENTS.md`内の「同一model step」表現がA02へ波及した。Candidate58は波及を止めたが、A02 tokenを`29.30%`増やした。

したがって、A / F境界を同じglobal method predicateの条件式だけで作る試行は停止する。次に進むなら、F TaskSpecへmethod flagまたは局所instructionを提示し、A TaskSpecから完全に不可視にする別評価軸とする。これはfile分割ではなくTaskSpec可視入力の分離であり、prompt変更と評価条件変更を同じ比較へ混ぜない。
