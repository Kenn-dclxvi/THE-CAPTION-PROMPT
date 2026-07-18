# Candidate37 exact evidence location targeted N=5 result

## 結論

Candidate37は、C34 F05で観測したcriterion projection欠落と、C35 F10で観測したsource location不一致を、targeted 2-case N=5で再現しなかった。

F05 clarifyとF10 monthly reviewは各5 / 5、合計10 / 10 runがvalid、rateable、score `4`だった。`quality_score`中央値は`100.000`である。

Candidate37はCandidate36のprojection規則を累積している。したがって、F05はCandidate36由来、F10はCandidate37由来の制御を同じprompt setで確認した。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 固定条件

- prompt set: `the-caption-3ce91a4-exact-evidence-location-r1`
- bundle SHA-256: `c5e16b17d0da4608f0b08201ec8541870ce45902986cbe1fd53b40b9594a1559`
- cases: `TC-F05-CLARIFY-UNITS-MODE r1`、`TC-F10-MONTHLY-FORMAT-TEST-REVIEW r3`
- evaluation set: `the-caption-prompt-fixes-f05r1-f10r3-r1`
- evaluation set identity: `4564c49730ab0d135bb2a1ff5530d02f49f71808e4ee2c2c4405beca99a1cca7`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- quality rating: `owner-producer-quality-v8`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v5`
- execution: global queue `M=10`、各case `N=5`

## 結果

- valid / rateable run: 10 / 10
- score `4`: 10
- score `0..3`: 0
- owner-producer evidence eligible: 10 / 10
- command protocol violation: 0 / 10
- all-agent token total: `2,484,749`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `526,440`
- `elapsed_seconds` median: `265.577`
- result ID: `6a93bfc62d6f41a68e93e582a82b7c09`
- compatibility key: `4fc262a28717c6ded71d250d4d172e404fdb1acb51ae98b4d420e51d1d0e85fb`

F05は5 / 5で、既定modeの`daily` / `strict`選択と、`strict`時のlive CSV `fallback` policyを1回のclarificationとして返した。変更、test、外部operationは行っていない。

F10は5 / 5で、`major` findingを`src/app/entrypoints/monthly_main.py:25`へ結び付けた。`args.format_test`を使わず`args.force`を渡す直接根拠と、`-t` / `-F`のuser-visible impactを返した。artifactは変更していない。

## 試験側の実行回帰

初回dispatchでは、F04以外のprofileでadapter-owned cleanup pathが未定義の場合に、診断collectorへ`None`を渡す試験側の例外を検出した。

各Agentはterminal responseまで完了していたが、adapterが成果保存前に例外終了したため、該当attemptはvalid resultへ登録していない。

adapterの未定義値を空配列へ正規化し、単体回帰試験を追加した。その後に同じ10 slotを新規実行し、上記の公式resultを登録した。

この試験側回帰はprompt qualityへ算入していない。公式resultの`excluded_attempts`は0であり、修正後の10 runだけから構成する。

## Evidence boundary

- profile: `evaluations/profiles/candidate37-exact-evidence-location-owner-producer-v8-targeted2-global-m10-n5-r1.json`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate37-exact-evidence-location-owner-producer-v8-targeted2-global-m10-n5-20260718-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/6a93bfc62d6f41a68e93e582a82b7c09.json`
- quality audit、Layer 4 registration、lossless archive、final compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。

N=5の観測であり、この2 case以外や低頻度事象へ一般化しない。
