# TC-F01 r2 identical bundle pilot

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- purpose: `r1`で見つかった開始状態不整合を解消し、bit-identicalなprompt bundle A / Bでcase executionをqualificationする
- repetition: `N=1`
- case qualification: `execution_qualified_external_failure_rerun_pending`
- prompt evaluation status: `not_evaluated`
- official prompt comparisonへの使用: 不可

`r2`はcase task、seed patch、oracle、grader contractを`r1`から変更せず、seedをdeterministic commitへ固定してAgent開始時のworking treeをcleanにしたrevisionである。

## Fixed input

### Evaluation set

- set ID: `tc-f01-domain-duplicate-asset-key-r2`
- case ID: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY`
- case revision: `r2`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- seeded fixture commit: `4e6910d08f49b0825beff08837178f5106cbd0f2`
- seeded fixture tree: `f3dfbad104884a27251573ce7d8c58b046a81661`
- condition commit: `da76d2e1181cdb04b6f3aedc0451077c8466c64b`
- condition tree: `f3dfbad104884a27251573ce7d8c58b046a81661`
- model-visible task SHA-256: `08e35096387b648a715732af219eb947c08ab4afbea2192dec97a65b3f18b0b9`

### Prompt set A

- prompt identity: `the-caption-3ce91a4-current-r1`
- artifact role: `baseline`
- file entries: `17`
- bundle SHA-256: `94e6fedf856952cbeb29c6cb631d9917adc8fddb5ac3846dc5ca2a06d83a885c`

### Prompt set B

- prompt identity: `the-caption-3ce91a4-current-copy-r1`
- artifact role: `candidate`
- content relation: `bit_identical_copy`
- file entries: `17`
- bundle SHA-256: `94e6fedf856952cbeb29c6cb631d9917adc8fddb5ac3846dc5ca2a06d83a885c`

A / Bのmanifest file entries、bundle SHA-256、condition commit、condition treeは一致する。

## Agent environment

- Codex CLI: `codex-cli 0.144.0`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- sandbox: `workspace-write`
- approval policy: `never`
- session: `ephemeral`
- user config: ignored
- exec rules: ignored
- `multi_agent`: enabled
- `agents.max_threads`: `4`
- memories: disabled
- Python: `3.14.5`
- pytest: `9.0.2`
- `.venv/pyvenv.cfg` SHA-256: `68d300fe4c312d93fa3c70f3fa21429f8b11959151f028cb5c95481303af9490`
- `requirements.txt` SHA-256: `ea5bf43d60b6c407f8946388186c4fd759ab46e8e1e6098f6df0fb79771dd355`
- `requirements-dev.txt` SHA-256: `07860bf03fdb0d50ba8693a976c8a6d1dc70408f5da9986b130e5521fc8723b8`

known-good `.venv`はLayer 1 freeze前にfixture内へ実体copyした。各Layer 2 workspaceは計時開始前に同じself-contained fixtureから作られる。外部venvへのsymlinkは使用しない。

## Qualification attempts excluded from comparison

final cycleの前に、次のenvironment qualification attemptを行った。どちらもAだけを実行し、A / Bが揃わないためLayer 4へ使用していない。

| attempt | environment | terminal outcome | exclusion reason |
| --- | --- | --- | --- |
| 1 | `.venv`なし | focused gate開始不能 | required environment不足 |
| 2 | `/Users/kenn/repos/THE-CAPTION/.venv`へのsymlink | focused 23 passed、full 1 failed / 325 passed / 3 skipped | checkout外venv pathにより`test_bootstrap_works_with_minimal_path`が失敗 |

environment failureをpromptまたはcase behaviorの失敗へ混ぜず、final cycleとは別attemptとして扱う。

## Final cycle result

| condition | quality score | total tokens | elapsed seconds | focused gate | full gate |
| --- | ---: | ---: | ---: | --- | --- |
| A | 100 | 710,797 | 395.840 | 23 passed | 326 passed, 3 skipped |
| B | 100 | 468,884 | 313.325 | 23 passed | 326 passed, 3 skipped |

両runで次を確認した。

- `src/domain/market_units_snapshot.py`へ既存の重複検証1行だけを復元した
- final Git blobはreference postimage `e3af06ab26c74a98815a53de7ec0661af82e3e18`と一致した
- focused test fileは開始時blob `a854b1e85795418c372a26c72a2f4a9a3e24d6a2`から変更されていない
- 許可外driftなし
- 監査の停止指摘0件
- レビューの重大指摘0件
- commit、push、merge、deployなし

Layer 4は実行時点で`winner: b`を出力したが、事後のstderr確認によりAで`collab spawn failed: no thread with id:`が発生していたことを確認した。これはpromptまたはtask behaviorではなくCodex collaborationの親thread登録失敗である。Aは比較対象から除外し、このLayer 4出力を有効なwinnerとして扱わない。Bは保持し、同じA slotの再実施を待つ。

## Qualification judgement

`r2`は、clean preflight、壊れたfixture、実装修正、focused / full gate、scope drift、監査、レビューまで両conditionで完走した。この範囲でcase execution経路をqualifiedとする。

一方、Aの初回実装SA起動は、親threadをcollaboration registryから解決できず失敗して再送されていた。この外部要因によりAのtokenと時間は比較用KPIとして無効であり、bit-identical bundleの実行ばらつきとしても確定できない。performance calibrationはAの再実施まで未完了である。

また、Layer 3のscoreは同一のmachine evidenceから同じ4を記録したが、独立したblind quality raterによるqualificationではない。blind rater入力境界の未解決事項は維持する。

以上から、case qualificationを`execution_qualified_external_failure_rerun_pending`とする。prompt set A / Bを評価済みまたはcandidate改善済みとは扱わない。

## Evidence handling

一時cycle、workspace、Codex JSONL、stdout / stderr、copied `.venv`はlocal temporary evidenceとして保持し、repositoryへcommitしない。本recordにはidentity、集計値、terminal behavior、qualification判断、除外理由だけを記録する。
