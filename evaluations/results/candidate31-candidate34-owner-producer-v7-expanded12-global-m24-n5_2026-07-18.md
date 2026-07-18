# Candidate31 / Candidate34 owner-producer v7 expanded N=5 comparison

## 結論

command evidence v4と`owner-producer-quality-v7`へ評価条件を揃え、Candidate31とCandidate34をexpanded 12 case、`N=5`で新規実行した。

両prompt setとも60 / 60がvalidかつrateableで、全60件がscore `4`だった。`quality_score`中央値は両方とも`100.000`である。

Candidate34のall-agent `total_tokens`中央値はCandidate31比で`-625,986`（`-15.98%`）、60 run合計は`-2,779,489`（`-14.39%`）だった。5反復すべてでCandidate34のtoken合計が小さかった。

`elapsed_seconds`中央値差は`-18.304`秒（`-1.23%`）だった。ただし、反復別でCandidate34が短い回は1 / 5であり、安定した短縮とは判断しない。

評価collectorの偽陰性は今回の120 runでは観測されなかった。Candidate34のF07 dependencyとCandidate31のF04は、それぞれ5 / 5がscore `4`だった。

採用、release承認、THE-CAPTION本体反映は未判断、未実施である。

## 評価更新

rating v6で残ったCandidate34 F07 dependencyのscore `3`は、required validationが成功していたにもかかわらず、command evidence v3がcustom wrapperのmarkdown-heading形式を固定commandへbindできなかったcollector偽陰性だった。

command evidence v4は、source側のtemplateと固定name-command表へ一意にbindできる場合だけ、`### <name>`直後の`exit_code=0`を成功証跡として収集する。workerの自己申告だけでは成功扱いしない。

rating v7はcommand evidenceをv4へ更新した。prompt、Evaluation set、fixture、TaskSpec、permission、executor parameter、反復条件はv6から変更していない。

- quality rating: `owner-producer-quality-v7`
- rating contract SHA-256: `5df75d3214f9dacd49198e261f2f0abb97f1de60f7560e4b4e40baff50bdac9a`
- C31 profile SHA-256: `c65b9e6fa4d43c54e311013cb607bac1236630eb939677a97799381efd7e48ea`
- C34 profile SHA-256: `41b6b8197aa764c579aceafc093b64be62d984951b513160acde573d344eca5b`

rating v6の保存済みresultは変更していない。rating revisionが異なるv6とv7の数値は、同一comparison viewへ混ぜていない。

## 固定条件

- Evaluation set: `the-caption-expanded12-f10r3-r1`
- case / iteration: 12 case × `1..5`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- executor: global queue `M=24`、max attempts `3`
- token accounting: all-agent `v1`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v4`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`
- compatibility key: `f0a5ff65b23e2c6d67641b37f600f9bc1109829d7388daac5729d18893cf03ac`

C31とC34のprofileは`profile_id`と`prompt_set_identity`以外が同一である。実行は環境競合を避けるためC31、C34の順に行い、同時実行していない。

## KPI中央値比較

保存済みcomparison viewの差分方向は`Candidate34 - Candidate31`である。

| KPI中央値 | Candidate31 | Candidate34 | Candidate34 - Candidate31 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| `total_tokens` | 3,916,601 | 3,290,615 | -625,986 |
| `elapsed_seconds` | 1,485.419 | 1,467.115 | -18.304 |

| 集計 | Candidate31 | Candidate34 | Candidate34 - Candidate31 |
| --- | ---: | ---: | ---: |
| valid / rateable run | 60 / 60 | 60 / 60 | 0 |
| retry / excluded attempt | 0 / 0 | 0 / 0 | 0 |
| score `4` | 60 | 60 | 0 |
| score `3`以下 | 0 | 0 | 0 |
| all-agent token合計 | 19,318,346 | 16,538,857 | -2,779,489 |

## 反復別比較

| iteration | C31 quality | C34 quality | C31 tokens | C34 tokens | token差 | C31 elapsed | C34 elapsed | elapsed差 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100.000 | 100.000 | 4,080,780 | 3,290,615 | -790,165 | 1,446.180 | 1,467.115 | +20.935 |
| 2 | 100.000 | 100.000 | 4,032,216 | 3,106,436 | -925,780 | 1,590.029 | 1,396.781 | -193.248 |
| 3 | 100.000 | 100.000 | 3,395,839 | 3,180,925 | -214,914 | 1,402.439 | 1,432.263 | +29.824 |
| 4 | 100.000 | 100.000 | 3,892,910 | 3,486,326 | -406,584 | 1,605.539 | 1,617.565 | +12.026 |
| 5 | 100.000 | 100.000 | 3,916,601 | 3,474,555 | -442,046 | 1,485.419 | 1,569.734 | +84.315 |

Candidate34のtoken合計は5 / 5反復、12 case中10 caseでCandidate31より小さかった。case別で増えたのはF04 `+211,146`とF07 dependency `+55,985`である。

N=5のため、個別prompt規則とtoken差の因果を評価範囲外へ一般化しない。

## 偽陰性対応の確認

| 観測 | Candidate31 | Candidate34 |
| --- | ---: | ---: |
| 全case score `4` | 60 / 60 | 60 / 60 |
| quality audit failure | 0 | 0 |
| F04 score `4` | 5 / 5 | 5 / 5 |
| F07 dependency score `4` | 5 / 5 | 5 / 5 |

事前の実rollout replayでは、v4 collectorがCandidate34の`static_validation`、`git diff --check`、`git diff --name-only`を取得できることを確認した。また、Candidate31 v6でprocess開始に失敗した`npm run lint`は成功証跡として取得しなかった。

今回の新規N5では両prompt setの全runがscore `4`であり、v6で観測したcollector偽陰性は再現しなかった。ただし、120 runで未観測であることを全形式への完全性保証とはしない。

## 観測範囲

- 事実: C31とC34は各60 / 60がscore `4`だった。
- 事実: Candidate34のall-agent token合計は5反復すべてでCandidate31より小さかった。
- 事実: Candidate34のcase別token合計は12 case中10 caseでCandidate31より小さかった。
- 事実: elapsed差は反復間で符号が揺れた。
- 推測: 今回の範囲では、Candidate34はqualityを維持しつつtokenを抑制した可能性が高い。
- 提案: release判断ではv7 resultを現行evidenceとし、v5 / v6 resultは評価修正前の履歴として併記する。

## Evidence boundary

- C31 result ID: `d7fcf9bf3444420bac89abe775f6a72c`
- C34 result ID: `f8316de4af124128a96173abfa22e677`
- C31 result content SHA-256: `73eb9985062cf31a27b3e946229fd1113d9c0a11fd8e00d3eb218bd38559f1f0`
- C34 result content SHA-256: `c8e12458b0297806ed2eeca33a20bddd73f08ebf96069121ffc6c5050f5e218e`
- C31 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate31-operation-terminal-closure-owner-producer-v7-expanded12-global-m24-n5-20260718-r1`
- C34 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate34-owner-result-state-separation-owner-producer-v7-expanded12-global-m24-n5-20260718-r1`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate31-vs-candidate34-owner-producer-v7-n5.json`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/<result_id>.json`
- C31 final archive SHA-256: `926d83a69d7da14c8f6a0ff48f17a03fda9280245c8497fddee4d278882584db`
- C34 final archive SHA-256: `eb1d4dfa4bf9c150452eb8bd1bed86efd923ec3b92b10bad0f389e93b9f3f649`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
