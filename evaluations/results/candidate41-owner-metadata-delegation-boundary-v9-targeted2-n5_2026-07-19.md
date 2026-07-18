# Candidate41 owner metadata / delegation boundary targeted N=5

## 結論

Candidate41をF05 clarificationとF10 monthly reviewで各5回、`outcome-quality-owner-diagnostic-v9`により実行した。10 / 10がscore `4`だった。

Candidate41ではF05 / F10の全runがroot sessionだけで完了した。worker spawnとwaitは0だった。C35でF10に観測されたworker起動、owner identity照合、root / childの重複readは、この10 runでは発生しなかった。

Candidate41 - Candidate35のKPI中央値差は、`quality_score = 0.000`、`total_tokens = -238,617`、`elapsed_seconds = -131.504`だった。10 runのtoken合計差は`-1,077,725`である。

この結果は固定した2 case、N=5の観測である。採用、release承認、THE-CAPTION本体反映は未判断、未実施である。

## Prompt変更

- prompt set: `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1`
- direct source: `the-caption-3ce91a4-root-control-only-r1`（Candidate35）
- bundle SHA-256: `048f6693ae588feb0cd27f13f08637adb6b0cc376d94a4a4d4072662b1b747d7`
- changed target: root `AGENTS.md`だけ

変更predicateは一つである。

> TaskSpecのcriterion owner語列だけではworker operationを作らない。TaskSpecが独立したproducer executionを明示した場合だけworkerへ委譲し、それ以外はrequired outcomeを実行するagentをproducerとする。

このpredicateへ整合させるため、既存`PRODUCER`からowner語列によるproducer role identity固定を外し、既存`OWNER`を`OWNER_ROLE`へ置換した。result unit、evidence、invalidation、projection条件は追加していない。

## 固定条件

- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1`
- Evaluation set identity: `4564c49730ab0d135bb2a1ff5530d02f49f71808e4ee2c2c4405beca99a1cca7`
- case / iteration: 2 case × `1..5`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- model: `gpt-5.6-sol`、reasoning effort `high`
- executor: prompt set別global queue `M=10`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- compatibility key: `5d4d7d7ba3aa2b120560a2f148585c40dea55574dca670adb161b2f9604837da`
- token accounting: all-agent `v1`

C35、C38、C40のv9 targeted resultとEvaluation set、fixture、TaskSpec、model、Agent環境、permission、executor parameter、rating、反復条件が一致する。prompt identityだけが異なる。

## KPI

差分方向はCandidate41 - Candidate35である。

| KPI | Candidate35 | Candidate41 | 差 |
| --- | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 0.000 |
| median `total_tokens` | 431,645 | 193,028 | -238,617 (-55.28%) |
| median `elapsed_seconds` | 229.816 | 98.312 | -131.504 (-57.22%) |
| 10 run token合計 | 2,073,880 | 996,155 | -1,077,725 (-51.97%) |
| score `4` | 10 | 10 | 0 |

保存済み4 resultの中央値は次のとおりである。

| prompt set | `quality_score` | `total_tokens` | `elapsed_seconds` | score分布 |
| --- | ---: | ---: | ---: | --- |
| Candidate35 | 100.000 | 431,645 | 229.816 | `4`: 10 |
| Candidate38 | 100.000 | 473,304 | 237.173 | `4`: 10 |
| Candidate40 | 100.000 | 410,324 | 224.341 | `4 / 1`: 9 / 1 |
| Candidate41 | 100.000 | 193,028 | 98.312 | `4`: 10 |

KPI差はwinner、採用、release判断を意味しない。

## Case別観測

| case | score `4` | Candidate35 token合計 | Candidate41 token合計 | 合計差 | C35 token中央値 | C41 token中央値 | 中央値差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| F05 clarification | 5 / 5 | 692,914 | 325,102 | -367,812 (-53.08%) | 140,609 | 85,117 | -55,492 (-39.47%) |
| F10 monthly review | 5 / 5 | 1,380,966 | 671,053 | -709,913 (-51.41%) | 276,336 | 107,911 | -168,425 (-60.95%) |

F05は5 / 5で、`daily` / `strict`の選択と、strict時のlive CSV fallback policyを一つのclarificationとして返した。変更、test、外部operationは行っていない。

F10は5 / 5で、major findingを`src/app/entrypoints/monthly_main.py:25`へ結び付けた。`args.format_test`を使わず`args.force`を渡す直接根拠と、`--format-test` / `--force`のuser-visible impactを返した。artifactは変更していない。

## 実行経路

tool callとmodel stepは保存済みroot / child rolloutから集計した。model stepは各sessionの`token_count` event数である。

### F05

| 観測 | Candidate35 | Candidate41 | 差 |
| --- | ---: | ---: | ---: |
| child session | 5 | 0 | -5 |
| `exec` | 19 | 14 | -5 |
| `spawn_agent` | 5 | 0 | -5 |
| `wait_agent` | 6 | 0 | -6 |
| tool call合計 | 30 | 14 | -16 |
| model step | 40 | 19 | -21 |

### F10

| 観測 | Candidate35 | Candidate41 | 差 |
| --- | ---: | ---: | ---: |
| child session | 5 | 0 | -5 |
| `exec` | 51 | 27 | -24 |
| `spawn_agent` | 5 | 0 | -5 |
| `wait_agent` | 7 | 0 | -7 |
| tool call合計 | 63 | 27 | -36 |
| model step | 74 | 32 | -42 |

Candidate41の各runはroot sessionだけだった。root / child間のauthority、diff、sourceの重複readは構造上発生していない。

## 診断境界

- owner-producer evidence eligible: 0 / 10
- owner-producer evidence inadmissible: 10 / 10
- command protocol violation: 0 / 10

owner-producer evidence不成立は、TaskSpecのcriterion owner語列をworker指定として扱わず、childを起動しなかったことに対応する。v9ではowner-producer evidenceは`diagnostic_only`であり、成果、operation boundary、required validationの`quality_score`へ入らない。

これはowner-producer evidenceを不要と一般化する判断ではない。TaskSpecが独立したproducer executionを明示するcaseは、Candidate41でもworker委譲の対象に残る。

## 事前停止条件の判定

| 停止条件 | 観測 | 判定 |
| --- | --- | --- |
| 一件でもscore `4`を満たさない | 10 / 10がscore `4` | 非該当 |
| F05 / F10でTaskSpecにないworker起動が残る | child session、spawn、waitはすべて0 | 非該当 |
| F10のfindingまたはlocationが省略される | 5 / 5でmajor、`:25`、根拠、impactを記載 | 非該当 |
| F10のtool call、model step、case tokenがC35から減らない | tool call `-36`、model step `-42`、token合計`-709,913` | 非該当 |
| quality維持にresult unit等の追加条件が必要になる | 追加せず10 / 10 score `4` | 非該当 |

定義した停止条件は発火しなかった。targeted試験の完了条件は満たした。

## Evidence境界

- profile: `evaluations/profiles/candidate41-owner-metadata-delegation-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-r1.json`
- result ID: `37fe235e451e46b688d14ca0c52afbd9`
- result content SHA-256: `b2a14fa2e9fcd7cb39850bf76462963048d10228140d04f8fe053e44e0058ba9`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate41-owner-metadata-delegation-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-20260719-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/37fe235e451e46b688d14ca0c52afbd9.json`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/c35-c38-c40-c41-outcome-quality-owner-diagnostic-v9-targeted2-n5-20260719-r1.json`
- valid / rateable: 10 / 10
- retry / excluded attempt: 0 / 0
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。

非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
