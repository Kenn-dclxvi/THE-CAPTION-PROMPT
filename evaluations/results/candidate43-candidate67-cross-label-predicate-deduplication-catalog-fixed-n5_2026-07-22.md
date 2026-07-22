# Candidate43 / Candidate67 cross-label predicate deduplication catalog固定 N=5

## 結論

Candidate67はCandidate43を直接sourceとし、root `AGENTS.md`の9 labelと順序を維持したまま、別labelへ重複していた二つの文だけを正本labelへ集約した。root bytesは`3,980 -> 3,792`、`-188`、`-4.72%`である。

F10-only、A01 / A02、F05 / F10、明示producer D01の30 runでは、Candidate67のscore分布は`4 / 3 = 29 / 1`だった。対応するCandidate43の保存結果も`29 / 1`である。A / Fはroot-only、D01は5 / 5でTaskSpec指定workerだけがreview対象を読んだ。二つの重複文を削除したことによる意味欠落は、この観測範囲では確認しなかった。

一方、runtime削減は再現しなかった。最初のF10-onlyはtoken合計`-10.32%`でgateを通過したが、追加F set内のF10は`+13.03%`、D01は`+7.24%`だった。A scope全体は`-1.31%`、F scope全体は`+1.65%`である。

したがって、Candidate67は`targeted_evaluated / stopped`とする。二つの重複predicateを一か所へ統合できる意味証拠として保持するが、runtime効率候補、採用候補、release候補へ進めない。Candidate43を参照promptとして維持する。

## 静的差分

- 直接source: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate67: `the-caption-3ce91a4-cross-label-predicate-deduplication-r1`
- Candidate43 bundle SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- Candidate67 bundle SHA-256: `0676b5c34f3fa68e71984f28fa0fc49938fde5b3ee822fe4cffa7522b6bcce87`
- changed target: root `AGENTS.md`だけ
- label: `SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / METHOD / RECOVERY`を同じ順序で保持
- root bytes: `3,980 -> 3,792`、`-188`、`-4.72%`

削除した文と正本は次の二組である。

| 意味 | 削除元 | 正本 |
| --- | --- | --- |
| TaskSpecが独立producer executionを明示した場合だけ委譲する | `PRODUCER`の短い再記述 | `OWNER_ROLE`のowner境界、task identity binding、predicate前spawnを含む全文 |
| 同一predicateを別producerへ再割当てしない | `INDEPENDENCE`の短い再記述 | `PRODUCER`のoperation単位、順次・並行を含むsingle producer全文 |

残りの本文はCandidate43と逐語一致である。`F5 / F9`、`D6`、`R1 / R2`、label構成、route、permissionは変更していない。

## 固定条件

- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- memories / apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- repetition: 各case `N=5`
- excluded attempt: 0

各Candidate67 profileは、対応するCandidate43 profileから`profile_id`と`prompt_set_identity`だけを変更した。scope間はEvaluation setとcompatibility keyが異なるため、各scope内だけで比較する。

| scope | Layer 1 identity | compatibility key |
| --- | --- | --- |
| F10-only | `98da7e8c9ea12d91be50bb4d66ac15926b53a4ddee4d2035bc61bace13b01507` | `cc9fcfebbc698f3f2601439eed2783fd2786082b847bd526f1c31ece4bfce083` |
| A01 / A02 | `9814b0a53807151e8d4a4f2bf5d089a765e0c9efc66888f77d22616fc98dd8b5` | `5c1cc7a1844a073f074ca57aca27f601f5a3a184523d4c30dafbb3b46bb872b2` |
| F05 / F10 | `1e24a2074f52483fb83f6e477c829f7d51bb66600412bb6f899066094256dd90` | `f4802b4ba17db5480070526a3370c8ca7e21facfc3bd8e38f4421ca42b7bc12a` |
| D01 | `4b36be3a9fd5c89bb7ea3cf9e1b150e9cd5d83eab632db055ec6044161ee998e` | `4a8e61d6c314a12b30650bb3c64edb49c80938a8f3d2cb77eb9f5874817000b1` |

## 測定定義の訂正

作成前gateはCandidate66結果記録からF10-onlyのshell commandを`55`と転記した。immutableなCandidate43 execution archiveと`all-agent-command-evidence/v5`を再照合すると、実値は各run 10件、合計`50`である。Candidate67も同じ`50`だった。gateの目的である「同じcommand集合を維持」は成立し、判定前に数値を`50`へ訂正した。

同じ記録の`model step=29`はrolloutの`response_item.reasoning`数と一致し、`token_count` event数`46`とは一致しない。Candidate67は同じ数え方で`26`、`token_count` eventは`40`である。本書では曖昧な`model step`という語だけを使わず、`reasoning item`と`token_count event`を別々に記録する。

