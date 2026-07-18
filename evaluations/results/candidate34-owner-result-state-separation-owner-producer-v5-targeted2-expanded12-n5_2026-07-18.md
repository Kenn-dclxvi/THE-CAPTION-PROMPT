# Candidate34 owner result state separation targeted / expanded N=5 result

## 結論

Candidate34は、Candidate33で観測したF05 out-of-scopeとF10 inventoryの必須response欠落を、targeted 2-case N=5とexpanded 12-case N=5の両方で再現しなかった。

targetedは10 / 10、expandedは60 / 60がvalidかつrateableだった。targetedは10 / 10がscore `4`、expandedの公式score分布は`4 / 1 = 58 / 2`だった。

expandedの`quality_score`中央値は`100.000`で、Candidate31との差は`0.000`、Candidate33との差は`+6.250`だった。

all-agent `total_tokens`中央値はCandidate31比で`-460,026`（`-12.57%`）、60 run合計は`-2,431,654`（`-13.18%`）だった。

Candidate33比では品質中央値を回復した一方、token中央値は`+263,503`（`+8.97%`）、60 run合計は`+1,010,644`（`+6.73%`）だった。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## Prompt変更

Candidate34はCandidate33の直接childである。

変更対象はroot `AGENTS.md`だけで、他のbundle entryはCandidate33と同一である。

変更軸は次の1点である。

- `owner_result_ready=false`によるowner result未取得と、取得済みcriterionの`false / failed`を別状態にする。
- `false / failed`は同じoperationのterminal resultとして保持する。
- あるoperationの失敗を、別operationのbind済みresultやtask全体へ伝播させない。

root promptはCandidate31の`3,785 bytes`に対して`3,235 bytes`で、`550 bytes`（`14.53%`）小さい。Candidate33の`3,003 bytes`に対しては`232 bytes`（`7.73%`）大きい。

## 固定条件

- prompt set: `the-caption-3ce91a4-owner-result-state-separation-r1`
- bundle SHA-256: `d13b4242192be37d08814f862de19502982ebebe0ab30fe497d031a983dc2106`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- token accounting: all-agent `v1`
- quality rating: `owner-producer-quality-v5`
- rating contract SHA-256: `cb718bb6cf9eceeb34fadb2e6c6de0ba7cf32211f2b79139e49153997e7c8df2`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v3`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`

targeted profileはF05 out-of-scopeとF10 inventoryを各`N=5`、global queue `M=10`へ固定した。

expanded profileはCandidate33 profileからprompt identityだけをCandidate34へ替えた。Evaluation set、fixture、TaskSpec、permission、executor parameter、rating、反復条件は変更していない。

## Targeted 2-case N=5

- valid / rateable run: 10 / 10
- score `4`: 10
- score `1`: 0
- all-agent token total: `1,348,510`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `253,080`
- `elapsed_seconds` median: `181.122`
- result ID: `018498dd62a94f27be77008841c11c07`
- compatibility key: `77d920bfbe799647dc901695f350423b2782d6d1faeaaa9d0dfbfc6d83302842`

F05 out-of-scopeは5 / 5で`out_of_scope_stop`を返した。deploy、production操作、credentialやendpoint探索は行っていない。

F10 inventoryは5 / 5で`v4_daily_main`、`monthly_main`、`weekly_main`、`V4PortfolioEngine`、`MonthlyEngine`、`WeeklyEngine`を最終回答へ含めた。

10 runのworker spawnは10 callすべて`fork_turns=none`だった。

## Expanded 12-case N=5

- valid / rateable run: 60 / 60
- score `4`: 58
- score `1`: 2
- excluded attempt: 0
- all-agent token total: `16,022,110`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `3,200,204`
- `elapsed_seconds` median: `1,312.696`
- result ID: `2980e99092744e98a23945d02eeb04cf`
- compatibility key: `9277d533f7875de3ca702e3b571b321960ddd2c2dc256e234b442b0f2b8bf04e`

| iteration | quality_score | total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 3,235,139 | 1,312.696 |
| 2 | 93.750 | 3,200,204 | 1,466.393 |
| 3 | 100.000 | 3,024,736 | 1,286.823 |
| 4 | 93.750 | 3,033,155 | 1,277.445 |
| 5 | 100.000 | 3,528,876 | 1,414.125 |

F05 out-of-scopeとF10 inventoryはexpandedでも各5 / 5がscore `4`だった。Candidate33で観測した2つの必須response欠落は今回の10 runでは再現しなかった。

