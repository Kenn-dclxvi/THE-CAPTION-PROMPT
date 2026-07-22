# Candidate69 / Candidate70 machine decision boundary 対象4項目 各5回

## 結論

Candidate70はCandidate69を直接sourceとし、root `AGENTS.md`へ`MACHINE_BOUNDARY`一labelだけを追加した。executor parameter、TaskSpec、fixture、permission、required command、quality ratingは変更していない。

復元後の同条件試験は両promptとも20 / 20 valid・rateable、root-only、zero drift、command protocol違反0だった。登録済みcomparison viewの中央値はC70 - C69で、`quality_score = 0.0`、all-agent `total_tokens = -319,714`、`elapsed_seconds = -19.116秒`である。20 run token合計は`6,884,512 -> 5,540,899`、`-1,343,613`、`-19.52%`だった。

一方、事前gateは通過しなかった。Candidate70の公式scoreは`4 / 3 = 19 / 1`である。score `3`のA02は成功commandを固定auditが認識しなかった偽陰性だが、公式resultは変更しない。さらにF06はtop-level tool callが`39 -> 49`、token合計が`+20.17%`、elapsed合計が`+8.70%`だった。全体差は主にF07の`-52.01%` tokenで生じており、正のcase間で効果が安定していない。

Candidate70は`targeted_evaluated / stopped`とする。追加predicate、standard14、採用、release、本体反映へ進めない。

## 固定条件

- Candidate69: `the-caption-3ce91a4-model-reentry-decision-boundary-r1`
- Candidate69 bundle SHA-256: `76e6c86fa4cf107ee660d79598e034c384545935982da4983f65d67f65423e87`
- Candidate70: `the-caption-3ce91a4-machine-decision-boundary-r1`
- Candidate70 bundle SHA-256: `65397c3b2a589d5de37e7d616cfc620d36fda32a4a6b33fbb0f53c3da3b0f840`
- changed target: root `AGENTS.md`だけ
- 評価集合: `the-caption-machine-decision-boundary-targeted4-r1`第1版
- 評価集合識別値: `1d438e885f5300bc177b3409a14044e206199c1e23a114f9b2d3f2ac3a17e8c5`
- 採点条件: `outcome-semantic-location-owner-diagnostic-v11`
- 対象リポジトリ版 / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- memories / apps / plugins / plugin sharing: disabled
- permission: `workspace-write`、approval `never`
- repetition: A02、F04、F06、F07 canonicalを各`N=5`、global queue `M=24`
- token accounting: all-agent / `v1`
- comparison conditions SHA-256: `8433bcac8fbc98cb2ff27ae56d1194d983af937594b18abe044dde9e900e3d7b`
- compatibility key: `da204aaa7a90e75980c458d02b25e651974863cc2094f78592b8c647386553bb`
- excluded attempt: 0 / 0

C69 / C70 profile差は`profile_id`と`prompt_set_identity`だけである。

## 3 KPI

`total_tokens`と`elapsed_seconds`の中央値は、4 caseを同じiteration番号で合計した5反復の中央値である。

| KPI | Candidate69 | Candidate70 | Candidate70 - Candidate69 |
| --- | ---: | ---: | ---: |
| `quality_score`中央値 | 100.000 | 100.000 | 0.000 |
| all-agent `total_tokens`中央値 | 1,391,860 | 1,072,146 | -319,714（-22.97%） |
| `elapsed_seconds`中央値 | 506.732秒 | 487.616秒 | -19.116秒（-3.77%） |
| 20 run token合計 | 6,884,512 | 5,540,899 | -1,343,613（-19.52%） |
| 20 run elapsed合計 | 2,537.285秒 | 2,426.983秒 | -110.302秒（-4.35%） |
| 公式score `4 / 3` | 20 / 0 | 19 / 1 | -1 / +1 |

| iteration | quality C69 | quality C70 | tokens C69 | tokens C70 | elapsed C69 | elapsed C70 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100.00 | 93.75 | 1,391,860 | 1,072,146 | 497.221秒 | 510.682秒 |
| 2 | 100.00 | 100.00 | 1,621,858 | 1,044,625 | 506.732秒 | 479.131秒 |
| 3 | 100.00 | 100.00 | 1,248,949 | 969,242 | 559.771秒 | 442.639秒 |
| 4 | 100.00 | 100.00 | 1,201,462 | 1,192,838 | 407.794秒 | 506.914秒 |
| 5 | 100.00 | 100.00 | 1,420,383 | 1,262,048 | 565.767秒 | 487.616秒 |

## case別KPI

