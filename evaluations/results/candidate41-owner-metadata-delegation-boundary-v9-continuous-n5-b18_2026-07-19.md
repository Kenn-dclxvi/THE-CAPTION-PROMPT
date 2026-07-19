# Candidate41 owner metadata delegation boundary continuous N=5 B=18

## 結論

Candidate41のexpanded 12-case continuous B18試験は、18 / 18 batch、1,080 / 1,080 runをvalidかつrateableとして完了した。各batchは独立resultへ登録し、archive、compactまで完了している。

score分布は`4 / 3 = 1,078 / 2`だった。score `0..2`は0件である。score `3`の2件は、いずれもF10 monthly reviewで主要findingを特定したが、locationが実変更行`monthly_main.py:25`と一致しなかった。

18 resultの`quality_score`中央値はすべて`100.000`だった。18 result中央値の中央値は、all-agent `total_tokens = 2,856,386`、`elapsed_seconds = 1,100.052`秒である。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- profile: `candidate41-owner-metadata-delegation-boundary-outcome-quality-owner-diagnostic-v9-expanded12-f04r2-global-m24-n5-r1`
- prompt set: `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1`
- bundle SHA-256: `048f6693ae588feb0cd27f13f08637adb6b0cc376d94a4a4d4072662b1b747d7`
- evaluation set: `the-caption-expanded12-f04r2-f10r3-r2`
- evaluation set identity: `de4d1deacc470127eaf612f4b18d638febf5a2b44b1e82a1f673942b05c772c7`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v5`
- execution: expanded 12 case、各batch `N=5`、global queue `M=24`、18 batch
- token accounting: `all_agents` / `v1`
- comparison conditions SHA-256: `5873a40101f78a2524a621eeecef752acf36b2d98f9ac46c084d8626388850c7`
- compatibility key: `abc7d7a9a4db052f417a200e5c7b873e39edb27bc5d564163fbb150f560100a4`

既存のC41 expanded N=5 resultとprompt identity、Evaluation set、fixture、TaskSpec、model、Agent環境、permission、executor parameter、rating revision、反復条件を一致させた。既存resultは変更せず、18個の一次resultをappend-onlyで追加した。

## 集計

- valid / rateable run: `1,080 / 1,080`
- score `4`: `1,078`
- score `3`: `2`
- score `0..2`: `0`
- excluded / retry attempt: `0 / 0`
- score合算率: `99.953704%`（`Σ(score) / (4 × 1,080)`）
- all-agent token total: `259,826,013`
- 18 resultの`quality_score`中央値の中央値: `100.000`
- 18 resultのall-agent `total_tokens`中央値の中央値: `2,856,386`
- 18 resultの`elapsed_seconds`中央値の中央値: `1,100.052`秒
- 90 iteration全体の記述的token中央値: `2,851,547`
- 90 iteration全体の記述的elapsed中央値: `1,102.017`秒
- campaign wall-clock: `5,373`秒（1時間29分33秒）
- controller elapsed合計: `5,058.498`秒
- command protocol violation: `4`
- owner evidence eligible / inadmissible: `91 / 989`

## Batch results

| batch | result ID | quality median | token median | elapsed median | score 4 / 3 |
| --- | --- | ---: | ---: | ---: | ---: |
| B1 | `66904b1eb9a84e5b81e6856bd9490f82` | 100.000 | 2,907,267 | 1,178.801秒 | 59 / 1 |
| B2 | `4339386fb55b49b3ba375c90000e18ec` | 100.000 | 2,867,396 | 1,104.894秒 | 60 / 0 |
| B3 | `e91b963c480a477fbf6acb9adfdff198` | 100.000 | 2,772,063 | 1,091.590秒 | 60 / 0 |
| B4 | `7cddca7843bd4e4982b4ca61a3971ebd` | 100.000 | 2,650,049 | 1,084.427秒 | 60 / 0 |
| B5 | `dde6d9fe6ded4fe9b58d3576bb34945c` | 100.000 | 3,019,632 | 1,126.296秒 | 60 / 0 |
| B6 | `171a029867ef424ba441a3ae54f414cd` | 100.000 | 3,093,010 | 1,155.481秒 | 60 / 0 |
| B7 | `5e89463d21614fa39f30a16c6f2b077d` | 100.000 | 2,623,868 | 1,078.279秒 | 60 / 0 |
| B8 | `5b5d96c5bd5845c793849708fa2be0f2` | 100.000 | 2,828,180 | 1,088.829秒 | 60 / 0 |
| B9 | `5a925eb074164e90a8611bfbde554dc7` | 100.000 | 2,956,142 | 1,112.207秒 | 60 / 0 |
| B10 | `62863f66a1e749f99bbd52391c0e6e7a` | 100.000 | 2,688,321 | 1,074.065秒 | 60 / 0 |
| B11 | `697415b0511046c696ceb3e23562a97e` | 100.000 | 2,845,376 | 1,096.658秒 | 60 / 0 |
| B12 | `7a9bd3ce03fb461facd0c97767ebfea0` | 100.000 | 2,844,833 | 1,106.034秒 | 60 / 0 |
| B13 | `7376d3c0380c467886dc0ee613bff22a` | 100.000 | 3,122,501 | 1,163.587秒 | 60 / 0 |
| B14 | `9fdba2f2014b4e9cbe5cab8a3fec96d7` | 100.000 | 2,818,127 | 1,090.023秒 | 60 / 0 |
| B15 | `5e990df8937b407286a4a0cd90565776` | 100.000 | 2,719,699 | 1,064.640秒 | 59 / 1 |
| B16 | `beb9cc50ee8546318b43486b418c5c32` | 100.000 | 2,893,206 | 1,103.447秒 | 60 / 0 |
| B17 | `a203c95a5d1640ca9415c798519d6687` | 100.000 | 2,893,386 | 1,074.180秒 | 60 / 0 |
| B18 | `162d0959bdd84fd9a2c797c6a8f8bcdc` | 100.000 | 3,179,284 | 1,137.897秒 | 60 / 0 |
| 18 result中央値 | — | 100.000 | 2,856,386 | 1,100.052秒 | 1,078 / 2（合計） |

最終行のKPIは18個の保存済みresult中央値に対する記述的な中央値であり、新しいLayer 4 resultではない。

## Case distribution

| case | runs | score 4 / 3 | token total | token median |
| --- | ---: | ---: | ---: | ---: |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 90 | 90 / 0 | 21,937,842 | 236,024.5 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 90 | 90 / 0 | 33,812,271 | 350,737.5 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 90 | 90 / 0 | 20,353,645 | 212,818.5 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY r2` | 90 | 90 / 0 | 23,526,236 | 244,447.0 |
| `TC-F05-CLARIFY-UNITS-MODE` | 90 | 90 / 0 | 5,603,524 | 78,538.5 |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 90 | 90 / 0 | 5,483,263 | 78,728.5 |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 90 | 90 / 0 | 29,711,162 | 322,137.0 |
| `TC-F07-CANONICAL-V4-RUNNER` | 90 | 90 / 0 | 35,176,343 | 371,766.0 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 90 | 90 / 0 | 14,035,653 | 148,081.0 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 90 | 90 / 0 | 35,026,926 | 387,156.5 |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 90 | 90 / 0 | 17,865,535 | 199,256.5 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 90 | 88 / 2 | 17,293,613 | 223,415.5 |

