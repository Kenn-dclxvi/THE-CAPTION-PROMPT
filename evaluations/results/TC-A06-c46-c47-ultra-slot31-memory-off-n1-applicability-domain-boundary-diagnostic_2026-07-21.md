# TC-A06 Candidate46 / Candidate47 Ultra slot31 memory-off N=1 diagnostic

## 結論

Candidate47の適用域境界は、新しい対象を一律にscope extensionへ送らず、同じrequired outcomeに対する監査対象として扱う方向に動作した。Candidate46が主結論から除外したWeb Editorは専任producerで判定され、空SSOT保存とloopback外bindを含むfindingとして最終報告へ入った。週次も専任producerと3つの子producerで調査され、`-F`の過剰なguard解除をfindingとして報告した。rootが集約段階へ移行した後に、Candidate46のような8本のroot直下反証waveは起動しなかった。

実行量はCandidate46比でsession `43 → 35`、worker `42 → 34`、tool call `935 → 807`、model step `1,029 → 905`、root duration `2,268.757 → 1,662.582`秒、all-agent `total_tokens` `74,748,801 → 65,251,694`となった。token差は`-9,497,107`、`-12.71%`である。

一方、未解決問題は残った。初期inventoryは深さ4まで再分割され、4件のspawnが`agent thread limit reached`で失敗した。成功した34 spawnのうち8件が`fork_turns=all`で、`docs/reference`参照は`139 → 175` call、参照sessionは`27 → 32`へ増えた。rootもADR専任producerの終端前にReferenceとADRを直接読み、rootの`docs/reference`参照は`1 → 9`へ戻った。さらにnested worker 1件がfinal resultを返さないまま中断された後、rootは全producerが終端したと宣言した。

成果範囲はCandidate46より広がったが、private oracleの週次legacy ledger依存は、週次用V4 dataset/schema authorityがないという規約衝突へ分類し、確認済み不適合としては報告しなかった。既知false positiveのprovider role分離は報告せず、開始・終了stateはcleanだった。blind quality ratingは未実装のため`quality_score`は保存しない。既知finding 6件のうち5件を確認したが、週次findingの未確定と、test時にrepository外の一時fileを作成した点からscore `4`の維持は確認しない。

Candidate47は`diagnostic_only / draft`のままとする。適用域の再分類には作用したが、producerへ適用predicateとevidence conditionがbindされる前の探索分割とcontext継承は収束していない。candidate作成前gateのroot authority再取得とnested waveの停止条件に該当するため、追加candidate、採用、release、本体反映へ進まない。

## 固定条件

| 項目 | Candidate46 | Candidate47 |
| --- | --- | --- |
| case | `TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1` | 同左 |
| target commit | `eebc1c6c106f504978482238fd760fb73f5fff36` | 同左 |
| target tree | `6366adbb7eaf9db55763e39797b5e070905ede16` | 同左 |
| prompt identity | `the-caption-3ce91a4-resolved-premise-input-boundary-r1` | `the-caption-3ce91a4-applicability-domain-boundary-r1` |
| bundle sha256 | `d0e393f2e77f98677013e97ab3d388c3d421b520d254d6ed706ded3bd8581e11` | `da626369ab4462da166c05bb0503c745a32a058d409cefde599e70326b47b998` |
| prompt overlay commit | `9983a1e6fa3c52b4bfbff969e35ca917abb0966b` | `be51dabe247a87d639bc6a4ead06368664b95373` |
| prompt overlay tree | `2f22b022f6ac40ea4006002d3a05626c6a2cf4d1` | `4f4838e514ca2e89f14d547b0dc9f020e9833629` |
| model / reasoning | `gpt-5.6-sol` / `ultra` | 同左 |
| Agent-visible concurrency | root込み`31` | 同左 |
| Memory instructions | `absent` | `absent` |
| runtime | Python `3.14.5` / `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` | 同左 |
| workspace | `/Users/kenn/repos/THE-CAPTION-DESKTOP-EVAL-SLOT-01` | 同左 |
| root thread | `019f8110-41f2-7521-bc47-5b81b4e5bc4a` | `019f820c-bf56-7fb0-bc8e-2e4d9e28b77b` |
| start gate / end drift | pass / none | pass / none |
| comparison status | `diagnostic_only / memory_off / N=1` | 同左 |

Candidate47のrun終了後、user configの`features.memories`は`true`へ復元した。

## 診断値

`tool call`は全session rolloutの`custom_tool_call`と`function_call`を数えた。`model step`は全session rolloutの`token_count` eventを数えた。時間はroot taskの`duration_ms`である。tokenはrootと全descendant 35 sessionで最後に記録されたusageを合算した`all_agents/v1`であり、推定値を含まない。中断sessionも中断直前の最終usageを取得できた。

