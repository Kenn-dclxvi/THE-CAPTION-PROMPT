# Candidate64 self-contained execution paths設計記録

## 結論

Candidate64はCandidate43を直接sourceとし、root `AGENTS.md`の9つの横断labelを、実行時に一度だけ選ぶ4 blockへ並べ替える。

最初の版では重複を削らない。root producer operationとdelegated producer operationの両方へ、operation scope、single producer、terminal、`false / failed`保持を重複して置き、それぞれを単独で読める形にする。

これは圧縮candidateではなく、圧縮前の構造candidateである。意味要素、成果条件、permission、tool methodは削除または追加しない。静的bytesが増えても停止理由にせず、構造確定後の別candidateで説明と重複を圧縮する。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。最短正常経路は、requested outcome valueが未確定なら編集・試験前に未固定値だけを質問して終了し、確定済みならoperationごとに一つのproducerをbindして全predicateのterminal resultを得る経路である。TaskSpecが独立producer executionを明示しないoperationはrootが実行し、明示したoperationだけを指定workerが実行する。
2. 同一F05 / F10 Layer 1のCandidate43 `N=5`は、F10の固定evidence範囲と成果を維持しながら、top-level tool callが`11 / 3 / 11 / 11 / 7`へ分岐した。目的別に再配置したCandidate53も10 / 10 score `4`だったが、F10はCandidate43比でmodel step `48 -> 54`、tool call `43 -> 49`、token合計`+13.37%`だった。見出し分離だけでは短いroot経路を安定させなかった。
3. TaskSpec、repository authority、repository stateはrequired outcomeと証拠を固定するが、root-only operationが`SPEC / PRODUCER / TERMINAL / OWNER_ROLE / INDEPENDENCE`から必要部分だけを組み立てるprompt内読解は制御しない。delegation非適用条件を書いても、常時可視のD系説明をroot経路から除けない。
4. 置換する一つのpresentation predicateは、`execution_path := TaskSpecが独立producer executionを明示するならdelegated、そうでなければroot`である。rootとdelegatedの各blockへ同じF系predicateを複製し、選択後に別blockを参照しない。
5. このpredicateが消す判断点は、root operationがdelegation gate、worker packet、runtime provenance、non-producer root境界を適用するかを各labelで再判断する経路と、delegated operationが共通F系labelへ戻ってterminal stateを組み立てる経路である。
6. 新たに増えるのは一つのpath選択とF系文の重複である。新しいoutcome、permission、constraint、result state、tool、read順序、SA起動条件は増やさない。静的bytesと入力tokenは初期版で増える可能性がある。
7. 構造保持は、Candidate43の32 atomic clauseが一つ以上残り、root / delegated両blockがscope、single producer、terminal、`false / failed`保持を自己完結して持つことで判定する。behavioral確認ではA01 / A02、F05 / F10、明示的な独立producer executionを持つD系caseを同一互換条件で各`N=5`実行し、全run score `4`を必須とする。
8. 初期構造版ではprompt bytesとtokenの削減を期待値にしない。root-only caseでdelegation toolを起動せず、F10のtool call、model step、all-agent tokenが同条件Candidate43を超えないことを次段へ進む条件とする。D系caseでは指定workerの起動、result provenance、root非再実行を確認する。
9. source clauseの欠落、root / delegatedの非排他的選択、必要なworker不起動、不要worker起動、score `4`喪失、またはroot-only F10のtool call・model step・token増加があれば停止する。Candidate64へ補助predicateを継ぎ足さず、構造draftへ戻る。

九項目を定義済みであるため、Candidate64の構造bundleを作成できる。評価profileは構造review後の別artifactとする。

## 4 block

```text
1. Start and path selection
   spec_ready=false -> clarification result -> stop
   spec_ready=true  -> operationごとにpathを一つ選ぶ
                       |                    |
                       v                    v
2. Root producer operation      3. Delegated producer operation
   F coreを自己完結                 F core + D controlを自己完結
                       |                    |
                       +---------+----------+
                                 v
4. Failure and recovery
   M method / permission + R recovery counter
```

`A / F / D / M / R`は設計上の分類として保持する。model-visible見出しは実行順とpathだけを示し、case labelや既知ユースケースを分岐条件にしない。