## Score 3

| batch / iteration | run ID | case | 直接原因 |
| --- | --- | --- | --- |
| B1 / i3 | `2323995569a24adf864d6639d5d2d18f` | `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 主要findingは特定したが、指摘位置が実変更行`monthly_main.py:25`と一致しなかった |
| B15 / i4 | `b358e09c9369475fad74bb2238dbef7b` | `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 同上 |

F10 monthly review内の発生率は2 / 90、全runでは2 / 1,080だった。N=5単発で0 / 5だった誤経路がB18で2件観測された。

## Routingと診断

1,079 / 1,080 runはroot sessionだけで完了した。1 runだけがrootに加えて2つのchild sessionを起動した。

- batch / case / iteration: B1 / `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` / i2
- run ID: `48c509e52e5b4954a33b2c6c7cb705b3`
- child path: `/root/independent_contract_check`、`/root/independent_contract_recheck`
- score: `4`
- all-agent total tokens: `1,007,494`
- child and additional tokens: `160,742`
- command protocol violation: `4`

このrun以外にchild sessionはなかった。v9のowner evidenceは診断であり、quality scoreの条件ではない。

## 既存C41 N=5との記述的比較

| scope | quality median | token median | elapsed median | score 4 / 3 |
| --- | ---: | ---: | ---: | ---: |
| 既存C41 N=5 result | 100.000 | 2,861,019 | 1,172.182秒 | 60 / 0 |
| B18の18 result中央値 | 100.000 | 2,856,386 | 1,100.052秒 | 1,078 / 2 |
| 差 | 0.000 | -4,633（-0.16%） | -72.129秒（-6.15%） | — |

