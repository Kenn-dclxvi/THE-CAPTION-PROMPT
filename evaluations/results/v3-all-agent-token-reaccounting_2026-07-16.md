# v3 all-agent token再集計

## 位置づけ

v3で保存済みだった`prompt-set-result/v1`の`total_tokens`はroot agentだけのusageだった。この文書は、同じrunの保存済みCodex rolloutからroot agentと全descendant SA sessionの最終usageを合算し、all-agent tokenとしてappend-onlyで再集計した結果を記録する。

旧`prompt-set-result/v1`と旧比較文書はroot-onlyの履歴として変更しない。再集計結果は`prompt-set-result/v2`であり、各resultの`source_result_id`が元のv1 resultを示す。`quality_score`と`elapsed_seconds`は元resultから変更していない。

token accounting identityは次のとおりである。

```json
{
  "scope": "all_agents",
  "revision": "v1",
  "source": "codex_rollout_final_usage_by_workspace"
}
```

## 再集計範囲

- source result: 28件
- run: 1,536件
- usage欠損または推計値: 0件
- source registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- backfill evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/v3-all-agent-token-reaccounting-20260716-r1`

各runはevaluation workspaceを厳密一致させ、root threadから再帰的に到達できるsessionだけを対象にした。forked rolloutに継承された親の`session_meta`はsession自身のidentityとして扱わず、rollout先頭のmetadataを使用した。全sessionの最終usageとroot-only保存値が一致する場合だけv2 resultへ登録した。

## N=1比較

`total_tokens`は12 caseのiteration合計である。

| set | `quality_score` | root-only履歴 | all-agent `total_tokens` | all-agent - root-only | `elapsed_seconds` |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 100.000 | 4,015,257 | 9,201,674 | 5,186,417 | 3,041.619秒 |
| Candidate1 | 100.000 | 3,782,381 | 4,974,295 | 1,191,914 | 1,699.304秒 |
| Candidate2 | 100.000 | 3,513,610 | 7,620,229 | 4,106,619 | 2,627.176秒 |

all-agent比較viewは`baseline-candidate1-candidate2-expanded12-global-m24-n1-all-agent-20260716.json`として外部comparison viewへ保存した。

## N=5比較

各値は5 iterationの中央値であり、各iterationの`total_tokens`は12 caseの合計である。

| set | `quality_score` | root-only履歴 | all-agent `total_tokens` | 中央値差 | `elapsed_seconds` |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 100.000 | 3,888,115 | 8,925,798 | 5,037,683 | 2,828.032秒 |
| Candidate1 | 97.917 | 4,338,633 | 5,732,480 | 1,393,847 | 1,932.971秒 |
| Candidate2 | 100.000 | 3,841,478 | 7,381,355 | 3,539,877 | 2,477.185秒 |
| Candidate3 | 100.000 | 3,112,542 | 6,240,246 | 3,127,704 | 2,465.865秒 |
| Candidate4 | 100.000 | 4,579,476 | 5,909,205 | 1,329,729 | 1,676.820秒 |
| Candidate5 | 100.000 | 4,503,816 | 5,740,441 | 1,236,625 | 1,714.914秒 |
| Candidate6 | 100.000 | 4,692,041 | 5,951,457 | 1,259,416 | 1,715.486秒 |

all-agent比較viewは`baseline-candidate1-candidate2-candidate3-candidate4-candidate5-candidate6-expanded12-global-m24-n5-all-agent-20260716.json`として外部comparison viewへ保存した。

root-only値ではBaselineがCandidate5より615,701少なく見えていたが、all-agent値ではBaselineがCandidate5より3,185,357多い。したがって、root-only値から導いた「SA利用setほどtokenが少ない」という読みは成立しない。Candidate1とCandidate5のall-agent中央値差は7,961、Candidate6とCandidate5の差は211,016である。この結果は数値差の記録であり、winner、採用、release判断を行わない。

## Candidate5追加18 result

同条件の追加18件、合計1,080 runもall-agentへ再集計した。

| 集計対象 | all-agent `total_tokens` |
| --- | ---: |
| 18 resultの中央値 | 5,980,342.5 |
| 最小 | 5,436,524 |
| 最大 | 6,884,831 |
| 平均 | 6,019,644.9 |

qualityとelapsedの値、score内訳、fixtureに関する観測は元resultのままである。token値だけはこのall-agent再集計を現行値として使い、旧文書のroot-only値と同じ比較へ混ぜない。

## Result identity

| set | N | source v1 result | all-agent v2 result |
| --- | ---: | --- | --- |
| Baseline | 1 | `0ffce98fda7b48a7a1e188c0a8ff709c` | `8233fe784faf48f4a2aaa96f863e9148` |
| Candidate1 | 1 | `4584e31f75374cedbdda3fa81c8e2edf` | `7848a8d0255a49bea5908ac93a82b845` |
| Candidate2 | 1 | `6dd0458db8eb46f9a9e41306d373158a` | `c508ab4078aa4128832b718672ebb7f8` |
| Baseline | 5 | `7748386da9cf4cc8a5fc35025f5972f2` | `b38148b0022343539b928058aa15d3a2` |
| Candidate1 | 5 | `7105fa9353824d3187ad299c1f3542f3` | `fd30705e3c2e4f45b891d468f75badde` |
| Candidate2 | 5 | `0fe03069e84a4778a8b2cee90c327878` | `5802f1c4e12d48b9970fb4023c534a62` |
| Candidate3 | 5 | `35650f74c9034c959d6806350ec9a5dd` | `59f55a2897d84f8c87da5c93e39793a8` |
| Candidate4 | 5 | `24874ca754284603a79b5144137e5c81` | `bc2eb141b4ca4909ba7953a47231e4e0` |
| Candidate5 | 5 | `c93afa1d55b149b6b6499219d07d0f77` | `da8505348e4741a4a413618fbfa9aa1f` |
| Candidate6 | 5 | `db405b73e3ca4ed5aa367bed3fa1e5ce` | `e6d8b72bc13c449da2092f92b666fa38` |
