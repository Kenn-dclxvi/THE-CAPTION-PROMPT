# TC-F01 r2 identical bundle parallel M=2 N=3 qualification

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- run window: `2026-07-15T09:16:24+09:00`から`2026-07-15T09:29:58+09:00`
- case ID: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY`
- case revision: `r2`
- outer parallelism: `M=2`
- repetition: `N=3`
- valid runs: `6 / 6`
- external failure / retry: `0 / 0`
- qualification: `qualified`

このrunは新しい外側並列条件`M=2`の資源競合とworkspace分離を確認するためのqualificationである。A / Bの両方へ同じbaseline bundleを与えており、prompt比較のwinnerは決めない。

## Fixed prompt and execution

| condition | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| A | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |

同じcase・反復のA / Bを同じwaveへ置き、両方の終了後に次waveへ進めた。3 wave、6 slotを実行し、各slotは独立workspaceを使用した。内側の`agents.max_threads=4`は既存条件から変更していない。

## Result

| repetition | A tokens | A seconds | B tokens | B seconds |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 268,921 | 285.218 | 332,637 | 260.943 |
| 2 | 241,375 | 215.382 | 321,517 | 238.055 |
| 3 | 533,286 | 277.153 | 272,093 | 289.594 |

6 workspaceすべてで次を確認した。

- production postimage: `src/domain/market_units_snapshot.py` blob `e3af06ab26c74a98815a53de7ec0661af82e3e18`
- focused contract file: `tests/unit/test_market_units_snapshot.py` blob `a854b1e85795418c372a26c72a2f4a9a3e24d6a2`
- tracked差分は許可されたproduction fileだけ
- full gate: `326 passed, 3 skipped`
- Codex exit 0、external failureなし

同一bundleでもtokenと時間は揺れており、特にA repetition 3のtokenが大きい。この値をprompt差として扱わない。

## Parallel and OS observation

- runner wall time: `813.271`秒
- 同じ6 runを逐次実行した場合の実測時間合計: `1,567.082`秒
- observed speedup: `1.927x`
- wave max合計との差: `0.036`秒
- OS samples: `55`
- load average 1分値: median `2.389`、max `2.865`
- memory free: median / min `72% / 72%`
- swap used max: `0 MiB`
- disk free min: `31.134 GiB`
- monitor sample error: `0`

local resource saturation、workspace衝突、未分類controller failureは観測されなかった。したがって、このホストと固定条件では`M=2`をcore comparisonへ使用可能と判断した。これは`M>2`の適格性を示さない。

## Evidence handling

raw workspace、Codex JSONL、OS samples、controller attempt記録は次に保持する。

`/Users/kenn/repos/THE-CAPTION-prompt-ab-measurement/runs/f01-null-parallel-m2-n3-20260715`

これらはlocal evidenceであり、repositoryへcommitしない。
