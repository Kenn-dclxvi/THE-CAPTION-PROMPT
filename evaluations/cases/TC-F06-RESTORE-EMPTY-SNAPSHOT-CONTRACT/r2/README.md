# TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT r2

## 目的

削除されたempty-items regression testを復元するtest-only caseである。

## Revision delta

`r2`は`r1`のtarget、seed、fixture、oracle、F06-C1からF06-C3を変更しない。N=3比較でfocused testとtests全体の包含関係が契約矛盾として扱われたため、両commandは明示的にrequiredであり、重複は許可済みとした。

過去の`r1`結果は変更しない。

## Identity

- revision: `r2`
- base revision: `r1`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `90dc14b47c5419e8158f3027437cd297d2f4b9ed`
- trial input SHA-256: `38bb19c8b4df5cf87c8e8542c3e64972ea994a56b79c20bca110d8d6acbde371`
- seed / oracle: `r1`と同一

作成時qualification receiptは`fixture_qualified_prompt_not_evaluated`である。その後、[`core9 r2 global M=4 staged N=3`](../../../results/revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)でprompt比較を実施した。workerへ渡したのは`trial-prompt-input.json`だけであり、比較済みであることは採用、release、本体反映を意味しない。