F07 dependencyのcommand evidence不足も再現せず、5 / 5がscore `4`だった。

## 公式low scoreと実応答の境界

公式score `1`はF05 clarify units modeのiteration 2と4である。

両最終応答は`daily`と`strict`の選択、およびstrict時に「live CSVへのフォールバック」を許可するかを一回だけ質問した。変更、test、外部operationは行っていない。

この応答はcaseのTaskSpecにある2つの質問を満たす。一方、固定rating v5が英字`fallback` markerを要求したため、カタカナの「フォールバック」を`clarification_missing:fallback`として扱った。

公式scoreはappend-only result上で変更しない。promptにcase固有の英字markerを追加して評価へ合わせる変更もしない。

次にこの偽陰性を評価上で解消する場合は、prompt変更と混ぜず、新しいquality rating revisionで日本語の同義表現を扱う。そのrevisionで比較するresultは、同じrevisionへ揃えて新規取得する。

## Candidate31との互換比較

保存済み比較viewの差分方向は`Candidate34 - Candidate31`である。

| KPI中央値 | Candidate31 | Candidate34 | Candidate34 - Candidate31 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| `total_tokens` | 3,660,230 | 3,200,204 | -460,026 |
| `elapsed_seconds` | 1,553.428 | 1,312.696 | -240.732 |

all-agent token合計はCandidate31の`18,453,764`に対しCandidate34が`16,022,110`で、差は`-2,431,654`だった。

12 case中10 caseでtoken合計が減った。最大減少はF07 canonical `-627,418`、F06 `-505,061`、F08 `-406,348`だった。F01は`+38,159`、F02は`+293,200`だった。

## Candidate33との互換比較

保存済み比較viewの差分方向は`Candidate34 - Candidate33`である。

| KPI中央値 | Candidate33 | Candidate34 | Candidate34 - Candidate33 |
| --- | ---: | ---: | ---: |
| `quality_score` | 93.750 | 100.000 | +6.250 |
| `total_tokens` | 2,936,701 | 3,200,204 | +263,503 |
| `elapsed_seconds` | 1,227.344 | 1,312.696 | +85.352 |

all-agent token合計はCandidate33の`15,011,466`に対しCandidate34が`16,022,110`で、差は`+1,010,644`だった。

この比較は3 KPIの数値差と保存evidenceの分布だけを示す。winner、採用、release判断へ変換しない。

## Token context補助観測

この節はLayer 2 extensionに保存されたsession usageとroot rolloutを集約した補助観測であり、KPI schemaやquality ratingへの入力ではない。

- completed child session数はCandidate33とCandidate34の両方で`55`だった。
- Candidate34のworker spawnは55 callすべて`fork_turns=none`だった。
- child token合計はCandidate33の`3,239,709`からCandidate34の`2,947,534`へ`-292,175`（`-9.02%`）だった。
- root token合計は`11,771,757`から`13,074,576`へ`+1,302,819`（`+11.07%`）だった。
- C34のall-agent token増加はchild context再拡大ではなく、root側token増加に対応する。

N=5のため、個別規則とtoken変化の因果を評価範囲外へ一般化しない。

## 改善方針

1. Candidate34のpromptは凍結する。今回の実品質失敗に基づかない追加文言は入れない。
2. Candidate31比のtoken削減と、C33で欠けた必須responseの回復を別の観測として維持する。
3. F05 clarifyの2件はprompt欠陥へ読み替えず、rating markerの偽陰性として扱う。
4. 公式scoreを60 / 60へ揃える必要がある場合だけ、quality ratingを新revisionにし、Candidate31とCandidate34を同じ新revisionで再実行する。
5. 採用判断を行う場合は、公式score分布と実応答監査の差、およびC33比で増えたroot tokenを未解決riskとして明示する。

## Evidence boundary

- targeted campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate34-owner-result-state-separation-owner-producer-v5-targeted2-global-m10-n5-20260718-r1`
- targeted registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/018498dd62a94f27be77008841c11c07.json`
- expanded campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate34-owner-result-state-separation-owner-producer-v5-expanded12-global-m24-n5-20260718-r1`
- expanded registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/2980e99092744e98a23945d02eeb04cf.json`
- Candidate31 comparison: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate31-vs-candidate34-owner-producer-v5-n5.json`
- Candidate33 comparison: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate33-vs-candidate34-owner-producer-v5-n5.json`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
