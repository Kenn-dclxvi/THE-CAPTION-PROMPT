# TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY r1

## 目的

広いread-only適合性監査で、成果に必要なauthority、対象範囲、既知stateを各producerへどこまで渡すかをAgent自身が決める状況を再現する。

正しい監査成果を維持したまま、rootとworkerが同じauthority探索、scope確定、finding再検証を反復するかを診断する。

## 観測元

THE-CAPTION-DEVのtask `019f7e0b-c2a3-7571-8bd0-6a075bec45e0` では、`ここまでのv4コードが規約通り製造されているかチェックして`という入力に対し、12の初期監査workerと15の再検証workerが起動された。

複数workerが個別に適用authority、production surface、reachable behaviorを再解決した。これは同一predicateの再割当てだけではなく、producerへ渡す情報の境界と、確定済みresultを後段でどう扱うかの問題を含む。

## Fixture

観測元監査の開始identityであるTHE-CAPTION `eebc1c6c106f504978482238fd760fb73f5fff36` のclean checkoutを使う。

このcommitには、監査で確認された複数の到達可能な不適合と、検討対象にはなるが契約違反ではないprompt role分離候補が同時に存在する。

## Visibility

model-visible入力は、広いv4適合性監査というrequired outcome、read-only permission、no-driftだけを指定する。

監査の分割方法、worker数、担当file、読取り順、再検証方法、既知finding、誤検出候補は指定しない。

## 判定境界

qualityは最終監査の正しさ、根拠、重大な見落とし、誤検出、no-driftで判定する。

worker数、tool call、model step、authority再読、worker packet、all-agent tokenは診断evidenceとして保存し、qualityの正解手順や新しいKPIにはしない。

## 初回診断

C43、`gpt-5.6-sol`、Ultra、`N=1`の初回runは、capsuleが`agents.max_threads=30`を宣言した一方、adapterが実行時に4を固定していた。このrunは環境不一致として保持し、routingと効率の比較には使わない。

adapterが宣言値を実行commandへbindするよう修正した再試験では、rootと7 workerの8 sessionになった。同じfindingを別validatorへ再割当てする段は再現しなかった。後段の`extended_validation`は、既出findingの再発見ではなく、未実行test群だけを担当した。

authority専任workerを含む各監査workerとrootは、担当findingに必要なauthorityと実装を個別に取得した。この取得が削減可能な重複か、独立判断に必要な読取りかは、resolved shared premiseを渡さないA06単独では判定しない。結果と比較は[`A06 C43 Ultra max-thread diagnostic`](../../../results/TC-A06-c43-ultra-n1-context-boundary-diagnostic_2026-07-20.md)に記録する。

## 判断成立責任境界diagnostic

Candidate43の手続き的なproducer exclusivityを、judgment resultの成立責任境界へ置換したCandidate45でもUltra `N=1`を実行した。rootと4 workerの5 sessionになり、3つの初期producer result、root admission、4候補を扱う独立反証resultが成立した。producer resultを別roleが暗黙に補完して同一resultへ統合する挙動は観測しなかった。

C43比でsession、tool call、model step、root task durationは減ったが、all-agent tokenは`15,783,901`、`+10.04%`だった。反証workerは4候補をすべて確認し、棄却は0件だった。finalはknown weekly / Web findingを報告せず、test中の一時file生成もあったため、成果品質維持は未確定である。

C43とCandidate45はどちらも`agents.max_threads=30`をadapterへ渡したが、Agentへ提示されたavailable concurrency slotsはroot込み4だった。両runは相互には同じ並行条件だが、元THE-CAPTION-DEVと同じ並行条件ではない。詳細は[`C43 / Candidate45 判断成立責任境界diagnostic`](../../../results/TC-A06-c43-c45-ultra-n1-judgment-authority-boundary-diagnostic_2026-07-20.md)に記録する。

## Desktop slot31 diagnostic

fixed Desktop slotでC43とCandidate45を順次materializeし、両方でAgent-visible concurrency root込み31を確認した。C43はrootと34 worker、Candidate45はrootと24 workerだった。Candidate45はC43比でtool call、model step、all-agent tokenが約32〜33%少なかったが、root tokenは32.22%多く、root duration差は-1.68%だった。

C43は初期17 workerの後に17本の独立再検証workerを起動した。Candidate45は追加反証workerを起動せず、rootが主要候補のauthorityと到達経路を再確認してadmissionした。

ただし、Desktopのdeveloper instructionsへ過去A06情報を含むMemoryが注入され、Candidate45が実際に読んだ。このためslot31 runをcleanなprompt比較へ使わない。詳細とmemory gateは[`slot31 diagnostic`](../../../results/TC-A06-c43-c45-ultra-slot31-n1-judgment-authority-boundary-diagnostic_2026-07-20.md)に記録する。

## Desktop slot31 memory-off diagnostic

user configで`memories=false`へ変更した後、新しいDesktop taskを開始し、C43とCandidate45の両方でslots 31、Memory指示なしを確認した。C43はrootと46 worker、Candidate45はrootと31 workerだった。

Candidate45はC43の候補別validator waveと最終report guardを発生させず、root duration、tool call、model stepを減らした。一方、16本の入れ子workerがauthorityと対象範囲を個別に再取得し、all-agent tokenはC43比`+2.33%`だった。

判断成立責任境界はresultの暗黙補完を防ぐ方向へ動いたが、authority、scope、既知resultをproducerへ渡す情報境界までは作らない。詳細は[`slot31 memory-off diagnostic`](../../../results/TC-A06-c43-c45-ultra-slot31-memory-off-n1-judgment-authority-boundary-diagnostic_2026-07-21.md)に記録する。

