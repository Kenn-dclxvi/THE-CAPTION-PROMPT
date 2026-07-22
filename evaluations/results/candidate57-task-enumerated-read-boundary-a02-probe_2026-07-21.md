# Candidate57 task-enumerated read boundary A02 probe

## 結論

Candidate57はA02 probe 1件で停止した。

実行前TaskSpecの明示列挙だけを`FIXED_READ`適用根拠へ狭めたが、repository authority / state探索中に複数readを同一model stepへ置く経路は止まらなかった。残り9 slot、F05 / F10、standard14、A06へ進めない。

## 観測

- run ID: `f7cc5f0ce3f846e98738f334fe3c2031`
- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` / iteration 1
- Layer 2 status: `valid`
- total tokens: `268,088`
- elapsed: `123.153秒`
- top-level tool call: `10`
- shell command: `19`
- unexpected changed path: `0`
- catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`

開始identityはTaskSpec列挙済みの4 commandを同一model stepで取得した。その後、`rg --files`のresultからrepository内対象を決める過程で、3 read、3 read、3 readをそれぞれ同一model stepへまとめた。Candidate57の非適用文は、別routeを指定しないためmodelの一般的な並列readを禁止できなかった。

最終validationでは`git diff --check`を実行した。Candidate56の欠落は再現しなかったが、A系authority探索のbatch非適用gateはprobe時点で不成立である。

このprobeは2 case × `N=5`を満たさず、Layer 4 resultへ登録していない。互換KPI比較へ使わない。

## 次の対象

次candidateではpredicateを追加しない。`FIXED_READ`をA / F両routeを持つ`READ_ROUTE`一文へ置換する。

- TaskSpecが実行前に有限列挙した独立readは同一model stepで取得する。
- repository authority / stateから対象を決める間は、各result後に次のreadを一つ決める。
- authority探索中は複数readを同一model stepへ置かない。

F適用条件の否定だけでA routeを表現せず、目的の違いを実行方法へ直接bindする。
