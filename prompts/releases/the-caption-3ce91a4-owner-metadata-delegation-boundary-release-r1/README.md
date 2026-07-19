# Candidate41 release preparation

## 結論

Candidate41の19 path full bundleを、内容変更なしで唯一のrelease候補として固定した。

release準備状態は`prepared_for_decision`、承認状態は`pending`である。

既存のCandidate34 release候補は`cancelled`とした。これはCandidate34の不採用またはartifact削除を意味しない。

このartifactの存在は、採用承認、THE-CAPTION本体への反映、runtime有効化を意味しない。

## Identity

- release identity: `the-caption-3ce91a4-owner-metadata-delegation-boundary-release-r1`
- source candidate: `the-caption-3ce91a4-owner-metadata-delegation-boundary-r1`
- bundle SHA-256: `048f6693ae588feb0cd27f13f08637adb6b0cc376d94a4a4d4072662b1b747d7`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- content relation: `release_snapshot_of_candidate`
- changed targets from Candidate41: none

## Evaluation evidence

- rating v9 targeted result ID: `37fe235e451e46b688d14ca0c52afbd9`
- targeted: F05 / F10各N=5、10 / 10がscore `4`、全run root-only
- rating v9 expanded result ID: `f9f8b177031e401093ee60717d5e602e`
- expanded: 12 case × N=5、60 / 60 valid、score `4 = 60 / 60`、全run root-only
- Candidate35比`quality_score`中央値差: `0.000`
- Candidate35比all-agent `total_tokens`中央値差: `-1,704,754`（`-37.34%`）
- Candidate35比60 run token合計差: `-7,347,269`（Candidate35がC41より`50.02%`多い）
- Candidate35比`elapsed_seconds`中央値差: `-668.926`秒（`-36.33%`）
- continuous B18: 18 / 18 result、1,080 / 1,080 validかつrateable、score `4 / 3 = 1,078 / 2`
- B18の18 result中央値の中央値: `quality_score 100.000`、all-agent `total_tokens 2,856,386`、`elapsed_seconds 1,100.052`秒

Candidate35との数値差は、同じv9条件で実行したexpanded N=5の互換比較である。保存済みCandidate35 B18はrating revisionが異なるため、C41 B18との互換比較へ混ぜない。

## Unresolved risks

- B18のF10 monthly reviewで、主要findingは正しいがlocationが実変更行`monthly_main.py:25`と一致しないscore `3`を2 / 90件観測した。
- 1,079 / 1,080 runはroot-onlyだったが、F02の1 runではTaskSpecに明示されない2 childを起動した。root-only経路は完全な不変条件ではない。
- B18の観測を範囲外へ一般化できない。
- exact coordinateの決定的保証には、prompt規則ではなく、実運用と評価で共通する構造化evidence interfaceの別要件が残る。
- Candidate37のcase固有`LOCATION`規則はC41へ統合していない。

## Approval state

- release preparation: `complete`
- release candidate status: `prepared_for_decision`
- adoption approval: `pending`
- runtime projection: `not_authorized`
- THE-CAPTIONへのwrite / push / PR / merge: `not_authorized`

## Evidence

- continuous result: [`Candidate41 continuous B18`](../../../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-continuous-n5-b18_2026-07-19.md)
- expanded comparison: [`Baseline / ControlFreeRepository / Candidate35 / Candidate41 rating v9 N=5`](../../../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md)
- expanded result: [`Candidate41 expanded N=5`](../../../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-expanded12-n5_2026-07-19.md)
- targeted result: [`Candidate41 targeted N=5`](../../../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-targeted2-n5_2026-07-19.md)
- candidate manifest: [`Candidate41 manifest`](../../candidates/the-caption-3ce91a4-owner-metadata-delegation-boundary-r1/manifest.json)
