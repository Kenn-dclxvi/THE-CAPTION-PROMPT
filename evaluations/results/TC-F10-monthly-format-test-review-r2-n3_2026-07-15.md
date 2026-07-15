# TC-F10 monthly format-test review r2 N=3 comparison

## Status

- run date: `2026-07-15`（Asia/Tokyo）
- valid run window: `2026-07-15T18:20:08+09:00`から`2026-07-15T18:21:21+09:00`
- set ID: `tc-f10-monthly-format-test-review-r2`
- case: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW r2`
- repetition: `N=3`
- execution: `global_queue`、既定の外側並列上限`M=24`、requested slots `6`
- valid runs: `6 / 6`
- excluded attempts: `0`
- comparison status: `observed_n3`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本比較は、固定commitの1行差分を変更なしでreviewし、severity、location、直接根拠、user-visible impactを持つfindingを返すcontrol pathを、A / Bで各3回観測した結果である。単一case、`N=3`の観測範囲を超えてprompt性能を一般化しない。

## r1 execution blocker and r2 binding

`r1`はreview対象を`HEAD^..HEAD`としたが、adapterがseeded fixtureの上へprompt condition commitを追加するため、全6 runがseed diffを参照できず停止した。これはprompt比較へ使用していない。

`r2`はtarget、seed、expected finding、operation boundaryを変更せず、review対象だけを固定seed commit `a53601614b41f52633f1d75e77c72861a0f0f1c8`へbindした。r2の全workspaceでprompt condition commitの直接parentが固定seed commitであることをrepository evidenceから確認した。

## Prompt sets and fixed environment

| condition | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| A | `the-caption-3ce91a4-current-r2` | `63225d2d7430bc20ac6d126a0070385461136ca82dad8a0744e2127a3668e48d` |
| B | `the-caption-9b3a96a-revision-2-r1` | `f5ea64185324da9e36c8e7e1a38956d0ab5893f4ef29b5a866d3c89234aac865` |

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `a53601614b41f52633f1d75e77c72861a0f0f1c8`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- runtime Python: `3.14.5`
- runtime identity SHA-256: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73`

## Expected finding and repository integrity

固定diffは`src/app/entrypoints/monthly_main.py:25`の`format_test=args.format_test`を`format_test=args.force`へ変更する。直接根拠上、`-t / --format-test`がengineへ渡らず通常処理へ進み得る一方、`-F / --force`がformat-test early-return pathを起動する。

全6 workspaceは開始・終了ともcleanで、file変更、test、application実行、dependency操作、Git write、network、外部操作はなかった。

## Quality rating

Aの3 runとB repetition 1は、期待するdefectを`major` findingとしてchanged line、直接根拠、両CLI flagへのimpact付きで1件返したためscore `4`とした。

B repetition 2 / 3は、実際には`HEAD^`が固定seed commitと一致していたが、開始identity不一致と誤認してreviewを開始せず、findingを返さなかった。zero driftと禁止operation回避だけは満たしたためscore `1`とした。

採点は保存evidenceに基づくが、独立したblind quality raterによるものではなく、raterがcondition identityを知らない入力境界は未実装である。

## Layer 4 comparison

値は各conditionの3反復median、差分は固定schemaどおり`B - A`である。

| KPI | A | B | `B - A` |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 25.000 | -75.000 |
| `total_tokens` | 78,206 | 48,434 | -29,772 |
| `elapsed_seconds` | 63.755 | 48.487 | -15.268 |

反復別の値は次のとおりである。

| condition | repetition | score | `total_tokens` | `elapsed_seconds` | outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| A | 1 | 4 | 78,206 | 47.511 | expected finding 1件 |
| A | 2 | 4 | 79,474 | 63.755 | expected finding 1件 |
| A | 3 | 4 | 76,354 | 72.652 | expected finding 1件 |
| B | 1 | 4 | 82,696 | 61.857 | expected finding 1件 |
| B | 2 | 1 | 48,434 | 35.116 | identity誤認によるreview未実施 |
| B | 3 | 1 | 48,191 | 48.487 | identity誤認によるreview未実施 |

B repetition 2 / 3のtokenと時間は、reviewを完了した値ではなく早期停止を含む。KPIへ優先順位や閾値を置かず、数値をwinner、改善・悪化、採用可否へ変換しない。

## Observed response parsing variation

B repetition 2 / 3の開始確認commandは、`pwd`、branch、`HEAD`、status、`HEAD^`を一度に実行した。detached branchとclean statusが空出力だったため、保存された出力は実質的にworkspace path、prompt condition commit、固定seed commitの3行だった。agent responseは後ろ2つを`HEAD`と`HEAD^`へ逆に対応付け、成立しているgateをfailedとした。

Aの3 runは同種の複合command出力を正しく解釈し、B repetition 1は各identity commandを分けて実行してreviewを完了した。このcase、`N=3`ではresponse parsing pathのvariationとして記録し、他caseへ一般化しない。

## Parallel execution observation

- runner wall time: `72.895`秒
- 6 runのexecution時間合計: `329.379`秒
- OS samples: `16`
- load average 1分値 max: `4.220`
- memory free min: `68%`
- swap used max: `0 MiB`
- evaluation process count max: `6`
- Codex process count max: `10`
- disk free min: `33.156 GiB`

local resource pressure、workspace衝突、controller error、external failureは観測されなかった。

## Evidence handling

r1 blocker evidence:

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/f10-monthly-review-r1-n3-m24-20260715`

r2 comparison evidence:

`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/f10-monthly-review-r2-n3-m24-20260715`

raw evidenceはrepositoryへcommitしない。
