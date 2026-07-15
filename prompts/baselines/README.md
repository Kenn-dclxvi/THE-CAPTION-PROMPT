# Baselines

比較元として固定したプロンプトを置く。各baselineは取得元repository、commit / tree、source path、content SHA-256を記録し、取得後に内容を変更しない。

| prompt identity | path数 | 用途 |
| --- | ---: | --- |
| `the-caption-3ce91a4-current-r1` | 17 | 初回null calibrationで使用した比較元 |
| `the-caption-3ce91a4-current-r2` | 19 | revision 2 candidateの全変更targetを含めた比較元 |