この訂正はprompt、Layer 1、result、rating、token accountingを変更しない。保存archiveから導く診断値の名称とcommand総数だけを訂正する。

## 最初のF10-only gate

| 指標 | Candidate43 | Candidate67 | Candidate67 - Candidate43 |
| --- | ---: | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 | 0 |
| top-level tool call | 40 | 35 | -5（-12.50%） |
| reasoning item | 29 | 26 | -3（-10.34%） |
| token_count event | 46 | 40 | -6（-13.04%） |
| shell command | 50 | 50 | 0 |
| token合計 | 811,578 | 727,855 | -83,723（-10.32%） |
| token中央値 | 211,070 | 150,603 | -60,467（-28.65%） |
| elapsed中央値 | 87.367秒 | 89.280秒 | +1.913秒（+2.19%） |

Candidate67のiteration順tool callは`3 / 11 / 3 / 7 / 11`、reasoning itemは`4 / 5 / 4 / 5 / 8`だった。5 runはすべてroot-only、zero driftで、各runが同じ10 commandを実行した。事前上限を超えなかったためA / F / Dへ進んだ。

## A / F / DのKPI

| scope | score `4 / 3` C43 | score `4 / 3` C67 | token合計 C43 | token合計 C67 | C67 - C43 | 反復別token中央値 C43 | C67 | elapsed中央値 C43 | C67 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 / A02 | 10 / 0 | 10 / 0 | 2,186,911 | 2,158,319 | -28,592（-1.31%） | 452,817 | 453,024 | 141.235秒 | 153.719秒 |
| F05 / F10 | 9 / 1 | 9 / 1 | 1,179,045 | 1,198,460 | +19,415（+1.65%） | 241,405 | 242,570 | 118.825秒 | 128.047秒 |
| D01 | 5 / 0 | 5 / 0 | 1,318,767 | 1,414,252 | +95,485（+7.24%） | 272,781 | 274,239 | 138.809秒 | 139.017秒 |

case別では、削減と増加が分かれた。

| case | token合計 C43 | token合計 C67 | token差 | elapsed中央値 C43 | elapsed中央値 C67 |
| --- | ---: | ---: | ---: | ---: | ---: |
| A01 | 538,947 | 434,185 | -104,762（-19.44%） | 46.149秒 | 39.499秒 |
| A02 | 1,647,964 | 1,724,134 | +76,170（+4.62%） | 98.260秒 | 112.637秒 |
| F05 | 330,657 | 239,532 | -91,125（-27.55%） | 33.201秒 | 27.765秒 |
| F10 | 848,388 | 958,928 | +110,540（+13.03%） | 85.624秒 | 90.050秒 |
| D01 | 1,318,767 | 1,414,252 | +95,485（+7.24%） | 138.809秒 | 139.017秒 |

## 保存traceの実行形

| case | tool call C43 -> C67 | reasoning item C43 -> C67 | token_count event C43 -> C67 | shell command C43 -> C67 |
| --- | ---: | ---: | ---: | ---: |
| A01 | 19 -> 18 | 24 -> 23 | 24 -> 23 | 19 -> 22 |
| A02 | 46 -> 45 | 51 -> 53 | 51 -> 50 | 47 -> 64 |
| F05 | 17 -> 11 | 14 -> 12 | 22 -> 16 | 20 -> 20 |
| F10 | 43 -> 48 | 28 -> 29 | 48 -> 53 | 50 -> 51 |
| D01 | 66 -> 69 | 56 -> 58 | 77 -> 79 | 54 -> 44 |

追加F10は最初のF10-onlyと逆方向だった。短い3-call routeは1 / 5で、残り4 runは11〜12 callだった。したがって、二つの重複文削除が短経路を安定化したとはいえない。

A01は5 / 5で未固定値を推測せず、変更と試験の前に確認して停止した。A02は5 / 5でrepository authorityから起動先を解決し、要求成果と試験を満たした。10 runはroot-onlyだった。A02のcommandは`47 -> 64`へ増えたため、A scope合計tokenの微減だけを効率化と判断しない。

D01は5 / 5で次を満たした。

1. sessionはrootと指定workerの2つだった。
2. rootは`monthly_format_review_producer`を1回だけspawnした。
3. review対象diff、`monthly_main.py`、`monthly_engine.py`の読取りはworkerだけが行った。
4. rootのreview対象readは0件だった。
5. response、zero drift、許可範囲を満たした。

D01のroot token合計は`554,833 -> 411,785`、`-25.78%`、child token合計は`763,934 -> 1,002,467`、`+31.22%`だった。all-agent合計は`+7.24%`である。正しい分担は維持したが、child側costが増えた。