| 診断値 | Candidate46 | Candidate47 | C47 - C46 |
| --- | ---: | ---: | ---: |
| session | 43 | 35 | -8 (-18.60%) |
| worker | 42 | 34 | -8 (-19.05%) |
| root直下worker | 24 | 21 | -3 (-12.50%) |
| nested worker | 18 | 13 | -5 (-27.78%) |
| tool call | 935 | 807 | -128 (-13.69%) |
| model step | 1,029 | 905 | -124 (-12.05%) |
| root task duration seconds | 2,268.757 | 1,662.582 | -606.175 (-26.72%) |
| all-agent `total_tokens` | 74,748,801 | 65,251,694 | -9,497,107 (-12.71%) |
| root tokens | 10,533,949 | 9,023,992 | -1,509,957 (-14.33%) |
| child tokens | 64,214,852 | 56,227,702 | -7,987,150 (-12.44%) |
| child token / worker | 1,528,925 | 1,653,756 | +124,831 (+8.16%) |

参考としてCandidate47はCandidate45 strict run比でtool call`-20.34%`、model step`-16.51%`、all-agent token`-38.13%`だった。一方、sessionは`+9.38%`、workerは`+9.68%`、durationは`+7.37%`だった。いずれも同一N=1の診断値であり、分布へ一般化しない。

Candidate47のtoken内訳はinput `64,693,050`、cached input `60,894,720`、output `558,644`、reasoning output `302,031`だった。

Candidate47のtool call内訳は`exec 694`、`spawn_agent 38`、`wait_agent 18`、`send_message 27`、`list_agents 26`、`interrupt_agent 2`、`followup_task 2`だった。spawn attempt 38件のうち34件がsessionとして成立し、4件は`agent thread limit reached`で失敗した。

## Context再取得

次はtool-call入力に各文字列を含むcallとsessionを数えた診断値である。文字列一致はreadの意味や必要性を自動判定しない。

| 参照 | Candidate46 call / session | Candidate47 call / session |
| --- | ---: | ---: |
| `AGENTS.md` | 95 / 34 | 72 / 32 |
| `docs/reference` | 139 / 27 | 175 / 32 |
| `docs/adr` | 54 / 18 | 63 / 18 |
| `git status` | 30 / 18 | 28 / 20 |
| `rg --files` | 57 / 40 | 53 / 32 |

root sessionだけでは、`docs/reference`が`1 → 9`、`docs/adr`が`1 → 2`、`rg --files`が`1 → 4`、`exec`が`18 → 46`だった。rootの総tool callは`119 → 106`へ減ったため、tool数全体は増えていない。しかし、authority本文をroot admissionで再取得しないというCandidate46の挙動は維持されなかった。

rootは開始時に自分の担当をauthorityの適用関係と宣言し、同時に`authority_adr` workerを起動した。rootのADR / Reference読取りはworkerのterminal result前に始まった。したがって、terminal resultを受けた後の再検証ではないが、authority解決のproducer責任が一部重なり、同じsourceを並行取得する経路は残った。

## Worker routing

Candidate47はrootから最初に17 workerを起動した。authority、v4 inventory、日次orchestration、ingestion、ledger finalization、guard / lock、date / freshness、market history、daily context、renderer 2系統、monthly 2系統、weekly、repository I/O、CLI isolation、layeringを分離した。

後段では`dependencies`、`test_coverage`、`process_evidence`を追加した。集約中にWeb Editorを同じ監査required outcomeで判定する`web_editor` producerも追加した。Candidate46のような高重要度候補ごとの8本のroot直下反証waveは起動しなかった。

nested workerは13本だった。

- `inventory_v4`配下は10本で、subtree全体は11 session、`14,905,197` tokenだった。日次traceからさらに3 worker、週次traceから2 worker、file I/O traceから1 workerが起動され、最大深さ4になった。
- `weekly_pipeline`配下は3本で、subtree全体は4 session、`6,897,702` tokenだった。
- 成功した34 spawnのうち`fork_turns=none`は26本、`fork_turns=all`は8本だった。全履歴を継承した8 childは合計`8,126,652` tokenだった。
- depth別session数はroot `1`、depth 1 `21`、depth 2 `7`、depth 3 `5`、depth 4 `1`だった。
- `dependencies`、`graph_verify`、`domain_lib_io_candidates`、`scan_weekly_docs`の初回spawnはslot枯渇で失敗した。`dependencies`は後で再起動してterminalになった。他3件は親producerが自分の結果をterminalにした。
- `inventory_v4/daily_trace/file_io_trace`は子workerの結果を受信したが、自身のfinal resultを返す前に親からinterruptされ、`turn_aborted`で終了した。35 session中`task_complete`は34件だった。その後rootは「独立監査の全producerが終端」と宣言したため、`TERMINAL`が禁止するnonterminal sessionの補完を観測した。

Candidate47は「新しい対象を同じpredicateで判定できるならscopeを再開しない」という方向では動作した。しかし、初期inventory自身が対象到達経路を子operationへ再分割し、複数childがauthorityとfile inventoryを再取得した。適用域境界は、resolved premiseが存在した後のadmissionには作用したが、premiseを解決する前の探索topologyとcontext継承までは閉じなかった。

## 成果範囲

Candidate47は`FAIL`と結論し、20のfinding groupを報告した。Python testは`326 passed / 3 skipped`、typecheckはtoolと設定がないため`unavailable`、開始・終了stateはcleanだった。

