# 制御メカニズム（機能別整理）

本節は、README本文から分離した制御要素を、再利用しやすい形でまとめます。

## Worker

- **問題**: rootで完結可能な場面でworker起動が増える
- **対処**: 委譲条件を厳密化し、producerが必要な場合だけdelegate
- **確認指標**: top-level tool call、all-agent token、再現性

## Context

- **問題**: 不要情報継承で子セッションの再解析コストが増える
- **対処**: packet継承を最小化し、必要十分な範囲へ圧縮
- **確認指標**: 失敗率、quality scoreへの影響

## Decision Boundary

- **問題**: 同一結論でも再判断が走りstepが増える
- **対処**: 再入条件を明示し、同一invocationでの戻りを抑制
- **確認指標**: model step、tool call、elapsed_seconds

## Validation Closure

- **問題**: 検証フェーズの読み直しが都度戻る
- **対処**: 変更後検証を1波で完結し、追加readを原則禁止
- **確認指標**: 応答時間、検証漏れリスク

## Read

- **問題**: read順序の散乱で往復が増える
- **対処**: 定型readをbatch化・一括確定化
- **確認指標**: model step、read回数、再実行率

## Runtime

- **問題**: evidenceとchild final resultの接続不一致
- **対処**: producer identity・実行identity・結果受領の条件を固定化
- **確認指標**: 結果整合、再開時の誤復旧

## 補足

評価は`effect`（効果）だけで判断しません。`quality_score`、`all-agent total_tokens`、`elapsed_seconds`を同時に確認し、採用可否は別ゲートで扱います。
