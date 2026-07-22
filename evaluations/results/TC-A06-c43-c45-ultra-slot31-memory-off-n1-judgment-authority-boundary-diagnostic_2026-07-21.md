# TC-A06 C43 / Candidate45 Ultra slot31 memory-off N=1 diagnostic

## 結論

user configで`memories=false`にした後、新しいCodex Desktop taskを開始する方法で、C43とCandidate45をAgent-visible concurrency `31`、Memory指示なしの同一条件へ揃えられた。Desktopの再起動は不要だった。

Candidate45は、C43で発生した候補別validator waveと最終report guardを発生させなかった。sessionは`47 → 32`、root task durationは`-38.12%`、tool callは`-11.30%`、model stepは`-10.41%`だった。

一方、all-agent `total_tokens`は`103,070,239 → 105,471,441`で`+2.33%`だった。Candidate45は31 workerのうち16 workerを入れ子で起動し、同じauthorityと対象範囲を各workerが個別に探索した。child tokenは`+3.71%`、worker当たりchild tokenは`+53.90%`だった。

したがって、Candidate45の判断成立責任境界は、producer resultの暗黙補完と候補別再検証waveを抑える方向には動作した。しかし、成果に必要なauthority、対象範囲、既知resultをproducerへ渡す情報境界までは作らない。今回のtoken観測は、同一predicate再割当てより、入れ子探索と個別context再取得が残ることを示す。

両runとも監査結論、主要な高影響finding、Python test、no-driftは成立した。ただしfinal findingの範囲とgroupingは一致せず、blind quality ratingを行っていないため、成果品質が同等とは確定しない。N=1からwinner、採用、release、本体反映は判断しない。

## 固定条件

| 項目 | C43 | Candidate45 |
| --- | --- | --- |
| case | `TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1` | 同左 |
| target commit | `eebc1c6c106f504978482238fd760fb73f5fff36` | 同左 |
| target tree | `6366adbb7eaf9db55763e39797b5e070905ede16` | 同左 |
| prompt identity | `the-caption-3ce91a4-outcome-authority-boundary-r1` | `the-caption-3ce91a4-judgment-authority-boundary-r1` |
| bundle sha256 | `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531` | `1527dc5770c17225c42cb6d9eebf9de8f5b929a15b7dc4812b08b4d84965c622` |
| prompt overlay commit | `a1d5945332bac14972d037b3676fe2ed6f7d5580` | `b282091df35e669215beb0e22a3aeb2b39a98250` |
| prompt overlay tree | `6366adbb7eaf9db55763e39797b5e070905ede16` | `abf7592037ab9253b8df4ae6b1fc3a2cc074dc95` |
| model / reasoning | `gpt-5.6-sol` / `ultra` | 同左 |
| Agent-visible concurrency | root込み`31` | 同左 |
| Memory instructions | `absent` | `absent` |
| runtime | Python `3.14.5` / `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` | 同左 |
| workspace | `/Users/kenn/repos/THE-CAPTION-DESKTOP-EVAL-SLOT-01` | 同左 |
| root thread | `019f8016-d9c7-7532-b52e-a927ced3b6bd` | `019f8040-0cde-7261-b18d-328f2b4fae54` |
| start gate | pass | pass |
| end drift | none | none |
| comparison status | `diagnostic_only / memory_off / N=1` | 同左 |

固定slotを順番に使用した。同時実行はしていない。各run前にtarget、prompt bundle、runtimeを再materializeした。

## 診断値

`tool call`は全session rolloutの`custom_tool_call`と`function_call`を数えた。`model step`は全session rolloutの`token_count` eventを数えた。時間はroot taskの`duration_ms`である。tokenは全sessionの最終usageを合算した`all_agents/v1`である。

| 診断値 | C43 | Candidate45 | C45 - C43 |
| --- | ---: | ---: | ---: |
| session | 47 | 32 | -15 (-31.91%) |
| worker | 46 | 31 | -15 (-32.61%) |
| tool call | 1,142 | 1,013 | -129 (-11.30%) |
| model step | 1,210 | 1,084 | -126 (-10.41%) |
| root task duration seconds | 2,502.236 | 1,548.498 | -953.738 (-38.12%) |
| all-agent `total_tokens` | 103,070,239 | 105,471,441 | +2,401,202 (+2.33%) |
| root tokens | 11,574,431 | 10,578,558 | -995,873 (-8.60%) |
| child tokens | 91,495,808 | 94,892,883 | +3,397,075 (+3.71%) |
| child token / worker | 1,989,039 | 3,061,061 | +1,072,021 (+53.90%) |