B18の最終行は18 result中央値の記述的集計であり、単一の登録resultではない。少数反復の中央値が同じでも、N=5で観測しなかった低頻度location mismatchとworker routingをB18で観測した。

## 判断

### 事実

- 18 resultは同じcompatibility keyへappend-only登録された。
- 1,078 / 1,080 runがscore `4`だった。
- score `3`の2件は同じF10 location mismatchだった。
- 1,079 / 1,080 runはroot-onlyだった。残る1 runは2 workerを起動した。
- F10 monthly review r3のTaskSpecは、findingへ`path:line`を含めることを既に要求している。private assertionもchanged-line locationを評価対象としている。
- Candidate41がCandidate35から変更したtargetはroot `AGENTS.md`だけである。`src/AGENTS.md`を含むpath-scoped repository authorityはControlFreeRepository、Candidate35、Candidate41で同一である。
- 同じv9互換条件のControlFreeRepository N=5でも、F10 monthly reviewのlocation mismatchが1件観測された。
- Candidate37には、F10のlocation mismatchだけを対象に、line番号付きsourceでexact lineを確認する`LOCATION`規則が既に存在する。Candidate37はCandidate36の直接childであり、Candidate41の直接系譜ではない。

### 推論

Candidate41はB18の観測範囲で、TaskSpecに明示されないworker routingをほぼ抑制した。ただし、root-only経路を完全な不変条件にはできていない。

F10 location mismatchは主要findingの欠落ではないが、N=5では見えなかった低頻度誤経路である。今回の2件だけから発生率を評価範囲外へ一般化できない。

同じ誤りがroot制御を持たないControlFreeRepositoryでも観測されているため、C41の`OWNER_ROLE`境界を原因とは判断できない。`path:line`要件は既にcase taskへ置かれており、line番号付きsourceの使用をrootへ重ねる変更は、repository-wideな実行境界ではなくF10の出力精度へ方法を追加する試験対策になる。

Candidate37のN=5は60 / 60 score `4`だったが、別rating revisionであり、B18による低頻度事象の確認もない。この結果から、`LOCATION`規則の一般的な正味効果またはC41へ統合する根拠は得られない。

### 提案

このB18をCandidate41の長期観測evidenceとして保持する。Candidate37の`LOCATION`規則はF10固有の方法指定なのでCandidate41へ統合しない。`EVIDENCE_PRECISION`のような「推測しない」という禁止事項も変更候補にしない。

保存traceから、exact coordinateを個別line番号のないtextから生成する経路でlocationが揺れたことは確認できる。一方、この経路がrepository-wideなprompt制御のどの誤分岐で生じたかは確認できない。`RESULT_SOURCE`もF10のtarget diff / behavior reference / location構造を抽象化した試験依存の案なので変更候補から外す。

この結果から新しいprompt predicateを導かない。score `3`は有効なquality observationと未解決riskとして保持し、Candidate41の採用またはrelease判断で隠さない。exact coordinateの決定的保証が必要な場合は、prompt candidateではなく、実運用と評価で共通する構造化evidence interfaceの別要件として扱う。評価adapterだけを変更して本caseを通す対応は行わない。

## Compatibility boundary

このB18はC41 v9 expanded N=5、および同じv9で実行したbaseline、ControlFreeRepository、Candidate35の各N=5 resultと互換である。

保存済みCandidate35 B18は`owner-producer-quality-v7`、comparison conditions SHA-256 `328aa909…24c6`であり、本C41 B18のv9、`5873a401…50c7`とは互換でない。両B18を評価基盤v3の同一comparison viewへ混ぜない。Candidate35とのB18比較には、Candidate35を同じv9条件で別途B18実行する必要がある。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate41-owner-metadata-delegation-boundary-outcome-quality-owner-diagnostic-v9-continuous-n5-b18-20260719-r1`
- registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/`
- campaign window: `2026-07-19T03:22:00+09:00`から`2026-07-19T04:51:33+09:00`
- 18 / 18 result registration、final compact receipt、campaign summaryを確認した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
