# TC-A06 C43 / Candidate45 Ultra 判断成立責任境界 diagnostic

## 結論

Candidate45は、同じpredicateを別producerへ割り当てること自体を禁止せず、一つのjudgment resultの成立責任だけを一つのproducer execution identityへ置く境界として動作した。

rootは3つの初期worker resultを独立した候補として受け取り、sourceを確認してadmissionを判断した。後段の`challenge_candidates`も元resultの補完ではなく、4候補を対象とする別result identityとして実行された。別roleがproducer resultを暗黙に修理して同一resultへ統合する挙動は観測しなかった。

一方、効率は改善しなかった。C43比でsession、tool call、model step、root task durationは減ったが、all-agent `total_tokens`は`+1,440,115`、`+10.04%`だった。rootが最終監査全体のproducerを引き受け、root tokenが`+186.43%`になった。4候補を反証したworkerは全件を`CONFIRMED`とし、棄却または判定不能化は0件だった。

成果品質の維持も確定しない。最終応答は14件を報告し、private oracleのF1、F2、F3、F6と既知false positive除外を満たしたが、F4 weekly接続とF5 Web Editorを報告しなかった。また、full test中にignoredの`logs/test.log`を生成してから除去しており、no-driftは回復したが、TaskSpecのfile作成禁止は満たしていない。

これは非blindの`N=1` diagnosticである。winner、改善・悪化、採用、release、本体反映は判断しない。

## Candidate identity

Candidate44はcomplete spec readiness boundaryとして既に保存済みである。このため、今回のcandidateはCandidate43の直接子Candidate45として作成した。

| 項目 | 値 |
| --- | --- |
| source prompt | `the-caption-3ce91a4-outcome-authority-boundary-r1` |
| candidate prompt | `the-caption-3ce91a4-judgment-authority-boundary-r1` |
| bundle sha256 | `1527dc5770c17225c42cb6d9eebf9de8f5b929a15b7dc4812b08b4d84965c622` |
| changed target | root `AGENTS.md`だけ |
| design gate | `docs/candidate45-judgment-authority-boundary-design.md` |
| state | `draft / diagnostic_observed / not_projected` |

Candidate45はC43の`PRODUCER`と`ROOT`をjudgment resultの成立責任境界へ置換し、同一predicateの別producer割当てを一律禁止していた`INDEPENDENCE`を削除した。worker数、担当file、tool、読取り順、再検証方法は追加していない。

## 固定条件と互換境界

| 項目 | 値 |
| --- | --- |
| case | `TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1` |
| target commit | `eebc1c6c106f504978482238fd760fb73f5fff36` |
| target tree | `6366adbb7eaf9db55763e39797b5e070905ede16` |
| C45 prompt overlay commit | `b282091df35e669215beb0e22a3aeb2b39a98250` |
| model | `gpt-5.6-sol` |
| reasoning effort | `ultra` |
| declared `agents.max_threads` | `30` |
| Agentへ提示されたavailable concurrency slots | root込み`4` |
| 実測最大同時worker | `3` |
| runtime identity | Python `3.14.5`, `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` |
| iteration | `1` |
| valid run id | `1431276fd4d94bbda0ba1f22ffb35797` |
| execution status | `valid` |
| rating status | `not_blind_rated` |

C43再試験も`agents.max_threads=30`をadapterへ渡したが、Agentへ提示されたavailable concurrency slotsは同じくroot込み4だった。したがってC43とC45はこの診断上の並行条件が一致する。

元THE-CAPTION-DEV taskは28 sessionが約27 workerを広く起動した観測である。実効slot 4のC43 / C45を、THE-CAPTION-DEVと同じ並行条件として扱わない。次回の同条件試験では、設定値だけでなくAgentへ提示されるavailable concurrency slotsも30であることを開始gateにする。

## 除外attempt

valid run前の2 attemptは計測へ含めない。

- `b13f0afd5c0d4b3c9beaee6e8a31222d`: workspaceを`/Users/.../_verification`下へ置き、runtime linkをcapsuleへ含めなかった。local shell hookの`.venv/bin/activate not found`をworkerが開始gate失敗と解釈したため停止した。
- `bd7fb057b15c47fb8db6179daf4e41ae`: `/private/tmp`へ移したがruntime linkをまだ含めておらず、Codex作業開始直後に停止した。

valid runではC43と同じ`venv_shim`とruntime identityをmaterializeし、Codex session内のcommandへshell hookのblocking出力が入らないことを確認した。

## 実行topology

全workerは`fork_turns=none`だった。

| session | role | final tokens | terminal |
| --- | --- | ---: | --- |
| root | authority確定、call graph、admission、full test、最終報告 | 8,259,858 | 13:31:51Z |
| `/root/audit_architecture_cli` | CLI、layer、Monex audit | 1,568,025 | 13:20:49Z |
| `/root/audit_ledger_ssot` | Canonical Ledger、SSOT、保存 | 1,417,173 | 13:19:57Z |
| `/root/audit_guard_render_monthly` | Guard、renderer、monthly | 3,233,170 | 13:24:19Z |
| `/root/challenge_candidates` | 4候補の独立反証 | 1,305,675 | 13:28:00Z |
| 合計 | all-agent | 15,783,901 |  |