## 解決済み前提入力境界diagnostic

Candidate45を直接sourceとし、`CONTEXT`と`ROOT`だけを解決済み前提の入力境界へ置換したCandidate46を、同じfixed Desktop slot、Ultra、root込み31 slot、Memory指示なし、`N=1`で実行した。

Candidate45比でall-agent tokenは`-29.13%`、tool callは`-7.70%`、model stepは`-5.07%`だった。rootの`docs/reference`参照は`22 → 1`となり、解決済みauthorityをroot admissionのopen predicateへ戻さない挙動を確認した。

一方、workerは`31 → 42`、nested workerは`16 → 18`、root durationは`+46.51%`だった。8本の独立反証workerと、3本の`fork_turns=all`を含むprovenance探索が新しい長尾になった。週次legacy ledger依存とWeb Editorの既知findingを最終報告へ含めず、test中に3つのignored fileを一時生成したため、score `4`の維持は確認できない。

Candidate46はdraftのdiagnosticとして保持し、追加candidate、採用、release、本体反映へ進まない。詳細は[`Candidate45 / Candidate46 解決済み前提入力境界diagnostic`](../../../results/TC-A06-c45-c46-ultra-slot31-memory-off-n1-resolved-premise-input-boundary-diagnostic_2026-07-21.md)に記録する。

## 適用域境界diagnostic

Candidate46を直接sourceとし、解決済みpremiseの適用域を対象列挙ではなく適用predicateとevidence conditionで閉じるCandidate47を、同じfixed Desktop slot、Ultra、root込み31 slot、Memory指示なし、`N=1`で実行した。

Candidate46比でsessionは`43 → 35`、tool callは`-13.69%`、model stepは`-12.05%`、root durationは`-26.72%`、all-agent tokenは`-12.71%`だった。Candidate46で除外したWeb Editorを同じ監査適用域へ取り込み、root直下の8本の独立反証waveは発生しなかった。

一方、初期inventoryは深さ4まで再分割され、4件のthread-limit失敗と8件の`fork_turns=all`が発生した。rootの`docs/reference`参照も`1 → 9`となった。1件のnested workerをnonterminalのまま中断した後、rootは全producer終端として集約した。週次は4 sessionで探索したが、oracleのlegacy ledger依存を規約衝突として合否から除外した。repository driftはなかったが、testはrepository外の一時fileを作成して削除したため、score `4`の維持は確認しない。

Candidate47はdraftのdiagnosticとして保持し、追加candidate、採用、release、本体反映へ進まない。詳細は[`Candidate46 / Candidate47 適用域境界diagnostic`](../../../results/TC-A06-c46-c47-ultra-slot31-memory-off-n1-applicability-domain-boundary-diagnostic_2026-07-21.md)に記録する。

## Candidate47未実施検証の補完

元runでskipされた3つのdata-dependent test functionは、THE-CAPTION-DEVの実データ132 ledgerをmodel-invisibleな一時fixtureとして与えると38 caseへ展開し、全件通過した。全suiteは`364 passed / 0 skipped / 0 failed`だった。

元runが見落としたWeb Editorの正規typecheck `npm run lint`（`tsc --noEmit`）も、Candidate47 exact commitとlockfile依存で通過した。この後続検証は元runのrouting、token、final reportを変更しないため、A06の実行比較には加算せず、validation補完としてだけ扱う。

## 前提依存境界diagnostic

Candidate47を直接sourceとし、先行premiseに依存するjudgmentをpremise terminal前に独立operationとして分散しないCandidate48を、同じfixed Desktop slot、Ultra、root込み31 slot、Memory指示なし、`N=1`で実行した。

開始時はauthority inventoryとscope inventoryだけを起動し、その終端後に依存worker waveを開始した。known finding 6件をすべて報告し、既知false positiveは報告しなかった。一方、Candidate47比でroot直下workerは`21 → 29`、tool callは`+20.57%`、model stepは`+15.03%`、root durationは`+5.05%`、all-agent tokenは`+42.22%`だった。

rootとpremise producerのauthority読取りは重なった。1件のnested workerはnonterminalのまま、親producerがcompleteを宣言した。Candidate48は依存waveの開始順には作用したが、判断成立責任の重なり、context再取得、terminal補完を解消していない。

Candidate48はdraftのdiagnosticとして保持する。blind rating、追加candidate、採用、release、本体反映へ進まない。詳細は[`Candidate47 / Candidate48 前提依存境界diagnostic`](../../../results/TC-A06-c47-c48-ultra-slot31-memory-off-n1-premise-dependency-boundary-diagnostic_2026-07-21.md)に記録する。

## C43 max diagnostic

C43を`gpt-5.6-sol`、reasoning effort `max`、fixed Desktop slot、root込み31 slot、Memory指示なし、`N=1`で再実行した。

開始gateとno-driftを満たし、最終監査は12件の不適合を報告した。このrunではrootが監査operationの唯一のproducerになり、workerを起動しなかった。sessionは1、tool callは72、model stepは74、all-agent tokenは`9,415,805`、root durationは`1,352.530`秒だった。

reasoning effortとAgent環境が異なるため、過去の`ultra` runと互換KPI比較へ混ぜない。blind rating、winner、採用、release、本体反映は判断しない。詳細は[`C43 max slot31 memory-off diagnostic`](../../../results/TC-A06-c43-max-slot31-memory-off-n1-diagnostic_2026-07-21.md)に記録する。
