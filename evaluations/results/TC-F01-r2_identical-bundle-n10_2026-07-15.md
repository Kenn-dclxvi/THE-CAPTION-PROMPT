# TC-F01 r2 identical bundle N=10 null calibration

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- run window: `2026-07-14T16:22:58Z`から`2026-07-14T18:04:15Z`
- purpose: bit-identicalなprompt bundle A / Bを`N=10`で比較し、null条件で評価基盤が安定するか確認する
- repetition: `N=10`
- case execution: `qualified`
- null calibration: `failed`
- qualification status: `execution_qualified_null_calibration_failed`
- prompt evaluation status: `not_evaluated`
- official prompt comparisonへの使用: 不可

20有効runはすべて同じcase、task、bundle content、model、permission、fixture、Codex CLI、session modeで実行した。奇数repetitionはA→B、偶数repetitionはB→Aとし、condition orderを均した。

## Fixed input

- set ID: `tc-f01-domain-duplicate-asset-key-r2`
- case ID: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- condition commit: `da76d2e1181cdb04b6f3aedc0451077c8466c64b`
- condition tree: `f3dfbad104884a27251573ce7d8c58b046a81661`
- model-visible task SHA-256: `08e35096387b648a715732af219eb947c08ab4afbea2192dec97a65b3f18b0b9`
- bundle SHA-256: `94e6fedf856952cbeb29c6cb631d9917adc8fddb5ac3846dc5ca2a06d83a885c`
- Codex CLI: `codex-cli 0.144.0`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- sandbox: `workspace-write`
- approval policy: `never`
- session mode: `persisted`
- `multi_agent`: enabled
- `agents.max_threads`: `4`
- memories: disabled

Prompt set Aは`the-caption-3ce91a4-current-r1`、Bは`the-caption-3ce91a4-current-copy-r1`である。identityは異なるが、bundle file content、bundle SHA-256、condition commit、condition treeは一致する。identityとcondition labelはworkerへ渡していない。

## Environment revision

最初に`--ephemeral`を維持したN=10 cycleを開始したが、A repetition 1で`codex_collab_parent_thread_missing`が3attempt連続して自動検出された。3attemptはraw evidenceを保持して`excluded`とし、有効回数へ含めていない。制御script停止後に開始しかけた未完了attemptも正式runへ含めていない。

この再現結果から、`codex exec --ephemeral`とmulti-agentの組合せをenvironment blockerと判定した。adapterから`--ephemeral`を除き、親threadをlocal session storeへpersistするenvironment revisionへ変更した後、新しいcycleでA / Bを最初から実行した。

persisted-session cycleでは20runすべてが初回attemptで`valid`となり、外部要因による除外は0件だった。

## Quality evidence

20runすべてで次を確認した。

- production fileのGit blobがreference postimage `e3af06ab26c74a98815a53de7ec0661af82e3e18`と一致
- focused gate: `23 passed`
- full gate: `326 passed, 3 skipped`
- focused test fileのGit blobは開始時の`a854b1e85795418c372a26c72a2f4a9a3e24d6a2`から不変
- final changed pathは`src/domain/market_units_snapshot.py`だけ
- unexpected changed pathなし
- Codex exit code `0`

この事実根拠により全runへquality score `4`を記録した。ただし、独立したblind quality raterによる採点ではない。この制約は維持する。

## Per-repetition result

| repetition | order | A quality | A tokens | A seconds | B quality | B tokens | B seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | A→B | 100 | 197,494 | 232.452 | 100 | 436,138 | 282.085 |
| 2 | B→A | 100 | 511,303 | 253.592 | 100 | 704,411 | 306.137 |
| 3 | A→B | 100 | 278,395 | 262.936 | 100 | 480,950 | 233.802 |
| 4 | B→A | 100 | 332,642 | 313.523 | 100 | 338,298 | 288.978 |
| 5 | A→B | 100 | 267,301 | 185.667 | 100 | 302,562 | 288.462 |
| 6 | B→A | 100 | 540,199 | 290.140 | 100 | 304,106 | 283.133 |
| 7 | A→B | 100 | 246,366 | 276.041 | 100 | 658,529 | 265.521 |
| 8 | B→A | 100 | 321,988 | 255.033 | 100 | 564,371 | 282.779 |
| 9 | A→B | 100 | 438,810 | 276.802 | 100 | 552,051 | 497.223 |
| 10 | B→A | 100 | 425,276 | 263.814 | 100 | 782,211 | 673.857 |

