# layer2 instructions

`layer2/`の指示は、KPIに含めないrun-bound diagnostic extensionを扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。

- `layer2/extensions/<run_id>/<feature>/`をrun-boundな診断artifactとして扱う。
- root／worker別token、session、command、routing情報をKPIへ入力しない。
- extensionをLayer 3のquality score変更へ使用しない。
- featureごとにschemaとsource identityを固定する。
- 元runとのbindingが確認できないextensionを比較根拠にしない。
- extensionの欠落を推定値で補完しない。
- extensionの追加をevaluation foundationのLayerまたはKPI拡張として扱わない。
- private raw dataを公開extensionへ無条件に保存しない。
