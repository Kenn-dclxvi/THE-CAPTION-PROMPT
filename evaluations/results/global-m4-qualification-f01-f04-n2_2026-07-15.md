# Global queue M=4 qualification

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- run window: `2026-07-15T12:16:33+09:00`から`2026-07-15T12:31:20+09:00`
- cases: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY r3`、`TC-F04-WEB-AUDIT-COLUMN-VISIBILITY r1`
- outer parallelism: `M=4`
- repetition: `N=2`
- valid runs: `8 / 8`
- external failure / retry: `0 / 0`
- schedule: `global_queue`、過去のcase・condition別median所要時間が長い順
- qualification: `qualified`

このrunは、case単位のbarrierを持たないglobal queueと外側並列`M=4`が、独立workspaceを保ったまま安定して実行できるかを確認するためのqualificationである。A / Bの両方へ同じbaseline bundleを与えており、prompt比較のwinnerは決めない。

## Fixed prompt and execution

| condition | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| A | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |

内側の`agents.max_threads=4`を含む実行条件は既存比較から変更していない。queueはA / Bの実行環境を揃える目的では使わず、estimated durationの降順だけで投入順を固定した。空いたworkerへ次のjobを即時投入し、caseや反復の完了待ちは設けていない。

## Execution integrity

8 slotはすべてattempt 1、controller exit 0、execution status `valid`で終了した。各slotは独立workspaceを使い、tracked差分はF01が`src/domain/market_units_snapshot.py`、F04が`src/web/market_units_editor/src/App.tsx`だけだった。許可外changed path、workspace衝突、controller failure、外部要因による除外は0件だった。

F01の4 runは新しいr3 contractどおり、周辺caller riskを報告しても完了を妨げず、停止理由なしで終了した。F04の4 runもrequired Node validationとtemporary output cleanupを完了した。

最初のF04が終了した直後、他のF04を待たずにF01を開始した。これにより、case単位barrierを外したwork-conservingな投入が実際に機能したことを確認した。

## Throughput and OS observation

- runner wall time: `887.110`秒（14分47秒）
- 8 runの実測時間を逐次合計した値: `2,870.893`秒（47分51秒）
- observed speedup: `3.236x`
- wall time reduction: `69.1%`
- OS samples: `60`
- load average 1分値: median `1.921`、max `3.925`
- memory free: median `81%`、min `80%`
- swap used max: `0 MiB`
- disk free min: `28.089 GiB`
- Codex process count max: `8`
- evaluation process count max: `4`
- monitor sample error: `0`

local resource saturationは観測されなかった。このホストと固定条件では、global queueの`M=4`を次のcore comparisonへ使用可能と判断する。これは`M>4`の適格性を示さない。

## Evidence handling

raw workspace、Codex JSONL、OS samples、controller attempt記録は次に保持する。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/global-m4-qualification-f01-f04-n2-20260715`

これらはlocal evidenceであり、repositoryへcommitしない。
