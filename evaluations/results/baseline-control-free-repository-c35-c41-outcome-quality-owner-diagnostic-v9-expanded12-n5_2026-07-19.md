# Baseline / ControlFreeRepository / Candidate35 / Candidate41 expanded 12-case N=5 comparison

## 結論

同じ試験revisionと互換条件でbaseline、ControlFreeRepository、Candidate35を各60 run実行し、保存済みCandidate41 resultと4-result comparison viewを生成した。

Candidate35とCandidate41は、ともに60 / 60 runがscore `4`だった。Candidate35のall-agent token合計はCandidate41より`7,347,269`、`50.02%`多かった。`total_tokens`中央値差は`+1,704,754`、`elapsed_seconds`中央値差は`+668.926`秒だった。

ControlFreeRepositoryはscore `4 / 3 = 59 / 1`だった。all-agent token合計はCandidate41より`189,510`、`1.29%`多かった。baselineはscore `4 / 3 = 58 / 2`で、token合計はCandidate41より`46,062,125`、`313.59%`多かった。

この結果は比較evidenceであり、winner、採用、release、THE-CAPTION本体反映を決定しない。

## 固定条件

- evaluation set: `the-caption-expanded12-f04r2-f10r3-r2`
- evaluation set identity: `de4d1deacc470127eaf612f4b18d638febf5a2b44b1e82a1f673942b05c772c7`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v5`
- execution: global queue `M=24`、12 case、各`N=5`
- compatibility key: `abc7d7a9a4db052f417a200e5c7b873e39edb27bc5d564163fbb150f560100a4`

4 profileはprompt identityだけが異なる。Evaluation set、target、model、Agent、TaskSpec、permission、fixture、executor parameter、rating、反復条件は同一である。

| label | prompt set | bundle SHA-256 |
| --- | --- | --- |
| baseline | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| ControlFreeRepository | `the-caption-3ce91a4-control-free-repository-r1` | `999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d` |
| Candidate35 | `the-caption-3ce91a4-root-control-only-r1` | `f53fbf36491a88794b3fa54d8653204f14dd4f00919043de76c12d008cea76b3` |
| Candidate41 | `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1` | `048f6693ae588feb0cd27f13f08637adb6b0cc376d94a4a4d4072662b1b747d7` |

## KPI

| prompt set | score 4 / 3 | quality median | token median | token total | elapsed median | result ID |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| baseline | 58 / 2 | 100.000 | 10,826,033 | 60,750,594 | 3,705.409 | `4b48aa3c83b9429da1576bd7fda4b843` |
| ControlFreeRepository | 59 / 1 | 100.000 | 2,808,523 | 14,877,979 | 1,135.178 | `4a80edae9f4843e39ae7170ccab53e6b` |
| Candidate35 | 60 / 0 | 100.000 | 4,565,773 | 22,035,738 | 1,841.107 | `73466eef372949b3aa40ebc862df144a` |
| Candidate41 | 60 / 0 | 100.000 | 2,861,019 | 14,688,469 | 1,172.182 | `f9f8b177031e401093ee60717d5e602e` |

## 中央値比較

12 case分をまとめた各iterationについて、5 iterationの中央値を比較する。差分方向は`各result - Candidate41`である。

| prompt set | quality median | token median | token C41差 | elapsed median | elapsed C41差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 100.000 | 10,826,033 | +7,965,014（+278.40%） | 3,705.409秒 | +2,533.228秒（+216.11%） |
| ControlFreeRepository | 100.000 | 2,808,523 | -52,496（-1.83%） | 1,135.178秒 | -37.003秒（-3.16%） |
| Candidate35 | 100.000 | 4,565,773 | +1,704,754（+59.59%） | 1,841.107秒 | +668.926秒（+57.07%） |
| Candidate41 | 100.000 | 2,861,019 | reference | 1,172.182秒 | reference |

quality中央値は4 setとも同じである。ControlFreeRepositoryはCandidate41よりtoken・時間の中央値が小さい一方、60 run合計tokenはCandidate41より`189,510`多い。

## Campaign全体の参考時間

global queueのcontroller実測時間はKPIではなく、同時実行を含むcampaign全体のwall-clock参考値である。

| prompt set | controller elapsed | C41との差 | C41比 |
| --- | ---: | ---: | ---: |
| baseline | 909.771秒 | +603.084秒 | +196.64% |
| ControlFreeRepository | 281.344秒 | -25.344秒 | -8.26% |
| Candidate35 | 577.189秒 | +270.501秒 | +88.20% |
| Candidate41 | 306.688秒 | 0.000秒 | reference |

## Candidate35とCandidate41のcase別token

両setは全caseで5 / 5がscore `4`だった。差分方向は`Candidate35 - Candidate41`である。

| case | Candidate35 token total | Candidate41 token total | 差 |
| --- | ---: | ---: | ---: |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 1,118,653 | 1,158,233 | -39,580 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 2,931,501 | 2,036,889 | +894,612 |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 1,827,337 | 1,012,921 | +814,416 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY r2` | 1,828,929 | 1,621,682 | +207,247 |
| `TC-F05-CLARIFY-UNITS-MODE` | 613,698 | 395,664 | +218,034 |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 683,740 | 338,595 | +345,145 |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 2,627,765 | 1,455,901 | +1,171,864 |
| `TC-F07-CANONICAL-V4-RUNNER` | 2,790,808 | 1,810,356 | +980,452 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 1,277,411 | 677,182 | +600,229 |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 3,053,624 | 2,230,572 | +823,052 |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 1,730,706 | 941,831 | +788,875 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3` | 1,551,566 | 1,008,643 | +542,923 |

Candidate35のtoken合計は12 case中11 caseでCandidate41より大きかった。

## Quality failureと診断

baselineのscore `3`はF07 dependency provenance pairの2 runだった。両runはrequired command `python3:PyYAML>=6.0.1:pyyaml==6.0.3`をattemptしていなかった。

ControlFreeRepositoryのscore `3`はF10 monthly reviewの1 runだった。major findingのlocationが期待する`monthly_main.py:25`と一致しなかった。

Candidate35とCandidate41にはquality failureがなかった。

| prompt set | command protocol violation | owner evidence eligible | owner evidence inadmissible |
| --- | ---: | ---: | ---: |
| baseline | 470 | 12 | 48 |
| ControlFreeRepository | 0 | 5 | 55 |
| Candidate35 | 18 | 60 | 0 |
| Candidate41 | 0 | 5 | 55 |

owner evidenceはv9では診断であり、quality scoreの条件ではない。

## 判断

### 事実

- 4 resultは同じcompatibility keyへappend-only登録された。
- Candidate35とCandidate41は、12 caseすべてで5 / 5がscore `4`だった。
- Candidate35はCandidate41よりtoken合計が`50.02%`多く、case別では11 / 12 caseで多かった。
- Candidate35の`elapsed_seconds`中央値はCandidate41より`668.926`秒、`57.07%`長かった。
- Candidate35は60 / 60でowner evidenceがeligibleだった。Candidate41は5 / 60だった。
- ControlFreeRepositoryはCandidate41と近いtoken合計だったが、F10 monthly reviewでlocation mismatchが1件あった。

### 推論

Candidate35のroot controlは、このN=5ではCandidate41を上回る成果scoreを示さず、owner evidence成立とtoken costを増やした。KPI viewだけでは個々の追加tokenをowner経路へ因果帰属できないが、全caseへ広がる差はF05 / F10だけの局所事象ではない。

Candidate41はControlFreeRepositoryと近いtoken量を保ちながら、今回観測したF10 location mismatchを再現しなかった。ただし、N=5で1件対0件の差から低頻度誤経路の解消を一般化できない。

baselineの大きなtoken差には多数のcommand protocol violationが併存する。prompt制御だけの純粋なcostとして読み替えない。

### 提案

このcomparisonをC35のroot-wide owner制御とC41の明示delegation境界を判断するevidenceとして使う。次の変更、追加candidate、release判断は、この結果だけで自動的に開始しない。

## Evidence boundary

- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparison-views/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5-20260719-r1.json`
- baseline campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/baseline-outcome-quality-owner-diagnostic-v9-expanded12-f04r2-global-m24-n5-20260719-r1`
- ControlFreeRepository campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/control-free-repository-outcome-quality-owner-diagnostic-v9-expanded12-f04r2-global-m24-n5-20260719-r1`
- Candidate35 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate35-root-control-only-outcome-quality-owner-diagnostic-v9-expanded12-f04r2-global-m24-n5-20260719-r1`
- Candidate41 resultは保存済みcampaignとregistry resultを再利用した。
- 4 campaignはquality audit、Layer 4 registration、lossless archive、final compactまで完了している。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
