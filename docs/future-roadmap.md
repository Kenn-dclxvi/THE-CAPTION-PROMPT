# 今後の運用ロードマップ

## 方針

このリポジトリは、
「プロンプト保存庫」ではなく
**AI実行制御を設計・評価・改善する研究基盤**として運用します。

## 今回移送した内容

- README末尾の運用ノートは本稿へ移設
- 候補評価・採用・反映の責務分離を維持
- 候補追加時は旧内容を保持しつつ分離保存

## 改善サイクル（実行）

1. 問題を1文で定義
2. control-free最短経路を固定
3. 候補は1責任で作成
4. targeted → expanded の順で検証
5. `quality_score` / `all-agent total_tokens` / `elapsed_seconds` を記録
6. 採用判断は評価外側で実施

## 評価運用

- 条件不一致混在を避ける
- 新条件は新revisionとして保存
- 既存`result`は上書きせずappend-only

## Runtime化・採用連携

- runtime反映はprojectionゲートを通して実施
- リリース状態と本体反映は別フロー

## モデル比較

- model/環境/permission/task変更は同一比較に混在させない
- 追加比較は新revisionとして保存

## 直近アクション

- docs間リンクの参照漏れ点検
- 各Candidate成果と新評価結果の差分は`evaluations/results/`へ追加保存
