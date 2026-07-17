# Candidate31 operation terminal closure expanded N=5 result

## 結論

Candidate31のexpanded 12-case N=5試験は、60 / 60 valid runを完了し、Layer 4へ登録した。

score分布は`4 / 3 = 59 / 1`だった。

score `3`はF07 dependency provenanceのiteration 5で発生した。

成果、Owner結果、許可pathは成立していたが、`all-agent-command-evidence/v2`がrequired validationの成功結果を採点入力へmaterializeできなかったため、固定済みrating contractに従ってscore `3`とした。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- profile: `candidate31-operation-terminal-closure-owner-producer-v4-expanded12-global-m24-n5-r1`
- prompt set: `the-caption-3ce91a4-operation-terminal-closure-r1`
- bundle SHA-256: `b43d3a62dafe3d489800b1cbb6c6871e6062a040d74a34a75c66e882415de304`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- evaluation set: `the-caption-expanded12-f10r3-r1` / `r1`
- cases: expanded 12 case
- repetition: 各case `N=5`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- executor: global queue `M=24`、max attempts `3`
- token accounting: all-agent `v1`
- quality rating: `owner-producer-quality-v4`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v2`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`

## 結果

- valid / rateable run: 60 / 60
- score `4`: 59
- score `3`: 1
- excluded attempt: 2
- all-agent token total: `19,714,134`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `3,800,682`
- `elapsed_seconds` median: `1,516.395`
- result ID: `70ecc211f8c74f769d4f136120aca52a`
- compatibility key: `b8a2c57576fc1bcff35c069532f69c79421accefce66d200697b5fd0dea52cee`

| iteration | quality_score | total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 3,785,248 | 1,609.051 |
| 2 | 100.000 | 3,684,017 | 1,443.888 |
| 3 | 100.000 | 3,800,682 | 1,615.263 |
| 4 | 100.000 | 4,249,807 | 1,516.395 |
| 5 | 97.917 | 4,194,380 | 1,436.753 |

F07 dependency provenance以外の11 caseは各5 / 5でscore `4`だった。

F07 dependency provenanceはscore `4 / 3 = 4 / 1`だった。

初回dispatchではF02 iteration 4と5の2 attemptが`codex_model_at_capacity`となった。

この2 attemptは外部要因として除外し、同じslotを再実行してvalid resultを得た。除外attemptはKPIへ含めていない。

## Score 3の事実

対象runは`0cc83c6aca1842839377ed95d15e7b87`である。

workspace成果はrequirements 2 fileの限定変更を満たし、Owner producer resultもscore `4`の必要条件を満たした。

保存済みdescendant rolloutには、指定Python validation、`git diff --check`、`git diff --name-only`がすべてexit `0`になったtool outputがある。

一方、固定済みcommand evidence viewは`successful_command_count=0`だった。

このrunは、複数commandを`tools.exec_command`で並列実行し、`<name>: exit=0`として集約したcustom `exec` wrapperを使った。現行collectorはこの集約結果を各commandへ対応付けられなかった。

したがって、score `3`は成果またはOwner resultの失敗ではなく、required validationの成功を固定済み採点入力へmaterializeできなかった評価証跡側の不足である。

既存resultは再採点せず、この不足を未解決事項として残す。

## 観測範囲

事実として、60 valid runの全てでOwner producer evidenceは成立した。

事実として、F06とF07 canonical runnerは各5 / 5でscore `4`だった。

判断として、targeted試験で解消したoperation terminal closureの問題は、expanded試験のF06とF07 canonical runnerでも再発しなかった。

ただし、単一のexpanded N=5 resultを未評価caseや長期連続試験へ一般化しない。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate31-operation-terminal-closure-owner-producer-v4-expanded12-global-m24-n5-20260718-v3-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/70ecc211f8c74f769d4f136120aca52a.json`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