## Source clause配置

Candidate43の各labelを句点単位で32 atomic clauseへ分ける。文言を残したまま次へ配置する。

| Candidate43 clause | Candidate64 block | count |
| --- | --- | ---: |
| `SPEC1..5` | Start and path selection | 1 |
| `SPEC6` | Root / Delegated | 2 |
| `PRODUCER1 / 2 / 5` | Root / Delegated | 2 |
| `PRODUCER3 / 4` | Start / Delegated | 2 |
| `TERMINAL1 / 2` | Root / Delegated | 2 |
| `CONTEXT1..3` | Delegated | 1 |
| `OWNER_ROLE1` | Start / Delegated | 2 |
| `OWNER_ROLE2..5 / 7` | Delegated | 1 |
| `OWNER_ROLE6` | Root / Delegated | 2 |
| `ROOT1` | Delegated | 1 |
| `INDEPENDENCE1` | Start | 1 |
| `INDEPENDENCE2` | Root / Delegated | 2 |
| `METHOD1..4` | Failure and recovery | 1 |
| `RECOVERY1 / 2` | Failure and recovery | 1 |

追加する橋渡し文は、`spec_ready=true`後に各operationのpathをrootまたはdelegatedへ一度だけ固定する一文だけとする。

## 構造確定後の圧縮順序

1. 各block内で同じpredicateを二度説明している文を統合する。
2. root / delegated間で重複したF coreから、path選択後も誤適用を起こさない共通文だけを前段へ戻す。
3. label名、背景説明、negative例を、対応するpredicateを残したまま短縮する。
4. 静的bytes、model-visible token、behavioral KPIを別々に測る。

Candidate64の構築、構造確認、behavioral評価、採用、release、本体反映は別状態である。

## 構築結果

Candidate64のfull bundleを構築し、構造testを完了した。

- prompt identity: `the-caption-3ce91a4-self-contained-execution-paths-r1`
- bundle SHA-256: `b5b8d9486b901336d86d062af3d3fca0ec82dd797d39ef3e28ea89857e121e42`
- changed target: root `AGENTS.md`だけ
- Candidate43 root: `3,980 bytes`、11 lines、9 flat label
- Candidate64 root: `5,594 bytes`、28 lines、4 ordered block
- static差: `+1,614 bytes`、`+40.55%`
- Candidate43 atomic clause: 32 / 32保持
- Candidate64内のsource clause occurrence: 43。root / delegatedへ11 occurrenceを意図的に追加
- new semantic bridge: root / delegated pathを一度だけ選ぶ一文

構築時の`tests/test_candidate64.py`は5 test、32 subtestを通過した。N=5 profileとD01 caseの同一条件test追加後は7 test、38 subtestである。19 target中、manifest差があるのはroot `AGENTS.md`だけである。root / delegatedの両blockがscope、single producer、terminal、`false / failed`保持を持ち、delegation固有のpacket、provenance、root境界はroot blockへ入っていない。

これは構造保持の静的確認であり、この時点ではbehavioral評価ではなかった。

## Catalog固定 N=5結果

A01 / A02、F05 / F10、明示producer D01を同じcatalog固定条件で各`N=5`実行した。Candidate64の25 / 25 runはscore `4`だった。A / Fの20 runはroot-onlyであり、D01は5 / 5で指定workerを一つ起動し、rootがreviewを再実行しなかった。

一方、事前停止対象のroot-only F10はCandidate43比で次のとおり増えた。

- top-level tool call: `43 -> 54`
- model step: `48 -> 59`
- all-agent token合計: `848,388 -> 1,093,565`、`+28.90%`

A scope、F scope、D scopeのtoken合計もCandidate43比でそれぞれ`+13.32%`、`+13.57%`、`+12.35%`だった。root / delegatedへF coreを全文重複する構造は成果を保持したが、実行costを抑えなかった。

事前gateに従い、Candidate64は`targeted_evaluated / stopped`とする。Candidate64へ補助predicateを追加せず、Candidate43を直接sourceに戻して重複なしの短文化を検討する。詳細は[`Candidate43 / Candidate64 catalog固定 N=5`](../evaluations/results/candidate43-candidate64-self-contained-execution-paths-catalog-fixed-n5_2026-07-22.md)に置く。
