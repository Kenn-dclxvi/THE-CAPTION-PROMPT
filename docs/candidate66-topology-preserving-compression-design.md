# Candidate66 topology-preserving compression設計記録

## 結論

Candidate66はCandidate43を直接sourceとし、一層9 label、label順、各clauseの所属を変えず、同一label内の表面表現だけを短くする。

Candidate65で行った目的見出しの追加、9 labelから11 labelへの分割、clauseの別labelへの移動は行わない。Candidate43で重複している表現もlabelをまたいで削除せず、構造と意味圧縮を同時に変えない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-outcome-authority-boundary-r1`（Candidate43）とする。変更targetはroot `AGENTS.md`だけとし、残り18 targetを同一に保つ。
2. Candidate65は32 / 32 source clauseを保持し、root bytesを`7.01%`縮小した。F05 / F10は10 / 10 score `4`だったが、F10はCandidate43比でtool call `43 -> 49`、model step `48 -> 54`、token合計`+14.25%`となった。
3. Candidate65はCandidate43の一層9 labelを3 purpose block、11 labelへ組み替えた。保存traceではshell commandが`50 -> 51`に留まる一方、top-level tool cycleが増えた。構造変更が原因とは確定していないが、次の一変更では構造を固定して表面圧縮だけを分離する。
4. 置換する一つのrelationは、`compressed label body := 同じlabelに属する全source clauseを同じ順序で含み、重複主語、助詞、接続語、同義の動詞句だけを短くしたbody`である。
5. labelは`SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / METHOD / RECOVERY`の9個とし、この順序を変えない。新しい見出し、label、route、predicate、例外、permission、tool methodを追加しない。
6. clauseを別labelへ移さない。`PRODUCER`と`OWNER_ROLE`の明示委譲gate、`PRODUCER`と`INDEPENDENCE`の再割当て禁止は、重複していても両方へ残す。
7. 静的保持は32 source clauseすべてを元label内で対応付け、root bytesがCandidate43の`3,980 bytes`未満であることで判定する。bytes減少をruntime改善とは扱わない。
8. behavioral gateはF10-only正式resultを使う。既存Candidate43 result `6965832090ad4b1b8507c7c8496dc1c5`と同じLayer 1 identity `98da7e8c9ea12d91be50bb4d66ac15926b53a4ddee4d2035bc61bace13b01507`、model、Agent環境、permission、TaskSpec、fixture、executor parameter、各`N=5`へ固定する。
9. 次へ進むにはCandidate66が5 / 5 score `4`、root-only、zero drift、shell command 55件を満たし、Candidate43 F10-onlyのtool call `40`、model step `29`、all-agent token合計`811,578`を超えないことを必須とする。いずれかを満たさなければCandidate66を停止し、A / Dへ進めず、補助predicateを追加しない。

九項目を定義済みであるため、Candidate66の構造bundleを作成できる。構造testに合格した場合だけF10-only profileを作る。

## Source clause所属

| Candidate43 label | source clause | Candidate66 label | 処置 |
| --- | --- | --- | --- |
| `SPEC` | `SPEC1..6` | `SPEC` | 同じ順序で保持し、同一文中の主語と接続だけを短文化 |
| `PRODUCER` | `PRODUCER1..5` | `PRODUCER` | 明示委譲gateを含めて同labelへ保持 |
| `TERMINAL` | `TERMINAL1..2` | `TERMINAL` | 同labelへ保持 |
| `CONTEXT` | `CONTEXT1..3` | `CONTEXT` | packet 9 fieldとhistory境界を同labelへ保持 |
| `OWNER_ROLE` | `OWNER_ROLE1..7` | `OWNER_ROLE` | runtime provenanceとresult stateを同labelへ保持 |
| `ROOT` | `ROOT1` | `ROOT` | 同labelへ保持 |
| `INDEPENDENCE` | `INDEPENDENCE1..2` | `INDEPENDENCE` | 再割当て禁止を削除せず保持 |
| `METHOD` | `METHOD1..4` | `METHOD` | 同じ順序で保持 |
| `RECOVERY` | `RECOVERY1..2` | `RECOVERY` | 同labelへ保持 |

合計は`6 + 5 + 2 + 3 + 7 + 1 + 2 + 4 + 2 = 32` clauseである。

## 許可する短文化

- `Aを固定する。Bを選ぶ。`を、主語と条件が同じ場合だけ`Aを固定し、Bを選ぶ。`へ結合する。
- `別operation / task全体`、`順次・並行`、`false / failed`などpredicateを区別する列挙は削らない。
- 定義式、runtime field、worker packet field、permission停止条件、recovery counterは語列を保持する。
- label間の重複削除、label名の変更、目的見出しの追加は許可しない。

Candidate31からCandidate34の同条件`N=5`では60 / 60 score `4`を維持し、all-agent token中央値が`-15.98%`だった。一方、Candidate32とCandidate65は静的bytesを減らしてもruntime tokenが増えた。Candidate66も静的差ではなく同条件behavioral resultで判定する。

Candidate66の構築、構造確認、F10評価、A / D評価、採用、release、本体反映は別状態とする。

## 構築結果

Candidate66をCandidate43の直接childとして構築した。

- prompt identity: `the-caption-3ce91a4-topology-preserving-compression-r1`
- bundle SHA-256: `7468c94831164ecbb9ce086ce2fd1e549b2bcbdc97bcad37f6d41575253d690a`
- changed target: root `AGENTS.md`だけ
- root bytes: `3,980 -> 3,923`、`-57`、`-1.43%`
- label: 9 / 9を同じ順序で保持
- clause: 32 / 32を元label内へ保持
- cross-label duplicate: 明示委譲gateとproducer再割当て禁止を保持

`SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / METHOD`内の文法表現だけを短くした。`ROOT / INDEPENDENCE / RECOVERY`はCandidate43と逐語一致である。

## 評価結果

最初のF10-only `N=5`は事前gateを通過した。

- score `4`: 5 / 5
- root-only / zero drift: 5 / 5
- shell command: `55 -> 55`
- top-level tool call: `40 -> 39`
- model step: `29 -> 28`
- all-agent token合計: `811,578 -> 795,013`、`-2.04%`

gate通過後にA01 / A02、F05 / F10、D01を各`N=5`で実行した。Candidate66は25 / 25がscore `4`だった。A / Fはroot-onlyで、D01は指定workerだけがreviewを実行した。

一方、追加F set内のF10では次の逆方向を観測した。

- top-level tool call: `43 -> 57`
- model step: `48 -> 62`
- shell command: `55 -> 57`
- all-agent token合計: `848,388 -> 1,114,433`、`+31.36%`

最初のF10-onlyではCandidate66が2 / 5で短いcycleへ収束したが、追加F10では0 / 5だった。したがって、表面圧縮によるruntime削減は再現していない。個々の文法変更がroute差を生んだ因果も確定しない。

## 状態

Candidate66は`targeted_evaluated / stopped`とする。意味保持の観測には使えるが、圧縮候補、採用候補、release候補へ進めない。

次は表面表現を続けて削らず、`docs/candidate43-control-element-classification.md`で`merge / review / conditional`とした重複predicateと常時core外へ分離可能な要素を、意味単位で判定する。詳細は[`Candidate43 / Candidate66 catalog固定N=5`](../evaluations/results/candidate43-candidate66-topology-preserving-compression-catalog-fixed-n5_2026-07-22.md)を正本とする。
