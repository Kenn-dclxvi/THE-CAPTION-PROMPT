# Candidate34 release preparation

## 結論

Candidate34の19 path full bundleを、内容変更なしでrelease判断可能な単位へ固定した。

release準備状態は`prepared_for_decision`、承認状態は`pending`である。

このartifactの存在は、採用承認、THE-CAPTION本体への反映、runtime有効化を意味しない。

## Identity

- release identity: `the-caption-3ce91a4-owner-result-state-separation-release-r1`
- source candidate: `the-caption-3ce91a4-owner-result-state-separation-r1`
- bundle SHA-256: `d13b4242192be37d08814f862de19502982ebebe0ab30fe497d031a983dc2106`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- content relation: `release_snapshot_of_candidate`
- changed targets from Candidate34: none

## Evaluation evidence

- rating v7 expanded result ID: `f8316de4af124128a96173abfa22e677`
- rating v7 expanded: 12 case × N=5、60 / 60 valid、score `4 = 60 / 60`
- C31比`quality_score`中央値差: `0.000`
- C31比all-agent `total_tokens`中央値差: `-625,986`（`-15.98%`）
- C31比60 run token合計差: `-2,779,489`（`-14.39%`）
- C31比`elapsed_seconds`中央値差: `-18.304`秒（`-1.23%`）

rating v5のtargeted result `018498dd62a94f27be77008841c11c07`とexpanded result `2980e99092744e98a23945d02eeb04cf`、rating v6のexpanded result `9a414feb95744ed4970c48a859cf7ec7`は履歴として保持する。既存resultは再採点していない。

## False-negative boundary

rating v5でF05 clarifyの日本語「フォールバック」を英字`fallback` markerが認識しなかった偽陰性は、response evidenceだけを更新したrating v6で修正した。

同じrating v6へ揃えたC31とC34のF05 clarifyは、それぞれ5 / 5がscore `4`だった。ただし、今回の10応答はすべて英字`fallback`を使った。日本語「フォールバック」の受理は固定回帰試験で確認し、N5の自然観測とは分ける。

rating v5 resultはappend-only履歴として変更していない。このrelease artifactのprompt内容も変更していない。

rating v6で残ったscore `3`はF07 dependencyの1件である。実ログではrequired validation commandが成功していたが、command evidence v3がcustom wrapperのmarkdown-heading形式を固定commandへbindできなかったcollector偽陰性だった。

この形式はcommand evidence v4と`owner-producer-quality-v7`で修正した。実rollout replayで不足commandの取得を確認したうえで、C31とC34を同じv7条件で新規実行した。両方とも60 / 60がscore `4`であり、collector偽陰性は再現しなかった。v6 resultは再採点していない。

## Unresolved risks

- Candidate33比では`total_tokens`中央値が`+263,503`、root token合計が`+1,302,819`だった。
- N=5の観測を範囲外へ一般化できない。
- elapsed差は反復間で符号が揺れ、安定した短縮とは判断できない。
- v6 N5のF05応答はすべて英字`fallback`であり、日本語同義語の受理は固定回帰試験の確認である。
- command evidence v4で今回扱った形式以外の未知のwrapper形式まで完全に収集できるとは保証しない。

## Approval state

- release preparation: `complete`
- adoption approval: `pending`
- runtime projection: `not_authorized`
- THE-CAPTIONへのwrite / push / PR / merge: `not_authorized`

## Evidence

- current result: [`Candidate31 / Candidate34 rating v7 N=5 comparison`](../../../evaluations/results/candidate31-candidate34-owner-producer-v7-expanded12-global-m24-n5_2026-07-18.md)
- historical rating v6 result: [`Candidate31 / Candidate34 rating v6 N=5 comparison`](../../../evaluations/results/candidate31-candidate34-owner-producer-v6-expanded12-global-m24-n5_2026-07-18.md)
- result record: [`Candidate34 targeted / expanded N=5`](../../../evaluations/results/candidate34-owner-result-state-separation-owner-producer-v5-targeted2-expanded12-n5_2026-07-18.md)
- candidate manifest: [`Candidate34 manifest`](../../candidates/the-caption-3ce91a4-owner-result-state-separation-r1/manifest.json)
- C31 rating v7 comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate31-vs-candidate34-owner-producer-v7-n5.json`
- C33 comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/comparisons/candidate33-vs-candidate34-owner-producer-v5-n5.json`
