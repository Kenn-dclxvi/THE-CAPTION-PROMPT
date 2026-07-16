# Candidate17 typed boundary evidence F10 N=90

## 目的と範囲

Candidate17のF10 monthly format-test reviewで残った開始identity誤認2 / 90に対し、prompt、TaskSpec、case、fixtureを変更せず、実行adapterの[`typed boundary evidence`](../../docs/typed-boundary-evidence.md)だけを追加して再発を確認した。

これはF10限定のpartial-set diagnostic evidenceである。expanded 12 caseのLayer 4 resultへ登録せず、採用、release、THE-CAPTION本体反映は判断・実施しない。

## 固定条件

- profile: `candidate17-operation-qualified-evidence-f10-boundary-v1-global-m5-n5-r1`
- prompt set: `the-caption-9b3a96a-operation-qualified-evidence-r1`
- bundle SHA-256: `4c492dbb7b7bdf62d1602c6e6b1235cbce5ba2116f763cc64ae876527a740d4a`
- case: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r2`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- permission: `workspace-write` / `never`
- token accounting: `all_agents/v1`
- execution: 18 batch、各`N=5`、batch内`M=5`
- adapter / evidence: `the-caption-prompt.codex-adapter/v4` / `the-caption-prompt.boundary-evidence/v1`

## Result

| 観測 | 結果 |
| --- | ---: |
| valid / rateable run | 90 / 90 |
| score `4` | 90 |
| score `1` | 0 |
| typed observation `passed` | 450 / 450 |
| 開始identityのraw再観測 | 0 / 90 |
| unexpected changed path | 0 |
| external failure / excluded attempt | 0 / 0 |
| all-agent `total_tokens`合計 | 6,603,525 |
| all-agent `total_tokens`中央値 | 68,354 |
| `elapsed_seconds`中央値 | 41.373 |

全runがexpected major findingを`src/app/entrypoints/monthly_main.py:25`へ結び付け、`args.format_test`が無視され`args.force`がformat-test pathを起動するbehavior impactを記録した。全runはzero driftで終了した。

## 既存Candidate17観測との関係

| execution boundary | score分布 | token合計 | token中央値 |
| --- | --- | ---: | ---: |
| Agentがraw observationを対応付ける既存条件 | `4`: 88、`1`: 2 | 8,526,473 | 88,727.5 |
| adapter typed boundary v1 | `4`: 90 | 6,603,525 | 68,354.0 |

execution compatibilityが異なるため、この表は同一result comparisonではなく診断上の併記である。typed boundary側では開始identity誤認が観測90回中0件になり、token観測値も`-1,922,948`だったが、F10以外への一般化や自動的な優劣判定は行わない。

## 結論

- promptへ境界記述を追加し続けず、read-only観測、predicate、statusの対応をadapterで型付けした。
- C17で残った低頻度の`HEAD` / `HEAD^`対応誤認は、同じF10を90回実行した範囲では再発しなかった。
- interfaceはF10固有commandを受け取らず、adapter管理のsource registryと1 observation / 1 predicateに限定した。
- expanded 12 case回帰、prompt採用、release、runtime projectionは未実施である。

## Raw evidence

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate17-typed-boundary-f10-n5-b18-20260717`

18 batchはすべてseal済みで、campaign summary、quality audit、typed evidence、archive receiptを保持する。raw evidence、session情報、一時workspaceはrepositoryへcommitしない。