private oracleとの対応は次のとおりである。

| oracle | Candidate47最終報告 |
| --- | --- |
| F1 empty / non-positive ledger | 報告した |
| F2 persistence / CompletionLock | 報告した |
| F3 monthly history / fallback | 報告した |
| F4 weekly legacy ledger dependency | 確認済み不適合としては報告しなかった |
| F5 Web Editor empty SSOT / non-loopback bind | 報告した |
| F6 Jinja2 dependency | 報告した |
| R1 provider role separation false positive | 報告しなかった |

F4についてはweeklyを探索していないのではない。`weekly_pipeline` subtreeへ4 sessionを使い、`-F`がLedger存在と`VERIFIED`確認まで解除する別findingを報告した。一方、現行weeklyがlegacy ledgerへ依存する点は、V4固有dataset/schema authorityがないため具体的な置換値を一意に判定できない規約衝突として、合否から除外した。

Web Editorはroot集約中に新しい対象として発見した後、別のscope解決operationを挟まず専任producerへ渡した。最終報告は、空状態でSSOT全体を上書きできること、規定外の`portfolio_basis.json`書込みAPI、`PORT`指定による全interface bindを含めた。この挙動は適用域境界の意図に合う。

testはrepository内のignored出力を避けるため、Pythonの`TemporaryDirectory`配下で実行した。repository driftは発生しなかった。一方、TaskSpecの`file作成禁止`をrepository外も含む字義どおりの禁止として読む場合、一時directoryとtest出力の作成後削除は制約違反である。Candidate46のrepository内一時file生成は解消したが、file作成自体をなくしたわけではない。

## 解釈

- 事実: Web Editorは同じ監査required outcomeへ取り込まれ、Candidate46で除外したfindingを最終報告した。
- 事実: 週次は広く探索され、別の到達可能なfindingを報告したが、oracle F4はauthority conflictとして除外した。
- 事実: root直下の候補別反証waveは消え、session、tool call、model step、duration、all-agent tokenはCandidate46より減った。
- 事実: nested探索は深さ4へ達し、4件のthread-limit失敗と8件の全履歴継承が発生した。
- 事実: 1件のnested workerはnonterminalのまま中断され、rootが全producer終端として集約した。
- 事実: rootと多数のworkerによるauthority参照はCandidate46より増えた。
- 推測: Candidate47は「新対象が既存適用域のmemberか」という後段判断を減らしたが、「適用predicateとevidence conditionを誰が解決し、初期producerへ何を入力するか」は決めなかった。そのため、admission後のvalidator costは減った一方、初期探索とnested context取得が残った。
- 未確定: 同じrouting、token差、成果範囲が複数反復でも再現するか。

このN=1は、適用域を対象列挙ではなく判定基準で閉じる方向が成果範囲と実行量の双方へ作用し得ることを示した。ただし、Candidate47だけでC45以降の未解決問題を解消したとは判断しない。blind rating、Layer 4登録、winner、採用、release承認、本体反映は行っていない。

## 後続の未実施検証補完

2026-07-21に、元のA06 root runとは別operationとして、run内で実施できなかった検証をCandidate47のexact prompt overlay commit `be51dabe247a87d639bc6a4ead06368664b95373`から補完した。この補完はmodel routing、all-agent token、root duration、最終監査報告を変更しないため、上記診断値へ混ぜない。

Pythonの3 skipは、`tests/unit/test_ledger_mtd_regression.py`が評価checkoutに存在しない`data/current/ledger_*.json`をcollection時に列挙し、月初、週初、年初の各parameter setが空になった結果だった。THE-CAPTION-DEVの実データ132 ledgerを一時checkoutだけへ入力した。fixtureのファイル名と内容から作ったaggregate SHA-256は`335619ac7c578ddbfec377a706113653d360eb78d828a3de84fc6955154c6a19`である。private ledger自体は評価artifactへ保存しない。

実データ入力後、元の3 test functionは月初7 case、週初29 case、年初2 caseの合計38 caseへ展開した。対象file単独は`38 passed`、同じPython `3.14.5` runtimeによる全suiteは`364 passed / 0 skipped / 0 failed`だった。

Web Editorにはrootで探索したPython typecheckerとは別に、`src/web/market_units_editor/package.json`の`npm run lint`が存在し、実体は`tsc --noEmit`だった。Candidate47 commitの同directory tree `6eedafac1d09f4958bc6fcef0dedb54ca15c77d5`を一時展開し、`package-lock.json`から`npm ci --ignore-scripts`で依存を構築した。Node `v26.0.0`、npm `11.12.1`で`npm run lint`はexit `0`だった。

したがって、元runの`326 passed / 3 skipped`とtypecheck `unavailable`は、対象コードの失敗ではなく、実データfixtureを評価checkoutへ渡さなかったことと、Web Editorの正規typecheck commandを探索しなかったことによる検証未完了だった。補完後のvalidationはpassである。ただし、週次F4のauthority conflict、nonterminal workerの補完、初期nested探索は変わらないため、Candidate47の`diagnostic_only / draft`とquality未確定は維持する。
