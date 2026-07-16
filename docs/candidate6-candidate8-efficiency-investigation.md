# Candidate6からCandidate8までの効率化調査

> [!IMPORTANT]
> この文書のtoken数値とtoken由来の設計解釈はroot-only履歴である。現行値は[`v3 all-agent token再集計`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)を参照する。all-agentではCandidate5が5,740,441、Candidate6が5,951,457、Candidate5追加18 resultの中央値が5,980,342.5である。Baselineに実装SAがあるためtokenが少ないというroot-only由来の仮説は再集計後の結果と一致しない。以下は調査時点の経緯として保持する。

## 位置づけ

この文書は、Candidate5の品質と完了速度を維持したままtoken使用量を抑えるために作成したCandidate6、Candidate7、Candidate8の観測と、そこから得た設計上の結論を記録する。Evaluation set、test、quality rating基準は変更していない。

ここで扱う結論はprompt設計調査の範囲に限る。candidateの採用、release化、THE-CAPTION本体への反映は判断せず、評価基盤へwinnerや優先順位を追加しない。

## 調査系列

| set | parent | 変更軸 | 観測範囲 |
| --- | --- | --- | --- |
| Candidate5 | Candidate4 | 実行開始後の停止を、明示済み条件と観測事実へ限定 | expanded 12 case、`N=5`に加え、同条件の追加18 result |
| Candidate6 | Candidate5 | JIT節参照、SA packet最小化、結果再掲抑制 | expanded 12 case、`N=5` |
| Candidate7 | Candidate5 | required commandの完全evidenceとmodel-visible outputを分離 | `TC-F02`、`N=1`の診断観測 |
| Candidate8 | Candidate7 | command単位のprojectionを工程間result全体へ一般化 | `TC-F02`、`N=1`の診断観測 |

Candidate7とCandidate8の単回観測は、変更軸の挙動を見るための診断である。反復条件がCandidate5、Candidate6の保存済み`N=5` resultと一致しないため、Layer 4の互換比較resultとして扱わない。

## Candidate6 N=5

Candidate6はCandidate1のcontext効率化を参考にしつつ、Candidate5の完了志向、実装主体のモデル判断、Audit / Review routingを維持した。

| set | `quality_score`中央値 | `total_tokens`中央値 | `elapsed_seconds`中央値 | runner wall time |
| --- | ---: | ---: | ---: | ---: |
| Candidate5 | 100.000 | 4,503,816 | 1,714.914秒 | 426.528秒 |
| Candidate6 | 100.000 | 4,692,041 | 1,715.486秒 | 476.489秒 |
| C6 - C5 | 0.000 | +188,225 | +0.571秒 | +49.961秒 |

Candidate6では`docs/orchestration-process.md`と`docs/prompt-guide.md`の親run読取文字数は減ったが、標準KPIの`total_tokens`中央値はCandidate5より増えた。case別5回中央値では、減少したcaseがある一方、最大差の`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND`はCandidate5の978,822からCandidate6の1,179,844へ201,022増えた。

したがって、正本文書の読取量、SA起動packet、最終結果の再掲だけでは、Candidate5のtoken使用量を支配する要因を説明できなかった。Candidate6の一次結果と4-result viewは以下に保存する。

- [`Candidate6 N=5 result`](../evaluations/results/candidate6-expanded12-global-m24-n5_2026-07-16.md)
- [`Baseline / Candidate1 / Candidate5 / Candidate6 comparison view`](../evaluations/results/baseline-candidate1-candidate5-candidate6-expanded12-global-m24-n5_2026-07-16.md)

## Candidate7とCandidate8のF02診断観測

Candidate5とCandidate6の差が最大だった`TC-F02`について、実装主体やtestを変えず、親が次工程へ渡す情報量を絞る仮説を単回観測した。

| set | 変更軸 | 実装主体 | route | score | `total_tokens` | `elapsed_seconds` |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Candidate5 | 完了志向 | 親直接 | 保存済み5 runはいずれも`audit+review` | 4 × 5 | 978,822（5回中央値） | 352.938秒（5回中央値） |
| Candidate7 | command evidence projection | 親直接 | `audit+review` | 4 | 1,010,053 | 334.392秒 |
| Candidate8 | phase result projection | 親直接 | `audit+review` | 4 | 1,099,736 | 430.876秒 |

Candidate7とCandidate8はいずれも実装SAを起動せず、対象2 sourceだけを変更し、focused 24 testsとfull 326 testsを通過した。Auditの停止指摘とReviewの重大指摘は0件で、品質成果は維持した。

