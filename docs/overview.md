# Repository Overview

## 役割

THE-CAPTION-PROMPTは、THE-CAPTION本体を直接変更せず、
プロンプト設計・比較・評価・採用証拠管理を行うための研究基盤です。

## 目的

- 評価可能な形で候補を保存する
- 候補と評価結果を分離して採用判断の混線を防ぐ
- 互換条件を固定した比較のみを行い、再現性を担保する

## repository contract

運用の正本は[docs/repository-contract.md](repository-contract.md)です。
`v1`/`v2`の履歴は保持し、上書き再解釈は行いません。

## 評価基盤の考え方

評価は4層で管理します。

1. Evaluation set
2. Execution
3. Quality rating
4. KPI comparison

KPIは以下3つだけです。

- `quality_score`
- `all-agent total_tokens`
- `elapsed_seconds`

## 状態遷移（状態管理）

- `draft`
- `evaluation_ready`
- `evaluated`
- `release_candidate`
- `approved_for_projection`
- `projected`

## 主要ディレクトリ

- `prompts/baselines/`: 比較の起点
- `prompts/candidates/`: 制御実験候補
- `prompts/routes/`: 実行前の差分合成
- `prompts/releases/`: 固定化済み候補
- `evaluations/`: set/profile/result/ratingの履歴
- `docs/`: 設計・運用・履歴ドキュメント

## 推奨の読み順

1. [README.md](../README.md): 入口
2. [docs/overview.md](overview.md): 全体像
3. [docs/control-mechanisms.md](control-mechanisms.md): 制御の分類
4. [docs/control-evolution.md](control-evolution.md): 追加履歴
5. [docs/candidate-history.md](candidate-history.md): 系譜
6. [docs/future-roadmap.md](future-roadmap.md): 今後