rootは最初にauthorityを読み、3 workerを並行起動した。3 workerのうち2つがterminalになった後、残る1 workerと並行して`challenge_candidates`を起動した。追加validator群や、同じfindingを補完させるproducer交替はなかった。

初期workerは`3 + 3 + 11 = 17`件の候補を返した。空台帳、保存失敗、CompletionLockなど複数候補はworker間で重複した。rootの最終応答は14件だった。`challenge_candidates`は選択された4件をすべて再取得・再検証し、4件すべてを`CONFIRMED`とした。

## C43との診断値

`elapsed_seconds`の共通Layer 2 wrapper値はC45で保存していないため、時間は両rolloutのroot `task_complete.duration_ms`を比較する。これはLayer 4 KPI comparisonではない。

| 診断値 | C43 | Candidate45 | 差 |
| --- | ---: | ---: | ---: |
| session | 8 | 5 | -3 (-37.50%) |
| worker | 7 | 4 | -3 (-42.86%) |
| tool call | 205 | 155 | -50 (-24.39%) |
| model step | 220 | 164 | -56 (-25.45%) |
| root task duration seconds | 1,705.908 | 1,246.476 | -459.432 (-26.93%) |
| all-agent `total_tokens` | 14,343,786 | 15,783,901 | +1,440,115 (+10.04%) |
| root tokens | 2,883,686 | 8,259,858 | +5,376,172 (+186.43%) |
| child tokens | 11,460,100 | 7,524,043 | -3,936,057 (-34.35%) |

Candidate45のtool call内訳は`exec 145`、`spawn_agent 4`、`list_agents 3`、`wait_agent 3`だった。C43は`exec 156`、`spawn_agent 7`、`wait_agent 31`、`send_message 7`、`list_agents 4`だった。

Candidate45のinputは`15,661,439`、cached inputは`14,832,640`、outputは`122,462`、reasoning outputは`77,941`だった。rootはall-agent tokenの52.33%を占めた。C43のroot比率は20.10%だった。`challenge_candidates`だけで1,305,675 token、C45全体の8.27%だった。

## 情報取得と判断責任の観測

Candidate45は、最終監査全体をroot自身のjudgment resultと解釈した。worker resultはroot resultを構成する候補ではあるが、別identityの独立resultとして扱われた。rootはsourceを読み、候補を採用または棄却するadmissionを行った。

この解釈は判断責任境界には適合する。しかし、judgment resultの粒度を最終監査全体へ置けるため、rootがauthority、call graph、worker候補、反証、最終根拠を広く再取得した。source取得commandでは、rootを含む5 sessionすべてが`AGENTS.md`、`src/AGENTS.md`、`docs/reference/logic.md`、`docs/reference/system.md`、`src/app/v4_engine.py`、`src/domain/guard_rail.py`など13 pathを参照した。

同じpredicateを別producerが扱ったこと自体は境界違反ではない。問題となるのは、その独立判断がrequired outcomeへ追加価値を与えたかである。今回の反証workerは誤検出を除去せず、最終成果で新しいfindingも追加しなかった。そのため、このrunでは1,305,675 tokenに対応する観測可能な成果差を確認できない。

境界を元の一律禁止へ戻す根拠にはしない。一律禁止はroot admissionや有効な独立反証まで方法として抑止する。今回確定できるのは、判断成立責任境界だけでは独立判断の必要性やresult粒度を自動的に最小化せず、root集中と反証再取得が残り得ることまでである。

## 成果の診断

最終応答は`NONCONFORMING`と結論し、14件を報告した。

- private oracle F1: 空・ゼロ台帳を報告した。
- private oracle F2: final Ledger、daily input、CompletionLockのfail-openとcontext bypassを報告した。
- private oracle F3: 月次ShadowLedger履歴と旧台帳優先を報告した。
- private oracle F4: weeklyがlegacy ledgerへ依存する接続不良を報告しなかった。
- private oracle F5: Web Editorのempty saveとLAN公開を報告しなかった。
- private oracle F6: Jinja2 dependency欠落を報告した。
- rejected false positive R1: provider APIのsystem/user role分離を違反として報告しなかった。
- historical manufacturing provenance: 現物適合性と分離し、現在のcommit記録だけでは証明不能とした。

Python testは`326 passed, 3 skipped`だった。TypeScriptは既存`tsc`がなく、依存導入が禁止されるため未実施とした。

full testはignoredの`logs/test.log`を生成した。rootは生成物を除去し、終了時のworktreeとindexをcleanへ戻した。adapterの`final_changed_paths`は空である。しかし、TaskSpecはfile作成自体を禁止していたため、no-driftだけで成果品質の維持を主張しない。

## 判定境界

このrunから確定できる事実は次のとおりである。

- 判断成立責任境界は、root admissionと別identityの独立反証を許可した。
- producer resultの暗黙補完またはproducer交替は観測しなかった。
- C43比でsession、tool call、model step、root task durationは小さかった。
- all-agent tokenはC43より10.04%大きく、root集中と反証workerが発生した。
- known findingのcoverageは入れ替わり、file作成禁止違反もあるため、成果品質維持は未確定である。
- 実効slot 4なので、THE-CAPTION-DEVと同じ並行条件ではない。

単一runからCandidate45の優劣、採用、release、本体反映は判断しない。
