# Repository instructions

## Scope

このリポジトリはTHE-CAPTION向けプロンプトの構築、比較、評価、release準備を扱う。THE-CAPTION本体のruntime変更は、このリポジトリの通常作業範囲に含めない。

## Working rules

- 文書は原則として日本語で記述する。schema名、path、status、commandは再現性のため英語表記を使ってよい。
- artifactが存在することと、評価済み、採用済み、本体反映済みであることを混同しない。
- baseline、candidate、releaseを別pathで管理し、in-placeで上書きしない。
- 比較ではtarget repository ref、prompt identity、model、Agent環境、TaskSpec、permission、fixture、反復条件を固定する。
- model-visible入力とoracle、grader、expected resultなどのmodel-invisible情報を分離する。
- 単一caseや少数反復の結果を一般化しない。観測範囲と未解決事項を明記する。
- THE-CAPTION本体への書き込み、push、PR、merge、runtime有効化は、明示的に依頼された別作業として扱う。
- secret、credential、非公開の生run log、一時worktreeをcommitしない。

## Change discipline

- 1つの変更では1つの判断またはartifact単位を扱う。
- prompt変更と評価条件変更を同じ比較単位へ混ぜない。
- 結果を見た後に評価基準を変更する場合は、新しいprofile revisionとして扱う。
- release候補には由来、対象identity、評価結果、未解決risk、承認状態を含める。
