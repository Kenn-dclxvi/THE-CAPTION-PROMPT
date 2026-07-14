# Evaluations

prompt比較用のcase、execution profile、再現可能なresultを管理する。

- `cases/`: task入力、fixture contract、oracle / grader境界
- `profiles/`: model、Agent、environment、反復、順序、判定基準
- `results/`: profileとartifact identityへbindした結果

ローカル試行やidentity不一致のrunを正式結果へ昇格させない。
