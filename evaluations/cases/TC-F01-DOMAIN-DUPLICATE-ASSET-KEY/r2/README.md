# TC-F01-DOMAIN-DUPLICATE-ASSET-KEY r2

## 選定

THE-CAPTIONの最初の評価caseとして、CSVからmarket unitsを読み込む境界で重複した`asset_key`を拒否する挙動の復元taskを選定する。

このcaseは次の理由で最初の反復対象に適する。

- 現行THE-CAPTIONのdomain実装とfocused testへ直接対応する
- 外部I/Oを必要とせず、決定的なseedと観測可能な失敗を構成できる
- 編集許可pathをproduction sourceとfocused testの2 fileへ限定できる
- focused gate、full gate、scope driftを分離して確認できる
- 既存CaseCatalogで`core`かつ`repeatability-critical`として選定済みである

## Revision delta

`r2`は`r1`のtask、target commit、seed patch、oracle、grader contractを変更しない。`r1`のnull pilotで、seed済み未commit変更とmodel-visible TaskSpecのdrift停止条件が衝突したため、fixture内のseedをdeterministic commitとして固定し、Agent開始時のworking treeをcleanにする。

この変更は結果を見て評価基準を緩めるものではない。壊れたpost-seed fileとmodel-visible TaskSpecは`r1`と同一であり、開始状態の表現だけを新しいrevisionとして変更する。

## Identity

- case ID: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY`
- revision: `r2`
- target repository: `Kenn-dclxvi/THE-CAPTION`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- seeded fixture commit: `4e6910d08f49b0825beff08837178f5106cbd0f2`
- seeded fixture tree: `f3dfbad104884a27251573ce7d8c58b046a81661`
- source repository: `Kenn-dclxvi/ai-development-research`
- source commit: `161835826294775fc0b6a9a7583b354d8b4985da`
- source catalog path: `packages/the-caption/prompt-evaluation/case-catalog-v1.json`
- source `trial-prompt-input.json` SHA-256: `757c4d254ea9e11f049ebd36411ca08525de7c3dd99485047811df16b7a97962`
- base revision: `r1`

## Visibility boundary

`trial-prompt-input.json`だけをworkerへ渡す。`private/case-data.json`と`private/seed.patch`はfixtureの準備、quality raterが参照するevidenceの準備、qualificationに限定し、workerやprompt rendererへ渡さない。

## 現在の状態

case identity、model-visible入力、壊れたfixtureを作るmodel-invisibleな`seed.patch`、oracle / grader contract、fixture materializationを固定した状態である。

`seed.patch`は固定したtarget commitとpreimage hashが一致する場合だけ`git apply --check`後に適用し、適用後のblobとSHA-256も確認する。いずれかが一致しなければ曖昧に適用せず停止し、targetを変更する場合は新しいcase revisionとする。

`r2`ではseed patch適用後のpathだけをstageし、固定author、timestamp、messageでseed commitを作る。Agent開始前のcondition commitを含め、A / Bで同じcommit / treeになることを要求する。

bit-identicalなbaseline / candidateによる`N=10` null calibrationでは、persisted-sessionの20runすべてが実装、focused / full gate、監査、レビューまで完走し、同じreference postimageへ到達した。case executionはqualifiedである。

一方、quality 100対100でもtoken中央値はA 327,315対B 516,500.5となり、null条件で機械的winnerが生じた。SA待機pollingとcached inputの差が大きく、現行profileのperformance calibrationはfailedである。独立したblind quality raterの入力境界も未解決であり、このrevisionを正式なprompt比較へ使用しない。qualificationは`execution_qualified_null_calibration_failed`とする。詳細は[`evaluations/results/TC-F01-r2_identical-bundle-n10_2026-07-15.md`](../../../results/TC-F01-r2_identical-bundle-n10_2026-07-15.md)に記録する。

このartifactが存在しても、caseがevaluation ready、known-good、promptが評価済み、採用済みであることを意味しない。

## Fixture preparation

Evaluation set capsuleと、自己完結したlocal cloneへpatchを適用したfixtureは次でまとめて準備する。

```bash
python3 scripts/prepare_evaluation_set.py \
  --case evaluations/cases/TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r2 \
  --source-repo /Users/kenn/repos/THE-CAPTION \
  --output /tmp/the-caption-tc-f01-r2-set
```

output pathは存在しないpathを指定する。`set.json`と`fixture/`が作成され、`set.json`はmodel-visibleな`trial-prompt-input.json`だけをpayloadへ含む。privateなseed、oracle、graderは含めない。

処理はtarget identity、preimage、patch、postimage、seed commit、clean working treeを検証し、失敗時は作成途中のoutputを削除する。作成したfixtureはGit remoteやalternate object databaseを持たず、元repositoryへ依存しない。作成後は次でLayer 1へ固定できる。

```bash
python3 scripts/evaluation_loop.py freeze-set \
  --set /tmp/the-caption-tc-f01-r2-set/set.json \
  --cycle /tmp/the-caption-tc-f01-r2-cycle
```
