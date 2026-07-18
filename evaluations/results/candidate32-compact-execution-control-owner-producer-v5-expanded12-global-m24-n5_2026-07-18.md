# Candidate32 compact execution control rating v5 expanded N=5 result

## 結論

Candidate32のexpanded 12-caseを各`N=5`で実行し、60 / 60 valid runを採点・登録した。

score分布は`4 / 2 / 1 = 58 / 1 / 1`だった。

Candidate31との互換比較では、all-agent `total_tokens`中央値が`+235,955`（`+6.45%`）、60 run合計が`+1,012,750`（`+5.49%`）だった。

root `AGENTS.md`のbyte数はCandidate31比で`32.6%`減ったが、今回のN=5ではall-agent token抑制を示す結果にならなかった。

`elapsed_seconds`中央値はCandidate31比で`-321.557`秒（`-20.70%`）だった。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- profile: `candidate32-compact-execution-control-owner-producer-v5-expanded12-global-m24-n5-r1`
- prompt set: `the-caption-3ce91a4-compact-execution-control-r1`
- bundle SHA-256: `b2bf61f5df5af45f021913c9402078e80cc7134f8a117f9e8b4d09da9cc5ff2e`
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
- profile SHA-256: `dc323fbb7309470f3ebab91e65637eccde2295ba16cb99ce05b3e212741775e2`

Candidate31 rating v5 profileからprompt identityだけをCandidate32へ替えた。Evaluation set、fixture、TaskSpec、permission、executor parameter、rating、反復条件は変更していない。

## 結果

- valid / rateable run: 60 / 60
- score `4`: 58
- score `2`: 1
- score `1`: 1
- excluded attempt: 0
- all-agent token total: `19,466,514`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `3,896,185`
- `elapsed_seconds` median: `1,231.870`
- result ID: `737d6abf557b4b2e8fe71838f072ceb5`
- compatibility key: `9277d533f7875de3ca702e3b571b321960ddd2c2dc256e234b442b0f2b8bf04e`

| iteration | quality_score | total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 3,594,532 | 1,264.755 |
| 2 | 100.000 | 4,193,482 | 1,201.556 |
| 3 | 100.000 | 3,896,185 | 1,231.870 |
| 4 | 93.750 | 3,555,116 | 1,202.355 |
| 5 | 95.833 | 4,227,199 | 1,318.163 |

## 低scoreの境界

| case / iteration | score | 保存evidenceに基づく理由 |
| --- | ---: | --- |
| F01 market units snapshot / 5 | 2 | quality auditが`tests/unit/test_market_units_snapshot.py`を`changed_paths_mismatch`とした。TaskSpecとcapsuleは同pathを許可し、adapter validationも`unexpected_changed_paths: []`だったため、実際のpermission違反ではなく固定rating側allowlistの不整合である。 |
| F10 entrypoint inventory / 4 | 1 | Agentは対象path、engine、authority commandを調査したが、independent response check失敗後のroot最終回答が停止報告だけとなり、必須inventory 6項目を返さなかった。 |

F01の公式score `2`はappend-only result上で変更しない。rating不整合の説明を補助観測として残し、別ratingへの読み替えやin-place再採点を行わない。

F10 inventoryのscore `1`はterminal responseの実失敗として扱う。Candidate31 rating v5では同caseが5 / 5 score `4`だったため、compact化後に観測された残存riskである。

その他58 runはscore `4`だった。

## Candidate31との互換比較

本resultとCandidate31 rating v5 result `1f67e36d3d3f414d834ac186d6fc2d33`は同じcompatibility keyを持つ。

保存済み比較viewの差分方向は`Candidate32 - Candidate31`である。

| KPI中央値 | Candidate31 | Candidate32 | Candidate32 - Candidate31 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| `total_tokens` | 3,660,230 | 3,896,185 | +235,955 |
| `elapsed_seconds` | 1,553.428 | 1,231.870 | -321.557 |

all-agent token合計はCandidate31の`18,453,764`に対しCandidate32が`19,466,514`で、差は`+1,012,750`だった。

この比較は3 KPIの数値差と保存evidenceの分布だけを示す。winner、採用、release判断へ変換しない。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate32-compact-execution-control-owner-producer-v5-expanded12-global-m24-n5-20260718-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/737d6abf557b4b2e8fe71838f072ceb5.json`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate31-vs-candidate32-owner-producer-v5-n5.json`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
