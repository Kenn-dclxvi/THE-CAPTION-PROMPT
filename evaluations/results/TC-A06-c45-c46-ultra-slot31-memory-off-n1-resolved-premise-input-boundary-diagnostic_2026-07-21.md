# TC-A06 Candidate45 / Candidate46 Ultra slot31 memory-off N=1 diagnostic

## 結論

Candidate46の解決済み前提入力境界は、root admissionでのauthority再取得とall-agent tokenを減らす方向には動作した。Candidate45比でrootの`docs/reference`参照は`22 → 1`、rootの`exec`は`66 → 18`、all-agent `total_tokens`は`105,471,441 → 74,748,801`で`-29.13%`だった。全42回のworker起動は成功し、Candidate45の11件の`agent thread limit reached`も発生しなかった。

一方、Candidate45の未解決問題を全体として解消したとは判断できない。sessionは`32 → 43`、workerは`31 → 42`、nested workerは`16 → 18`へ増えた。root直下で8本の独立反証workerが追加され、provenance workerの3子sessionは`fork_turns=all`を使った。root durationは`1,548.498 → 2,268.757`秒で`+46.51%`だった。

authority本文の反復readは減ったが、対象範囲の列挙は減らなかった。`docs/reference`参照は`271 → 139`、`docs/adr`参照は`126 → 54`へ減った一方、`rg --files`は`55 → 57` call、参照sessionは`30 → 40`へ増えた。解決済みauthorityを入力として閉じる境界は作用したが、scope membership、独立反証、provenance証明を新しいoperationへ分ける経路は残った。

最終監査は広い不適合を根拠付きで報告し、testと最終no-driftも成立した。ただしprivate oracleの既知findingでは週次legacy ledger依存を報告せず、Web Editor findingを`unavailable`として主結論から除外した。さらにpytestが3つのignored fileを一時作成し、rootが削除して開始状態へ戻した。blind quality ratingは実装されていないため`quality_score`は保存しないが、score `4`の維持は確認できない。

Candidate46は`diagnostic_only / draft`のままとする。Candidate作成前gateの「主要findingを失った場合」と「前提状態の判定が新しい再確認経路を増やした場合」に該当するため、追加candidate、採用、release、本体反映へ進まない。

## 固定条件

| 項目 | Candidate45 | Candidate46 |
| --- | --- | --- |
| case | `TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1` | 同左 |
| target commit | `eebc1c6c106f504978482238fd760fb73f5fff36` | 同左 |
| target tree | `6366adbb7eaf9db55763e39797b5e070905ede16` | 同左 |
| prompt identity | `the-caption-3ce91a4-judgment-authority-boundary-r1` | `the-caption-3ce91a4-resolved-premise-input-boundary-r1` |
| bundle sha256 | `1527dc5770c17225c42cb6d9eebf9de8f5b929a15b7dc4812b08b4d84965c622` | `d0e393f2e77f98677013e97ab3d388c3d421b520d254d6ed706ded3bd8581e11` |
| prompt overlay commit | `b282091df35e669215beb0e22a3aeb2b39a98250` | `9983a1e6fa3c52b4bfbff969e35ca917abb0966b` |
| prompt overlay tree | `abf7592037ab9253b8df4ae6b1fc3a2cc074dc95` | `2f22b022f6ac40ea4006002d3a05626c6a2cf4d1` |
| model / reasoning | `gpt-5.6-sol` / `ultra` | 同左 |
| Agent-visible concurrency | root込み`31` | 同左 |
| Memory instructions | `absent` | `absent` |
| runtime | Python `3.14.5` / `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` | 同左 |
| workspace | `/Users/kenn/repos/THE-CAPTION-DESKTOP-EVAL-SLOT-01` | 同左 |
| root thread | `019f8040-0cde-7261-b18d-328f2b4fae54` | `019f8110-41f2-7521-bc47-5b81b4e5bc4a` |
| start gate / end drift | pass / none | pass / none |
| comparison status | `diagnostic_only / memory_off / N=1` | 同左 |

Candidate46のrun終了後、user configの`features.memories`は`true`へ復元した。

## 診断値

`tool call`は全session rolloutの`custom_tool_call`と`function_call`を数えた。`model step`は全session rolloutの`token_count` eventを数えた。時間はroot taskの`duration_ms`である。tokenは全sessionの最終usageを合算した`all_agents/v1`である。

| 診断値 | Candidate45 | Candidate46 | C46 - C45 |
| --- | ---: | ---: | ---: |
| session | 32 | 43 | +11 (+34.38%) |
| worker | 31 | 42 | +11 (+35.48%) |
| root直下worker | 15 | 24 | +9 (+60.00%) |
| nested worker | 16 | 18 | +2 (+12.50%) |
| tool call | 1,013 | 935 | -78 (-7.70%) |
| model step | 1,084 | 1,029 | -55 (-5.07%) |
| root task duration seconds | 1,548.498 | 2,268.757 | +720.259 (+46.51%) |
| all-agent `total_tokens` | 105,471,441 | 74,748,801 | -30,722,640 (-29.13%) |
| root tokens | 10,578,558 | 10,533,949 | -44,609 (-0.42%) |
| child tokens | 94,892,883 | 64,214,852 | -30,678,031 (-32.33%) |
| child token / worker | 3,061,061 | 1,528,925 | -1,532,136 (-50.05%) |

参考としてCandidate46はC43 strict run比でも、worker`-8.70%`、tool call`-18.13%`、model step`-14.96%`、duration`-9.33%`、all-agent token`-27.48%`だった。これは同一N=1の診断値であり、分布へ一般化しない。

