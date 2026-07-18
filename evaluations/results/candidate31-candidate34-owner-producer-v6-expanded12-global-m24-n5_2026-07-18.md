# Candidate31 / Candidate34 owner-producer v6 expanded N=5 comparison

## 結論

日本語の「フォールバック」を英字`fallback`と同じ意味として扱う`owner-producer-quality-v6`を追加し、Candidate31とCandidate34を同じexpanded 12-case、`N=5`で新規実行した。

両prompt setとも60 / 60がvalidかつrateableで、score分布は`4 / 3 = 59 / 1`、`quality_score`中央値は`100.000`だった。

偽陰性の対象だったF05 clarifyは、Candidate31とCandidate34の両方で5 / 5がscore `4`だった。今回の10応答はすべて英字`fallback`を使ったため、日本語「フォールバック」の受理は固定回帰試験で確認し、N5の自然観測とは分ける。

Candidate34のall-agent `total_tokens`中央値はCandidate31比で`-833,631`（`-20.90%`）、60 run合計は`-3,993,229`（`-19.84%`）だった。5反復すべてでCandidate34のtoken合計が小さかった。

`elapsed_seconds`中央値差は`-14.356`秒（`-1.07%`）だったが、反復別ではCandidate34が小さい回は3 / 5であり、安定した短縮とは判断しない。

採用、release承認、THE-CAPTION本体反映は未判断、未実施である。

## 評価更新

rating v5のF05 clarify判定は、最終応答へ`daily`、`strict`、`fallback`の英字markerを要求していた。このため、TaskSpecを満たす日本語の「フォールバック」を欠落として扱う偽陰性が再現した。

rating v6はpromptやTaskSpecを変更せず、response evidenceだけを次のsemantic marker groupへ置き換えた。semantic marker groupは、同じ意味として許可する表現の集合である。

| 意味 | 許可する表現 |
| --- | --- |
| daily mode | `daily` |
| strict mode | `strict` |
| live CSV fallback policy | `fallback` または `フォールバック` |

照合前にUnicode NFKC正規化とcasefoldを行う。command evidence v3、owner-producer evidence v1、score規則は変更していない。

- quality rating: `owner-producer-quality-v6`
- rating contract SHA-256: `de05548558f64110c6c066c80ea57a516fb1a0bfed94fc25292736264c83eee3`
- C31 profile SHA-256: `6450e831c808bdddd5aabb09eacc53868583aead149622fec85304b1299c5a01`
- C34 profile SHA-256: `8a162fe1803e985a1dd3d161fc368bc31e555f531113229cd6d15c2d3eb9973f`

rating v5の保存済みresultは変更していない。rating revisionが異なるv5とv6の数値は、同一comparison viewへ混ぜていない。

## 固定条件

- Evaluation set: `the-caption-expanded12-f10r3-r1`
- case / iteration: 12 case × `1..5`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- executor: global queue `M=24`、max attempts `3`
- token accounting: all-agent `v1`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v3`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`
- compatibility key: `d555982b81c6b8106d4c5cadea8802340c7594e164c11b49701d000ba77aef8b`

C31とC34のprofileは`profile_id`と`prompt_set_identity`以外が同一である。実行は環境競合を避けるためC31、C34の順に行い、同時実行していない。

## KPI中央値比較

保存済みcomparison viewの差分方向は`Candidate34 - Candidate31`である。

| KPI中央値 | Candidate31 | Candidate34 | Candidate34 - Candidate31 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| `total_tokens` | 3,987,791 | 3,154,160 | -833,631 |
| `elapsed_seconds` | 1,336.306 | 1,321.951 | -14.356 |

| 集計 | Candidate31 | Candidate34 | Candidate34 - Candidate31 |
| --- | ---: | ---: | ---: |
| valid / rateable run | 60 / 60 | 60 / 60 | 0 |
| score `4` | 59 | 59 | 0 |
| score `3` | 1 | 1 | 0 |
| all-agent token合計 | 20,126,171 | 16,132,942 | -3,993,229 |

## 反復別比較

| iteration | C31 quality | C34 quality | C31 tokens | C34 tokens | token差 | C31 elapsed | C34 elapsed | elapsed差 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100.000 | 97.917 | 4,048,163 | 3,908,208 | -139,955 | 1,406.948 | 1,381.580 | -25.368 |
| 2 | 100.000 | 100.000 | 3,987,791 | 2,905,962 | -1,081,829 | 1,308.708 | 1,321.951 | +13.243 |
| 3 | 100.000 | 100.000 | 4,375,143 | 3,154,160 | -1,220,983 | 1,336.306 | 1,241.668 | -94.638 |
| 4 | 100.000 | 100.000 | 3,849,857 | 2,980,812 | -869,045 | 1,242.392 | 1,411.148 | +168.756 |
| 5 | 97.917 | 100.000 | 3,865,217 | 3,183,800 | -681,417 | 1,369.677 | 1,293.567 | -76.111 |

