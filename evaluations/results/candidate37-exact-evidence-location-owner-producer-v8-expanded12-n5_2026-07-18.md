# Candidate37 exact evidence location expanded 12-case N=5 result

## 結論

Candidate37のexpanded 12-case N=5は、60 / 60 runがvalid、rateable、score `4`だった。score `0..3`は0件で、`quality_score`中央値は`100.000`である。

targetedで確認したF05 criterion projectionとF10 source locationは、expandedでも各5 / 5でscore `4`だった。その他10 caseも各5 / 5でscore `4`だった。

F04 r2は5 / 5で実装とrequired Node commandを満たした。`node_modules`と`dist`は5 / 5でadapterが除去し、candidateによるcleanup試行は0件だった。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- profile: `candidate37-exact-evidence-location-owner-producer-v8-expanded12-f04r2-global-m24-n5-r1`
- prompt set: `the-caption-3ce91a4-exact-evidence-location-r1`
- bundle SHA-256: `c5e16b17d0da4608f0b08201ec8541870ce45902986cbe1fd53b40b9594a1559`
- evaluation set: `the-caption-expanded12-f04r2-f10r3-r2`
- evaluation set identity: `de4d1deacc470127eaf612f4b18d638febf5a2b44b1e82a1f673942b05c772c7`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- quality rating: `owner-producer-quality-v8`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v5`
- execution: global queue `M=24`、12 case、各`N=5`

## KPI

- valid / rateable run: 60 / 60
- score `4`: 60
- score `0..3`: 0
- owner-producer evidence eligible: 60 / 60
- excluded attempt: 0
- all-agent token total: `24,802,720`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `5,014,110`
- `elapsed_seconds` median: `2,065.663`
- result ID: `f5678385b48141d9ac5ce821726dedbf`
- compatibility key: `1fb630b6e729ada4a95aac6bc9e54b44547e69ef209c0ceb4038464f3d64f586`

| iteration | quality_score | total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 5,330,133 | 2,242.985 |
| 2 | 100.000 | 4,685,110 | 1,999.290 |
| 3 | 100.000 | 5,014,110 | 2,050.917 |
| 4 | 100.000 | 5,189,383 | 2,211.757 |
| 5 | 100.000 | 4,583,984 | 2,065.663 |

## Case別score

| case | score 4 | score 0..3 |
| --- | ---: | ---: |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 5 | 0 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 5 | 0 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 5 | 0 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY r2` | 5 | 0 |
| `TC-F05-CLARIFY-UNITS-MODE` | 5 | 0 |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 5 | 0 |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 5 | 0 |
| `TC-F07-CANONICAL-V4-RUNNER` | 5 | 0 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 5 | 0 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 5 | 0 |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 5 | 0 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 5 | 0 |

## 試験診断

command collectorは、9 / 60 runで合計26件のprotocol violationを診断として保存した。内訳はmachine-bound exitへ結び付かなかった非requiredのread / composite commandが23件、unparsed tool callが3件である。

全caseのrequired command groupは成功証跡へ結び付いた。したがって、この26件はrequired validation不足ではなく、collectorが収集精度の改善候補として保持する診断であり、quality scoreへ算入していない。

F04では5 / 5でadapterが`node_modules`と`dist`を除去した。candidateによるadapter-owned cleanupのtool attemptとmodel reportはいずれも0件だった。このcleanupは評価基盤の責務であり、candidate qualityのcriterionにしていない。

targeted試験で発見したcleanup path未定義時のadapter例外は、空配列への正規化後に再発しなかった。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate37-exact-evidence-location-owner-producer-v8-expanded12-f04r2-global-m24-n5-20260718-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/f5678385b48141d9ac5ce821726dedbf.json`
- quality audit、Layer 4 registration、lossless archive、final compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。

N=5の観測であり、低頻度事象の不存在や評価範囲外の一般性能を保証しない。
