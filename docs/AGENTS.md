# docs instructions

`docs/`の指示は、文書の正本、現在解釈、履歴、参照整合を扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。

- リポジトリ契約の正本は`docs/repository-contract.md`とする。
- 評価基盤のLayerと境界は`docs/prompt-comparison-workflow.md`を正本とする。
- 評価実行方法は`docs/evaluation-loop-manual.md`を正本とする。
- prompt制御の設計原則は`docs/prompt-control-design-principles.md`を正本とする。
- 現在状態、当時の評価、後続の再解釈を同一の事実として混ぜない。
- 過去の判定、score、result、statusを削除しない。
- 現在解釈は注記、新しいrevision、または別文書として追加する。
- 過去resultを、後続のrating contractで再採点したように記述しない。
- 数値、件数、status、commit、identityは一次artifactで確認する。
- 評価と採用、releaseとprojectionを別の状態として記述する。
- 文書移動時は、移動先基準で相対リンクを確認する。
- 同じ説明を複数文書へ全文複製せず、正本へのリンクを優先する。
- 見出し、用語、限定列挙を変更する場合は、文書全体の追従漏れを確認する。
- 未決事項を確定仕様として記述しない。
