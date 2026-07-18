# Candidate41 owner metadata delegation boundary expanded 12-case N=5 result

## 結論

Candidate41のexpanded 12-case N=5試験は、60 / 60 runがvalid、rateable、score `4`だった。score `0..3`は0件で、`quality_score`中央値は`100.000`である。

全60 runはroot sessionだけで完了した。child sessionは0件だった。TaskSpecが独立producer executionを明示しない限りworkerを起動しない`OWNER_ROLE` predicateは、12 caseの観測範囲で成果品質を維持した。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- profile: `candidate41-owner-metadata-delegation-boundary-outcome-quality-owner-diagnostic-v9-expanded12-f04r2-global-m24-n5-r1`
- prompt set: `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1`
- bundle SHA-256: `048f6693ae588feb0cd27f13f08637adb6b0cc376d94a4a4d4072662b1b747d7`
- evaluation set: `the-caption-expanded12-f04r2-f10r3-r2`
- evaluation set identity: `de4d1deacc470127eaf612f4b18d638febf5a2b44b1e82a1f673942b05c772c7`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v5`
- execution: global queue `M=24`、12 case、各`N=5`

## KPI

- valid / rateable run: 60 / 60
- score `4`: 60
- score `0..3`: 0
- excluded / retry attempt: 0 / 0
- all-agent token total: `14,688,469`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `2,861,019`
- `elapsed_seconds` median: `1,172.182`
- controller elapsed: `306.688`秒
- result ID: `f9f8b177031e401093ee60717d5e602e`
- result content SHA-256: `47eb31529873d665730f96a6442ded014ef45dd03229244814dee70702eaf7c8`
- compatibility key: `abc7d7a9a4db052f417a200e5c7b873e39edb27bc5d564163fbb150f560100a4`

| iteration | quality_score | total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 3,046,403 | 1,211.100 |
| 2 | 100.000 | 3,197,150 | 1,172.182 |
| 3 | 100.000 | 2,861,019 | 1,255.445 |
| 4 | 100.000 | 2,776,970 | 1,160.607 |
| 5 | 100.000 | 2,806,927 | 1,106.784 |

## Case別結果

| case | score 4 | token total | token median | owner evidence eligible |
| --- | ---: | ---: | ---: | ---: |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 5 | 1,158,233 | 228,496 | 5 / 5 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 5 | 2,036,889 | 423,745 | 0 / 5 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 5 | 1,012,921 | 197,750 | 0 / 5 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY r2` | 5 | 1,621,682 | 345,700 | 0 / 5 |
| `TC-F05-CLARIFY-UNITS-MODE` | 5 | 395,664 | 79,054 | 0 / 5 |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 5 | 338,595 | 79,157 | 0 / 5 |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 5 | 1,455,901 | 297,668 | 0 / 5 |
| `TC-F07-CANONICAL-V4-RUNNER` | 5 | 1,810,356 | 327,966 | 0 / 5 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 5 | 677,182 | 141,334 | 0 / 5 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 5 | 2,230,572 | 409,496 | 0 / 5 |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 5 | 941,831 | 201,473 | 0 / 5 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 5 | 1,008,643 | 224,753 | 0 / 5 |

## Routingと診断

all-agent usageでは60 / 60 runのsession数が1だった。child session合計は0である。

owner-producer evidenceは5 / 60がeligible、55 / 60がinadmissibleだった。eligible 5件はF01である。v9ではowner-producer evidenceを診断だけに使い、成果品質のscoreへ算入しない。

command protocol violationは0件だった。quality audit failureも0件だった。

F04では5 / 5でadapterが`node_modules`と`dist`を除去した。candidateによるadapter-owned cleanupのtool attemptは0件だった。最終responseでcleanup実施に言及したrunは3 / 5だった。実際の除去主体はadapterであり、これは診断として保持する。

## C35 expandedとの非互換参考値

C35 expanded resultは`owner-producer-quality-v8`、Candidate41は`outcome-quality-owner-diagnostic-v9`であり、compatibility keyが異なる。このため、評価基盤v3の互換比較viewは作成しない。

実行条件が一致する保存済み数値を参考として並べると、Candidate41の60 run token合計はC35の`21,317,983`から`-6,629,514`、`-31.10%`だった。token中央値は`4,145,776`から`-1,284,757`、`-30.99%`だった。elapsed中央値は`1,889.420`秒から`-717.238`秒、`-37.96%`だった。これらは非互換条件間の記述的観測であり、v3の比較結果またはwinner判断ではない。

## 判断

### 事実

- 12 caseすべてが5 / 5でscore `4`だった。
- TaskSpecにないworker routingは観測されなかった。
- result unit、owner runtime identity、evidence mappingを追加しなくても全caseが完了した。

### 推論

criterion owner語列をworker specificationとして扱わない変更は、targeted 2 caseだけでなくexpanded 12 caseでも最短経路を阻害しなかった。

N=5の観測であり、低頻度事象の不存在や評価範囲外の一般性能は保証しない。

### 提案

Candidate41のexpanded試験gateを`passed`とする。採用、release、本体反映は別判断として保持する。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate41-owner-metadata-delegation-boundary-outcome-quality-owner-diagnostic-v9-expanded12-f04r2-global-m24-n5-20260719-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/f9f8b177031e401093ee60717d5e602e.json`
- quality audit、Layer 4 registration、lossless archive、final compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