## Layer 4 result

| KPI median | A | B | difference |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.0 | 100.0 | 0 |
| `total_tokens` | 327,315.0 | 516,500.5 | Bが189,185.5多い（A比57.8%） |
| `elapsed_seconds` | 263.375 | 285.798 | Bが22.423秒長い（A比8.5%） |

3 KPIの固定判定規則による機械出力は`winner: a`である。qualityが同点で、Aのtoken中央値が小さいため時間比較へ進む前にAとなった。

ただし、A / Bはbit-identicalであり、workerが見るprompt、task、repository状態も同じである。したがって、この`winner: a`をprompt Aの優位またはprompt Bの悪化として解釈してはならない。null条件で勝敗が生じたため、null calibrationはfailedとする。

## Token variance analysis

- Aのtoken中央値: `327,315`
- Bのtoken中央値: `516,500.5`
- paired 10回のうちAのtokenが少なかった回数: `9`
- Aのwait call中央値: `4`
- Bのwait call中央値: `7`
- Aのcached input中央値: `292,864`
- Bのcached input中央値: `471,296`
- input token中央値差に占めるcached input差: `94.5%`

B repetition 7はwait `13`回、B repetition 10はwait `17`回で、tokenもそれぞれ`658,529`、`782,211`だった。A / Bのcommand execution中央値はいずれも`3.5`で、成果も同一である。

この観測範囲では、token差は実装量や成果品質ではなく、SA完了待ちのpolling回数と、各turnで再利用されるcached contextに強く影響されている。単一caseの`total_tokens`はprompt効率よりオーケストレーションの待機手数を大きく反映している。

## Serial OS baseline

persisted-session cycleと並行して15秒間隔で402sampleを取得した。raw monitor logはlocal temporary evidenceとしてcycle外へ分離した。

- machine: `Mac16,10`（Mac mini）
- OS: macOS `26.5.1`、Darwin `25.5.0`、arm64
- physical / logical CPU: `10 / 10`
- memory: `16 GiB`
- 1分load average: median `2.50`、min `1.69`、max `5.90`
- system-wide memory free: median `66%`、min `64%`
- swap used: max `0 MiB`
- disk free: `11–14 GiB`
- persisted-session cycleのlogical size: `8.1 GiB`

monitorの`iostat -c 1` CPU列はinterval peakではなく起動後平均になるため、parallel判断のpeak CPU根拠には使わない。load average、memory pressure、swap、disk、process samplingを判断材料とする。

直列実行ではCPU、memory、swapの飽和は観測されなかった。外側2並列を試すOS余地はあるが、次を満たす別cycleでqualificationする必要がある。

1. persisted sessionを維持する。
2. 外側parallelismはまず`2`だけを試し、各runの`agents.max_threads=4`は変えない。
3. current disk freeは別のN=10 cycleを安全に保持する余裕が小さいため、既存temporary evidenceを明示的に整理または別volumeへ移してから開始する。
4. load average、memory free、swap、disk free、external failure、run elapsedを直列baselineと比較する。
5. parallel cycleでcondition間のresource競合が出た場合、そのcycleを正式prompt比較に使わない。

OS飽和は今回のA / B token差を説明しない。parallel化は所要時間短縮候補であり、null calibration失敗の修正ではない。

## Judgement

case execution経路は20 / 20で同じ正解成果を作れたためqualifiedである。一方、qualityは全runでceilingとなり、bit-identical prompt間でtoken中央値に57.8%差が出て機械的winnerが生じた。

以上からstatusを`execution_qualified_null_calibration_failed`とする。このcaseと現行profileだけを使って実prompt candidateの改善・悪化を判定しない。先に、SA待機pollingと`total_tokens`の関係、またはmodel-invisibleなcondition差が存在しないことを追加検証する必要がある。

## Evidence handling

cycle、workspace、Codex JSONL、stdout / stderr、persisted Codex session、OS monitor raw logはlocal temporary evidenceとして保持し、repositoryへcommitしない。本recordには固定identity、集計値、terminal behavior、OS基準値、qualification判断だけを記録する。
