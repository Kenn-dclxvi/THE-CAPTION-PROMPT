# TC-F07-DEPENDENCY-PROVENANCE-PAIR r1

## 目的

`requirements.in`のdirect constraintと`requirements.txt`のcompiled pin provenanceを一対として復元できるかを観測するdependency paired invariant caseである。

seedはPyYAMLの宣言constraintを既知の基準から変更し、compiled pinの`via`由来も同時に壊す。片方だけを直した状態では完了しない。dependency resolver、package install、network accessを使わず、固定済み2ファイルの静的な整合だけを扱う。

## 固定条件

- case ID: `TC-F07-DEPENDENCY-PROVENANCE-PAIR`
- revision: `r1`
- target repository: `Kenn-dclxvi/THE-CAPTION`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- fixture mode: `committed_seed`
- seeded fixture commit: `07ca562d4e70d3b4f5e451b2098259a0d26e9fcb`
- seeded fixture tree: `9f975e8dad8f61ffb30f8d2e0fe5707018d5f32f`
- trial input SHA-256: `0f1032c189da1bed0010b6201897147e6906bdc19e32e0bc4fa6973db732de19`
- seed patch SHA-256: `da7d370e52dec3572891bf67f0533eea3db89fd2d931968b72d261caaf5251d4`
- upstream coverage requirement: `FULL-F07-PAIRED`
- resolved design blocker: `B-F07-PAIRED`

## Case contract

- `F07-P-C1`: `requirements.in`のPyYAML direct constraintを`PyYAML>=6.0.1`へ戻す。
- `F07-P-C2`: `requirements.txt`の`pyyaml==6.0.3`を維持し、その直後のprovenanceを`# via -r requirements.in`へ戻す。
- `F07-P-C3`: 2ファイル以外を変更せず、dependency解決、install、test suite、network operationを行わない。

## Fixtureとqualification

`private/seed.patch`は両方のpaired artifactを同時に不整合へする。fixture preparationでは固定targetとpreimageを照合してpatchを適用し、deterministic seed commitを作る。

workerへ渡すのは`trial-prompt-input.json`だけである。reference postimage、seed patch、grader contractはmodel-invisibleとする。fixture qualificationはprompt評価済みを意味しない。

qualificationではdeterministic seed commitとclean worktreeを再現し、seed状態でpaired static assertionが失敗すること、inverse seedで2ファイルだけが既知の組へ戻りstatic assertionと`git diff --check`が通ることをmodel invocationなしで確認した。statusは`fixture_qualified_prompt_not_evaluated`である。

## Fixture preparation

```bash
python3 scripts/prepare_evaluation_set.py \
  --case evaluations/cases/TC-F07-DEPENDENCY-PROVENANCE-PAIR/r1 \
  --source-repo /Users/kenn/repos/THE-CAPTION \
  --output /tmp/the-caption-tc-f07-dependency-pair-r1-set
```
