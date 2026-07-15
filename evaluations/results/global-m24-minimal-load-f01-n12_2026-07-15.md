# Global queue M=24 minimal load qualification

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- run window: `2026-07-15T15:41:28+09:00`から`2026-07-15T15:48:47+09:00`
- case: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY r3`
- outer parallelism: `M=24`
- repetition: `N=12`
- requested slots: `24`
- valid runs: `24 / 24`
- external failure / retry: `0 / 0`
- schedule: `global_queue`
- qualification: `load_qualified_minimal`

このrunは中間の並列度を飛ばし、`M=24`で24 slotを同時に埋めたときのlocal resource負荷、workspace分離、controller安定性、外部capacity failureの有無を最小構成で確認するqualificationである。A / Bの両方へ同じbaseline bundleを与えており、quality rating、KPI comparison、promptの優劣判定は行わない。

## Fixed execution

| condition | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| A | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |

caseはF01 r3だけとし、A / Bを各12反復、合計24 slot生成した。24 slotを同時投入し、追加waveは設けていない。内側の`agents.max_threads=4`を含む実行条件は既存qualificationから変更していない。

## Execution integrity

24 slotはすべてattempt 1、controller exit 0、execution status `valid`で終了した。各slotは独立workspaceを使用した。24 workspaceすべてで次を確認した。

- condition commit: `da76d2e1181cdb04b6f3aedc0451077c8466c64b`
- condition tree: `f3dfbad104884a27251573ce7d8c58b046a81661`
- final changed path: `src/domain/market_units_snapshot.py`だけ
- unexpected changed path: 0
- Codex exit: 0
- external failure: なし

## Load observation

- runner wall time: `439.118`秒（7分19秒）
- 24 runのexecution時間合計: `7,791.340`秒
- observed parallel factor: `17.743x`
- throughput: `196.758 runs/hour`
- run elapsed: min `235.577`秒、median `317.361`秒、max `439.070`秒
- OS samples: `45`
- load average 1分値: median `4.039`、max `6.840`
- load average 5分値: max `4.155`
- memory free: median `64%`、min `62%`
- swap used max: `0 MiB`
- disk free min: `34.368 GiB`
- Codex process count max: `29`
- evaluation process count max: `24`
- monitor sample error: `0`

24 controllerが同時稼働している間にloadとmemory使用量の増加は観測されたが、10-coreを超えるload、swap、memory pressure、disk pressure、未分類controller failure、workspace衝突、外部capacity failureは観測されなかった。このホストと固定条件では、`M=24`をlocal load上の実行可能値とする。

## M=8との観測差

| 指標 | M=8 | M=24 | 観測差 |
| --- | ---: | ---: | ---: |
| slots | 8 | 24 | 3倍 |
| runner wall time | 370.074秒 | 439.118秒 | 18.7%増 |
| throughput | 77.822 runs/hour | 196.758 runs/hour | 152.8%増 |
| observed parallel factor | 6.490x | 17.743x | 173.4%増 |
| run elapsed median | 297.711秒 | 317.361秒 | 6.6%増 |
| load average 1分 max | 3.203 | 6.840 | 3.637増 |
| memory free min | 72% | 62% | 10 point減 |
| swap used max | 0 MiB | 0 MiB | 変化なし |

slot数を3倍にしたのに対してwall time増加は18.7%、run median増加は6.6%だった。短い単一wave同士の観測であり並列度だけの効果とは一般化しないが、`M=24`で明確なthroughput増加と限定的なper-run latency増加を観測した。

## Boundary

このqualificationは1 case、1 full-occupancy waveだけを使った最小負荷確認である。case mixを含む長時間連続運転、正式比較におけるKPIの安定性、`M>24`の適格性は判断しない。新しいprompt比較で`M=24`を使う場合は、そのcycle内の全A / B slotで同じ実行条件を固定する。

## Evidence handling

cycle、raw workspace、Codex JSONL、OS samples、controller attempt記録は次に保持する。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/global-m24-load-f01-n12-20260715`

raw evidenceはrepositoryへcommitしない。
