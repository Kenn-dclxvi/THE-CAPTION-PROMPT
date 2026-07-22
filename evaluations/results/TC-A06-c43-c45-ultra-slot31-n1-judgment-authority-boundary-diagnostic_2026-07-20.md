# TC-A06 C43 / Candidate45 Ultra slot31 N=1 diagnostic

## 結論

固定pathのDesktop評価slotにより、C43とCandidate45をAgent-visible concurrency `31`で順次実行できた。candidateごとのcloneは不要になった。

観測値ではCandidate45はC43よりsession、tool call、model step、all-agent tokenが少なかった。一方、root tokenは多く、経過時間はほぼ同じだった。

実行経路も異なった。C43は17本の初期worker後に17本の独立再検証workerを起動した。Candidate45は24本の初期workerを起動し、追加の反証workerは起動しなかったが、rootが主要候補のauthorityと到達経路を再取得してadmissionした。

ただし、この2 runを互換比較、品質評価、Candidate45の効果判定には使わない。Desktop taskへCodex Memoryが注入され、Candidate45は過去の`Candidate45 / A06`記録を実際に読んだからである。これはmodel-visible入力と保存済み評価結果を分離するA06の条件を満たさない。

したがって、今回確定できるのは31-slotでの実挙動と、Desktop評価機構にmemory gateが必要だという事実までである。winner、採用、release、本体反映は判断しない。

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
| model | `gpt-5.6-sol` | 同左 |
| reasoning effort | `ultra` | 同左 |
| Agent-visible concurrency | root込み`31` | 同左 |
| runtime | Python `3.14.5` / `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` | 同左 |
| workspace | `/Users/kenn/repos/THE-CAPTION-DESKTOP-EVAL-SLOT-01` | 同左 |
| root thread | `019f7fd7-f057-76d0-9645-86c364aaa063` | `019f7ff5-858a-7bf0-8215-de56a7ccbe6c` |
| start gate | pass | pass |
| end drift | none | none |
| comparison status | `diagnostic_only / memory_contaminated` | 同左 |

両runは同じfixed slotを順番に使用した。同時実行はしていない。各run前にtarget、prompt bundle、runtimeを再materializeし、終了時にclean stateを確認した。

## 診断値

`tool call`は全session rolloutの`custom_tool_call`と`function_call`を数えた。`model step`は全session rolloutの`token_count` eventを数えた。時間はroot taskの`duration_ms`である。

| 診断値 | C43 | Candidate45 | C45 - C43 |
| --- | ---: | ---: | ---: |
| session | 35 | 25 | -10 (-28.57%) |
| worker | 34 | 24 | -10 (-29.41%) |
| tool call | 705 | 469 | -236 (-33.48%) |
| model step | 751 | 509 | -242 (-32.22%) |
| root task duration seconds | 1,636.573 | 1,609.110 | -27.463 (-1.68%) |
| all-agent `total_tokens` | 57,184,182 | 38,883,860 | -18,300,322 (-32.00%) |
| root tokens | 6,252,846 | 8,267,766 | +2,014,920 (+32.22%) |
| child tokens | 50,931,336 | 30,616,094 | -20,315,242 (-39.89%) |

C43のtool call内訳は`exec 642`、`spawn_agent 34`、`wait_agent 20`、`send_message 5`、`list_agents 4`だった。Candidate45は`exec 426`、`spawn_agent 24`、`wait_agent 5`、`send_message 2`、`list_agents 12`だった。

Candidate45のall-agent inputは`38,420,537`、cached inputは`35,862,016`、outputは`463,323`、reasoning outputは`285,015`だった。

## 実行境界の観測

### C43

C43は、production surface別の17本を初期起動した。その後、候補ごとに17本の`verify_*` workerを起動した。

後段workerは別operation identityとしてauthority、call path、到達例を再取得した。C43の同一predicate再割当て禁止は、同じfinding候補を別名の独立検証resultとして扱う経路を止めなかった。

### Candidate45

Candidate45はauthority抽出と実装領域を24本へ分けた。追加の反証workerは起動しなかった。

