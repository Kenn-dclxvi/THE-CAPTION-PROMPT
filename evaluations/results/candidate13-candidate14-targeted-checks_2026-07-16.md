# Candidate13 / Candidate14 targeted checks

## Purpose and boundary

expanded 12 caseのN=5を実行する前に、変更した境界へ直接到達するcaseだけを確認した。これはpartial setの診断evidenceであり、Layer 4 resultへ登録せず、Baseline等とのKPI comparisonへ混ぜない。

固定した共通条件はtarget commit / tree `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`、model `gpt-5.6-sol`、reasoning effort `high`、Codex CLI `0.144.0`、memories disabled、`agents.max_threads=4`、all-agent token accounting `v1`である。

## Candidate13 review route entry

- identity: `the-caption-9b3a96a-review-route-entry-boundary-r1`
- bundle SHA-256: `0732438a7f6b49600ae750364a15d54dbd7489b1671a8d2842a1e5fe74fb8e73`
- direct source: Candidate12
- changed target: `prompts/review.md`だけ
- target cases: F03 atomic cleanup、F04 web audit column
- repetition: 各`N=3`、合計6 run
- Layer 2: valid `6 / 6`、excluded attempt `0`
- runner wall time: `268.976`秒

review stageへ到達した5 runは、audit output identityを要求せずreview-only workerを起動し、5 / 5で独立reviewを完了した。F04 iteration 2の1 runは`npm` unavailableかつ`environment_recovery_max=0`のためmachine gateで停止し、review stageへ到達しなかった。これはrole接続の失敗として数えていない。

この観測によりCandidate13の構築と対象確認は完了したが、expanded result、採用、release判断を意味しない。

## Candidate14 validation authority

- identity: `the-caption-9b3a96a-validation-authority-precedence-r1`
- bundle SHA-256: `31417f770dfd1f7072ca9abda10cb3b6e1a27c2a5a898284b40f536aa4a9713f`
- direct source: Candidate13
- changed target: `AGENTS.md`だけ
- target case: F06 empty snapshot contract
- repetition: `N=3`
- Layer 2: valid `3 / 3`、excluded attempt `0`
- runner wall time: `210.745`秒

3 runすべてでTaskSpecが明示した対象test commandとtests全体commandを実行し、対象`23 passed`、全体`326 passed, 3 skipped`、独立contract audit停止0まで完了した。`bash scripts/dev/main_verify.sh`の追加または置換は3 runとも0回だった。

この確認を受け、Candidate14だけをexpanded 12 caseのN=5へ進めた。

## Raw evidence

- Candidate13: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate13-review-route-entry-f03-f04-n3-20260716-v3-r1`
- Candidate14: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate14-validation-authority-f06-n3-20260716-v3-r1`

raw evidenceはrepositoryへcommitしない。
