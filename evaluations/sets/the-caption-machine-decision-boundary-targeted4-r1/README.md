# THE-CAPTION machine decision boundary対象4項目 第1版

## 結論

Candidate70の`MACHINE_BOUNDARY`は、F04、F06、F07 canonicalを適用対象、A02を非適用対象として各5回確認する。

これは項目固有の原因確認であり、標準14項目の全体試験へ読み替えない。

## 構成

| 区分 | 評価項目 | 版 | 観測する境界 |
| --- | --- | --- | --- |
| 正 | `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | `r2` | `npm ci`成功後のlint、lint成功後のbuild |
| 正 | `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | `r2` | 対象test成功後の全test |
| 正 | `TC-F07-CANONICAL-V4-RUNNER` | `r2` | `bash -n`成功後のmain verify |
| 非trigger | `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | `r2` | canonical targetの意味解決前 |

## 固定条件

- target commit / tree、model、Agent環境、permission、reasoning、token accounting、反復条件はCandidate69標準14項目v11と同じにする。
- case revisionとmodel-visible TaskSpecは標準14項目から変更しない。
- quality ratingは`outcome-semantic-location-owner-diagnostic-v11`を使用する。
- required commandは個別commandとstructured exitを維持する。shell commandを結合しない。
- C69 / C70のprofile差は`profile_id`と`prompt_set_identity`だけにする。
- 各prompt setは4項目を各5回実行する。

## 判定範囲

Candidate70は20 / 20 valid・rateable・score `4`、root-only、zero drift、required command protocol違反0を必要条件とする。

正の3項目では、編集後top-level tool callとall-agent `total_tokens`がCandidate69より減ることを要求する。`elapsed_seconds`が減らない場合は時間短縮を主張しない。

A02では、canonical target確定前にmachine boundaryを適用してはならない。

この対象試験は採用、release、runtime projectionを判断しない。

## 実行結果

[C69 / C70各N=5結果](../../results/candidate69-candidate70-machine-decision-boundary-targeted4-n5_2026-07-22.md)をappend-only registryへ登録した。C70は公式score `4 / 3 = 19 / 1`とF06のtool call・token・elapsed増加により事前gate不通過となり、`targeted_evaluated / stopped`である。
