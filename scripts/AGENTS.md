# scripts instructions

`scripts/`の指示は、評価基盤の実行コード、adapter、collector、schema処理を扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。

- `scripts/evaluation_loop.py`をevaluation foundation v3の固定点として扱う。
- 再現可能な不具合または明示要件なしに、Layer、KPI、出力schemaを拡張しない。
- 書込処理はappend-onlyを維持する。
- 既存artifactを上書きしない。
- executor、evidence collector、quality rating、KPI comparisonの責務を混ぜない。
- tokenを推定しない。
- 全session usageが取得できないrunは、外部計測失敗として除外する。
- raw log、secret、credentialを公開artifactへ含めない。
- shell commandやfixture pathを文字列連結によって暗黙変更しない。
- schema変更時は既存revisionを保持し、新しいschema revisionを追加する。
- 実装コードの変更と、評価対象promptの変更を同一変更へ混ぜない。
- scripts変更では、対応するunit testを追加または更新する。
- temporary directoryや評価用workspaceをrepository内へ残さない。
