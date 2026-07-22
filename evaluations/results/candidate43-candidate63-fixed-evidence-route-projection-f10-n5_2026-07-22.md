# Candidate43 / Candidate63 fixed evidence route projection F10 N=5

## 結論

二つのroot `AGENTS.md`全文を保守せず、Candidate43を一つの共通sourceとして、固定証拠reviewでだけ一行差分を実行前合成する構成はF10で成立した。

Candidate63は5 / 5がscore `4`、root-only、zero driftだった。5 runすべて3 top-level tool call、4 model stepへ収束した。shell commandはCandidate43と同じ55件で、取得した意味上のevidence集合も同じだった。

all-agent token合計はCandidate43 `811,578`からCandidate63 `382,228`へ`429,350`、`52.90%`減った。token中央値は`211,070`から`76,409`へ`63.80%`、elapsed中央値は`87.367秒`から`54.086秒`へ`38.09%`小さくなった。

この結果は一つのF10型case、各`N=5`の範囲に限る。Candidate63は`targeted_evaluated / route_gate_passed`とする。採用、release、本体反映は未判断、未実施である。

## 一枚構成

authoring sourceは次の二つだけである。

- Candidate43のfull bundle
- `fixed-evidence-review-r1`の一行route delta

model実行前に両者を合成し、そのrunが見るroot `AGENTS.md`は一枚にする。非対象routeではdeltaを合成せず、Candidate43 identityを選ぶ。

評価基盤は実際のmodel-visible入力をimmutableに残す必要がある。このためCandidate63の解決済みfull bundleも生成artifactとして保存した。これは保守する二枚目のauthoring sourceではない。Candidate43とroute deltaから同じbytesへ再生成できる。

- Candidate43 bundle SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- route delta SHA-256: `b1c07fa804bc172a783a52b2d6bc01c4d40fb8ee1ea6d97c81630fddee5d7d60`
- Candidate63 bundle SHA-256: `ec0408c54fad05605fcfc8250250e791e603613d2ec7e42967901d21e7292d27`
- changed target: root `AGENTS.md`だけ
- model-visible差分: `FIXED_EVIDENCE_READ`一行だけ

## 固定条件

- Evaluation set: `tc-f10-monthly-format-test-review-r3` / `r3`
- Layer 1 identity: `98da7e8c9ea12d91be50bb4d66ac15926b53a4ddee4d2035bc61bace13b01507`
- fixture identity: `a99d551dbd6113886d7b13a141e22f1947c744df7f5de2cd78ab4e2287e4ef48`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- comparison compatibility key: `cc9fcfebbc698f3f2601439eed2783fd2786082b847bd526f1c31ece4bfce083`
- excluded attempt: 0

両profileは`profile_id`と`prompt_set_identity`以外を同一にした。既存F05 / F10 setとはcase集合とfixture identityが異なるため、旧resultを同一comparison viewへ混ぜていない。

## KPI

| 指標 | Candidate43 | Candidate63 | Candidate63 - Candidate43 |
| --- | ---: | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 | 0 |
| `quality_score`中央値 | 100.000 | 100.000 | 0.000 |
| all-agent token合計 | 811,578 | 382,228 | -429,350（-52.90%） |
| all-agent token中央値 | 211,070 | 76,409 | -134,661（-63.80%） |
| `elapsed_seconds`中央値 | 87.367 | 54.086 | -33.281（-38.09%） |
| controller elapsed | 115.348 | 64.451 | -50.897（-44.13%） |

controller elapsedはcampaign並列実行の診断値であり、評価基盤の3 KPIへ追加しない。

## 実行経路

| 指標 | Candidate43 | Candidate63 | 差 |
| --- | ---: | ---: | ---: |
| top-level tool call合計 | 40 | 15 | -25（-62.50%） |
| model step合計 | 29 | 20 | -9（-31.03%） |
| shell command合計 | 55 | 55 | 0 |
| failed shell command | 0 | 0 | 0 |
| worker / SA session | 0 | 0 | 0 |

iteration順の経路は次のとおりである。