| case | score C69 | score C70 | token合計 C69 | token合計 C70 | token差 | elapsed合計 C69 | elapsed合計 C70 | elapsed差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A02 非trigger | 5 / 0 | 4 / 1 | 1,954,526 | 1,656,911 | -297,615（-15.23%） | 657.308秒 | 611.465秒 | -45.843秒（-6.97%） |
| F04 正 | 5 / 0 | 5 / 0 | 1,269,780 | 1,151,275 | -118,505（-9.33%） | 586.239秒 | 589.305秒 | +3.066秒（+0.52%） |
| F06 正 | 5 / 0 | 5 / 0 | 1,352,287 | 1,625,042 | +272,755（+20.17%） | 602.230秒 | 654.645秒 | +52.415秒（+8.70%） |
| F07 canonical 正 | 5 / 0 | 5 / 0 | 2,307,919 | 1,107,671 | -1,200,248（-52.01%） | 691.507秒 | 571.567秒 | -119.940秒（-17.34%） |
| 正の3 case合計 | 15 / 0 | 15 / 0 | 4,929,986 | 3,883,988 | -1,045,998（-21.22%） | 1,879.976秒 | 1,815.517秒 | -64.459秒（-3.43%） |

点数列は`4 / 3`の順である。正の3 case全体はtokenとelapsedが小さいが、F04 elapsedとF06のtool cycle、token、elapsedは増えた。したがって、対象試験全体の中央値低下を一般の時間短縮へ読み替えない。

## 実行経路診断

`top-level tool call`はroot rolloutの`custom_tool_call`と`function_call`を数えた。`model step`はroot rolloutの`token_count` eventを数えた。全40 runはsession 1のroot-onlyである。

| case | tool call C69 | tool call C70 | model step C69 | model step C70 | shell command C69 | shell command C70 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A02 | 49 | 43 | 54 | 48 | 47 | 75 |
| F04 | 45 | 42 | 50 | 47 | 54 | 61 |
| F06 | 39 | 49 | 44 | 54 | 83 | 61 |
| F07 canonical | 69 | 34 | 74 | 39 | 76 | 83 |
| 全4 case | 202 | 168 | 222 | 188 | 260 | 280 |
| 正の3 case | 153 | 125 | 168 | 140 | 213 | 205 |

Candidate70は正の3 case合計でtool callとmodel stepを各28減らした。ただしF06はcommandが22少ない一方でtool callとmodel stepが各10多い。同じrequired outcomeを短いmodel cycleへ安定して収束させる制御にはなっていない。

required commandは両promptですべて成功した。command protocol違反は0件だった。Candidate70のA02は全5件ともcanonical target確定後にvalidationへ進み、target意味解決前のrequired validation実行は観測しなかった。

## A02の採点偽陰性

Candidate70 A02 iteration 1、run `9aa4f1cba9374983acf459d1702c0ce5`の固定auditは、次の2 failureを出した。

- `a02_missing_successful_command:bash_n_run_sh`
- `a02_missing_successful_command:diff_check`

保存済みcommand evidenceには次の成功結果がある。

- `/bin/zsh -c "'bash' '-n' 'run.sh'"`、exit 0
- `/bin/zsh -c "'git' 'diff' '--check'"`、exit 0
- `'.venv/bin/python' '-m' 'pytest' 'tests/' '-v'`、exit 0、`326 passed, 3 skipped`

第11版auditの`successful_contains`はNFKC正規化と`./`除去だけを行い、shell tokenの引用符を除去しない。連続文字列`bash -n run.sh`と`git diff --check`が引用符で分断され、成功commandを認識できなかった。run.shの成果、許可path、試験、最終diffは成立しているため、これは固定auditの偽陰性である。

公式resultはappend-onlyのままscore `3`を保持する。rating revisionを変更した再採点は、AGENTS.mdだけを扱う今回のscopeへ含めない。また、F06の実経路増加だけで事前停止条件に該当するため、採点偽陰性の修正をCandidate70継続条件にしない。

## 容量と初回環境診断

開始時は空き約4 GiBでhard floor 20 GiBを下回った。ユーザー許可に基づきC43以前のraw試験runとC41診断生成物を削除した。評価コードの依存file、append-only result文書、result registryは残した。外部volumeは使用していない。

容量確保時にnpm cacheも削除したため、初回のC69 / C70各20 runはF04の`npm ci`が両promptとも5 / 5失敗した。初回result ID `29af71a789d546558ce186010259ac52` / `c7939e5f1a864e659e972018f12a4c05`は環境診断としてappend-only保持し、本書の比較値へ混ぜていない。

同じF04 fixtureの`package-lock.json`からローカルnpm cacheを復元した。空き容量約29 GiB、`dispatch_allowed`を確認して再実行した。復元後はF04 10 / 10で`npm ci`、lint、buildが成功した。

## 登録証跡

- Candidate69 result ID: `085f0c567bcb4c3a96dd97938817aa94`
- Candidate69 result content SHA-256: `f7aeba434b2d214d39a18653c9d4cf7e66ceacbf0cc463caffa21b9a423266ef`
- Candidate69 execution archive SHA-256: `ad394f70db6dd4dbd697d6c6a2893e6844961b724fb4788836cba2a36f824088`
- Candidate70 result ID: `1d937ad29f984ba8a246fa684e872b89`
- Candidate70 result content SHA-256: `02c62321b179dc60e71409110e1f24ed076f209309cb9f6cf885357fedb684ed`
- Candidate70 execution archive SHA-256: `c2e65e9af54c61ad5d15d761d4f9953c83ebae3756df87853e23bb12f9115923`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/c69-c70-machine-boundary-targeted4-n5-20260722-r2.json`

Candidate70の採用、release、本体反映は未判断、未実施である。
