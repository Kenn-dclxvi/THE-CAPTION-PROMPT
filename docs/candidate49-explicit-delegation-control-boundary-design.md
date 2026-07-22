# Candidate49 明示委譲制御境界の設計記録

## 位置付け

Candidate49はCandidate43を直接sourceとし、常時適用される委譲制御graphを、TaskSpecまたはuserが独立したproducer executionを明示した場合だけ成立する境界へ圧縮する候補である。

Candidate45からCandidate48はA06の非blind診断用draftとして保持する。Candidate49のsource、評価結果、採用根拠には読み替えない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。control-freeな最短正常経路は、TaskSpec、path-scoped repository authority、source・test・diff・repository stateをrootが直接使い、required outcomeを成立させる経路である。独立実行が明示された場合だけ、担当producerへ解決済みのtask definitionを渡し、そのterminal resultを受け取る。
2. 保存済みA06のCandidate43 strict traceでは、rootが30本のsurface別workerを起動した後、15本の候補別validatorと`final_report_guard`を追加した。後段workerは同じfinding候補のauthority、実装path、到達可能性を別resultとして再取得し、46 worker、47 session、all-agent `total_tokens=103,070,239`になった。
3. A06 TaskSpec、repository authority、repository stateは監査対象、permission、正しい判断内容を制約するが、owner語列や監査surfaceを独立producer executionへ変換する条件を定めない。Candidate43の`INDEPENDENCE`は別result identityへの再検証を許し、`CONTEXT`はtask definitionの再探索と担当predicateに必要なsource確認を区別しない。
4. 置換する一つのpredicateは、worker固有のproducer、context、terminal制御を、TaskSpecまたはuserが独立producer executionを明示したdelegated operationだけへ限定する境界である。
5. この境界は、root-only taskでのproducer選択、owner語列からのworker生成、同じ判断の別workerへの再割当て、task definitionの再探索、result欠落のroot補完を消す。担当predicateの成立に必要なsource確認と、明示された独立検証は消さない。
6. 新たに必要になる判断は、独立producer executionが明示されているか、およびworker packetでtask definitionが解決済みかの二つである。runtime Sender三重照合、result identity追加、admission、premise、applicability、dependencyの新しいlabelは導入しない。
7. 成果品質はA01 / A02の仕様境界、F05 / F10のroot-only terminal output、A03のcompletion、F07の必要な実行と証拠、標準14項目のscore分布で確認する。A06はknown finding、既知false positive、no-drift、worker lifecycleを非blind診断し、単一runを一般化しない。
8. 想定する実行変化は、root-only taskのworker起動と制御説明、A06の候補別validator wave、task-definition再探索、nested worker、input token、tool call、model stepが減ることである。prompt byte数またはworker数だけを成功としない。
9. A01 / A02の境界が変わる、対象試験でscore `4`を失う、明示された独立実行を抑止する、nonterminal resultを補完する、A06の主要findingを失う、または同じtask definitionの再探索が残ったままtokenだけ移る場合は停止する。補助predicateを継ぎ足さない。

## 変更単位

Candidate43のroot `AGENTS.md`だけを変更する。

- `SPEC`、`METHOD`、`RECOVERY`はCandidate43と同一に保つ。
- `PRODUCER`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`を、明示された独立実行だけへ適用する`DELEGATION`へ置換する。
- `CONTEXT`は、解決済みtask definitionと担当predicateを分離する直接記述へ置換する。
- `TERMINAL`は、開始済みdelegated operationのresult欠落を補完しない`COMPLETION`へ置換する。

三つのlabelは、明示委譲が存在するときだけworker lifecycleを成立させる一つの境界を、起動、入力、完了の順に直接記述する。root-only taskへoperation identity graphを要求しない。

## 評価順序

1. bundle identity、C43との差分1 target、未変更18 targetのbit identityを確認する。
2. A01 / A02、F05 / F10、A03、F07を対象試験として各N=5で確認する。
3. 対象試験の停止条件に該当しない場合だけ、Candidate43と同じ標準14項目、第10版採点、各N=5へ進む。
4. 標準14項目で成果品質を維持した場合だけ、A06をAgent-visible `slots=31`、`memory=absent`で非blind診断する。
5. output token、説明文字数、TaskSpec再記述、worker routing、重複authority readはLayer 2 extensionの診断値とし、評価基盤のKPIへ追加しない。

Candidate49の作成、評価、採用、release、本体反映は別状態として扱う。

## 対象試験結果と停止

2026-07-21にA01 / A02とF05 / F10を各`N=5`で実行した。Candidate49は20 / 20件がscore `4`で、全件root-onlyだった。一方、互換条件のCandidate43比でall-agent `total_tokens`は20件合計`+425,761`、`+13.21%`だった。

root promptは39.12%縮小したが、F10は同じcommand数のままinput tokenが37.15%増えた。prompt byte数の縮小を効率化と判断できず、事前停止条件に該当する。

Candidate49は`draft / targeted_evaluated / stopped`とする。A03 / F07、標準14項目、A06、採用、release、本体反映へ進めない。詳細は[`対象試験結果`](../evaluations/results/candidate43-candidate49-explicit-delegation-control-boundary-targeted-n5_2026-07-21.md)に記録する。
