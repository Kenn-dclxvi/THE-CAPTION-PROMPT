# TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3

## 目的

固定された1 commitの差分を変更なしでreviewし、severity、path / line、根拠、影響を持つfindingを返せるかを観測するnon-destructive review caseである。

## Revision delta

`r2`はreview targetを固定seed commitへbindしたが、開始条件では現在の`HEAD^`が同じ固定seed commitであることも要求した。prompt overlay commitを作らない現行adapterでは現在のHEAD自体が固定seed commitとなるため、正しく停止したrunが発生した。

`r3`は固定seed commitの存在とclean statusだけを開始条件にする。review対象は引き続き`a536016^..a536016`へ固定する。現在のHEADとの親子関係は開始条件にしない。

target、seed patch、reference state、expected finding、operation boundaryは`r2`から変更しない。`r1`と`r2`のresultは変更しない。

## 固定条件

- case ID: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW`
- revision: `r3`
- base revision: `r2`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `a53601614b41f52633f1d75e77c72861a0f0f1c8`
- seeded fixture tree: `ee8f08a87d47290fc618fdc2ad5d8bfe8922c217`
- trial input SHA-256: `1111a935214909fc5253f77680e5749a05b8969c469c6f1e1166772a3faad1d7`
- seed patch SHA-256: `c943d1bff0267ae37b8bd3aea6aae12e68c17b296488a4f09d144fff56b6320a`
- upstream coverage requirement: `FULL-F10-REVIEW`
- resolved design blocker: `B-F10-REVIEW`

## Fixtureとqualification

deterministic seed、expected finding、no-drift oracleは`r2`と同一である。開始identity確認だけを、現行adapterでも成立する固定commit存在確認へ修正した。

workerへ渡すのは`trial-prompt-input.json`だけである。expected finding、seed patch、reference identity、grader contractはmodel-invisibleとする。private case artifactのqualification statusは、実行前の状態を示す`fixture_qualified_prompt_not_evaluated`として保持する。

`r3`はC29 expanded試験で再現した開始条件不整合を受けた新revisionである。prompt candidateとrating contractを混ぜず、Candidate30のexpandedとcontinuous profileで初めて使用した。合計30 / 30 runがscore `4`となった。評価結果は[`Candidate30 result`](../../../results/candidate30-runtime-owner-result-binding-owner-producer-v3-continuous-n5-b5_2026-07-17.md)へ分離して保存する。

## Fixture preparation

```bash
python3 scripts/prepare_evaluation_set.py \
  --case evaluations/cases/TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3 \
  --source-repo /Users/kenn/repos/THE-CAPTION \
  --output /tmp/the-caption-tc-f10-monthly-review-r3-set
```
