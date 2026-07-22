# TC-A06 C43 Ultra max-thread context boundary diagnostic

## 結論

実効`agents.max_threads=30`で再試験した結果、Agentはrootと7 workerの8 sessionを選んだ。同じfindingを別validatorへ再割当てする段は再現しなかった。

一方、authority専任worker、各surfaceの監査worker、rootが、それぞれ担当判断に必要なauthorityと実装を取得した。この個別取得は観測事実だが、resolved shared premiseを事前に渡していないA06だけでは、削減可能な重複か独立判断に必要な読取りかを区別できない。

初回runはcapsuleが`agents.max_threads=30`を宣言した一方、adapterが4を強制していた。このrunは環境不一致として保持し、routingと効率の比較には使わない。

## 位置付け

これはA06の非blind診断である。Layer 3のQuality ratingとLayer 4登録は行っていない。1回の観測からwinner、改善・悪化、採用、release、本体反映は判断しない。

比較対象のTHE-CAPTION-DEV taskは評価基盤に保存した互換resultではない。以下の差はKPI comparisonではなく、同じ対象treeとUltra modelで観測した実行topologyの参考値である。

## 固定条件

| 項目 | 値 |
| --- | --- |
| case | `TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1` |
| target repository | `Kenn-dclxvi/THE-CAPTION` |
| target commit | `eebc1c6c106f504978482238fd760fb73f5fff36` |
| target tree | `6366adbb7eaf9db55763e39797b5e070905ede16` |
| prompt overlay commit | `a1d5945332bac14972d037b3676fe2ed6f7d5580` |
| prompt set | `the-caption-3ce91a4-outcome-authority-boundary-r1@r1` |
| bundle sha256 | `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531` |
| model | `gpt-5.6-sol` |
| reasoning effort | `ultra` |
| iteration | `1` |
| declared `agents.max_threads` | `30` |
| effective `agents.max_threads` | `30` |
| Agentへ提示されたavailable concurrency slots | root込み`4` |
| 実測最大同時worker | `3` |
| rerun id | `2b523351e1654973b41524bfacedc6e7` |
| execution status | `valid` |
| rating status | `not_blind_rated` |

caseはworker数、担当file、読取り順、検証方法を指定していない。30は利用可能な上限であり、起動必須数ではない。

ここでのeffective `agents.max_threads=30`は、adapterがCLI設定として30を渡したことを示す。保存済みrolloutでAgentへ提示されたavailable concurrency slotsはroot込み4だった。したがって、このrunを30 worker同時実行または元THE-CAPTION-DEVと同じ並行条件とは扱わない。

## 発見したadapter不具合

初回run `7cf3dbdd97484ce78f87f338b0b39bf6`では、capsuleの`comparison_conditions.agent_environment.agents_max_threads`は30だった。しかし、`scripts/run_codex_evaluation.py`は`--ignore-user-config`を指定した上で、`agents.max_threads=4`を固定していた。

このため初回runの4 sessionはpromptだけで決まったtopologyではない。初回runの数値は次のとおりだが、比較から除外する。

| 状態 | session | worker | tool call | model step | all-agent tokens | elapsed seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| environment mismatch | 4 | 3 | 199 | 207 | 24,157,069 | 1,101.239 |

adapterを、宣言された正の整数を検証して実行commandへbindするよう修正した。`tests.test_run_codex_evaluation`の24件は成功した。system Pythonに`pytest` packageがないため、同じtest moduleを標準`unittest`で実行した。

## 再試験の実行topology

Agentは7 workerをすべて`fork_turns=none`で起動した。

| session | operation | final usage |
| --- | --- | ---: |
| root | identity、operation分割、結果集約、最終evidence確認 | 2,883,686 |
| `/root/authority_audit` | 適用authority集合と競合の確定 | 706,390 |
| `/root/v4_conformance` | daily engine / guard / rendererの適合性 | 3,682,888 |
| `/root/validation_record` | testと製造記録の証明範囲 | 1,285,705 |
| `/root/monthly_weekly_audit` | monthly / weekly接続 | 2,015,432 |
| `/root/v4_data_audit` | date / ingester / Web data contract | 2,083,890 |
| `/root/v4_ui_prompt_audit` | UI / deterministic context / prompt境界 | 1,357,400 |
| `/root/extended_validation` | 未実行の追加Python test群 | 328,395 |
| 合計 | all-agent | 14,343,786 |

