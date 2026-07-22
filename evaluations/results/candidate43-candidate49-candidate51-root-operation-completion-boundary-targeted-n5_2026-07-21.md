# Candidate43 / Candidate49 / Candidate51 root operation completion境界 対象試験 N=5

## 互換性訂正

登録後のroot rollout確認で、Candidate43 / Candidate49とCandidate51のmodel-visible skill / plugin catalogが一致していないことを確認した。registry上のcompatibility keyは同一だが、現行`runtime_identity_sha256`はこの差を検出していない。

このため、本書のC43 / C49 / C51 token、model step、tool call比較はdiagnostic-onlyとし、prompt identityだけが異なる互換比較として採用しない。Candidate51の単独result、score、実行traceはappend-onlyのまま保持する。増加要素は[`F10 token増加分析`](candidate43-candidate51-f10-token-increase-analysis_2026-07-21.md)に記録する。

この不一致を解消した[`C43 / C51 capability catalog固定再試験`](candidate43-candidate51-catalog-fixed-targeted-n5_2026-07-21.md)を別resultとして追加した。C49は再実行していない。固定再試験をC43 / C51の現行比較証跡とし、本書の数値を置換しない。

## 結論

Candidate51は、Candidate49で明示委譲時だけへ狭まったproducer bindingと全predicate completionをroot-only operationへ復元した。tool batch、read順序、`INDEPENDENCE`は指定していない。

F05 / F10各`N=5`は10 / 10がscore `4`、root-only、protocol違反0、zero driftだった。Candidate51の10 run token合計は`1,070,987`で、Candidate49の`1,309,324`から`-238,337`、`-18.20%`となった。

Candidate43比では10 run合計が`1,050,768 -> 1,070,987`、`+20,219`、`+1.92%`だった。F05は`-8.13%`、F10は`+6.91%`で相殺されているため、合計値だけで完全復元とは判断しない。

F10のmodel stepはCandidate43 / Candidate49 / Candidate51で`37 / 52 / 38`、input tokenは`689,536 / 945,707 / 737,406`だった。Candidate51はC49で増えた逐次分割をC43とほぼ同じ分布へ戻した。C43の`12 / 5 / 12 / 4 / 4`に対し、C51は`12 / 4 / 4 / 12 / 6`である。

数値上はC49で増えた逐次分割がC43とほぼ同じ分布へ戻った。ただしmodel-visible Agent環境が一致しないため、root operation completionのprompt効果として確定しない。F10の`+6.91%`も`INDEPENDENCE`不足の証拠にしない。

## Prompt差分

- Candidate43: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate49: `the-caption-3ce91a4-explicit-delegation-control-boundary-r1`
- Candidate51: `the-caption-3ce91a4-root-operation-completion-boundary-r1`
- Candidate51 bundle SHA-256: `62d8fe1e06a406f8feda2ebc634ea6d2f3e100aea7d3ba504541c78f7be07c48`
- Candidate51 source: Candidate49
- changed target: root `AGENTS.md`だけ
- 未変更target: 18 / 18がCandidate49とbit identity一致
- root prompt: C43 `3,980 bytes / 199 words`、C49 `2,423 / 120`、C51 `2,473 / 118`

Candidate51はCandidate49の`DELEGATION`と`COMPLETION`だけを変更した。明示委譲がなければrootをproducerとし、開始済みoperationは全predicateにbind済みproducerのterminal resultが揃うまで完了にしない。`SPEC / CONTEXT / METHOD / RECOVERY`はCandidate49と同一である。

## 固定条件

- Evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1`
- Evaluation set identity: `1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90`
- case / iteration: F05 clarification、F10 monthly review x `1..5`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent環境: `agents.max_threads=4`、`memories=false`
- executor: global queue `M=10`
- quality rating: `outcome-quality-owner-diagnostic-v9`
- compatibility key: `937499798438d2a3d9125c0887257badf7f21d460ba3fb6e923fefb2822570c1`
- token accounting: all-agent `v1`

profileとregistry key上はprompt identity以外が同一である。しかし実rolloutではskill / plugin catalogが異なり、実際のmodel-visible Agent環境は同一ではなかった。

## KPI

| KPI | Candidate43 | Candidate49 | Candidate51 | C51 - C43 | C51 - C49 |
| --- | ---: | ---: | ---: | ---: | ---: |
| median `quality_score` | 100.000 | 100.000 | 100.000 | 0.000 | 0.000 |
| median `total_tokens` | 178,705 | 294,543 | 167,306 | -11,399 (-6.38%) | -127,237 (-43.20%) |
| median `elapsed_seconds` | 86.902 | 118.549 | 97.201 | +10.299 (+11.85%) | -21.348 (-18.01%) |
| 10 run token合計 | 1,050,768 | 1,309,324 | 1,070,987 | +20,219 (+1.92%) | -238,337 (-18.20%) |
| score `4` | 10 | 10 | 10 | 0 | 0 |

## case別token

| case | Candidate43 | Candidate49 | Candidate51 | C51 - C43 | C51 - C49 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F05 | 348,448 | 348,501 | 320,118 | -28,330 (-8.13%) | -28,383 (-8.14%) |
| F10 | 702,320 | 960,823 | 750,869 | +48,549 (+6.91%) | -209,954 (-21.85%) |

## raw execution

| case | 指標 | Candidate43 | Candidate49 | Candidate51 | C51 - C43 | C51 - C49 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| F05 | model step | 22 | 22 | 19 | -3 | -3 |
| F05 | tool call | 17 | 17 | 14 | -3 | -3 |
| F05 | input token | 344,125 | 343,781 | 315,790 | -28,335 (-8.23%) | -27,991 (-8.14%) |
| F10 | model step | 37 | 52 | 38 | +1 | -14 |
| F10 | tool call | 32 | 47 | 33 | +1 | -14 |
| F10 | input token | 689,536 | 945,707 | 737,406 | +47,870 (+6.94%) | -208,301 (-22.03%) |

F10のmodel step / tool callは各runで次の分布だった。

| prompt set | model step | tool call |
| --- | --- | --- |
| Candidate43 | `12 / 5 / 12 / 4 / 4` | `11 / 4 / 11 / 3 / 3` |
| Candidate49 | `12 / 12 / 12 / 12 / 4` | `11 / 11 / 11 / 11 / 3` |
| Candidate51 | `12 / 4 / 4 / 12 / 6` | `11 / 3 / 3 / 11 / 5` |

Candidate51はC49の4 / 5逐次runを2 / 5へ戻した。C43も逐次runは2 / 5であり、operation completion復元と実行分割の変化は対応している。一方、C43 / C51ともrun間変動が大きく、単一prompt規則だけで全runを同じ方法へ収束させてはいない。

## 判定

- 事実: Candidate51はCandidate49比でF10 model stepを`52 -> 38`、input tokenを`945,707 -> 737,406`へ減らした。
- 事実: Candidate51とCandidate43のF10逐次run数は各2 / 5だった。
- 事実: Candidate51のF10 tokenはCandidate43より`+6.91%`、model stepは`+1`だった。
- 未確定: root operation completionの復元効果は、model-visible skill / plugin catalogを固定した再試験まで確定しない。
- 未確定: `INDEPENDENCE`復元が追加で必要かは、このresultから判定しない。
- 次段: model-visible Agent環境identityを固定するまでA01 / A02、Candidate52、`INDEPENDENCE`追加へ進まない。

## Evidence

- Candidate43 result: `40103b0900de4f40bfdf5a74c83126ff`
- Candidate49 result: `61e189fce2634677a405bb61b3c760ca`
- Candidate51 result: `df1e13d6fa2c4299a1f255698e15125e`
- Candidate51 content SHA-256: `33b25de21ee26dcdbc5ddea8f3e09655662fdc358eadc1f8a2a02ff5815e73f0`
- Candidate51 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate51-root-operation-completion-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-20260721-r1`

Candidate51 campaignはvalid 10 / 10、retry 0、excluded attempt 0である。quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。非公開raw run log、session情報、一時workspaceはrepositoryへ保存しない。

Candidate51の採用、release、本体反映は未判断・未実施である。
