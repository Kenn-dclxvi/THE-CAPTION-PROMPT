# Candidate43 / Candidate56 resolved fixed read boundary catalog固定対象試験

## 結論

Candidate56はF系gateを通過したが、A系非適用gateで停止した。

F05 / F10は10 / 10 score `4`、root-only、zero driftだった。F10は5 runすべてが3 top-level tool callへ収束し、token合計はCandidate43の`848,388`から`371,820`へ`56.17%`減った。

一方、A01 / A02はCandidate43が10 / 10 score `4`、Candidate56が9 / 10 score `4`だった。Candidate56 A02 iteration 4は`git diff --check`を実行せずscore `3`となった。A02のmodel step / tool callは`51 / 46`でCandidate43と同数だが、shell commandは`47 -> 70`へ増えた。

Candidate56を`catalog_fixed_targeted_n5 / stopped`とする。standard14、A06、採用、release、本体反映へ進めない。

## 固定条件

- F系Candidate43 result: `53f46f39073c4bf1aa1d7dc8fbc4b892`
- F系Candidate56 result: `1d968723dd4140b8819b204211712105`
- F系compatibility key: `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a`
- A系Candidate43 result: `c9c2d55acbd944a2a7026457aa1d6efd`
- A系Candidate56 result: `16fa6241369743fda3fa8e7a56306d31`
- A系compatibility key: `5c1cc7a1844a073f074ca57aca27f601f5a3a184523d4c30dafbb3b46bb872b2`
- model / reasoning: `gpt-5.6-sol` / `high`
- execution: global queue、`M=10`、各case `N=5`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`

初回F系campaignは実行時catalogが`8d068981...`となり、30 attemptを外部計測失敗として除外した。比較へ使った再試行は1 slot probeで固定catalog一致を確認してから残り9 slotを実行し、除外0で登録した。

## F系結果

| case | 指標 | Candidate43 | Candidate56 | 差 |
| --- | --- | ---: | ---: | ---: |
| F05 | score `4` | 5 / 5 | 5 / 5 | 0 |
| F05 | token合計 | 330,657 | 192,021 | -138,636、-41.93% |
| F05 | model step / tool call | 22 / 17 | 13 / 8 | -9 / -9 |
| F05 | shell command | 20 | 20 | 0 |
| F05 | elapsed中央値 | 33.201秒 | 26.236秒 | -6.965秒、-20.98% |
| F10 | score `4` | 4 / 5 | 5 / 5 | +1 |
| F10 | token合計 | 848,388 | 371,820 | -476,568、-56.17% |
| F10 | model step / tool call | 48 / 43 | 20 / 15 | -28 / -28 |
| F10 | shell command | 55 | 55 | 0 |
| F10 | elapsed中央値 | 85.624秒 | 55.772秒 | -29.852秒、-34.86% |

F10のiteration順tool callはCandidate43の`11 / 3 / 11 / 11 / 7`に対して、Candidate56は`3 / 3 / 3 / 3 / 3`だった。個別commandとexitを保ち、固定readのtop-level context再送だけを減らした。

## A系結果

| case | 指標 | Candidate43 | Candidate56 | 差 |
| --- | --- | ---: | ---: | ---: |
| A01 | score `4` | 5 / 5 | 5 / 5 | 0 |
| A01 | token合計 | 538,947 | 174,208 | -364,739、-67.68% |
| A01 | model step / tool call | 24 / 19 | 11 / 6 | -13 / -13 |
| A01 | shell command | 19 | 9 | -10 |
| A01 | elapsed中央値 | 46.149秒 | 14.849秒 | -31.300秒、-67.82% |
| A02 | score `4` | 5 / 5 | 4 / 5 | -1 |
| A02 | token合計 | 1,647,964 | 1,547,584 | -100,380、-6.09% |
| A02 | model step / tool call | 51 / 46 | 51 / 46 | 0 / 0 |
| A02 | shell command | 47 | 70 | +23、+48.94% |
| A02 | elapsed中央値 | 98.260秒 | 108.720秒 | +10.460秒、+10.65% |

失敗runは開始identity後に`rg --files`を実行し、その結果から選んだ`run.sh`、repository内参照、entrypoint、test、history、階層指示を同一model stepで取得した。TaskSpecがread集合を列挙したのではなく、modelがrepository stateから集合を決めているため、Candidate56の`FIXED_READ`がA系authority探索へ流入した事実である。

最終確認でも`git diff -- run.sh`、`git diff --stat`、`git status --short`は実行したが、必須の`git diff --check`を実行しなかった。単なるtoken変動ではなく、A系非適用境界と完了条件の両方で停止条件に該当する。

## 次の対象

次candidateでは文を追加しない。Candidate56の`FIXED_READ`一文を、実行前TaskSpecがread pathまたはcommandを有限列挙している場合だけへ置換する。repository authority / stateからread対象を決めるoperationは、列挙後に見えても常に対象外とする。

この置換でF10の明示列挙された固定read経路を維持し、A02のrepository探索へmethod controlが流入しないかを再確認する。

## Evidence

- F系campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate56-resolved-fixed-read-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-20260721-r2`
- A系Candidate43 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-20260721-r1`
- A系Candidate56 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate56-resolved-fixed-read-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-20260721-r1`

Candidate56は対象試験で停止した。candidate作成、評価、採用、release、本体反映は別状態である。