最初に3 workerを起動し、そのterminal result後に残余surfaceの3 workerを起動した。最後に、既出findingを再発見させず、未実行test群だけを`extended_validation`へ割り当てた。

tool callは205、model stepは220だった。tool call内訳は`exec 156`、`wait_agent 31`、`spawn_agent 7`、`send_message 7`、`list_agents 4`である。

token内訳はinput `14,227,239`、cached input `13,238,016`、output `116,547`、reasoning output `63,147`だった。cached inputはinputの約93.05%である。elapsedは`1,709.745`秒だった。

## 元THE-CAPTION-DEV観測との差

元観測はtask `019f7e0b-c2a3-7571-8bd0-6a075bec45e0`の最初の監査turnだけを集計した。root、12 initial audit worker、15 validatorの合計28 sessionだった。

| 診断値 | 元観測 | max30再試験 | 差 |
| --- | ---: | ---: | ---: |
| session | 28 | 8 | -20 (-71.43%) |
| spawn | 27 | 7 | -20 (-74.07%) |
| tool call | 583 | 205 | -378 (-64.84%) |
| model step | 626 | 220 | -406 (-64.86%) |
| all-agent `total_tokens` | 50,794,157 | 14,343,786 | -36,450,371 (-71.76%) |
| elapsed seconds | 1,632.851 | 1,709.745 | +76.894 (+4.71%) |

再試験はsession、tool call、tokenが小さい一方、elapsedはわずかに長い。operationを二つのwaveへ分けたこと、個々のworker所要時間、実行時の揺らぎを含むため、token差やelapsed差を単一controlの効果へ帰属しない。

## 成果の診断

最終応答は`NONCONFORMING`と結論し、16件の根拠付きfindingを返した。empty ledger、CompletionLock bypass、format-test side effect、Monex audit disconnect、Jinja2 dependency、monthly history、weekly connection、Web data contract、UI、LLM traceを含む。

private oracleでreject対象としたprovider APIのsystem/user role分離は違反として報告しなかった。historical manufacturing provenanceは現在のtree適合性と分離し、証明不能とした。終了時のrepository driftはなかった。

Python testは`41 passed`と追加の`127 passed`だった。TypeScript lintは`tsc: command not found`で、dependency installがpermission外のため実行不能として明記した。

private oracleの既知findingをすべて報告したわけではない。Web Editorのempty saveとLAN公開、およびpersistence failure後のdispatchは最終応答に含まれなかった。また、初回診断で「後に否定された」と記録したUS-date findingが再試験では再び報告された。このfindingの採否を再試験中にblind判定していないため、成果品質を維持したとは判断しない。

## 再現判定

### 再現しなかった事象

- initial producerのfindingを別validatorへそのまま再割当てする15-validator相当の段はなかった。
- `extended_validation`はfindingの再監査を行わず、未実行の安全なPython test群だけを実行した。
- provider role分離の既知false positiveは最終応答へ入らなかった。

### 観測したが、問題とは未判定の事象

- authority専任workerがauthority集合を確定した後も、各監査workerは担当findingに必要なauthority条項を直接読んだ。
- rootはworker resultを最終応答へ採用する前に、主要authorityと実装行を再取得した。
- これは同じsourceの複数回取得だが、独立判断とfinding admissionに必要な確認を含む。

A06はshared premiseをmodel-visible入力として渡していない。そのため、この読取りを削減可能な情報境界の欠陥と断定できない。

## この試験から確定できる境界

今回確定できるのは、並列上限30でもC43が同一findingの独立validator再割当てを選ばなかったことまでである。

shared context境界の効果を判定するには、required outcomeを変えず、片方だけにtarget identity、適用authority集合と関連条項、production surface、確定済みcommand receiptをresolved premiseとして渡すpaired diagnosticが必要になる。その比較でもworker数、担当file、tool、読取り順は固定せず、成果品質とsource再取得だけを分離して観測する。
