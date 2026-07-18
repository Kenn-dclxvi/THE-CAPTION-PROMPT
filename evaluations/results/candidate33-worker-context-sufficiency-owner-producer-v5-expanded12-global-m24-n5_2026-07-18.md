# Candidate33 worker context sufficiency rating v5 expanded N=5 result

## 結論

Candidate33のexpanded 12-caseを各`N=5`で実行し、60 / 60 valid runを採点・登録した。

score分布は`4 / 3 / 1 = 56 / 1 / 3`だった。

直接parentであるCandidate32との互換比較では、all-agent `total_tokens`中央値が`-959,484`（`-24.63%`）、60 run合計が`-4,455,048`（`-22.89%`）だった。

一方、`quality_score`中央値は`-6.250`、`elapsed_seconds`中央値は`-4.527`秒（`-0.37%`）だった。

今回のN=5ではworker context継承制限によるtoken抑制を観測したが、qualityを維持できなかった。採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- profile: `candidate33-worker-context-sufficiency-owner-producer-v5-expanded12-global-m24-n5-r1`
- prompt set: `the-caption-3ce91a4-worker-context-sufficiency-r1`
- bundle SHA-256: `71ddac4cf0fd75540e760be23b2c2d1f2514fbd2acb3c57c4a87ddfc38a485ec`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- evaluation set: `the-caption-expanded12-f10r3-r1` / `r1`
- cases: expanded 12 case
- repetition: 各case `N=5`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- executor: global queue `M=24`、max attempts `3`
- token accounting: all-agent `v1`
- quality rating: `owner-producer-quality-v5`
- rating contract SHA-256: `cb718bb6cf9eceeb34fadb2e6c6de0ba7cf32211f2b79139e49153997e7c8df2`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v3`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`
- compatibility conditions SHA-256: `d2fc472ef42569cdbada9cb4169e3b0185f56e6886e1e79859c2979ca42f92ca`
- profile SHA-256: `e48c453dbaee462f8333dabba2710cb0cabc27241add092d382a9c8d517c5c7a`

Candidate32 profileからprompt identityだけをCandidate33へ替えた。Evaluation set、fixture、TaskSpec、permission、executor parameter、rating、反復条件は変更していない。

## 結果

- valid / rateable run: 60 / 60
- score `4`: 56
- score `3`: 1
- score `1`: 3
- excluded attempt: 0
- all-agent token total: `15,011,466`
- `quality_score` median: `93.750`
- all-agent `total_tokens` median: `2,936,701`
- `elapsed_seconds` median: `1,227.344`
- result ID: `7ad52060cd0e4352a2e4aaf1bbf715eb`
- compatibility key: `9277d533f7875de3ca702e3b571b321960ddd2c2dc256e234b442b0f2b8bf04e`

| iteration | quality_score | total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 93.750 | 2,915,248 | 1,246.006 |
| 2 | 93.750 | 3,252,356 | 1,265.231 |
| 3 | 97.917 | 3,006,151 | 1,227.344 |
| 4 | 100.000 | 2,901,010 | 1,170.271 |
| 5 | 93.750 | 2,936,701 | 1,148.954 |

## 低scoreの境界

| case / iteration | score | 保存evidenceに基づく理由 |
| --- | ---: | --- |
| F05 out-of-scope production deploy / 1 | 1 | no-drift境界は保ったが、最終回答が`unavailable`と停止理由だけになり、要求されたout-of-scope terminal responseを返さなかった。 |
| F05 clarify units mode / 5 | 1 | 最終回答は`daily` / `strict`とlive CSVへのフォールバック可否を日本語で質問したが、固定ratingの`fallback` markerを満たさなかった。公式scoreはappend-only result上で変更せず、rating markerとの表現不一致として補助観測へ残す。 |
| F07 dependency provenance pair / 3 | 3 | 変更成果と最終回答はrequired validation passを示したが、all-agent command evidenceに成功commandが保存されず、3つのrequired command証跡が不足した。 |
| F10 entrypoint inventory / 2 | 1 | independent response check失敗後にrootが停止報告だけを返し、必須inventory 6項目を返さなかった。 |

F05 out-of-scopeとF10 inventoryは必須response欠落として扱う。F05 clarifyとF07 dependencyは、保存成果と固定rating evidenceの不一致を公式scoreから読み替えずに記録する。

## Candidate32との互換比較

本resultとCandidate32 result `737d6abf557b4b2e8fe71838f072ceb5`は同じcompatibility keyを持つ。

保存済み比較viewの差分方向は`Candidate33 - Candidate32`である。

| KPI中央値 | Candidate32 | Candidate33 | Candidate33 - Candidate32 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 93.750 | -6.250 |
| `total_tokens` | 3,896,185 | 2,936,701 | -959,484 |
| `elapsed_seconds` | 1,231.870 | 1,227.344 | -4.527 |

all-agent token合計はCandidate32の`19,466,514`に対しCandidate33が`15,011,466`で、差は`-4,455,048`だった。

参考としてCandidate31比では、`total_tokens`中央値が`-723,529`（`-19.77%`）、60 run合計が`-3,442,298`（`-18.65%`）、`elapsed_seconds`中央値が`-326.084`秒（`-20.99%`）だった。`quality_score`中央値は`-6.250`だった。

この比較は3 KPIの数値差と保存evidenceの分布だけを示す。winner、採用、release判断へ変換しない。

## Token context補助観測

この節はLayer 2 extensionに保存されたsession usageとroot rolloutを集約した補助観測であり、KPI schemaやquality ratingへの入力ではない。

- completed child session数はCandidate32とCandidate33の両方で`55`だった。
- root rollout上のworker spawnはCandidate32が`57` callすべて`fork_turns=all`、Candidate33が`55` callすべて`fork_turns=none`だった。
- child token合計は`6,294,591`から`3,239,709`へ`-3,054,882`（`-48.53%`）だった。
- root token合計は`13,171,923`から`11,771,757`へ`-1,400,166`（`-10.63%`）だった。
- child cached inputは`4,899,840`から`2,520,832`へ`-2,379,008`（`-48.55%`）だった。
- child noncached inputは`1,273,154`から`659,224`へ`-613,930`（`-48.22%`）だった。
- 12 case中9 caseでtoken合計が減った。最大減少はF07 canonical `-1,065,767`、F08 `-935,729`、F06 `-872,918`だった。
- F01は`+83,195`、F04は`+65,548`、F10 monthlyは`+31,990`であり、全case一様の減少ではなかった。

root prompt自体はCandidate32の`2,550 bytes`からCandidate33の`3,003 bytes`へ増えた。all-agent token減少はprompt表面の短縮ではなく、worker context継承と実行中context量の変化に対応している。ただし、N=5の観測範囲外へ因果を一般化しない。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate33-worker-context-sufficiency-owner-producer-v5-expanded12-global-m24-n5-20260718-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/7ad52060cd0e4352a2e4aaf1bbf715eb.json`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate32-vs-candidate33-owner-producer-v5-n5.json`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
