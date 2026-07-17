# Candidate22 / Candidate24 prompt-only owner result gate expanded 12-case N=5

## Status

- run date: `2026-07-17`（Asia/Tokyo）
- valid run window: `2026-07-17T16:27:37+09:00`から`2026-07-17T16:33:57+09:00`
- Candidate24 profile: `candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5-r1`
- Evaluation set: `the-caption-revision-2-expanded12-r1` / `r1`
- execution: expanded 12 case、`N=5`、`global_queue`、`M=24`
- quality rating: `owner-producer-quality-v1`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- adoption / release / THE-CAPTION本体反映: 未判断、未実施

Candidate24はCandidate23を直接sourceとし、root `AGENTS.md`だけへprompt-onlyの`owner_result_ready` AND predicateを追加した。Candidate22の保存済みresultと同じEvaluation set、fixture、TaskSpec、model、Agent環境、permission、executor parameter、rating revisionで新規実行し、保存済み2 resultから比較viewを生成した。

## Prompt set and fixed environment

- Candidate22: `the-caption-9b3a96a-owner-worker-lifecycle-gate-r1` / `3f6fd7…c20a5`
- Candidate24: `the-caption-3ce91a4-control-free-owner-result-gate-r1` / `8f3793…9488b`
- Candidate24 direct source: `the-caption-3ce91a4-control-free-operation-boundary-r1`（Candidate23）
- Candidate24 changed target: root `AGENTS.md`だけ
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`
- compatibility key: `46787dae7e03a4f182915b5eff62c17f40673d8d08ae86fdaf2cfb88284a72c8`

## KPI median comparison

| prompt set | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| Candidate22 | 100.000 | 4,904,017 | 1,746.454秒 |
| Candidate24 | 100.000 | 4,629,700 | 1,527.950秒 |
| Candidate24 - Candidate22 | 0.000 | -274,317 | -218.504秒 |

KPI差は保存済みLayer 4 comparison viewの数値であり、winner、改善・悪化、採用判断へ変換しない。

## Quality and owner-producer distribution

| prompt set | score `4` | score `3` | score `1` | owner-producer eligible |
| --- | ---: | ---: | ---: | ---: |
| Candidate22 | 58 | 2 | 0 | 58 / 60 |
| Candidate24 | 60 | 0 | 0 | 60 / 60 |

Candidate24は12 caseすべてで各5 runがscore `4`となり、owner固定criterionを持つ11 caseも各5 / 5でadmissible producer resultが成立した。Candidate22で残った2件はいずれもF10 monthlyのchild session / child final result不足だったが、Candidate24では同経路を観測しなかった。

## F10 monthly observation

| prompt set | score分布 | owner producer成立 | token中央値 | elapsed中央値 |
| --- | --- | ---: | ---: | ---: |
| Candidate22 | `4`: 3、`3`: 2 | 3 / 5 | 196,294 | 112.138秒 |
| Candidate24 | `4`: 5 | 5 / 5 | 239,213 | 95.092秒 |

Candidate24の5 runはすべて次を満たした。

- root rolloutに`/root/independent_response_check`のspawn resultがある。
- spawn後にtimeoutではないcompleted waitが1回ある。
- active executorと別thread identityのchild sessionが存在する。
- child自身の`task_complete` final resultが存在する。
- child resultが固定diffのmajor finding、`src/app/entrypoints/monthly_main.py:25`、`--format-test`と`--force`のbehavior impactを返す。
- zero driftで終了する。

F10 monthlyのscore `3`はCandidate22の2 / 5からCandidate24の0 / 5になった。開始identityの誤認によるscore `1`もこのN=5では0件だった。

## Residual boundary

この観測はprompt-only制御が60 run、特にF10 monthly 5 runで所定のchild lifecycleを成立させたことを示すが、runtimeによる物理的強制ではない。`owner-producer-evidence/v1`は実child identity、direct parent、role path、task completion、non-empty final resultを確認する一方、waitのreceiver identityやcriterion ID全文の明示をscore `4`必要条件にしていない。

F10 monthlyでは5 / 5に実child、completed wait、child final resultがあり、全child resultが対象findingを意味上bindしたが、criterion ID `F10-R-C1 / C2`を文字列として明示したresultは1 / 5だった。したがって、N=5の範囲外へ完全保証を一般化しない。

## Result identity and storage

- Candidate22 result ID: `d0e6649eeaef43cbb4f501285982ee91`
- Candidate24 result ID: `e6ea1e2c56054c6cb8774e32fddb17f6`
- Candidate24 result content SHA-256: `c79f2d07ff39e45628693a9ed699842ede9b4c33ac00a0f2c54570a965f67361`
- raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5-20260717-v3-r1`
- registry result: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/e6ea1e2c56054c6cb8774e32fddb17f6.json`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate22-candidate24-owner-producer-v1-expanded12-n5-20260717.json`

raw evidence、session情報、一時workspaceはrepositoryへcommitしない。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。
