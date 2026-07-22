# Candidate43 / Candidate69 model reentry decision boundary 標準14項目 各5回

## 結論

Candidate69を標準14項目で各5回、合計70回実行した。70件すべてが有効かつ採点可能で、除外attempt、command protocol違反、workspace driftは0件だった。

Candidate69からCandidate43を引いた3 KPI中央値差は、`quality_score = 0.000`、all-agent `total_tokens = -955,776`、`elapsed_seconds = -248.598秒`だった。70件token合計は`17,732,662 -> 13,726,510`、`-4,006,152`、`-22.59%`である。

実行経路はtop-level tool call `639 -> 469`、`-26.60%`、token count event `710 -> 539`、`-24.08%`だった。shell commandは`705 -> 689`、`-2.27%`に留まる。したがって、token差は必要作業の大幅省略ではなく、commandやreadの間でmodelへ戻る回数を減らした方向と一致する。

一方、点数分布はCandidate43の`4 = 70`に対し、Candidate69は`4 / 3 = 69 / 1`だった。score `3`はF10 monthlyのfinding位置を`monthly_main.py:24`と返し、期待する実変更行`:25`と一致しなかった一件である。finding内容、diff、対象source、影響分析は成立していたが、行番号付きsource確認を行わなかった。

Candidate69作成前gateは全70件score `4`を要求したため、Candidate69は`standard14_evaluated / stopped`とする。model再入境界が実tokenを減らす制御対象である証拠として保持するが、採用、release、本体反映へ進めない。Candidate69へ補助説明を追加しない。

## 変更内容

Candidate69はCandidate43を直接sourceとし、root `AGENTS.md`だけへ次の一labelを追加した。

> `DECISION_BOUNDARY: decision_boundary := 受領resultが未発行invocationのtarget / permission / method / stop conditionを変え得る`。decision boundaryを持たない既知の相互非依存invocationは分割せず同一model stepで発行し、全result受領後に一度だけ次を判断する。

- Candidate43 root bytes: `3,980`
- Candidate69 root bytes: `4,291`
- 差: `+311`、`+7.81%`
- changed target: root `AGENTS.md`だけ
- Candidate43の既存9 labelと残り18 target: 逐語・bit一致で保持
- Candidate69 bundle SHA-256: `76e6c86fa4cf107ee660d79598e034c384545935982da4983f65d67f65423e87`

prompt bytesは増えているため、観測したtoken減少をprompt文字数の縮小へ帰属できない。

## 固定条件

