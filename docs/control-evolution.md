# 制御追加の進化（問題軸）

README全文をそのまま保持したものは[readme-legacy-full.md](readme-legacy-full.md)です。
この文書は、Candidate番号順ではなく問題解決軸で再編します。

## 1) 不要worker起動の抑制

- 解決対象: 実行効率と再現安定性
- 主要系譜: C5, C15, C41, C43, C68
- 事実: worker起動抑制がall-agent token低減に最も寄与

## 2) 再入（再判断）の抑制

- 解決対象: model stepの増大、tool callの増加
- 主要系譜: C69, C70, C71
- 事実: 再入条件を固定するとstepとトップレベルtool callが下がる

## 3) read定型化・一括化

- 解決対象: 順序依存の散発読取・再読
- 主要系譜: C50, C56, C59, C63, C62
- 事実: read最適化は条件次第で効果幅が大きく変動

## 4) 証跡/境界の整合化

- 解決対象: owner/prod/resultの紐付け不整合
- 主要系譜: C17, C20, C21, C22, C34
- 事実: runtime一致条件を厳格化し、失敗経路の再開事故を減らす

## 5) 制御追加の安全運用

- 解決対象: 制御追加が品質低下を誘発するリスク
- 実務原則:
  - 制御前にcontrol-free最短路を固定
  - 候補は1責任ずつ追加
  - 互換条件固定下でだけ比較

## 参照先

- 全系譜: [prompts/candidates/README.md](../prompts/candidates/README.md)
- 分類基準: [docs/prompt-control-design-principles.md](prompt-control-design-principles.md)
