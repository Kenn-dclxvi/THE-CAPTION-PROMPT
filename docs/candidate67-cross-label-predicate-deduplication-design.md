# Candidate67 cross-label predicate deduplication設計記録

## 結論

Candidate67はCandidate43を直接sourceとし、root `AGENTS.md`の一層9 labelと本文表現を保ったまま、別labelに重複している二つのpredicateだけを正本label一か所へ集約する。

- 明示委譲gateの正本は`OWNER_ROLE`とし、`PRODUCER`側の短い重複文を削除する。
- 同一predicateのproducer再割当て禁止の正本は`PRODUCER`とし、`INDEPENDENCE`側の短い重複文を削除する。

`F5 / F9`、`D6`、`R1 / R2`は変更しない。表面短文化、label再編、route追加も混ぜない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。最短正常経路は、root-only operationではrootをproducerへ一度bindしてpredicateを一度だけ実行し、明示委譲operationではTaskSpecが指定したworkerをpredicate前に一度だけ起動する経路である。
2. 保存済み誤経路は二つある。Candidate41以前ではcriterion owner語列をworker指定へ読み替える不要worker起動があり、Candidate28以前では同一predicateのroot / worker重複実行とworker不成立後のroot差替えがあった。
3. TaskSpecはownerまたはproducerを記述できるが、criterion owner語列をproducer指定へ変換してよいか、同一predicateを別producerへ再割当てしてよいかという共通解釈までは定義しない。そのため明示委譲gateとproducer exclusivity自体は削除せず、それぞれ`OWNER_ROLE`と`PRODUCER`へ残す。
4. 変更する一つのrelationは、`duplicate predicate -> one canonical owner label`である。意味を担う正本を残し、別labelの短い再記述だけを削除する。
5. 消す判断は、`PRODUCER`と`OWNER_ROLE`にある明示委譲gateの語差を照合する判断、および`PRODUCER`と`INDEPENDENCE`にある再割当て禁止の適用単位を照合する判断である。
6. 新しい判断、参照、例外、permission、route、labelは追加しない。9 labelと順序を維持し、正本文はCandidate43と逐語一致で残す。
7. 品質gateは、最初にF10-onlyを`N=5`で実行し、root-only、成果、shell command、tool call、model step、all-agent tokenを確認する。通過時だけA01 / A02、F05 / F10、明示委譲の正のcaseであるD01を各`N=5`で確認する。
8. 期待する変化は、重複gateの再照合が消え、F10-onlyのtop-level tool call、model step、all-agent tokenがCandidate43以下になることである。worker routingはF10でroot-only、D01でTaskSpec指定worker一つだけを維持する。
9. F10-onlyが5 / 5 score `4`、root-only、zero drift、Candidate43と同じshell command集合を満たさない場合、またはCandidate43のtool call `40`、reasoning item `29`、all-agent token合計`811,578`を超える場合は停止する。通過後のD01で指定worker routeを満たさない場合も停止する。停止後に補助predicateを追加しない。

九項目を定義済みであるため、Candidate67のbundleと構造testを作成できる。構造testに合格した場合だけF10-only評価を開始する。

## 正本label

| 重複predicate | 削除元 | 正本 | 保持する理由 |
| --- | --- | --- | --- |
| TaskSpecが独立producer executionを明示した場合だけ委譲する | `PRODUCER` | `OWNER_ROLE` | owner語列との境界、task identity binding、predicate前spawnが一つの条件として完結している |
| 同一predicateを別producerへ再割当てしない | `INDEPENDENCE` | `PRODUCER` | operationごとのsingle producer bindingと順次・並行の重複実行禁止が一つの条件として完結している |

`INDEPENDENCE`には、先行result / artifactを対象とする独立確認を別operationとして事前固定する条件を残す。これはproducer再割当て禁止とは異なるTaskSpec境界である。

Candidate67の構築、評価、採用、release、本体反映は別状態とする。

## 構築結果

Candidate67をCandidate43の直接childとして構築した。

- prompt identity: `the-caption-3ce91a4-cross-label-predicate-deduplication-r1`
- bundle SHA-256: `0676b5c34f3fa68e71984f28fa0fc49938fde5b3ee822fe4cffa7522b6bcce87`
- changed target: root `AGENTS.md`だけ
- root bytes: `3,980 -> 3,792`、`-188`、`-4.72%`
- label: 9 / 9を同じ順序で保持
- 削除: 設計済みのcross-label duplicate 2文だけ

構造testは、候補全文がCandidate43から対象2文だけを削除した結果と完全一致すること、正本predicateが残ること、5 profileがprompt identity以外を変えないことを確認した。

## 測定訂正

作成前にCandidate66結果から転記したF10-only shell command `55`は、Candidate43のimmutable execution archiveと`all-agent-command-evidence/v5`の再照合で`50`へ訂正した。Candidate67も同じ`50`であり、同じcommand集合を維持した。

同じ旧記録の`model step=29`は`response_item.reasoning`数と一致し、`token_count` event数`46`とは一致しない。事前gateは宣言済み数値と同じreasoning item定義で`29 -> 26`を比較し、token_count eventも`46 -> 40`として別記録した。

## 評価結果

最初のF10-only `N=5`は事前gateを通過した。

- score `4`: 5 / 5
- root-only / zero drift: 5 / 5
- shell command: `50 -> 50`
- top-level tool call: `40 -> 35`
- reasoning item: `29 -> 26`
- token_count event: `46 -> 40`
- all-agent token合計: `811,578 -> 727,855`、`-10.32%`

gate通過後にA01 / A02、F05 / F10、D01を各`N=5`で実行した。Candidate67の30 runはscore `4 / 3 = 29 / 1`で、対応するCandidate43の保存結果と同じ分布だった。A / Fはroot-only、D01は5 / 5で指定workerだけがreview対象を読んだ。

一方、追加F set内のF10はtoken合計`848,388 -> 958,928`、`+13.03%`、D01は`1,318,767 -> 1,414,252`、`+7.24%`だった。最初のF10-only削減は再現していない。

## 状態

対象試験の終了時点ではCandidate67を`targeted_evaluated / stopped`とした。二つの重複predicateを正本一か所へ統合できる意味証拠として保持したが、追加F10とD01でruntime削減を再現しなかったためである。

その後、判断には14ケースが必要という別判断により、Candidate43の標準14 profileから候補identityだけを替えた各`N=5`を追加実行した。Candidate43とCandidate67は両方が70 / 70 score `4`だった。3 KPI中央値はCandidate67からCandidate43を引いてquality `0.000`、all-agent token `-84,992`、elapsed `-9.276秒`だった。一方、70件token合計はCandidate67が`+48,808`多い。

現在の状態は`standard14_evaluated`とする。標準14項目で意味欠落は観測しなかったが、runtime差は反復間で方向が揃わないため削減効果を確定しない。採用候補、release候補、本体反映は未判断である。詳細は[`Candidate43 / Candidate67標準14 N=5`](../evaluations/results/candidate43-candidate67-cross-label-predicate-deduplication-v10-standard14-n5_2026-07-22.md)を正本とする。
