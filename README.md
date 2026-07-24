# THE-CAPTION-PROMPT

このリポジトリはTHE-CAPTION本体のruntime変更ではなく、THE-CAPTIONへ渡すプロンプトを設計・比較・評価する研究基盤です。

## 目的

- プロンプトidentityを固定して比較可能な形で保存する
- 候補と評価結果を分離し、採用判断を明示的に別管理する
- `evaluation_foundation_v3`に従って再現性ある比較実験を運用する
- 本体反映はTHE-CAPTION本体リポジトリでの承認フローに委ねる

## 5〜10分で読める理解入り口

READMEはここを最短で読む設計に変更しました。全体像を把握し、詳細は`docs/`へ移しています。

## 現時点の要点（要約）

- 不要なworker起動を減らす制御が、all-agentのトークン削減で最も大きい効果を出した
- prompt文字量や説明文の圧縮だけでは、実行効率はほぼ改善しない
- Decision Boundary/Validation Closureは再判断と追加readを減らし、tool call・時間短縮に寄与した
- 評価（`quality_score` / `all-agent total_tokens` / `elapsed_seconds`）と採用判断は別レイヤーとして扱う

## 現在の運用状態

- baseline / candidate / releaseは`prompts/`配下で分離
- 評価結果は`evaluations/results/`をappend-onlyで保存
- 評価の可用性、採用、THE-CAPTION本体への反映、runtime有効化は互いに混ぜない
- 互換条件（評価セット、prompt set identity、model、Agent環境、TaskSpec等）を固定して比較する

## リポジトリ構成（最短版）

- `prompts/`: 比較対象とreleaseの制御資産
- `evaluations/`: set/case/profile/result/ratingの保存域
- `docs/`: 仕様・評価設計・制御設計・運用方針
- `tests/`, `scripts/`: 検証・再現の基盤

## 詳細ドキュメント

- [readme-legacy-full.md](docs/readme-legacy-full.md): 最新`origin/main`時点のREADME全文（移設前内容）
- [docs/overview.md](docs/overview.md): リポジトリの全体像・評価基盤の契約
- [docs/control-mechanisms.md](docs/control-mechanisms.md): 制御追加の問題軸別整理
- [docs/control-evolution.md](docs/control-evolution.md): 制御の進化履歴（原因→制御→知見）
- [docs/candidate-history.md](docs/candidate-history.md): Candidate系譜のテーマ別地図
- [docs/future-roadmap.md](docs/future-roadmap.md): 今後の運用計画と改善サイクル

## 先に読むべき正本

- [docs/repository-contract.md](docs/repository-contract.md)
- [docs/prompt-comparison-workflow.md](docs/prompt-comparison-workflow.md)
- [docs/evaluation-loop-manual.md](docs/evaluation-loop-manual.md)
- [docs/prompt-control-design-principles.md](docs/prompt-control-design-principles.md)
- [docs/evaluation-storage-maintenance.md](docs/evaluation-storage-maintenance.md)
