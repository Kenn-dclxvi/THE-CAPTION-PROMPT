# THE-CAPTION-PROMPT

THE-CAPTION向けプロンプトを設計、比較、評価し、反映可能な形へまとめるための専用リポジトリです。

## 目的

- 現行プロンプトの参照元とidentityを固定する
- 候補プロンプトを本体から分離して構築する
- 同一条件で比較できる評価caseとprofileを管理する
- 評価済み候補をrelease単位でまとめる
- THE-CAPTION本体への反映を明示的な承認作業として扱う

## 現在の状態

`bootstrap`。リポジトリ構造と運用境界だけを作成した状態です。候補プロンプトの採用、THE-CAPTION本体への反映、runtime有効化は行っていません。

## 構成

| Path | 役割 |
| --- | --- |
| `docs/` | リポジトリ契約、設計判断、反映手順 |
| `prompts/baselines/` | 比較元プロンプトと取得元identity |
| `prompts/candidates/` | 構築中の候補プロンプト |
| `prompts/releases/` | 承認可能な単位へ固定したprompt bundle |
| `evaluations/cases/` | 評価caseとmodel-visible / private境界 |
| `evaluations/profiles/` | model、Agent、環境、反復条件、判定基準 |
| `evaluations/results/` | 再現可能性を満たす評価結果 |

運用境界は[`docs/repository-contract.md`](docs/repository-contract.md)を正本とします。

## 初期作業

1. THE-CAPTIONの対象commitと現行prompt identityを固定する
2. 現行promptを`prompts/baselines/`へ取り込む
3. 最初の候補が解く問題と非目標を定義する
4. 比較前にevaluation profileを固定する
5. 評価結果と承認を分けて記録する