C43のtool call内訳は`exec 1,039`、`spawn_agent 46`、`wait_agent 42`、`send_message 7`、`list_agents 7`、`wait 1`だった。

Candidate45は`exec 897`、`spawn_agent 42`、`send_message 24`、`wait_agent 22`、`list_agents 22`、`interrupt_agent 4`、`followup_task 1`、`wait 1`だった。`spawn_agent` 42回のうち31回がworker sessionになり、11回は`agent thread limit reached`で失敗した。

Candidate45はC43比でinput tokenが`+2.44%`、cached inputが`+3.60%`だった。output tokenは`-12.89%`、reasoning outputは`-15.08%`だった。token増加は最終文量ではなく、探索中のinput再取得側にある。

## 実行境界の観測

### C43

C43はrootから30本のproduction surface別workerを起動した。その後、15本の候補別`verify_*` workerと`final_report_guard`を起動し、累計46 workerになった。

すべて`fork_turns=none`だったが、後段workerは同じfinding候補のauthority、実装path、到達可能性を別result identityとして再取得した。同一predicateを同じproducer resultへ再割当てしない制御は守った一方、候補validityという別predicateへの組替えを止めなかった。

`final_report_guard`は26候補groupを再確認し、約11分の長尾になった。rootは途中で探索拡大の停止を依頼した。

### Candidate45

Candidate45はrootからauthority、実装、test、dependency、履歴など14本を初期起動し、後で未監査surfaceを補う`web_editor`を1本追加した。

初期workerの一部は入れ子workerを起動した。実worker 31本の内訳はroot直下15本、入れ子16本だった。最深部はauthority探索を3段に分けていた。全spawn attemptは`fork_turns=none`だったため、token増加を全履歴継承だけには帰属できない。

候補別validatorと最終report guardは起動しなかった。rootはproducerが返したfindingを別resultのまま採用または棄却し、producer resultを補完して同一resultとして成立させる挙動は観測しなかった。

一方、rootと複数workerは適用authority、call graph、reachable behaviorをそれぞれ取得した。worker packetがresolved authority、確定scope、既知resultを十分に渡さず、各producerがrepositoryから再解決した。後発`web_editor`も、開始時のproduction surface確定がproducer群へ十分反映されなかった例である。

## 成果範囲

両runは`NONCONFORMING`と結論し、Python testは`326 passed / 3 skipped`、TypeScriptは依存未導入のためunavailable、開始・終了stateはcleanだった。

Jinja2本番依存欠落、空または総額0の台帳送信、保存失敗後の送信継続、CompletionLock fail-open、日次format-testの副作用、Monex境界、欠損市場値の推測補完、snapshotとlive CSVのidentity混在、`--scope context`のlock迂回、日次State分類、月次入力、週次`-F`、LLM traceは両方が報告した。

C43は21 group、Candidate45は16 groupにまとめた。C43だけが報告した項目とCandidate45だけが報告した項目がある。Candidate45は編集UIによる空上書きなどの高影響findingを追加した一方、C43が報告したdomain layer、SSOT-B fallback、非正規daily metrics計数、FLP prefixなどはfinalへ含めなかった。

したがって、主要riskの検出が維持された事実と、成果全体が同等という判断を分ける。今回はblind raterを実行しておらず、`quality_score`を保存しない。

## 解釈

- 事実: Memoryを除外した31-slot条件でも、C43の候補別再検証waveは再現した。
- 事実: Candidate45では候補別再検証waveと最終report guardは発生しなかった。
- 事実: Candidate45は短時間、少session、少tool callだったが、all-agent tokenは`+2.33%`だった。
- 事実: Candidate45のchild探索は入れ子化し、worker当たりtokenが`+53.90%`だった。
- 推測: 判断成立責任境界は後段のresult再検証を抑えたが、前段のauthority・scope再解決costを抑えなかった。
- 未確定: quality ratingを含む複数反復でも同じ分布になるか。

Candidate45を「効率化済み」とは扱わない。一方、tokenが増えたことだけで判断成立責任境界を不適切とも扱わない。この境界の目的はresultの成立責任を保つことであり、情報流入の境界は別の変更軸だからである。

blind rating、Layer 4登録、winner、採用、release承認、本体反映は行っていない。
