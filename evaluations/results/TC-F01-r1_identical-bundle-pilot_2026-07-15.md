# TC-F01 r1 identical bundle pilot

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- purpose: bit-identicalなprompt bundle A / Bを使い、最初のevaluation caseと実行経路の妥当性を確認する
- repetition: `N=1`
- pilot conclusion: `case_revision_not_qualified`
- prompt evaluation status: `not_evaluated`
- official comparisonへの使用: 不可

本pilotは単一case、単一反復であり、prompt setの性能を一般化しない。開始状態契約の不整合により両runがtaskへ着手しなかったため、prompt qualityの比較結果として扱わない。

## Fixed input

### Evaluation set

- set ID: `tc-f01-domain-duplicate-asset-key-r1`
- case ID: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY`
- case revision: `r1`
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
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

A / Bのmanifest file entriesとbundle SHA-256は一致する。prompt identityとartifact roleだけが異なる。

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

両runで、bundle適用後のcondition commitは`5189456f72a1b5f0395fcf53c84764c57677b1f6`、condition treeは`88eecfa29f7016b4d77061d3aabe3e7d176fea9b`となった。したがってAgent開始時のtracked treeも一致している。

## Result

| condition | quality score | total tokens | elapsed seconds | terminal behavior |
| --- | ---: | ---: | ---: | --- |
| A | 0 | 103,360 | 33.294 | seed対象を予期しない既存driftと判断し、編集とvalidationを行わず停止 |
| B | 0 | 203,571 | 99.286 | seed対象を予期しない既存driftと判断し、編集とvalidationを行わず停止 |

Layer 4の機械判定は`winner: a`となった。qualityが同点のため、tokenが少ないAが選ばれた。このwinnerはprompt差を示さない。A / Bのbundle内容はbit-identicalであり、両runともtaskへ着手していない。

## Qualification finding

fixture preparationは、`seed.patch`を適用した`src/domain/market_units_snapshot.py`を未commit変更としてAgentへ渡す。一方、model-visible TaskSpecは、開始時点に予期しないdriftがあれば変更せず停止するよう要求する。TaskSpecはseed済みのdirty pathを既知の開始状態として区別していない。

実際に両runは次を開始時driftとして検出した。

```text
 M src/domain/market_units_snapshot.py
```

この停止はprompt set A / Bの差ではなく、case fixtureとmodel-visible TaskSpecの不整合による。両conditionで同じ停止が再現したため、`TC-F01 r1`は現状のまま正式評価へ使用できない。

## Null comparison finding

bit-identicalなbundleでも、単一反復のtokenと時間は一致しなかった。現行Layer 4はKPIの完全一致だけを`tie`とし、quality同点時はtoken、時間の順に必ず比較する。このため、null比較でも実行ばらつきがあればAまたはBがwinnerになる。

本pilotの`winner: a`を改善、悪化、baseline優位の根拠として使用しない。評価setの妥当性を確認する次のattemptでは、開始状態契約を修正した新しいcase revisionを使い、A / Bで同じ`1..N`を揃える必要がある。

## Evidence handling

一時cycle、workspace、Codex JSONL、stdout / stderrはlocal temporary evidenceとして保持し、repositoryへcommitしない。本recordには再現に必要なidentity、集計値、terminal behavior、除外理由だけを記録する。
