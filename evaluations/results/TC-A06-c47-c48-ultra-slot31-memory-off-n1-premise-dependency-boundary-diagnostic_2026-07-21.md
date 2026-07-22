# TC-A06 Candidate47 / Candidate48 Ultra slot31 memory-off N=1 diagnostic

## 結論

Candidate48の`DEPENDENCY`境界は、先行premiseがterminalになる前に依存judgmentを独立operationとして分散しない方向に動作した。開始時はauthority inventoryとscope inventoryだけを起動し、その終端後に下流worker群を開始した。最終報告はprivate oracleのknown finding 6件をすべて含み、既知false positiveのprovider role分離は報告しなかった。

一方、実行量はCandidate47比でtool call`+20.57%`、model step`+15.03%`、root duration`+5.05%`、all-agent `total_tokens` `+42.22%`だった。root直下workerは`21 → 29`へ増えた。rootはpremise producerと並行して同じADR / Referenceを読み、全sessionの`docs/reference`参照も`175 → 223`へ増えた。

さらに、nested worker 1件が`turn_aborted`のまま、その親producerは`END_STATUS: COMPLETE`を返した。Candidate48は先行premiseに依存する下流waveの開始時点を遅らせたが、producer責任の重なり、context再取得、terminal result欠落の補完を解消していない。

blind quality ratingは行っていないため、`quality_score`は保存しない。Candidate48は`diagnostic_only / draft`とし、評価済み、採用済み、release済み、本体反映済みとは扱わない。candidate作成前gateのroot authority再取得、実行量増加、nonterminal補完の停止条件に該当するため、追加candidate、採用、release、本体反映へ進まない。

## 固定条件

| 項目 | Candidate47 | Candidate48 |
| --- | --- | --- |
| case | `TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1` | 同左 |
| target commit | `eebc1c6c106f504978482238fd760fb73f5fff36` | 同左 |
| target tree | `6366adbb7eaf9db55763e39797b5e070905ede16` | 同左 |
| prompt identity | `the-caption-3ce91a4-applicability-domain-boundary-r1` | `the-caption-3ce91a4-premise-dependency-boundary-r1` |
| bundle sha256 | `da626369ab4462da166c05bb0503c745a32a058d409cefde599e70326b47b998` | `b885774ade895c5a03ffd2a9bb3b766707eac32e2c77ffac4c31d84f63f073f1` |
| prompt overlay commit | `be51dabe247a87d639bc6a4ead06368664b95373` | `f68d46692059959d6e62382e97446066304bc396` |
| prompt overlay tree | `4f4838e514ca2e89f14d547b0dc9f020e9833629` | `4b78bf3e4390ad115923f6e498640218a8350eaa` |
| model / reasoning | `gpt-5.6-sol` / `ultra` | 同左 |
| Agent-visible concurrency | root込み`31` | 同左 |
| Memory instructions | `absent` | `absent` |
| runtime | Python `3.14.5` / `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` | 同左 |
| workspace | `/Users/kenn/repos/THE-CAPTION-DESKTOP-EVAL-SLOT-01` | 同左 |
| root thread | `019f820c-bf56-7fb0-bc8e-2e4d9e28b77b` | `019f82ed-6fb0-7822-9461-0f6916934623` |
| start gate / end drift | pass / none | pass / none |
| comparison status | `diagnostic_only / memory_off / N=1` | 同左 |

Candidate48の開始時刻は`2026-07-21T04:27:07.819Z`、終了時刻は`2026-07-21T04:56:14.373Z`だった。run終了後、user configの`features.memories`は`true`へ復元した。

## 診断値

`tool call`は全session rolloutのtool callを数えた。`model step`は全session rolloutのusage eventを数えた。時間はroot task durationである。tokenはrootと全descendant 34 sessionで最後に記録されたusageを合算した`all_agents/v1`であり、推定値を含まない。中断sessionも中断直前の最終usageを取得できた。

| 診断値 | Candidate47 | Candidate48 | C48 - C47 |
| --- | ---: | ---: | ---: |
| session | 35 | 34 | -1 (-2.86%) |
| worker | 34 | 33 | -1 (-2.94%) |
| root直下worker | 21 | 29 | +8 (+38.10%) |
| nested worker | 13 | 4 | -9 (-69.23%) |
| 最大depth | 4 | 3 | -1 |
| tool call | 807 | 973 | +166 (+20.57%) |
| model step | 905 | 1,041 | +136 (+15.03%) |
| root task duration seconds | 1,662.582 | 1,746.568 | +83.986 (+5.05%) |
| all-agent `total_tokens` | 65,251,694 | 92,801,081 | +27,549,387 (+42.22%) |
| root tokens | 9,023,992 | 10,358,893 | +1,334,901 (+14.79%) |
| child tokens | 56,227,702 | 82,442,188 | +26,214,486 (+46.62%) |
| child token / worker | 1,653,756 | 2,498,248 | +844,492 (+51.07%) |