rootは「主要な不適合候補は、別担当の結果だけで確定せず、authorityと現行到達経路をこちらでも突き合わせる」と明示した。worker resultを暗黙に補完して同一resultへ統合せず、別resultをadmissionする境界は守った。

一方、admissionに必要な情報取得量は制限していない。rootはGuard、価格日付、Monex、描画、永続化、CompletionLockなどを広く再読した。root tokenがC43比`+32.22%`なのは、このroot集中と対応する。

### 解釈

判断成立責任境界は、producer resultの暗黙修理を防ぐ境界としては動作した。独立判断を禁止しないため、必要な反証やadmissionも保持した。

ただし、境界だけで探索量や再読量は最小化されない。今回のCandidate45は独立再検証workerを起動しなかったが、root再取得へ置き換わった。経過時間が`-1.68%`に留まったことも、worker削減がそのまま完了時間短縮にならない観測と一致する。

この因果をCandidate45だけへ帰属させない。N=1であり、後述のmemory流入もある。

## Memory流入による除外

両Desktop taskのdeveloper instructionsには`MEMORY_SUMMARY`が注入されていた。summary自体にA06、Candidate45、available concurrencyの過去観測が含まれていた。

C43 rootは`MEMORY.md`をtoolで読まなかった。Candidate45 rootは開始直後に`MEMORY.md`から`Candidate45 / A06 / concurrency slots`を検索し、終了前に該当行を再読した。最終応答にもmemory citationを付けた。

したがって、Candidate45は今回のrepositoryとTaskSpecだけで探索方針を決めていない。過去resultがmodel-visibleであり、A06のvisibility boundaryに反する。このrunのquality coverageと効率差を、cleanなprompt差として扱わない。

## 再利用機構と開始gate

[`prepare_desktop_evaluation_slot.py`](../../scripts/prepare_desktop_evaluation_slot.py)は一つのmanaged workspaceを再利用する。markerのない既存repo、dirty slot、identity不一致、runtime不一致を拒否する。

今回の観測を受け、receiptへ`model_context_gate`を追加した。その後のpreflightで、user configの`features.memories=false`が新しいDesktop taskへ反映されることを確認した。project登録commandは`codex app <slot>`であり、memory除外はuser configと開始gateで担保する。

ただし、起動済みDesktopへこのcommandを送っても既存hostのmemory設定は変わらなかった。preflightは`memory=present`だった。

分離`app-server`を`--disable memories`で起動すると`memory=absent`になったが、Agent-visible concurrencyはroot込み4だった。31-slot条件の代替にはならない。

後続のstrict runはDesktopを再起動せずに実施できた。新しいtaskの最初の調査前に次の両方を確認する。

- `available concurrency slots = 31`
- developer instructionsのMemory指示が`absent`

どちらか一方でも不一致ならenvironment mismatchとして除外する。評価adapterが通常利用中のDesktopを自動終了してはならない。

後続結果は[`slot31 memory-off diagnostic`](TC-A06-c43-c45-ultra-slot31-memory-off-n1-judgment-authority-boundary-diagnostic_2026-07-21.md)へ分離した。このmemory contaminated result自体の値と除外理由は変更しない。

機構の詳細は[`Desktop評価slot`](../../docs/desktop-evaluation-slot.md)に記録した。repository全体の試験は`130 passed, 8 subtests passed`だった。

## 判定境界

- 事実: fixed slotはcandidateごとのcloneなしでC43 / C45を順次materializeできた。
- 事実: 両runでAgent-visible concurrency 31とclean start/endを確認した。
- 事実: C43は34 worker、Candidate45は24 workerを起動した。
- 事実: Candidate45はworkerとall-agent tokenが少なく、root tokenが多かった。
- 事実: Candidate45は過去A06 memoryを読んだ。
- 推測: Candidate45の判断成立責任境界は独立再検証workerを減らし、root admissionへcostを移した可能性がある。
- 未確定: memoryを除外した同一31-slot条件でも同じ差が再現するか。

blind rating、Layer 4登録、winner、採用、release承認、本体反映は行っていない。
