# Candidate21 / Candidate22 owner worker targeted check

## 目的と範囲

Candidate20の連続試験で`owner_producer_evidence_inadmissible`となった4 caseに対し、owner固定criterionをrequired worker起動とcompleted producer resultへ接続したCandidate21と、実child lifecycleを追加で固定したCandidate22を確認する。

本書は4 case、各`N=5`のpartial-set diagnostic evidenceであり、expanded 12 caseのLayer 4 resultへ登録しない。winner、採用、release、THE-CAPTION本体反映、runtime有効化は判断・実施しない。

## 固定条件

- cases: `TC-F05-CLARIFY-UNITS-MODE`、`TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY`、`TC-F07-DEPENDENCY-PROVENANCE-PAIR`、`TC-F10-MONTHLY-FORMAT-TEST-REVIEW`
- repetition: 各case `1..5`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- evaluation set: `the-caption-revision-2-expanded12-r1` / `r1`
- model: `gpt-5.6-sol`、reasoning effort `high`
- Agent: Codex CLI `0.144.0`、multi-agent enabled、`agents.max_threads=4`、memories disabled
- permission: `workspace-write`、approval `never`
- executor: global queue、最大`M=24`、max attempts `3`
- token accounting: all-agent `v1`
- quality rating: `owner-producer-quality-v1`

Evaluation set、fixture、TaskSpec、permission、adapter、rating contractはCandidate20のowner-producer expanded `N=5`から変更していない。targeted cycle間で異なるのはprompt identityだけである。

## Candidate21

- prompt identity: `the-caption-9b3a96a-required-owner-result-gate-r1`
- bundle SHA-256: `444fd1e751cd791320744736da1921365309b5846a32390494b248dc9d08ed77`
- direct source: Candidate20
- changed target: root `AGENTS.md`のみ
- valid runs: 20 / 20
- score `4 / 3`: `19 / 1`
- owner producer eligible: `19 / 20`
- all-agent `total_tokens`合計: `3,866,979`
- controller elapsed: `176.456`秒

F05 clarification、F05 out-of-scope、F10 monthlyは各5 / 5、F07 dependencyは4 / 5でowner producer resultが成立した。F07 dependency iteration 3は成果とstatic validationを完了し、root responseも独立checkを実施したと記述したが、実child sessionは存在しなかった。receiver未確定のwait後にrootが`contract_stop=0`を自己申告したため、`owner_producer_evidence_inadmissible`のscore `3`とした。

## Candidate22

- prompt identity: `the-caption-9b3a96a-owner-worker-lifecycle-gate-r1`
- bundle SHA-256: `3f6fd7f60f9eb043eaaa88e9d498ccea7563ae7372a5190bea7737c75e6c20a5`
- direct source: Candidate21
- changed target: root `AGENTS.md`のみ
- valid runs: 20 / 20
- score `4 / 1`: `19 / 1`
- owner producer eligible: `20 / 20`
- `owner_producer_evidence_inadmissible`: `0`
- all-agent `total_tokens`合計: `3,511,007`
- controller elapsed: `166.818`秒

4 caseすべて5 / 5で、active executorとは別thread、rootをparentとするowner対応producerがcompleted final resultを返した。Candidate20連続試験のscore `3`原因だったowner producer evidence不足は、この20 runでは観測されなかった。

F10 monthly iteration 4はowner producer result自体は成立したが、active executorが開始identityを不一致と誤認してreviewを実施しなかったためscore `1`とした。これはCandidate20でも観測済みの開始identity解釈に関する別原因であり、owner producer evidence不足へ読み替えない。

## 判断境界

- Candidate21はowner worker起動を大幅に増やしたが、root自己申告を実child resultへ変換できる余地が1件残った。
- Candidate22はtargeted 20 runでowner producer eligibility 20 / 20を満たし、このtargeted観測時点でScore 3対応の次gateである同一条件expanded 12-case `N=5`へ進む根拠を得た。後続観測は[`Candidate20 / Candidate22 expanded result`](candidate20-candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)へ分離する。
- Candidate22の採用、release、runtime projectionは未判断である。

## Raw evidence

- Candidate21: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate21-required-owner-result-gate-targeted-owner-cases-n5-20260717`
- Candidate22: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate22-owner-worker-lifecycle-targeted-owner-cases-n5-20260717`

非公開raw run log、session情報、一時workspaceはrepositoryへcommitしない。
