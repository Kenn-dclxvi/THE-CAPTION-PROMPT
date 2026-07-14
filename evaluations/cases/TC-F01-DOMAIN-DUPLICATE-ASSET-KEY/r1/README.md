# TC-F01-DOMAIN-DUPLICATE-ASSET-KEY r1

## 選定

THE-CAPTIONの最初の評価caseとして、CSVからmarket unitsを読み込む境界で重複した`asset_key`を拒否する挙動の復元taskを選定する。

このcaseは次の理由で最初の反復対象に適する。

- 現行THE-CAPTIONのdomain実装とfocused testへ直接対応する
- 外部I/Oを必要とせず、決定的なseedと観測可能な失敗を構成できる
- 編集許可pathをproduction sourceとfocused testの2 fileへ限定できる
- focused gate、full gate、scope driftを分離して確認できる
- 既存CaseCatalogで`core`かつ`repeatability-critical`として選定済みである

## Identity

- case ID: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY`
- revision: `r1`
- target repository: `Kenn-dclxvi/THE-CAPTION`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- source repository: `Kenn-dclxvi/ai-development-research`
- source commit: `161835826294775fc0b6a9a7583b354d8b4985da`
- source catalog path: `packages/the-caption/prompt-evaluation/case-catalog-v1.json`
- source `trial-prompt-input.json` SHA-256: `757c4d254ea9e11f049ebd36411ca08525de7c3dd99485047811df16b7a97962`
- source `private/case-data.json` SHA-256: `b583f0af0870c852891280dff933933880bf1a457f57caeb612c6ca4ef259b38`

## Visibility boundary

`trial-prompt-input.json`だけをworkerへ渡す。`private/case-data.json`と`private/seed.patch`はfixtureの準備、quality raterが参照するevidenceの準備、qualificationに限定し、workerやprompt rendererへ渡さない。

## 現在の状態

case identity、model-visible入力、壊れたfixtureを作るmodel-invisibleな`seed.patch`、oracle / grader contractを固定し、fixture preparationまで実装した状態である。

`seed.patch`は固定したtarget commitとpreimage hashが一致する場合だけ`git apply --check`後に適用し、適用後のblobとSHA-256も確認する。いずれかが一致しなければ曖昧に適用せず停止し、targetを変更する場合は新しいcase revisionとする。

Evaluation set capsule、fixture preparation、prompt file bundleを使うexecution adapterは実装済みである。bit-identicalなbaseline / candidateによるnull pilotのqualificationは`case_revision_not_qualified`となった。

fixtureはseed対象を未commit変更として保持するが、model-visible TaskSpecは開始時の予期しないdriftで停止するよう要求し、そのseed対象を既知の開始状態として区別していない。実際に両runが実装前に停止したため、このrevisionを正式なprompt比較へ使用しない。詳細は[`evaluations/results/TC-F01-r1_identical-bundle-pilot_2026-07-15.md`](../../../results/TC-F01-r1_identical-bundle-pilot_2026-07-15.md)に記録する。

このartifactが存在しても、caseがevaluation ready、known-good、promptが評価済み、採用済みであることを意味しない。

## Fixture preparation

Evaluation set capsuleと、自己完結したlocal cloneへpatchを適用したfixtureは次でまとめて準備する。

```bash
python3 scripts/prepare_evaluation_set.py \
  --case evaluations/cases/TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r1 \
  --source-repo /Users/kenn/repos/THE-CAPTION \
  --output /tmp/the-caption-tc-f01-r1-set
```

output pathは存在しないpathを指定する。`set.json`と`fixture/`が作成され、`set.json`はmodel-visibleな`trial-prompt-input.json`だけをpayloadへ含む。privateなseed、oracle、graderは含めない。

処理はtarget identity、preimage、patch、postimage、変更pathを検証し、失敗時は作成途中のoutputを削除する。作成したfixtureはGit remoteやalternate object databaseを持たず、元repositoryへ依存しない。作成後は次でLayer 1へ固定できる。

```bash
python3 scripts/evaluation_loop.py freeze-set \
  --set /tmp/the-caption-tc-f01-r1-set/set.json \
  --cycle /tmp/the-caption-tc-f01-r1-cycle
```
