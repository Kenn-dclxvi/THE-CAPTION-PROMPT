# Candidate31 operation terminal closure rating v5 expanded N=5 result

## 結論

command evidence collectorをv3へ修正した後、Candidate31のexpanded 12-case N=5試験を新しいcampaignとして再取得した。

60 / 60 valid runを採点・登録し、score `4 / 3 = 60 / 0`だった。

旧rating v4でscore `3`となったcustom `exec` wrapperの証跡不足は、新しい60 runでは発生しなかった。

旧v4 resultは変更せず、rating v5 resultをappend-onlyで追加した。

採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 修正した評価境界

`all-agent-command-evidence/v3`は、custom `exec` wrapperが固定command nameと`<name>: exit=0`を出力した場合、nameとcommandを一意に対応付けて成功証跡へ含める。

sourceに`${r.name}`または`${r.label}`と`${r.exit_code}`があり、固定command表へnameをbindできる場合だけ対象にする。

worker final responseだけの成功申告、固定command表に存在しないname、一意に対応付けられないtextは証跡にしない。

旧v4でscore `3`となった保存runへ新collectorを適用する実証確認では、旧collectorの`successful_command_count=0`に対し、指定Python validation、`git diff --check`、`git diff --name-only`を含む4 commandを成功証跡として復元した。

この修正を`owner-producer-quality-v5`として固定し、旧resultを再採点せず新campaignを実行した。

## 固定条件

- profile: `candidate31-operation-terminal-closure-owner-producer-v5-expanded12-global-m24-n5-r1`
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
- quality rating: `owner-producer-quality-v5`
- rating contract SHA-256: `cb718bb6cf9eceeb34fadb2e6c6de0ba7cf32211f2b79139e49153997e7c8df2`
- command evidence: `the-caption-prompt.all-agent-command-evidence/v3`
- producer evidence: `the-caption-prompt.owner-producer-evidence/v1`

## 結果

- valid / rateable run: 60 / 60
- score `4`: 60
- score `3`: 0
- quality audit failure count: 0
- excluded attempt: 3
- all-agent token total: `18,453,764`
- `quality_score` median: `100.000`
- all-agent `total_tokens` median: `3,660,230`
- `elapsed_seconds` median: `1,553.428`
- result ID: `1f67e36d3d3f414d834ac186d6fc2d33`
- compatibility key: `9277d533f7875de3ca702e3b571b321960ddd2c2dc256e234b442b0f2b8bf04e`

| iteration | quality_score | total_tokens | elapsed_seconds |
| ---: | ---: | ---: | ---: |
| 1 | 100.000 | 3,660,230 | 1,528.929 |
| 2 | 100.000 | 3,804,305 | 1,676.298 |
| 3 | 100.000 | 3,621,850 | 1,695.875 |
| 4 | 100.000 | 3,809,200 | 1,524.924 |
| 5 | 100.000 | 3,558,179 | 1,553.428 |

12 caseはすべて各5 / 5でscore `4`だった。

初回dispatchの3 attemptは`codex_model_at_capacity`となった。

この3 attemptは外部要因として除外し、同じslotを再実行してvalid resultを得た。除外attemptはKPIへ含めていない。

## 旧resultとの境界

旧rating v4 result `70ecc211f8c74f769d4f136120aca52a`はscore `4 / 3 = 59 / 1`の履歴として保持する。

新rating v5 resultはcollector revisionが異なるため、旧v4 resultとcompatibility keyが異なる。

評価基盤の互換比較へ両resultを混ぜず、それぞれの固定条件下の単独resultとして扱う。

## Evidence boundary

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate31-operation-terminal-closure-owner-producer-v5-expanded12-global-m24-n5-20260718-v3-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/1f67e36d3d3f414d834ac186d6fc2d33.json`
- quality audit、Layer 4 registration、lossless archive、compact receiptまで完了した。
- 非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
- 採用、release、THE-CAPTION本体反映、runtime有効化は未判断、未実施である。
