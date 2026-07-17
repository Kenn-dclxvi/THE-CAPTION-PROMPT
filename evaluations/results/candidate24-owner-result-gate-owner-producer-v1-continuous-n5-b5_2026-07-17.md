# Candidate24 prompt-only owner result gate continuous N=5 B=5

## Status

- run date: `2026-07-17`（Asia/Tokyo）
- campaign window: `2026-07-17T16:45:27+09:00`から`2026-07-17T17:28:14+09:00`
- profile: `candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5-r1`
- Evaluation set: `the-caption-revision-2-expanded12-r1` / `r1`
- execution: expanded 12 case、各batch `N=5`、`global_queue`、`M=24`、連続5 batch
- quality rating: `owner-producer-quality-v1`
- valid runs: `300 / 300`
- excluded attempts: `1`（`codex_model_at_capacity`。同一slotを再実行してvalid runへ置換）
- prompt evaluation status: `observed_n5_b5`
- adoption / release / THE-CAPTION本体反映: 未判断、未実施

Candidate24の最初のexpanded 12-case `N=5`に続き、同じprompt identity、Evaluation set、fixture、TaskSpec、model、Agent環境、permission、executor parameter、rating revisionを固定したまま、60 runのappend-only resultを5つ連続で保存した。5 resultは独立した一次結果として保持し、300 runを単一resultへ読み替えていない。

## Prompt set and fixed environment

- Candidate24: `the-caption-3ce91a4-control-free-owner-result-gate-r1` / `8f3793…9488b`
- direct source: `the-caption-3ce91a4-control-free-operation-boundary-r1`（Candidate23）
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`
- compatibility key: `46787dae7e03a4f182915b5eff62c17f40673d8d08ae86fdaf2cfb88284a72c8`

## Batch results

| batch | result ID | `quality_score`中央値 | `total_tokens`中央値 | `elapsed_seconds`中央値 | score 4 / 3 / 1 | excluded attempts |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| B1 | `f52c9bc67d414ee29448745138f42334` | 100.000 | 4,789,686 | 1,656.917秒 | 59 / 1 / 0 | 0 |
| B2 | `7a3d8d602cbb4bebb272a7df1dca2d01` | 100.000 | 4,976,013 | 1,709.149秒 | 60 / 0 / 0 | 0 |
| B3 | `e40bd570ddfe452d85897322b6721061` | 100.000 | 5,030,048 | 1,679.771秒 | 60 / 0 / 0 | 0 |
| B4 | `b71086874a4e4e47bf1b97ae0f02eaa2` | 100.000 | 4,789,839 | 1,764.084秒 | 58 / 0 / 2 | 0 |
| B5 | `6426e06836fc46f69a96bb428cb1bb52` | 100.000 | 5,147,190 | 1,693.691秒 | 57 / 1 / 2 | 1 |
| 5 batch中央値 | — | 100.000 | 4,976,013 | 1,693.691秒 | 294 / 2 / 4（合計） | 1（合計） |

最終行のKPIは5つの保存済みresult中央値に対する記述的な中央値であり、新しいLayer 4 resultではない。campaignのvalid runに記録されたall-agent token合計は`122,767,531`だった。5 batchともKPI中央値の`quality_score`は100だが、全run分布にはscore `3`が2件、score `1`が4件ある。

## Case distribution

| case | score 4 | score 3 | score 1 |
| --- | ---: | ---: | ---: |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 24 | 1 | 0 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 24 | 1 | 0 |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 21 | 0 | 4 |
| その他9 case | 225 | 0 | 0 |
| 合計 | 294 | 2 | 4 |

owner固定criterionを持つ275 runのうち、admissible producer resultは273件、欠落は2件だった。F10 monthlyは25 / 25で実child identityとchild final resultが成立したが、4件はreview成果を返さずscore `1`となった。

## Score 3以下

| batch / iteration | case | score | 直接原因 |
| --- | --- | ---: | --- |
| B1 / i4 | `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 3 | 所定変更とvalidationは満たしたが、申告した`/root/criterion_owner`に対応する実child resultが保存証跡に存在しない |
| B4 / i4 | `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 1 | childが開始identityを逆に解釈してreviewを開始せず、major findingとbehavior impactを返さない |
| B4 / i5 | `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 1 | 同上 |
| B5 / i2 | `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 1 | 同上 |
| B5 / i4 | `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 3 | 所定変更、lint、build、cleanupは満たしたが、申告した`/root/audit_key_owner`に対応する実child resultが保存証跡に存在しない |
| B5 / i4 | `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 1 | 同上 |

F07 / F04の2件は成果未達ではなく、promptが要求するowner producer evidenceの欠落である。root responseは別execution identityのownerがPASSしたと記載したが、runtime evidenceにはそのchild sessionがなく、prompt内のAND predicateを実行時に守れなかった。

F10 monthlyの4件では、root自身のmachine observationは`HEAD=1de2c3d…`、`HEAD^=a536016…`でTaskSpecと一致していた。一方、independent response checkのchild final resultは`HEAD=a536016…`、`HEAD^=1de2c3d…`または後者だけを根拠として開始identity不一致と判断した。rootはowner固定criterionを自己判断で上書きせず、fail-closedで`review_findings: unavailable`を返した。この停止処理自体はCandidate24の制御どおりだが、要求されたcorrectness reviewは未実施のためscore `1`である。

## Observed boundary

Candidate24のowner result gateは「実childが存在し、そのchildがfinal resultを返したか」を高率で制御したが、「child resultがrootと同じmachine stateを前提にしているか」は制御していない。F10 monthlyではowner producer成立が25 / 25でもqualityは21 / 25に留まった。したがって、child lifecycleのidentity一致だけでは、promptが要求する状態とexecutorが各identityで解釈した状態の一致にはならない。

次のprompt-only境界は、owner finalの自由記述を受け取るだけでなく、開始状態を`workspace identity + command + observed value + producer identity`のtupleとしてrootからchildへ渡し、childが同じ値をechoしてcriterionへbindできた場合だけreviewを開始する制御である。ただし、これもruntime強制ではなくprompt遵守の観測に留まる。

## Audit and storage notes

batch 1の採点時、campaign専用audit helperがroot command eventだけを検索し、独立owner側で実行したrequired validationを2件検出できなかった。sealed owner resultを確認するとF07のstatic validation一式とF03のfocused / full testが実行identity付きで存在したため、owner producer eligibleなchild実行も採点対象にするようhelperを補正し、この2件はscore `4`とした。raw evidenceやscore `3`以下を成功へ読み替えていない。

- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate24-control-free-owner-result-gate-owner-producer-v1-continuous-n5-b5-20260717`
- registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/`

raw evidence、session情報、一時workspaceはrepositoryへcommitしない。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。300 runの範囲外へ完全保証を一般化しない。