Candidate46のtoken内訳はinput `74,154,136`、cached input `70,044,672`、output `594,665`、reasoning output `315,068`だった。

Candidate46のtool call内訳は`exec 761`、`spawn_agent 42`、`wait_agent 59`、`send_message 38`、`list_agents 25`、`interrupt_agent 7`、`followup_task 2`、`wait 1`だった。42件のspawn attemptはすべてsessionとして成立し、thread-limit失敗は0件だった。

## Context再取得

次はcustom tool-call入力に各文字列を含むcallとsessionを数えた診断値である。文字列一致はreadの意味や必要性を自動判定しない。

| 参照 | Candidate45 call / session | Candidate46 call / session |
| --- | ---: | ---: |
| `AGENTS.md` | 84 / 32 | 95 / 34 |
| `docs/reference` | 271 / 30 | 139 / 27 |
| `docs/adr` | 126 / 29 | 54 / 18 |
| `git status` | 33 / 24 | 30 / 18 |
| `rg --files` | 55 / 30 | 57 / 40 |

root sessionだけでは、`docs/reference`が`22 → 1`、`docs/adr`が`3 → 1`、`rg --files`が`3 → 1`だった。rootの`exec`も`66 → 18`へ減った。一方、rootの総tool callは`99 → 119`へ増えた。Candidate46はsource readを減らしたが、spawn、wait、list、messageによるorchestrationへcostを移した。

## Worker routing

Candidate46はrootから最初に16 workerを起動した。内訳はauthority、v4 scope、test、12のsubsystem監査、横断candidate scanである。その後、高重要度候補に対して8本の独立反証workerを追加した。

nested workerは18本だった。

- `v4_scope`配下は5本で、test mapはさらに2本を起動して深さ3になった。
- `audit_monthly`配下は4本だった。
- `audit_provenance`配下は3本だった。この3本だけが`fork_turns=all`を使い、合計`15,212,033` tokenだった。親`audit_provenance`を含む4 sessionは合計`22,471,654` tokenだった。
- `audit_web_editor`配下は2本だった。
- `verify_layering`配下は4本だった。

全42 spawnのうち39本は`fork_turns=none`、3本は`fork_turns=all`だった。最大深さは3で、depth別session数はroot `1`、depth 1 `24`、depth 2 `16`、depth 3 `2`だった。

Candidate46はauthority conflictを9項目の未解決規範として分離し、一意に確定できた規範だけをsubsystem workerへ渡した。この挙動は、解決済みpremiseとconflictを分離する意図に合う。

一方、独立反証を8つの別result identityとして新規生成した。これはproducer resultの暗黙補完ではないため`PRODUCER`違反ではないが、C43で観測した候補別validator costの一部を再導入した。また、provenance、scope、layeringのworkerは自分の配下へ探索を再分割したため、解決済み前提の入力境界だけではworker topologyを収束させなかった。

## 成果範囲

Candidate46は`FAIL`と結論し、23のfinding groupを報告した。Python testは`326 passed / 3 skipped`、TypeScriptは依存未導入のため`unavailable`、開始・終了stateはcleanだった。

private oracleの既知findingでは次を最終報告した。

- 空または総額0のledger送信。
- 保存失敗後の送信継続とCompletionLock、`--scope context`のlock迂回。
- 月次ShadowLedger履歴とfallbackの不整合。
- Jinja2本番依存欠落。

次は最終報告へ含めなかった。

- 現行v4が生成しないlegacy ledgerへ週次処理が依存するfinding。
- Web Editorが空SSOTを保存でき、serverがloopback外へbindするfinding。専任workerは起動したが、rootはWeb Editorをv4 production合否へ含めるauthorityを`unavailable`とした。

provider APIのsystem/user role分離自体を契約違反とする既知false positiveは、最終findingとしては報告しなかった。月次LLM findingは、sanitize欠落と固定句gateを未知入力が通過できる到達経路へ根拠を限定した。

現物の適合性と製造履歴は分離し、後者を`not proved`とした。この区別はTaskSpecの意図に合う。ただしprovenance確認は全tokenの30.06%を占め、3本の全履歴継承を含む最大の長尾になった。

test実行中に`reports/test-result.xml`、`.coverage`、`logs/test.log`を新規作成した。rootはbirth timeを確認して今回の3 fileだけを削除し、最終stateをcleanへ戻した。最終driftはないが、実行中のfile作成禁止は満たしていない。

## 解釈

- 事実: rootはbind済みresultからadmissionし、Candidate45のような`docs/reference`再取得をほぼ行わなかった。
- 事実: authority本文のall-session反復readとall-agent tokenは大きく減った。
- 事実: scope列挙の参照session、worker数、独立反証worker、durationは増えた。
- 事実: 主要既知findingの一部を最終報告から除外し、file作成禁止へ一時違反した。
- 推測: 解決済み前提入力境界は「前提内容の再取得」を減らしたが、「対象範囲のmembership確定」「独立反証の必要性」「製造履歴の証明範囲」を閉じなかった。
- 未確定: 同じrouting、token差、成果範囲が複数反復でも再現するか。

したがって、Candidate46の境界方向を全面的に否定する結果ではない。しかしC45の未解決問題に対する完成案でもない。次に検討すべき対象は新しい手続きの追加ではなく、TaskSpecが要求する監査成果のscopeと、下流operationへ渡すresolved premiseの有効範囲をどこで閉じるかである。このN=1の後に新しいcandidateを自動作成しない。

blind rating、Layer 4登録、winner、採用、release承認、本体反映は行っていない。
