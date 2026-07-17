# Candidate31 operation terminal closure targeted result

## 結論

Candidate31のtargeted試験は、15 / 15 runがscore `4`となった。

Candidate31のprompt変更は、test commandを列挙する対策ではない。

変更した境界は、TaskSpecへ固定した全predicateのbind済みproducer terminal resultが揃うまで、operationをterminalにしない制御である。

targeted試験では、C30 continuous試験でscore `3`が残ったF06とF07の3 caseを各5回確認した。

この観測範囲では、成果、Owner結果、required commandのterminal evidenceが15 / 15 runで揃った。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 問題だった挙動

C30 continuous試験では、F06とF07の7 runがscore `3`だった。

7件のうち5件は、既存collectorが子sessionのstructured command array、継続中sessionの完了結果、または実行時に確定したcommandを収集できない評価側の問題だった。

残る2件は、必要な処理がterminal resultへ到達する前に、上位operationが完了扱いになる実行側の問題だった。

具体例は、実行が継続中を返した後に完了結果を待たず、最終応答で完了を宣言する挙動である。

したがって、個別test commandを強制するのではなく、既存のoperation、predicate、producer、terminalの境界を閉じる必要があった。

## 変更した境界

Candidate31はCandidate30の直接childである。

prompt bundleで変更したtargetはroot `AGENTS.md`だけである。

追加した制御は次のとおりである。

1. operationは、全predicateのbind済みproducer terminal resultが揃った場合だけterminalにする。
2. invocation、worker、sessionがnonterminalなら、operationもnonterminalのままにする。
3. predicate resultが欠けている間は、進行報告、集約結果、final responseで補完しない。

この制御はtest、command、exit code、case、pathを列挙しない。

例えば、非同期処理が「受付済み」だけを返した場合は、最終結果が返るまで完了扱いにしない。

## 評価側の別revision

prompt変更と評価側の修正は別artifactにした。

`owner-producer-quality-v4`は、`all-agent-command-evidence/v2`を使う。

command evidence v2は、子sessionのstructured command arrayと、継続中sessionに対応する完了結果を収集する。

このcollector変更は、実行されていた処理を未実行と誤判定しないための証跡修正である。

collectorはcommandを実行せず、保存済みtool callとtool resultだけを解析する。

既存のrating v3 resultは変更していない。

## 固定条件

- prompt set: `the-caption-3ce91a4-operation-terminal-closure-r1`
- bundle SHA-256: `b43d3a62dafe3d489800b1cbb6c6871e6062a040d74a34a75c66e882415de304`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- evaluation set: `the-caption-operation-terminal-closure-targeted3-r1` / `r1`
- cases: F06 empty snapshot、F07 canonical runner、F07 dependency provenance
- repetition: 各case `N=5`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- executor: global queue `M=15`、max attempts `3`
- token accounting: all-agent `v1`
- quality rating: `owner-producer-quality-v4`
- rating contract SHA-256: `996875126f1f30bb146df78a47274ffd08e003ebb6c54c24e8cda98754a9dd53`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v2`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`

## 結果

- valid / rateable run: 15 / 15
- score `4`: 15
- score `3`: 0
- Owner証跡 eligible: 15 / 15
- excluded attempt: 0
- all-agent token total: `5,690,052`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `1,100,300`
- `elapsed_seconds` median: `396.091`
- result ID: `9f9a9d87b1814cc48eaefde686de90c5`
- compatibility key: `aa1d9b8c69804dd21c126ed165f42126b7065cfac5e750d38482aecaa3630b5a`

| case | score 4 | score 3 |
| --- | ---: | ---: |
| F06 empty snapshot | 5 | 0 |
| F07 canonical runner | 5 | 0 |
| F07 dependency provenance | 5 | 0 |

F06は5 / 5で、対象test、tests全体、差分確認のterminal evidenceが揃った。

F07 canonicalは5 / 5で、shell静的確認、main verify、差分確認のterminal evidenceが揃った。

F07 dependencyは5 / 5で、指定static validationと差分確認のterminal evidenceが揃った。

## 判断

事実として、targeted 15 runでは、nonterminalまたは欠落したpredicate resultをfinal responseで補う挙動は観測されなかった。

事実として、Candidate31のprompt本文にcase固有またはcommand固有の条件はない。

判断として、C30で残った3 caseの低頻度score `3`は、このtargeted観測範囲では再発しなかった。

推測として、operation terminal closureが2件の実行側問題を防ぎ、collector v2が5件の評価側見落としを防いだと考えられる。

ただし、prompt変更とcollector変更を同じcampaignで評価したため、それぞれの寄与率は分離できない。

この結果を未評価caseや長期連続試験へ一般化しない。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate31-operation-terminal-closure-owner-producer-v4-targeted3-n5-20260717-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/9f9a9d87b1814cc48eaefde686de90c5.json`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
