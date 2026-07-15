# TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND r1

## 選定

revision 2 candidateに対する最初の追加variationとして、V4 engineからCollectionHistoryUpdaterへ実行対象日を渡すcross-layer挙動の復元taskを選定する。

F01の単一domain source復元に対し、このcaseは次を追加で観測する。

- 2 sourceと2 testにまたがるmulti-file scope
- application layerとdomain layerのcross-layer contract
- primary refreshとselective retryの両経路
- test-contract riskに対するconditional audit
- focused gateとfull Python completion
- 許可済み4 path以外のscope drift

## Identity

- case ID: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND`
- revision: `r1`
- target repository: `Kenn-dclxvi/THE-CAPTION`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- seeded fixture commit: `b802eae75710d6c54b3250cc790b29a3ff56f675`
- seeded fixture tree: `6a16ad792b317331d4b2bfcc6ae30716cb6d8aef`
- source repository: `Kenn-dclxvi/ai-development-research`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- source catalog path: `packages/the-caption/prompt-evaluation/case-catalog-v1.json`
- source case revision: `r1`
- source `trial-prompt-input.json` SHA-256: `73f3b34386012f4e417146babdf6d7d9535ff5370db637e3b154b51b74905592`
- source private case-data SHA-256: `a3b48be044a85873e9a0a3f1d62d1c0f524067baf05c753963cf8ddfeeb3e725`
- local `seed.patch` SHA-256: `110d9ee7f0e0ded81433e515a5734db9772ade88c4c454be2f984a767d834392`

## Visibility boundary

`trial-prompt-input.json`だけをworkerへ渡す。`private/case-data.json`、`private/seed.patch`、reference postimage、oracle、grader contractはmodel-invisibleとし、fixture準備、quality rating、qualificationにだけ使う。

## Fixture

`seed.patch`は次の2点を壊す。

1. primary refreshから`target_date`と`us_market_date`を除去する。
2. domain updaterのmarket end-date解決を除去し、unbounded fetchへ戻す。

focused testは変更しない。patch適用前にtarget commit / treeと2 preimageを照合し、適用後に2 post-seed blobとSHA-256を照合する。その後、固定author、timestamp、messageでseed commitを作り、Agent開始時のtracked worktreeをcleanにする。

## Fixture qualification

2026-07-15にmodel invocationなしで次を確認した。

| 状態 | command | 結果 |
| --- | --- | --- |
| seeded | `.venv/bin/python -m pytest tests/unit/test_collection_history_updater.py tests/unit/test_v4_engine.py -q` | exit `1`、`10 failed / 14 passed` |
| reference postimage | 同じfocused gate | exit `0`、`24 passed` |
| reference postimage | `bash scripts/dev/main_verify.sh` | exit `0`、`326 passed / 3 skipped` |

full gateはN=10 null calibrationと同じknown-good venvをcopy materializationして確認した。別venvで発生した`test_bootstrap_works_with_minimal_path`の1 failureはenvironment差としてcase結果へ含めていない。

fixtureとreference behaviorはqualifiedである。ただしA / B prompt実行、quality rating、KPI comparisonは未実施であり、case statusは`fixture_qualified_prompt_not_evaluated`とする。

## Fixture preparation

```bash
python3 scripts/prepare_evaluation_set.py \
  --case evaluations/cases/TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1 \
  --source-repo /Users/kenn/repos/THE-CAPTION \
  --output /tmp/the-caption-tc-f02-r1-set
```

outputはtarget identity、preimage、patch、post-seed identity、seed commit、clean tracked worktreeを検証する。実行時のknown-good `.venv`はrun capsuleのmodel-invisible runtime materializationとしてA / Bで同一に固定し、case bundleへcommitしない。

このartifactが存在しても、promptが評価済み、candidateが改善済み、採用済み、本体反映済みであることを意味しない。
