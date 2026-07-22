# TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW r1

## 結論

Candidate64のdelegated producer pathを正に適用するため、F10 monthly review r3と同じreview対象、read範囲、seed、oracleへ、独立producer executionの明示だけを加えたcaseである。

root-only F10との成果差を作るcaseではない。TaskSpecがworker producerを明示した場合に、指定workerの起動、result provenance、rootによるpredicate再実行の有無を観測する。

## 固定差分

- case ID: `TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW`
- revision: `r1`
- source case: `TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3`
- operation identity: `monthly-format-review`
- local task name: `monthly_format_review_producer`
- canonical producer identity: `/root/monthly_format_review_producer`
- model-visible追加: `task_kind_goal_and_done_condition`内のoperation identityとproducer execution bindingだけ
- unchanged: target commit、seed commit / tree、seed patch、allowed read、forbidden operation、expected finding、no-drift oracle

workerへ渡すのはmodel-visible TaskSpecから構築したpacketだけである。private data、seed patch、expected finding、oracle、grader contractはmodel-invisibleとする。

## 判定境界

成果品質はF10 r3と同じfindingとzero driftで判定する。route診断は品質採点と分離し、次を保存traceから確認する。

1. 指定canonical identityのworkerが一つ以上起動する。
2. workerのterminal resultをroot final responseへbindできる。
3. rootはreview predicateを実行または再生成しない。
4. worker terminal前にrootがoperationを完了扱いしない。

このcaseの作成、fixture qualification、prompt評価、採用、release、本体反映は別状態である。

## Fixture preparation

```bash
python3 scripts/prepare_evaluation_set.py \
  --case evaluations/cases/TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1 \
  --source-repo /Users/kenn/repos/THE-CAPTION \
  --output /tmp/the-caption-tc-d01-explicit-producer-monthly-review-r1-set
```