- 評価集合: `the-caption-standard14-r1`第1版
- 評価集合識別値: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`
- Candidate43: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate43 bundle SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- Candidate69: `the-caption-3ce91a4-model-reentry-decision-boundary-r1`
- 採点条件: `outcome-boundary-owner-diagnostic-v10`
- 採点条件SHA-256: `987a10b29862b4b75daa73a696ec922cddbce6f84e6cb0459349383f1767c1b4`
- 対象リポジトリ版: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- 使用模型 / reasoning: `gpt-5.6-sol` / `high`
- Agent環境: Codex CLI `0.144.0`、memory / apps / plugins / plugin sharing無効
- 実行方式: 全体待ち行列、同時実行上限24、各項目5回
- token accounting: root agentと全子sessionの合計、第1版
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- 互換条件識別値: `4948b6b613f3d5a809774ba29fa5cc82d0244fd6e1340e618b7b5f5abfaf6236`

Candidate69 profileはCandidate43の標準14 profileから`profile_id`と`prompt_set_identity`だけを変更した。比較viewは両resultのcompatibility key一致を確認して生成した。

## 3 KPI

| prompt set | 点数分布 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | 70件token合計 |
| --- | --- | ---: | ---: | ---: | ---: |
| Candidate43 | `4 = 70` | 100.000 | 3,647,298 | 1,353.458秒 | 17,732,662 |
| Candidate69 | `4 / 3 = 69 / 1` | 100.000 | 2,691,522 | 1,104.860秒 | 13,726,510 |
| Candidate69 - Candidate43 | — | 0.000 | -955,776（-26.21%） | -248.598秒（-18.37%） | -4,006,152（-22.59%） |

中央値は14項目をまとめた各反復の値から算出した。点数分布を中央値で代替しない。

## 反復別KPI

| 反復 | C43 quality | C69 quality | C43 tokens | C69 tokens | token差 | C43 elapsed | C69 elapsed | elapsed差 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100.000 | 98.214 | 3,647,298 | 2,825,812 | -821,486 | 1,439.351秒 | 1,064.571秒 | -374.780秒 |
| 2 | 100.000 | 100.000 | 3,422,707 | 2,883,163 | -539,544 | 1,353.458秒 | 1,166.780秒 | -186.677秒 |
| 3 | 100.000 | 100.000 | 3,740,820 | 2,687,450 | -1,053,370 | 1,440.509秒 | 1,104.860秒 | -335.649秒 |
| 4 | 100.000 | 100.000 | 3,670,184 | 2,638,563 | -1,031,621 | 1,328.981秒 | 1,022.322秒 | -306.659秒 |
| 5 | 100.000 | 100.000 | 3,251,653 | 2,691,522 | -560,131 | 1,241.287秒 | 1,133.223秒 | -108.064秒 |

Candidate69はall-agent tokenとelapsedが5 / 5反復でCandidate43より小さかった。反復別qualityは4 / 5が100.000で、反復1だけF10 monthlyのscore `3`により98.214だった。

## 区分別token合計

| 区分 | Candidate43 | Candidate69 | Candidate69 - Candidate43 |
| --- | ---: | ---: | ---: |
| F項目12件、各5回 | 15,490,426 | 11,762,124 | -3,728,302（-24.07%） |
| A01・A02、各5回 | 2,242,236 | 1,964,386 | -277,850（-12.39%） |
| 標準14項目、各5回 | 17,732,662 | 13,726,510 | -4,006,152（-22.59%） |

## case別数値

Candidate69のF10 monthlyだけが`4 / 3 = 4 / 1`で、残り13 caseは各`4 = 5`だった。Candidate43は全caseが各`4 = 5`である。

| case | token合計 C43 | token合計 C69 | 合計差 | token中央値 C43 | token中央値 C69 | 中央値差 | elapsed中央値 C43 | elapsed中央値 C69 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 455,061 | 461,842 | +6,781 | 75,325 | 102,413 | +27,088 | 39.802秒 | 46.301秒 | +6.499秒 |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 1,787,175 | 1,502,544 | -284,631 | 331,365 | 322,250 | -9,115 | 135.743秒 | 89.546秒 | -46.197秒 |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 1,062,766 | 1,272,198 | +209,432 | 214,709 | 247,400 | +32,691 | 84.974秒 | 87.458秒 | +2.484秒 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 1,729,308 | 2,022,259 | +292,951 | 347,063 | 381,762 | +34,699 | 112.119秒 | 132.582秒 | +20.464秒 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 1,311,471 | 1,358,887 | +47,416 | 259,117 | 250,428 | -8,689 | 111.068秒 | 96.218秒 | -14.850秒 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 1,124,137 | 1,138,796 | +14,659 | 216,546 | 221,234 | +4,688 | 100.967秒 | 94.215秒 | -6.752秒 |
| `TC-F05-CLARIFY-UNITS-MODE` | 299,778 | 254,170 | -45,608 | 78,992 | 32,161 | -46,831 | 29.271秒 | 25.007秒 | -4.264秒 |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 480,758 | 207,224 | -273,534 | 85,769 | 31,504 | -54,265 | 44.523秒 | 25.012秒 | -19.510秒 |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 1,772,211 | 1,269,919 | -502,292 | 396,341 | 256,372 | -139,969 | 116.818秒 | 82.726秒 | -34.092秒 |
| `TC-F07-CANONICAL-V4-RUNNER` | 2,250,479 | 1,383,836 | -866,643 | 460,217 | 275,241 | -184,976 | 133.997秒 | 90.369秒 | -43.629秒 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 757,156 | 601,317 | -155,839 | 141,167 | 106,620 | -34,547 | 70.367秒 | 71.086秒 | +0.718秒 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 2,282,726 | 966,293 | -1,316,433 | 386,364 | 211,687 | -174,677 | 136.120秒 | 88.001秒 | -48.119秒 |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 1,273,947 | 714,781 | -559,166 | 274,203 | 128,641 | -145,562 | 117.183秒 | 89.888秒 | -27.295秒 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 1,145,689 | 572,444 | -573,245 | 223,484 | 86,987 | -136,497 | 105.681秒 | 60.874秒 | -44.808秒 |

token合計は14 case中9 case、case中央値は14 case中10 caseでCandidate69が小さかった。F01とF02はtool call、reasoning、command、tokenがすべて増えており、global proseが全caseを同じ方向へ収束させたとは判断しない。

## 実行経路診断

`top-level tool call`は各root rolloutの`custom_tool_call`と`function_call`を数えた。`reasoning item`と`token_count event`は別に数えた。`shell command`は`all-agent-command-evidence/v5`のattempted commandである。

| 診断値 | Candidate43 | Candidate69 | Candidate69 - Candidate43 |
| --- | ---: | ---: | ---: |
| session | 70 | 70 | 0 |
| child / additional token | 0 | 0 | 0 |
| input token | 17,504,107 | 13,516,839 | -3,987,268（-22.78%） |
| output token | 228,555 | 209,671 | -18,884（-8.26%） |
| top-level tool call | 639 | 469 | -170（-26.60%） |
| reasoning item | 548 | 499 | -49（-8.94%） |
| token_count event | 710 | 539 | -171（-24.08%） |
| shell command | 705 | 689 | -16（-2.27%） |
| failed shell command | 15 | 11 | -4 |

両prompt setは70 / 70件がroot-onlyだった。Candidate69はshell commandを2.27%しか減らしていない一方、tool callとinput tokenを約23〜27%減らした。これは`DECISION_BOUNDARY`が狙ったmodel再入削減と一致する。

required command protocol違反は0件だった。`owner-producer-evidence/v1`がdiagnostic-onlyで`inadmissible`とした記録はCandidate69で55件だった。これは品質点へ使用していない。

## A02境界

Candidate69のA02は5 / 5 score `4`で、全runがrepository authorityから`src.app.entrypoints.v4_daily_main`を特定してから`run.sh`の一行だけを変更した。canonical target確定前に探索結果を仮定して編集したrunはない。

| 診断値 | Candidate43 | Candidate69 | 差 |
| --- | ---: | ---: | ---: |
| all-agent token合計 | 1,787,175 | 1,502,544 | -284,631（-15.93%） |
| top-level tool call | 47 | 41 | -6 |
| reasoning item | 56 | 47 | -9 |
| token_count event | 52 | 46 | -6 |
| shell command | 44 | 32 | -12 |

Candidate69のiteration順tool callは`9 / 9 / 9 / 6 / 8`だった。探索を固定read routeへ変えず、target確定後のvalidationとdiffをまとめる方向で減っている。

## F10 monthly score 3

score `3`のrunは`27e98720d6ac4c6998f18f0b82bb5aaf`である。

- finding: `format_test=args.force`が`--format-test`を無視し、`--force`をformat testへ誤接続することを正しく指摘した。
- 読取: 固定diff、`monthly_main.py`全文、`monthly_engine.py`の`format_test`分岐を取得した。
- command: 所定の10件を実行し、zero driftを維持した。
- tool call: 4件。
- 失敗: 最終locationを`monthly_main.py:24`と返し、採点側が要求する実変更行`:25`と一致しなかった。

同caseのscore `4`低cycle runは`git show ... | nl -ba`で行番号付きsourceを取得した。score `3` runは内容全文を取得したが、行番号を付けなかった。model再入削減とfinding内容の維持は両立した一方、terminal evidence addressの精度は自動的には維持されなかった。

Candidate43のcontinuous B18にも同じreview location mismatchがあるため、Candidate69固有原因とは確定しない。ただし今回の事前gateは全件score `4`を要求したため、結果後に基準を変更して通過扱いにはしない。

## 保存記録

### Candidate69

- profile: `candidate69-model-reentry-decision-boundary-v10-standard14-global-m24-n5-r1`
- 結果識別子: `a861676ceede45de97235d2ed9839b3d`
- 結果内容SHA-256: `8e2cc44a961e261d9b836efc8516326252a38f70d2fd94072951582955514e9f`
- 実行場所: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate69-model-reentry-decision-boundary-v10-standard14-global-m24-n5-20260722-r1`
- execution archive SHA-256: `e97056d113f3e4367a5f58387bb10a12531b0637f55e473c20f530abf1588ec8`
- final archive SHA-256: `f7cd5eacde37201c51927d4a406536378b439195c58d8aca577f218a4062e745`
- 有効 / 採点可能 / 除外: 70 / 70 / 0
- 保存状態: 登録済み、圧縮済み

### Candidate43

- 結果識別子: `b62428c2361b435fbd0fc7c8979868e7`
- 結果内容SHA-256: `f09b08972579f2d33bb90ab669a11fc9edfa2c33209a93735ffdf2bd3d7e7226`
- 有効 / 採点可能 / 除外: 70 / 70 / 0

比較viewは次へ保存した。

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-n5-20260722-r1.json`

Candidate69の採用、release、本体反映は未判断・未実施である。
