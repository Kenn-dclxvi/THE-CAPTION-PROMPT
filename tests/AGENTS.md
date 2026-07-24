# tests instructions

`tests/`の指示は、評価基盤とrepository contractの回帰検証を扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。

- testは公開contractとschemaの挙動を検証する。
- privateな実装順序や内部関数構造へ過剰に固定しない。
- fixtureやexpected dataを、実装結果へ合わせて無条件に変更しない。
- append-only、identity、compatibility、model-visible境界の回帰を維持する。
- 過去schemaと現行schemaの共存を検証する。
- nonzero exit、計測不完全、外部失敗、品質失敗を別状態として検証する。
- test実行中に生成した一時artifactをrepositoryへ残さない。
- scripts変更時は関連testだけでなく、全test discoveryで回帰を確認する。
- symlink構造を検査するtestまたは検証手段では、checkout環境の表示だけでなくGit tree modeも確認する。
