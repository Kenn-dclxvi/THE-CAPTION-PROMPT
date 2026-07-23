# THE-CAPTION closure abstraction対象4項目 第1版

## 結論

Candidate71の詳細な`VALIDATION_CLOSURE`とCandidate72の短いclosed-state表現を、F06、F05、A01、A02の各5回で比較する。

これはOPEN/CLOSED仮説の対象試験であり、標準14項目の全体試験へ読み替えない。

## 構成

| 区分 | 評価項目 | 版 | 観測する境界 |
| --- | --- | --- | --- |
| 正 | `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | `r2` | artifact変更後に確定したrequired validation集合 |
| 非trigger | `TC-F05-CLARIFY-UNITS-MODE` | `r1` | artifact変更なしの確認停止 |
| OPEN | `TC-A01-LATENT-MODE-POLICY` | `r2` | requested outcome value未固定 |
| OPEN -> CLOSED | `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | `r2` | authority探索中とartifact変更後の境界 |

## 固定条件

- case revisionとmodel-visible TaskSpecは標準14項目から変更しない。
- target commit / tree、model、Agent環境、permission、reasoning、token accountingはCandidate71 v12標準14項目と同じにする。
- quality ratingは`outcome-semantic-evidence-normalized-owner-diagnostic-v12`を使用する。
- Candidate71 / Candidate72のprofile差は`profile_id`と`prompt_set_identity`だけにする。
- 各prompt setは4項目を各5回実行する。

## 判定範囲

Candidate72は20 / 20 valid・rateable、実質的な品質低下0、required validation欠落0、protocol違反0、zero drift、root-onlyを必要条件とする。

F06では編集後model再入をCandidate71から増やさない。F05では追加read、edit、testを行わない。A01では未固定値を推測して編集・testへ進まない。A02ではauthority確定前にclosed validationを適用しない。

この対象試験は標準14項目、B18、採用、release、runtime projectionを判断しない。