- Candidate43 tool call: `11 / 3 / 11 / 11 / 4`
- Candidate43 model step: `7 / 4 / 6 / 7 / 5`
- Candidate63 tool call: `3 / 3 / 3 / 3 / 3`
- Candidate63 model step: `4 / 4 / 4 / 4 / 4`

shell commandは両promptとも各run 11件だった。開始identity 5件、root / `src` authority、固定diff、変更file、関連engineのevidence 5件、終了status 1件である。command表記や`git show` / current file readの選択には反復差があるが、許可外path、test、edit、dependency、network、workerへのscope expansionは0件だった。

したがって、Candidate63のtoken差はevidence省略ではない。同じ11 commandを3 top-level callへ束ね、逐次context再送を減らした観測と整合する。単一case `N=5`のため、因果を範囲外へ一般化しない。

## Route gate

事前に定めたgateはすべて満たした。

1. Candidate63は5 / 5がvalid、rateable、score `4`だった。
2. 5 runすべて3 top-level tool callだった。
3. shell command 55件と固定evidence範囲を維持した。
4. Candidate43よりtoken合計と中央値が小さかった。
5. base + route deltaから解決済みbundleをbit-for-bit再生成できた。
6. F05、A02、A06型の非一致factsはCandidate43 identityを選び、Candidate63をmaterializeしない機械契約を通過した。

第6項は非対象taskをCandidate63で実行したbehavioral evidenceではない。非対象promptへdelta bytesを渡さないselector契約の検証である。

## 最初の不成立campaign

初回は既存F05 / F10 Layer 1からF10だけを実行した。Layer 2とLayer 3は各5 runを完了したが、Layer 4はfrozen setのF05未実行を検出し、`prompt set must cover every frozen case and iteration`でfail-closedした。

この二つはresult registryへ登録せず、正式比較へ使っていない。

- Candidate43 diagnostic campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate43-outcome-authority-boundary-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-20260722-r1`
- Candidate63 diagnostic campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate63-fixed-evidence-route-projection-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-20260722-r1`

F10だけの新しいLayer 1をfreezeし、両promptを同じidentityで再実行した正式resultだけを以下へ登録した。

## 判断と次の対象

一枚の共通promptへ適用条件とmethodを同居させるC62方式は、methodがA02へ流入した。一方、Candidate63はmethod bytes自体を非対象promptから外す。この構造差により、A / F境界をprompt内の否定条件へ依存させずに済む。

今回確認できたのは、F10型の固定証拠reviewでは一行deltaが短経路を安定させ、保守対象の全文を二枚にしなくてよいことまでである。汎用selectorの成立は未確認である。

次は、F10とは異なる二つ目の固定証拠review caseを用意し、同じroute factsと一行deltaで`N=5`を再現できるかを確認する。その後、既存task contractからroute factsを安全に確定できない場合は必ずCandidate43へ戻る外部selectorを検証する。利用者に細かな実行方法を書かせることや、case labelのA / Fをroute条件にすることは対象にしない。

## 登録証跡

- Candidate43 result ID: `6965832090ad4b1b8507c7c8496dc1c5`
- Candidate43 result content SHA-256: `7b08f0ae70c79e41f6c96a4471ba483c7878cf1271ce079a7dc3f9446ab7acb0`
- Candidate43 execution archive SHA-256: `4f1ea04a29a8e01141985ff311b1f0d82631677fe89511d7825448f6cce9c99f`
- Candidate63 result ID: `96b5d896fbc248b9b3aacdd351795c06`
- Candidate63 result content SHA-256: `5e111b1248dcdcf0c8b31b2514830b0d3688963493ef11d265c1f9496a1e8215`
- Candidate63 execution archive SHA-256: `6f48f4948542ff8dd2189826e590a445ecfc5d8b4796c19e384cf7167f266cb5`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate63-fixed-evidence-review-f10-n5-20260722-r1.json`
- Candidate43 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate43-outcome-authority-boundary-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-20260722-r2`
- Candidate63 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate63-fixed-evidence-route-projection-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-20260722-r2`

