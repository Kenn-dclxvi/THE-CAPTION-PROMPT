# THE-CAPTION-PROMPT

THE-CAPTION向けプロンプトを設計、比較、評価し、反映可能な形へまとめるための専用リポジトリです。

## 目的

- 現行プロンプトの参照元とidentityを固定する
- 候補プロンプトを本体から分離して構築する
- 同一条件で比較できる評価caseとprofileを管理する
- 評価済み候補をrelease単位でまとめる
- THE-CAPTION本体への反映を明示的な承認作業として扱う

## 現在の状態

`evaluation_foundation_v3`。1つのimmutableなprompt set identityごとに3 KPIをappend-onlyで保存し、互換条件を満たす任意個のresultを後から取得・比較できます。固定A / B pair、winner、改善・悪化は保存・出力しません。v1 / v2 resultは履歴として保持し、migrationや再解釈は行っていません。候補の採用、THE-CAPTION本体への反映、runtime有効化も行っていません。

## 構成

| Path | 役割 |
| --- | --- |
| `docs/` | リポジトリ契約、設計判断、反映手順 |
| `prompts/baselines/` | 比較元プロンプトと取得元identity |
| `prompts/candidates/` | 構築中の候補プロンプト |
| `prompts/releases/` | 承認可能な単位へ固定したprompt bundle |
| `evaluations/cases/` | 評価caseとmodel-visible / private境界 |
| `evaluations/profiles/` | model、Agent、環境、反復条件、比較条件 |
| `evaluations/results/` | 公開済みの履歴評価結果。v3 runtime registryとは分離 |

運用境界は[`docs/repository-contract.md`](docs/repository-contract.md)を正本とします。
評価基盤のLayerと境界は[`docs/prompt-comparison-workflow.md`](docs/prompt-comparison-workflow.md)に定義します。実行方法は[`docs/evaluation-loop-manual.md`](docs/evaluation-loop-manual.md)、検証cloneの容量維持は[`docs/evaluation-storage-maintenance.md`](docs/evaluation-storage-maintenance.md)を参照します。
Candidate5の評価整理と次candidateの設計方向は[`docs/candidate5-token-efficiency-direction.md`](docs/candidate5-token-efficiency-direction.md)、Candidate6からCandidate8までの効率化調査と設計結論は[`docs/candidate6-candidate8-efficiency-investigation.md`](docs/candidate6-candidate8-efficiency-investigation.md)に記録します。

## 初期作業

1. THE-CAPTIONの対象commitと現行prompt identityを固定する
2. 現行promptを`prompts/baselines/`へ取り込む
3. 最初の候補が解く問題と非目標を定義する
4. 比較前にevaluation profileを固定する
5. 評価結果と承認を分けて記録する
