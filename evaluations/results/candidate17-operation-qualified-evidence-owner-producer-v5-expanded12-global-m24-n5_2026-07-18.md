# Candidate17 owner-producer rating v5 expanded N=5 result

## 結論

Candidate17を、現行のEvaluation setとquality ratingへ固定し、expanded 12-caseを各`N=5`で新規実行した。

60 / 60 valid runを採点・登録し、score `4 / 3 / 1 = 49 / 10 / 1`だった。

11件の低scoreのうち10件は、主要成果を満たしたがcriterion ownerに対応するproducer resultが成立しなかったscore `3`である。

残る1件はF05 clarificationで`fallback`確認が欠落し、owner producer resultも成立しなかったscore `1`である。

旧Candidate17 resultは変更せず、現行条件のappend-only resultを追加した。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- profile: `candidate17-operation-qualified-evidence-owner-producer-v5-expanded12-global-m24-n5-r1`
- prompt set: `the-caption-9b3a96a-operation-qualified-evidence-r1`
- bundle SHA-256: `4c492dbb7b7bdf62d1602c6e6b1235cbce5ba2116f763cc64ae876527a740d4a`
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
- command evidence: `the-caption-prompt.all-agent-command-evidence/v3`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`

## 結果

- valid / rateable run: 60 / 60
- score `4`: 49
- score `3`: 10
- score `1`: 1
- score-4 owner-evidence eligible: 49 / 60
- owner evidence status: available 44、not applicable 5、failed 11
- required command成功証跡不足: 0
- excluded attempt: 1
- all-agent token total: `25,856,226`
- `quality_score` median: `95.833`
- all-agent `total_tokens` median: `4,863,641`
- `elapsed_seconds` median: `2,349.530`
- result ID: `f8daa2e0ef43425c87a234aa8c514210`
- compatibility key: `9277d533f7875de3ca702e3b571b321960ddd2c2dc256e234b442b0f2b8bf04e`

| iteration | quality_score | total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 91.667 | 4,679,382 | 2,273.518 |
| 2 | 95.833 | 5,951,966 | 2,626.622 |
| 3 | 95.833 | 4,863,641 | 2,295.864 |
| 4 | 95.833 | 4,820,095 | 2,349.530 |
| 5 | 93.750 | 5,541,142 | 2,433.042 |

初回dispatchのF10 monthly iteration 1は`codex_model_at_capacity`となった。

このattemptは外部要因として除外し、同じslotを再実行してvalid resultを得た。除外attemptはKPIへ含めていない。

## 低scoreの分布

| case | score分布 | 保存evidenceに基づく理由 |
| --- | --- | --- |
| F05 clarify units mode | `3`: 4、`1`: 1 | 5 / 5でindependent boundary checkのproducer resultがなく、うち1件はclarification responseの`fallback`確認も欠落した。 |
| F07 dependency provenance pair | `4`: 4、`3`: 1 | iteration 5だけindependent contract checkのproducer resultがなかった。主要成果とrequired command成功証跡は満たした。 |
| F10 monthly format-test review | `3`: 5 | 5 / 5でmajor finding、直接根拠、user-visible impact、zero driftを返したが、independent response checkのproducer resultがなかった。 |

その他9 caseは各5 / 5でscore `4`だった。

F10 entrypoint inventoryは5 / 5で所定inventory、zero drift、independent response checkを完了した。

## Candidate31との互換比較

本resultとCandidate31 rating v5 result `1f67e36d3d3f414d834ac186d6fc2d33`は同じcompatibility keyを持つ。

保存済み比較viewの差分方向は`Candidate17 - Candidate31`である。

| KPI中央値 | Candidate31 | Candidate17 | Candidate17 - Candidate31 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 95.833 | -4.167 |
| `total_tokens` | 3,660,230 | 4,863,641 | +1,203,411 |
| `elapsed_seconds` | 1,553.428 | 2,349.530 | +796.103 |

この表は3 KPIの数値差と保存evidenceの分布だけを示す。winner、改善・悪化、採用判断へ変換しない。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate17-operation-qualified-evidence-owner-producer-v5-expanded12-global-m24-n5-20260718-v3-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/f8daa2e0ef43425c87a234aa8c514210.json`
- comparison view: `comparisons/candidate17-vs-candidate31-owner-producer-v5-n5.json`
- final archive SHA-256: `9cf518e733c755cc1260c4c3625dbb069dde9a3dbdcb01ba44ebc7083ee8659d`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