標準`owner-producer-evidence/v1` collectorはC43とCandidate67の両方を5 / 5で`inadmissible`とした。Candidate67の`all-agent-command-evidence/v5`は18件を`missing_machine_bound_exit_code`として報告し、C43は6件だった。保存rolloutでは各commandの実行と終了statusを確認でき、quality auditのfailureにはならない。これは診断上の警告として保持し、正式owner eligibilityへ読み替えない。

## 判断と次の対象

Candidate67から確定できる範囲は次のとおりである。

1. 明示委譲gateは`OWNER_ROLE`一か所に残しても、D01の指定worker境界を5 / 5で維持した。
2. producer再割当て禁止は`PRODUCER`一か所に残しても、A / Fのroot-onlyとD01のsingle workerを維持した。
3. 二つの重複文削除による成果品質の低下は、30 runでは観測しなかった。
4. F10とD01のtoken増加があるため、runtime効率改善は確認しない。
5. Candidate67へ補助predicateを追加せず、standard14、採用、release、本体反映へ進めない。

次の意味単位を試す場合はCandidate43へ戻り、`F9`の「先行result / artifactの独立確認を別operationへ固定する」一文だけを対象にする。`F5`、`D6`、`R1 / R2`や今回の二つの削除を同じcandidateへ混ぜない。個別削除の意味証拠が揃った後にだけ、統合bundleを別candidateとして検討する。

## 登録証跡

| scope | prompt | result ID | result content SHA-256 | execution archive SHA-256 |
| --- | --- | --- | --- | --- |
| F10-only | Candidate43 | `6965832090ad4b1b8507c7c8496dc1c5` | `7b08f0ae70c79e41f6c96a4471ba483c7878cf1271ce079a7dc3f9446ab7acb0` | `4f1ea04a29a8e01141985ff311b1f0d82631677fe89511d7825448f6cce9c99f` |
| F10-only | Candidate67 | `1c872681ce9742bf913947ccf168ceec` | `ce67fd8fbdbfc4431ee785fe736a96a306eee7da53595225364b835c55c48c2b` | `9c70815906c9ae2736c840f5c2222cfa124b0b887b0d8bb1d4b1de10c41372a9` |
| A | Candidate43 | `c9c2d55acbd944a2a7026457aa1d6efd` | `77743feeb4c04bd7d32d73bb2feec82402e93641a5a9487e81ef235efd5a7a7f` | `441b10aac8cff899fe3ea5d608efecff2aec32ab51d825c478fcbfb7dfcac56f` |
| A | Candidate67 | `dd8a88b26379492987a1ae561f2899cd` | `d6b0f35c30336a9f28e928d2daef0f5d0192a931571dc8b43a7b7d6b8c4e3aed` | `35849b29a742aa8c6d3072d7714ddcf1f976d5ea209fbfd908849296f73c1da5` |
| F | Candidate43 | `53f46f39073c4bf1aa1d7dc8fbc4b892` | `1c91cd9edaf8b47776c63f2e69bc9c47260fb1476a821eb185fded5011c69a96` | `6aaac40bc057662c41187197a8eed7df91cfa720eb650fe5fc23471bf85be595` |
| F | Candidate67 | `61ae262f36de4f019aa3eabfbc5a113e` | `7a84e8997161f47d4ec03ab4e51003cee04d77ba720f4646ac42384261c9c318` | `911041369e0df1ff8872c390dc5064cb62a9967b0f3c44207f83804dd94a8d65` |
| D | Candidate43 | `66f795a48d584249acd96d9e4383d89a` | `2de3b06c777ccd197111ecb94fee41690b53b9376a322c914ec0f4baed73e179` | `74f8f1a08a42c23d4dedc9d6c80c8b9b4546b937ec8589898b94fb239ff828be` |
| D | Candidate67 | `d81df65fb23145b1b94db40badc857be` | `06617631d4ff3eeb4b73cd78ba0d22a2eb17a449156e830d8b3b666333124b81` | `998e2151f34095d801fbfba665607ddf80e638ea603c32ded8f5067aff73d27d` |

comparison views:

- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate67-cross-label-predicate-deduplication-f10-n5-20260722-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate67-cross-label-predicate-deduplication-a01-a02-catalog-fixed-n5-20260722-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate67-cross-label-predicate-deduplication-f05-f10-catalog-fixed-n5-20260722-r1.json`
- `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate67-cross-label-predicate-deduplication-d01-catalog-fixed-n5-20260722-r1.json`

Candidate67の採用、release、本体反映は未判断、未実施である。
