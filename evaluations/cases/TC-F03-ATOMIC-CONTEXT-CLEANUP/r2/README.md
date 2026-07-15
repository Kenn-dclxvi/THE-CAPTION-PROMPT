# TC-F03-ATOMIC-CONTEXT-CLEANUP r2

## 目的

`os.replace`失敗時の一時JSON cleanupを復元するmocked-I/O caseである。

## Revision delta

`r2`は`r1`のtarget、seed、fixture、oracle、F03-C1からF03-C3を変更しない。N=3比較で未指定のcleanup-operation failureとfocused/full gateの包含関係が停止理由になったため、次を明記した。

- F03-C1は`os.replace`のmocked failure後に通常のcleanupが実行可能な条件を対象とする
- cleanup操作自体をfilesystemが恒久的に拒否する条件は評価範囲外とする
- focused gateとfull gateは両方requiredであり、scope重複は許可済みとする

過去の`r1`結果は変更しない。

## Identity

- revision: `r2`
- base revision: `r1`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `895d60764990f02f25c6a6c81babbcb1e0ad5ffa`
- trial input SHA-256: `82ccb1925c3a2f2412b9e079e40d0d8429e3e1383d13ea5e542969db8d683999`
- seed / oracle: `r1`と同一

作成時qualification receiptは`fixture_qualified_prompt_not_evaluated`である。その後、[`core9 r2 global M=4 staged N=3`](../../../results/revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)でprompt比較を実施した。workerへ渡したのは`trial-prompt-input.json`だけであり、比較済みであることは採用、release、本体反映を意味しない。