Candidate48のtoken内訳はinput `92,161,838`、cached input `87,248,640`、output `639,243`、reasoning output `428,108`だった。

tool call内訳は`exec 877`、`spawn_agent 35`、`wait_agent 30`、`send_message 15`、`list_agents 13`、`wait 2`、`interrupt_agent 1`だった。spawn attempt 35件のうち33件がsessionとして成立し、2件は`agent thread limit reached`で失敗した。

## Premise依存とWorker routing

Candidate48は開始時にauthority inventoryとscope inventoryの2 producerだけを起動した。依存する監査waveは両premise phaseの終端後に開始した。したがって、`DEPENDENCY`が意図した「未解決premiseを前提とするjudgmentの早期分散」は抑制された。

その後、rootは27本のroot直下workerを追加した。全体はroot直下29、nested 4、最大depth 3だった。Candidate47の深いnested分割は減ったが、root直下への広い分割へ置き換わった。

spawn失敗2件はいずれもnestedだった。

- `/root/architecture_paths/import_scan`
- `/root/architecture_paths/import_scan/monthly_import_evidence`

`/root/architecture_paths/import_scan`は最終resultを返さず`turn_aborted`で終了した。親の`/root/architecture_paths`はその後`task_complete`となり、`END_STATUS: COMPLETE`を宣言した。34 session中`task_complete`は33、`turn_aborted`は1だった。これは`TERMINAL`が禁止するnonterminal child resultの暗黙補完である。

## Context再取得

次はtool-call入力に各文字列を含むcallとsessionを数えた診断値である。文字列一致はreadの必要性を自動判定しない。

| 参照 | Candidate47 call / session | Candidate48 call / session |
| --- | ---: | ---: |
| `AGENTS.md` | 72 / 32 | 80 / 33 |
| `docs/reference` | 175 / 32 | 223 / 33 |
| `docs/adr` | 63 / 18 | 50 / 20 |
| `git status` | 28 / 20 | 43 / 23 |
| `rg --files` | 53 / 32 | 50 / 32 |

root sessionだけでは、`docs/reference`はCandidate47と同じ9 callだった。`docs/adr`は`2 → 4`へ増えた。rootはauthority producerのterminal resultを待つ前に同じADR / Referenceを直接読んだ。したがって、下流judgmentの開始順は閉じたが、premise producerとrootの判断成立責任は重なった。

## 成果範囲

Candidate48は`FAIL`と結論し、16のfinding group、authority conflict、manufacturing evidence riskを分離して報告した。Python testは`326 passed / 3 skipped / 0 failed`だった。Web Editorの`npm run lint`は依存未導入のため`tsc: command not found`となり、追加installは行わなかった。開始・終了stateは同じHEAD / treeでcleanだった。

private oracleとの対応は次のとおりである。

| oracle | Candidate48最終報告 |
| --- | --- |
| F1 empty / non-positive ledger | 報告した |
| F2 persistence / CompletionLock | 報告した |
| F3 monthly history / fallback | 報告した |
| F4 weekly legacy ledger dependency | 報告した |
| F5 Web Editor empty SSOT / non-loopback bind | 報告した |
| F6 Jinja2 dependency | 報告した |
| R1 provider role separation false positive | 報告しなかった |

known findingは6 / 6を報告し、既知false positiveを避けた。これはCandidate47で未確定だったF4を含む観測範囲の回復である。ただし、blind raterを通しておらず、testがrepository外の一時fileを作成し得る字義上の制約問題と、nonterminal補完が残る。このためscore `4`を確定しない。

## 解釈

- 事実: 先行premise phaseの終端後に依存worker waveが開始した。
- 事実: known finding 6件をすべて報告し、既知false positiveは報告しなかった。
- 事実: nested workerは減ったが、root直下worker、tool call、model step、duration、all-agent tokenは増えた。
- 事実: rootとpremise producerのauthority読取りが並行し、全sessionのReference参照も増えた。
- 事実: 1件のnested workerがnonterminalのまま、親producerがcompleteを宣言した。
- 推測: `DEPENDENCY`は依存waveの開始時点には作用したが、premise producerの排他責任、rootへ渡すterminal input、child lifecycleの成立条件を閉じていない。
- 未確定: 同じ品質範囲と実行量が複数反復でも再現するか。

このN=1は、premise依存の段階化がroutingへ作用したことを示す。しかし、Candidate48がCandidate47の未解決問題を解消したとは判断しない。blind rating、Layer 4登録、winner、採用、release承認、本体反映は行っていない。
