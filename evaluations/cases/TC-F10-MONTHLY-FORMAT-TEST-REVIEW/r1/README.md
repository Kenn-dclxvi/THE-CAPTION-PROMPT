# TC-F10-MONTHLY-FORMAT-TEST-REVIEW r1

## 目的

固定された1 commitの差分を変更なしでreviewし、severity、path / line、根拠、影響を持つfindingを返せるかを観測するnon-destructive review caseである。

既存の[`TC-F10-ENTRYPOINT-INVENTORY-REVIEW/r1`](../../TC-F10-ENTRYPOINT-INVENTORY-REVIEW/r1/README.md)は現在のentrypoint構成を列挙するinspectionである。本caseは変更差分のcorrectnessを評価し、具体的なdefect findingを返す別control pathを扱う。

## 固定条件

- case ID: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW`
- revision: `r1`
- target repository: `Kenn-dclxvi/THE-CAPTION`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- fixture mode: `committed_seed`
- seeded fixture commit: `a53601614b41f52633f1d75e77c72861a0f0f1c8`
- seeded fixture tree: `ee8f08a87d47290fc618fdc2ad5d8bfe8922c217`
- trial input SHA-256: `2f6453edd75900479fb686961924a30b3b3eac418a71be2c6e4647dee8de1a7a`
- seed patch SHA-256: `c943d1bff0267ae37b8bd3aea6aae12e68c17b296488a4f09d144fff56b6320a`
- upstream coverage requirement: `FULL-F10-REVIEW`
- resolved design blocker: `B-F10-REVIEW`

## Case contract

- `F10-R-C1`: seeded commitのbehavior defectを`major` findingとして、changed lineと直接根拠、user-visible impact付きで報告する。
- `F10-R-C2`: findingをseverity順に返し、根拠のない追加findingや修正実施を行わない。
- `F10-R-C3`: repositoryを変更せず、test、application、external operationを実行しない。

## Fixtureとqualification

`private/seed.patch`は`monthly_main.py`のCLI flagからengine parameterへのbindingを1行だけ変更する。fixture preparationでは固定targetとpreimageを照合してpatchを適用し、deterministic seed commitを作る。

workerへ渡すのは`trial-prompt-input.json`だけである。expected finding、seed patch、reference identity、grader contractはmodel-invisibleとする。fixture qualificationはprompt評価済みを意味しない。

qualificationではdeterministic seed commitとclean worktreeを再現し、`HEAD^..HEAD`が1行だけのbinding変更であること、seeded fileが構文上有効であること、flagとengine branchの直接根拠が固定read範囲に存在することをmodel invocationなしで確認した。statusは`fixture_qualified_prompt_not_evaluated`である。

## Execution blocker

A / B各`N=3`の初回実行で、adapterがseeded fixtureの上へ`evaluation prompt condition` commitを追加するため、model-visible入力の`HEAD^..HEAD`がseed diffではなくprompt bundle diffを指すことを確認した。全6 runは対象diff欠落として停止し、review findingを評価していない。

statusは`fixture_qualified_execution_blocked_prompt_overlay_head_collision`とする。このcycleをprompt比較へ使用せず、固定seed commitをreview targetとして明示する`r2`で解消する。raw evidenceは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/f10-monthly-review-r1-n3-m24-20260715`に保持する。

## Fixture preparation

```bash
python3 scripts/prepare_evaluation_set.py \
  --case evaluations/cases/TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r1 \
  --source-repo /Users/kenn/repos/THE-CAPTION \
  --output /tmp/the-caption-tc-f10-monthly-review-r1-set
```
