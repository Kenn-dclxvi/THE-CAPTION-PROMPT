# TC-F07-CANONICAL-V4-RUNNER r2

## 目的

root launcherの`v4|v` aliasをcanonical moduleへ戻すshell-script caseである。

## Revision delta

`r2`は`r1`のtarget、seed、fixture、oracle、F07-C1からF07-C3を変更しない。N=3比較で変更していないdefault pathが新たな停止理由になったため、F07-C2はseeded fixtureから周辺routingのtextを変更しないという条件であり、既存routing全体の再qualificationではないと明記した。

過去の`r1`結果は変更しない。

## Identity

- revision: `r2`
- base revision: `r1`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `5b17df6fc5c86be5614c37e0883277d52045c0cd`
- trial input SHA-256: `5d503fc1c18ec4d8f0b912dfa97ad1a8a0896c3ad44d47ff4267b2a753810e12`
- seed / oracle: `r1`と同一

作成時qualification receiptは`fixture_qualified_prompt_not_evaluated`である。その後、[`core9 r2 global M=4 staged N=3`](../../../results/revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)でprompt比較を実施した。workerへ渡したのは`trial-prompt-input.json`だけであり、比較済みであることは採用、release、本体反映を意味しない。
