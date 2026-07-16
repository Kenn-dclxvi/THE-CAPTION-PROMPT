# Candidate5 / Candidate15 連続試験比較

## 目的と範囲

Candidate5とCandidate15を、同じexpanded 12 case、各case `N=5`、1 batch 60 valid runの条件で18 batchずつ反復した結果をまとめる。各prompt setの観測結果と明示的な数値差だけを記録し、winner、採用、release、THE-CAPTION本体反映の判断は行わない。

| 項目 | Candidate5 | Candidate15 |
| --- | --- | --- |
| prompt set identity | `the-caption-3ce91a4-completion-persistence-r1` / `r1` / `63abe0…1667` | `the-caption-9b3a96a-selected-role-control-input-boundary-r1` / `r1` / `1a2ef9…6db8` |
| batch | 18 | 18 |
| valid run | 1,080 | 1,080 |
| iteration集計 | 90 | 90 |
| compatibility key | `ede1a4…d951` | `ede1a4…d951` |
| token accounting | `all_agents` / `v1` | `all_agents` / `v1` |

Candidate5の連続試験は、保存済みroot-only `prompt-set-result/v1`を変更せず、全session usageからappend-onlyで追加した`prompt-set-result/v2`をtoken比較に使用する。Candidate15は実行時からall-agent accountingを使用した`prompt-set-result/v2`である。evaluation set revision、fixture identity、target repository ref、model、Agent環境、TaskSpec、permission、executor parameter、case、iteration、反復条件は一致している。

## 18 batch集計

`quality_score`は1,080 run全体から算出する。`total_tokens`と`elapsed_seconds`の中央値は、各iterationで12 caseを合計した90値から算出する。

| 指標 | Candidate5 | Candidate15 | Candidate15 - Candidate5 |
| --- | ---: | ---: | ---: |
| 全run集約`quality_score` | 98.009% | 99.537% | +1.528 pt |
| score `4` | 1,048 | 1,072 | +24 |
| score `3` | 5 | 2 | -3 |
| score `1` | 27 | 6 | -21 |
| score `4`率 | 97.037% | 99.259% | +2.222 pt |
| 60 runすべてscore `4`のbatch | 3 / 18 | 12 / 18 | +9 batch |
| iteration `total_tokens`中央値 | 6,009,905 | 4,325,098 | -1,684,807 (-28.0%) |
| all-agent `total_tokens`合計 | 551,168,439 | 392,379,665 | -158,788,774 (-28.8%) |
| iteration `elapsed_seconds`中央値 | 1,601.537秒 | 1,478.979秒 | -122.558秒 (-7.7%) |
| 全run `elapsed_seconds`合計 | 144,819.824秒 | 134,692.037秒 | -10,127.787秒 (-7.0%) |
| 外部除外attempt | 1 | 3 | +2 |

KPIへ優先順位や閾値を置かず、数値差を改善・悪化、採用可否、release判断へ変換しない。

## 低score分布

| case / 観測理由 | Candidate5 | Candidate15 | Candidate15 - Candidate5 |
| --- | ---: | ---: | ---: |
| F10 monthly format-test review: 開始identity誤認、score `1` | 27 / 90 (30.0%) | 6 / 90 (6.7%) | -21 |
| F04 web audit column: cleanup未完了、score `3` | 4 / 90 (4.4%) | 2 / 90 (2.2%) | -2 |
| F02 history date bound: validation後の未完了停止、score `3` | 1 / 90 (1.1%) | 0 / 90 | -1 |
| その他9 case | 0 / 810 | 0 / 810 | 0 |

F10のscore `1`は、固定diffをreviewする前に開始identity不一致と判定して停止したrunである。F04のscore `3`は、`App.tsx`の実装と`npm ci`、lint、buildを完了した後、実行ポリシーに拒否された`rm -rf node_modules dist`から別の安全なcleanup commandへ切り替えず、test-owned outputを残して停止したrunである。Candidate5のF02 1件は、所定実装とrequired validation後にdate-bound test不足を残存指摘として停止したrunである。

これらは観測された停止理由の分類であり、prompt set全体または評価範囲外のtaskへ一般化しない。

## Batch別の観測値

`Q`はbatch内5 iterationの`quality_score`中央値、`tokens`と`seconds`も同じ5 iterationの中央値である。`distribution`はbatch内60 runの`score 4 / 3 / 1`件数を示す。

