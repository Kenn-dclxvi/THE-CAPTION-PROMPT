# Global queue M=6 minimal load qualification

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- run window: `2026-07-15T15:17:09+09:00`から`2026-07-15T15:25:56+09:00`
- case: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY r3`
- outer parallelism: `M=6`
- repetition: `N=3`
- requested slots: `6`
- valid runs: `6 / 6`
- external failure / retry: `0 / 0`
- schedule: `global_queue`
- qualification: `load_qualified_minimal`

このrunは`M=6`で6 slotを同時に埋めたときのlocal resource負荷、workspace分離、controller安定性だけを最小構成で確認するqualificationである。A / Bの両方へ同じbaseline bundleを与えており、quality rating、KPI comparison、promptの優劣判定は行わない。

## Fixed execution

| condition | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| A | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |

caseはF01 r3だけとし、A / Bを各3反復、合計6 slot生成した。6 slotを同時投入し、追加waveは設けていない。内側の`agents.max_threads=4`を含む実行条件は既存qualificationから変更していない。

## Execution integrity

6 slotはすべてattempt 1、controller exit 0、execution status `valid`で終了した。各slotは独立workspaceを使用した。6 workspaceすべてで次を確認した。

- condition commit: `da76d2e1181cdb04b6f3aedc0451077c8466c64b`
- condition tree: `f3dfbad104884a27251573ce7d8c58b046a81661`
- final changed path: `src/domain/market_units_snapshot.py`だけ
- unexpected changed path: 0
- Codex exit: 0
- external failure: なし

## Load observation

- runner wall time: `527.419`秒（8分47秒）
- 6 runのexecution時間合計: `2,554.039`秒
- observed parallel factor: `4.843x`
- run elapsed median: `418.992`秒
- OS samples: `37`
- load average 1分値: median `2.118`、max `2.823`
- load average 5分値: max `2.194`
- memory free: median `75%`、min `74%`
- swap used max: `0 MiB`
- disk free min: `35.518 GiB`
- Codex process count max: `10`
- evaluation process count max: `6`
- monitor sample error: `0`

6 controllerが同時稼働している間もswap、memory pressure、disk pressure、未分類controller failure、workspace衝突は観測されなかった。このホストと固定条件では、`M=6`をlocal load上の実行可能値とする。

## Boundary

このqualificationは1 case、1 full-occupancy waveだけを使った最小負荷確認である。case mixを含むthroughput比較、`M=4`に対する所要時間改善、長時間連続運転、`M>6`の適格性は判断しない。新しいprompt比較で`M=6`を使う場合は、そのcycle内の全A / B slotで同じ実行条件を固定する。

## Evidence handling

cycle、raw workspace、Codex JSONL、OS samples、controller attempt記録は次に保持する。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/global-m6-load-f01-n3-20260715`

raw evidenceはrepositoryへcommitしない。