Candidate34のtoken合計は5 / 5反復、12 case中10 caseでCandidate31より小さかった。case別で増えたのはF01 `+54,763`とF10 inventory `+74,732`である。

N=5のため、個別prompt規則とtoken差の因果を評価範囲外へ一般化しない。

## 偽陰性確認とlow score監査

| 観測 | Candidate31 | Candidate34 |
| --- | ---: | ---: |
| F05 clarify score `4` | 5 / 5 | 5 / 5 |
| 英字`fallback`を含む応答 | 5 / 5 | 5 / 5 |
| 日本語`フォールバック`を含む応答 | 0 / 5 | 0 / 5 |
| 全case score `4` | 59 / 60 | 59 / 60 |

日本語「フォールバック」を含む既知の応答がfailureなしになることは、`tests/test_response_evidence.py`の固定回帰試験で確認した。今回のN5は日本語同義語の自然発生試験ではない。

Candidate31のscore `3`はF04 iteration 5だった。実ログでは`npm run lint`がCreateProcessの`No such file or directory`で開始できず、`npm run build`は実行されていなかった。このscore `3`はcollectorの取りこぼしではなく、required validationが完了していない実行側の結果である。

Candidate34のscore `3`はF07 dependency iteration 1だった。実ログではPython dependency確認、`git diff --check`、`git diff --name-only`がすべてexit code 0だったが、custom `exec` wrapperの`### <name>`と次行の`exit_code=0`をcommand evidence v3が固定commandへbindできなかった。これはcollectorの偽陰性である。

この2件はF05のsemantic marker更新とは別系統であり、原因も同一ではない。公式v6 scoreは実ログ監査で上書きしない。

## Command evidence v4 follow-up

Candidate34で再現したcollector偽陰性は、`all-agent-command-evidence/v4`と`owner-producer-quality-v7`で修正した。

v4はsource側に`${r.name}`と`${r.exit_code}`があり、固定name-command表へ一意にbindできる場合だけ、`### <name>`直後の`exit_code=0`を成功証跡として扱う。worker final responseだけでは成功扱いしない。

実rolloutをv4 collectorへ再生し、Candidate34の`static_validation`、`git diff --check`、`git diff --name-only`を含む5 commandを取得できた。Candidate31の開始失敗した`npm run lint`は取得されず、`npm run build`も追加されなかった。

- quality rating: `owner-producer-quality-v7`
- rating contract SHA-256: `5df75d3214f9dacd49198e261f2f0abb97f1de60f7560e4b4e40baff50bdac9a`
- C31 v7 profile SHA-256: `c65b9e6fa4d43c54e311013cb607bac1236630eb939677a97799381efd7e48ea`
- C34 v7 profile SHA-256: `41b6b8197aa764c579aceafc093b64be62d984951b513160acde573d344eca5b`

v4 replayはcollector修正の検証であり、v6 resultの再採点ではない。その後、同じv7条件でC31とC34を新規実行し、[`v7 N=5 comparison`](candidate31-candidate34-owner-producer-v7-expanded12-global-m24-n5_2026-07-18.md)として分離した。

## 観測範囲

- 事実: v6のF05 clarify 10 runはすべてscore `4`だったが、10応答とも英字`fallback`を使用した。
- 事実: 日本語「フォールバック」の受理は固定回帰試験で確認した。
- 事実: Candidate34のall-agent token合計は、5反復すべてでCandidate31より小さかった。
- 事実: elapsed差の符号は反復間で揺れた。
- 事実: C31のscore `3`はrequired validation未完了、C34のscore `3`はcollector偽陰性だった。
- 提案: Candidate34のrelease判断では、現行v7 resultと評価修正前のv6 resultを分けて示す。

## Evidence boundary

- C31 result ID: `5a2e50558a064f67ac11a9d54d49bc80`
- C34 result ID: `9a414feb95744ed4970c48a859cf7ec7`
- C31 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate31-operation-terminal-closure-owner-producer-v6-expanded12-global-m24-n5-20260718-r1`
- C34 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate34-owner-result-state-separation-owner-producer-v6-expanded12-global-m24-n5-20260718-r1`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate31-vs-candidate34-owner-producer-v6-n5.json`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/<result_id>.json`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
