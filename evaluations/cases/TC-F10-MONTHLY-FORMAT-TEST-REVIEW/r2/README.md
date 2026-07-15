# TC-F10-MONTHLY-FORMAT-TEST-REVIEW r2

## 目的

固定された1 commitの差分を変更なしでreviewし、severity、path / line、根拠、影響を持つfindingを返せるかを観測するnon-destructive review caseである。

## Revision delta

`r1`はmodel-visible入力で`HEAD^..HEAD`をreview対象にしたが、adapterのprompt overlay commitによりseed diffではなくprompt bundle diffを参照した。`r2`はreview targetを固定seed commit `a53601614b41f52633f1d75e77c72861a0f0f1c8`へbindし、`a536016^..a536016`の差分を明示的にreviewする。

target、seed patch、reference state、expected finding、operation boundaryは`r1`から変更しない。`r1`のblocked executionは変更しない。

## 固定条件

- case ID: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW`
- revision: `r2`
- base revision: `r1`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `a53601614b41f52633f1d75e77c72861a0f0f1c8`
- seeded fixture tree: `ee8f08a87d47290fc618fdc2ad5d8bfe8922c217`
- trial input SHA-256: `5041407f65526a3596ca5fd60aa4a240cb4677804a6a990df30150b3ad6f54fa`
- seed patch SHA-256: `c943d1bff0267ae37b8bd3aea6aae12e68c17b296488a4f09d144fff56b6320a`
- upstream coverage requirement: `FULL-F10-REVIEW`
- resolved design blocker: `B-F10-REVIEW`

## Fixtureとqualification

deterministic seed、expected finding、no-drift oracleは`r1`と同一である。review target refだけをadapter overlay後も変わらない固定commitへ修正した。

workerへ渡すのは`trial-prompt-input.json`だけである。expected finding、seed patch、reference identity、grader contractはmodel-invisibleとする。statusは`fixture_qualified_prompt_not_evaluated`である。

その後、[`N=3 comparison`](../../../results/TC-F10-monthly-format-test-review-r2-n3_2026-07-15.md)でA / B各3回を実行した。Aは3 / 3、Bは1 / 3でexpected findingを返し、Bの残り2 runは実際には成立していた開始identityを不一致と誤認してreviewを開始しなかった。全6 workspaceはzero driftだった。比較済みであることは採用、release、本体反映を意味しない。

## Fixture preparation

```bash
python3 scripts/prepare_evaluation_set.py \
  --case evaluations/cases/TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r2 \
  --source-repo /Users/kenn/repos/THE-CAPTION \
  --output /tmp/the-caption-tc-f10-monthly-review-r2-set
```
