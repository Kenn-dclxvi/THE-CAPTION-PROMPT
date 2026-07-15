# TC-F08-CANONICAL-CLI-REFERENCE-SYNC r1

## 目的

sourceとscoped authorityを根拠に、weekly / monthlyのCLI referenceをcanonical module formへ同期するdocs-only caseである。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `9708b581e627027b97acc275369b8c517898e17d`
- seeded fixture tree: `07e08c16c2581211238cccc49fac6954750e9b27`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- trial input SHA-256: `728f68125b0d3751747d723a2a59802efda4953565213b10bc8e12ace00213e7`
- seed patch SHA-256: `04baf2fa818eef89fdb91ff3868ae99deb7f349ff526edffca0a454914f2c74b`

## Fixtureとqualification

`seed.patch`はreference内の2 commandを`python weekly.py`と`python monthly.py`へ戻す。canonical entrypoint filesは存在し、seeded command gatesと`git diff --check`はいずれも通るため、reference/source整合性を読む必要がある。

作成時qualification receiptは`fixture_qualified_prompt_not_evaluated`である。その後、[`core9 r2 global M=4 staged N=3`](../../../results/revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)でA / B prompt比較を実施した。比較済みであることは採用、release、本体反映を意味しない。

## Visibility

workerへ渡すのは`trial-prompt-input.json`だけで、誤った2 commandの生成方法、reference postimage、oracleはmodel-invisibleである。
