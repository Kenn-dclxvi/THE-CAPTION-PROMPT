# Repository contract

## 1. Artifact

このリポジトリが作るものは、THE-CAPTION向けのversioned prompt bundleと、その比較・評価・反映判断に必要な再現可能な根拠である。

このリポジトリ自体はTHE-CAPTIONのruntime正本ではない。`prompts/releases/`にbundleが存在しても、本体への反映または有効化は発生しない。

## 2. State

prompt bundleは次の状態を区別する。

| State | 意味 |
| --- | --- |
| `draft` | 構築中。比較判断へ使用しない |
| `evaluation_ready` | identityと評価条件を固定済み。評価開始可能 |
| `evaluated` | 固定profileで結果を取得済み。採用は未判断 |
| `release_candidate` | 評価範囲と未解決riskを確認し、反映候補に固定済み |
| `approved_for_projection` | THE-CAPTION本体への反映を明示承認済み |
| `projected` | 対象commitへの反映identityを記録済み |

状態は自動昇格させない。評価成功、release作成、承認、本体反映は別のgateとする。

## 3. Required identity

baseline、candidate、release、evaluation resultは、該当する範囲で次を固定する。

- target repositoryとstart commit / tree
- prompt source pathとcontent SHA-256
- model、reasoning設定、Agent / CLI version
- TaskSpec、permission、allowed / forbidden paths
- fixture、case revision、grader / oracle revision
- repetition、order、environment、実行時刻
- terminal outcome、変更path、validation結果

## 4. Evaluation boundary

- 同一比較内ではprompt以外の条件を揃える。
- workerへ見せる入力と、fixture seed、oracle、grader、expected resultを分離する。
- coverageと同一caseのrepeatabilityを別軸で扱う。
- tuningに使ったcaseを同じrevisionのheld-out evidenceとして扱わない。
- environment failureをpromptまたはtask behaviorの失敗へ混ぜない。
- 評価結果から言える範囲と、言えない範囲を併記する。

## 5. Projection boundary

THE-CAPTION本体への反映には、少なくとも次を別作業で固定する。

1. 対象THE-CAPTION commit
2. 反映するrelease identity
3. 変更対象path
4. required validation
5. rollback identity
6. commit、push、PR、merge、runtime有効化の許可

反映後は、release identityとTHE-CAPTION側のcommit identityをこのリポジトリへ記録する。