一方、Candidate7はCandidate5のF02中央値より31,231 token多く、Candidate8は120,914 token多かった。単回観測のため差を一般化できないが、出力formatをcommandまたは工程単位で指定するだけでは、Candidate5より少ないtoken使用を確認できなかった。Candidate8では、projection用wrapper自体の失敗回収と詳細な最終報告も発生しており、format規則が実際の行動を自動的に短縮するとは限らなかった。

- Candidate7 run ID: `5b56a2d094414805ac720ecabf11f62a`
- Candidate8 run ID: `dca883fc365f4f28b195982d159435b6`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate7-f02-n1-observation-20260716-v3-r1`、`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate8-f02-n1-observation-20260716-v3-r1`

両runはLayer 3までの診断観測であり、Layer 4 resultとして登録していない。raw evidenceはrepositoryへcommitしない。

## 実装SAとの関係

実装SAは、固定した作業単位を別contextへ渡し、親へ戻す情報を結果へ絞るため、親のcontext lifetimeを物理的に分けられる。これに対してCandidate7とCandidate8のprojectionは、同一の親context内で出力様式を指定するものであり、既に親が読んだ仕様、探索結果、command output、判断過程をcontextから除去またはresetしない。

この差から、Baselineで見えたtoken抑制を「実装SAへ渡す文章」または「実装SAが返す文章」のformatだけに還元することはできない。実装SAの効果がある場合は、入出力様式よりもcontext topologyの分離が寄与している可能性がある。

ただし、実装SAの必須化はCandidate5で維持した実装主体のモデル判断を変更する。Candidate5の品質と完了速度を維持するという目的に対して、token削減だけを理由に専用実装SAを戻すことは、この調査系列の変更境界と一致しない。

## Candidate5追加反復

Candidate5の最初の`N=5`結果だけに依存しないよう、同じcompatibility keyで18件の追加`N=5` resultを保存した。各resultはexpanded 12 case × 5 iterationの60 valid runで、合計1,080 runである。

| 集計対象 | `quality_score` | `total_tokens` | `elapsed_seconds` | runner wall time |
| --- | ---: | ---: | ---: | ---: |
| 18 resultの中央値 | 100.000 | 4,697,396.5 | 1,575.473秒 | 467.122秒 |
| 最小 | 93.750 | 4,386,829 | 1,498.270秒 | 363.203秒 |
| 最大 | 100.000 | 5,240,680 | 1,799.947秒 | 587.390秒 |

1,080 runのscore内訳は、score 4が1,048、score 3が5、score 1が27だった。score 3はF04のcleanup未完了4件とF02のReview残件1件である。score 1はすべてF10 monthly reviewで、TaskSpecが要求する開始identityと実workspaceのseed状態の不一致を理由にreview前に停止したrunである。この27件はratingへそのまま保持するが、fixture条件の矛盾を含むためCandidate5固有の品質低下とは断定しない。Evaluation setとtestはこの調査では変更していない。

追加反復ではquality中央値を維持した一方、`total_tokens`は最初のCandidate5 resultの4,503,816より広い分布を示した。今後token差を扱う場合は、単一の`N=5`中央値だけでなく、この反復変動を観測範囲として明示する必要がある。

- compatibility key: `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate5-overnight-n5-20260716`
- registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`

18件のLayer 4 resultはappend-onlyで登録済みである。raw evidenceとregistry resultはrepositoryへcommitしない。

## 設計上の結論

この調査系列では、Candidate6のJIT context規則、Candidate7のcommand evidence projection、Candidate8のphase result projectionのいずれも、Candidate5の品質特性を維持しながらtoken使用量を下げる根拠にはならなかった。主な観測は以下である。

1. 文書読取文字数の減少は`total_tokens`の減少と一致しなかった。
2. 同一親context内の出力format指定は、既に蓄積したcontextやモデルの探索行動を分離しなかった。
3. 実装SAによるcontext分離はformat指定とは別の変更軸であり、必須化するとCandidate5の設計目的を変える。
4. Candidate5の追加反復ではquality中央値と完了速度を維持したが、token量には無視できないrun間変動があった。

以上から、Candidate5をこの設計系列の完成点かつ次の調査の参照点とする。Candidate6は`observed_n5`、Candidate7とCandidate8は`observed_f02_n1`の調査artifactとして保持し、採用、release、runtime projectionは行わない。新しい効率化candidateを作る場合は、出力formatの追加ではなく、Candidate5の完了志向と実装主体判断を維持したまま別の因果仮説を独立した変更単位として定義する。