| batch | C5 Q | C5 tokens | C5 seconds | C5 distribution | C15 Q | C15 tokens | C15 seconds | C15 distribution |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100.000 | 6,747,119 | 1,641.576 | 59 / 0 / 1 | 100.000 | 4,544,333 | 1,506.982 | 60 / 0 / 0 |
| 2 | 100.000 | 5,849,008 | 1,555.076 | 60 / 0 / 0 | 100.000 | 4,242,008 | 1,554.759 | 60 / 0 / 0 |
| 3 | 100.000 | 5,436,524 | 1,513.451 | 59 / 0 / 1 | 100.000 | 4,320,791 | 1,462.406 | 59 / 1 / 0 |
| 4 | 100.000 | 5,970,017 | 1,544.922 | 59 / 0 / 1 | 100.000 | 3,992,804 | 1,376.695 | 60 / 0 / 0 |
| 5 | 100.000 | 6,006,103 | 1,526.144 | 58 / 0 / 2 | 100.000 | 4,631,477 | 1,540.683 | 60 / 0 / 0 |
| 6 | 100.000 | 6,383,556 | 1,697.770 | 58 / 0 / 2 | 100.000 | 4,250,525 | 1,497.596 | 59 / 0 / 1 |
| 7 | 93.750 | 6,130,107 | 1,701.645 | 56 / 1 / 3 | 100.000 | 4,383,291 | 1,605.964 | 58 / 0 / 2 |
| 8 | 100.000 | 6,884,831 | 1,799.947 | 58 / 1 / 1 | 100.000 | 4,494,439 | 1,533.129 | 60 / 0 / 0 |
| 9 | 100.000 | 5,632,584 | 1,578.176 | 59 / 0 / 1 | 100.000 | 4,063,499 | 1,618.600 | 60 / 0 / 0 |
| 10 | 97.917 | 5,990,668 | 1,572.715 | 57 / 1 / 2 | 100.000 | 4,268,542 | 1,393.747 | 60 / 0 / 0 |
| 11 | 100.000 | 5,838,256 | 1,535.149 | 60 / 0 / 0 | 100.000 | 4,890,036 | 1,590.250 | 60 / 0 / 0 |
| 12 | 100.000 | 5,905,197 | 1,578.199 | 58 / 1 / 1 | 100.000 | 4,339,853 | 1,462.122 | 59 / 0 / 1 |
| 13 | 100.000 | 6,056,461 | 1,572.770 | 60 / 0 / 0 | 100.000 | 4,252,823 | 1,430.742 | 60 / 0 / 0 |
| 14 | 100.000 | 6,109,711 | 1,608.192 | 58 / 0 / 2 | 100.000 | 4,293,870 | 1,449.646 | 60 / 0 / 0 |
| 15 | 97.917 | 5,813,690 | 1,534.579 | 57 / 1 / 2 | 100.000 | 4,371,951 | 1,487.013 | 60 / 0 / 0 |
| 16 | 100.000 | 5,844,397 | 1,498.270 | 58 / 0 / 2 | 100.000 | 4,443,742 | 1,417.748 | 59 / 0 / 1 |
| 17 | 93.750 | 5,548,234 | 1,581.860 | 56 / 0 / 4 | 100.000 | 4,552,011 | 1,448.422 | 60 / 0 / 0 |
| 18 | 100.000 | 6,207,146 | 1,621.039 | 58 / 0 / 2 | 100.000 | 4,302,157 | 1,440.718 | 58 / 1 / 1 |

## 外部除外

すべて`codex_model_at_capacity`であり、prompt behaviorではない外部要因として有効resultから除外した。同じcase / iterationを再実行し、両prompt setとも各batch 60 valid runを揃えている。

| set | excluded attempt | 対象 |
| --- | ---: | --- |
| Candidate5 | 1 | batch 12、F02 iteration 1 |
| Candidate15 | 3 | batch 8、F01 iteration 1 / F10 inventory iteration 1、batch 14、F07 runner iteration 5 |

## 読み取り境界

- 単発のexpanded 12-case `N=5`では、Candidate5とCandidate15はいずれも60 runすべてscore `4`だった。18 batchではCandidate5に32件、Candidate15に8件の低score runが観測され、少数反復の中央値だけでは低頻度停止を表せない。
- 18 batchでも対象は固定12 caseであり、未収録taskや別repositoryへ結果を一般化しない。
- `elapsed_seconds`は各runのLayer 2実行時間であり、外部除外後の待機、seal、rating、registry登録、compactを含むcampaign wall timeではない。
- raw evidenceは非公開の検証領域へ保持し、この文書へ生run logやsession情報を含めない。

## Provenance

- Candidate5 raw campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate5-overnight-n5-20260716`
- Candidate15 raw campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate15-continuous-n5-b18-20260716`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- Candidate5 all-agent reaccounting summary: [`evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)

この文書は比較判断に必要な情報提供で終了する。prompt修正、採用、release、本体反映は別の明示的な作業とする。
