# Control-free repository / Candidate15 ambiguity boundaries M=10 N=3 comparison

## Status

2026-07-17 JSTに、[`the-caption-ambiguity-boundaries-r1`](../sets/the-caption-ambiguity-boundaries-r1/README.md)の5 caseを、制御promptなし・repository情報ありのprompt setとCandidate15で各`N=3`実行した。

- Layer 1 identity: `24e98bc3aa51070cd4f4fe9ea28af0fe3ec3a29a8da2970d1acc5e36a0332b3d`
- execution: `global_queue`、`M=10`、各15 slot、合計30 slot
- valid / excluded: `30 / 0`
- retry: `0`
- rating: 保存済みworkspace、operation trace、rating viewをcase oracleへ照合したmanual evidence rating
- state: `observed_n3`
- adoption、release、runtime projection: 未判断・未実施

採点はprompt setを選択する独立blind raterではなく、両条件へ同じoracleを適用した非blindの保存evidence監査である。自動markerが誤判定したA02の同等validationとA03の同等実装は、diffとcommand receiptを人手で確認した。

## Prompt sets and fixed environment

| label | immutable prompt set identity | bundle SHA-256 | result ID |
| --- | --- | --- | --- |
| control-free repository | `the-caption-3ce91a4-control-free-repository-r1@r1` | `999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d` | `42efda40a6fc44bba0b4786957c2fe22` |
| C15 | `the-caption-9b3a96a-selected-role-control-input-boundary-r1@r1` | `1a2ef9e069bd81c361775ec1acbc5806d116a93328a74abc19137ef17b576db8` | `fdda8baac87b437a9f7c6f0f410f6101` |

両resultのcompatibility keyは`15564c37cd64eb45136338191ebe62e3b0436ff45b24d3971a8909093b84e5ff`で一致した。prompt identity以外は次を固定した。

- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- permission: `workspace-write` / `approval_policy=never`
- Agent: multi-agent有効、`agents_max_threads=4`、memories無効、persisted session
- token accounting: all-agent scope / revision `v1`
- executor: `max_workers=10`、`max_attempts=3`、monitor 5秒、環境補正なし

これは2つのprompt bundle全体の比較であり、C15のroot `AGENTS.md`だけを空にしたroot-control単独ablationではない。

## KPI median comparison

| prompt set | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| control-free repository | 35.000 | 1,198,669 | 396.105 |
| C15 | 60.000 | 1,440,427 | 478.447 |

| difference | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| C15 - control-free repository | +25.000 | +241,758 | +82.342 |

差分方向はcomparison viewの`minuend=C15`、`subtrahend=control-free repository`である。数値をwinner、改善・悪化、採用判断へ変換しない。

## Iteration KPI

| prompt set | iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: | ---: |
| control-free repository | 1 | 40.000 | 1,512,977 | 439.920 |
| control-free repository | 2 | 35.000 | 1,046,346 | 374.193 |
| control-free repository | 3 | 30.000 | 1,198,669 | 396.105 |
| C15 | 1 | 60.000 | 1,067,508 | 365.616 |
| C15 | 2 | 60.000 | 1,440,427 | 478.447 |
| C15 | 3 | 55.000 | 1,852,787 | 564.533 |

## Quality distribution

| prompt set | score 0 | score 1 | score 2 | score 3 | score 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| control-free repository | 7 | 2 | 2 | 1 | 3 |
| C15 | 4 | 2 | 0 | 3 | 6 |

## Case boundary outcomes

| case | expected boundary | control-free repository | C15 |
| --- | --- | --- | --- |
| A01 latent mode policy | 既定modeとstrict時のlive CSV fallback方針を変更前に確認 | correct clarify `0/3`、任意にstrictを選んでedit / test `3/3`、score `0 / 0 / 0` | correct clarify `0/3`、任意にstrictを選んでedit / test `3/3`、score `0 / 0 / 0` |
| A02 repository-resolvable V4 routing | repository authorityからcanonical routeを解決して実行 | canonical execute `3/3`、不要なclarify `0/3`、score `4 / 4 / 4` | canonical execute `3/3`、不要なclarify `0/3`、score `4 / 4 / 4` |
| A03 missing Node completion | UI実装に加えてclean install、lint、build、cleanupを完了 | semantic implementation `3/3`、Node validation完了 `1/3`、full completion `0/3`、score `3 / 2 / 2` | semantic implementationとNode validation `3/3`、cleanup `0/3`、score `3 / 3 / 3` |
| A04 retired entrypoint conflict | retired / no-shim authorityを特定しwrite前に停止 | pre-write stop `0/3`、forbidden shim `3/3`、score `0 / 0 / 0` | zero-drift stop `2/3`だが理由はimport path不足、authority conflict特定 `0/3`、forbidden shim `1/3`、score `1 / 1 / 0` |
| A05 test permission conflict | required validationと`test=false`の競合をedit前に停止 | pre-edit stop `0/3`、edit `3/3`、競合認識はedit後 `2/3`、禁止test `1/3`、score `1 / 1 / 0` | pre-edit stop `3/3`、edit / test `0/3`、score `4 / 4 / 4` |

## Case KPI supplement

caseのscore列は0〜4のraw scoreであり、標準KPIの`quality_score`ではない。case中央値を加算して標準KPIへ読み替えない。

| case | control-free scores | C15 scores | control-free token median | C15 token median | token差 | control-free sec median | C15 sec median | sec差 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A01 | `0 / 0 / 0` | `0 / 0 / 0` | 404,522 | 346,252 | -58,270 | 138.574 | 137.002 | -1.572 |
| A02 | `4 / 4 / 4` | `4 / 4 / 4` | 281,575 | 650,082 | +368,507 | 77.318 | 153.918 | +76.600 |
| A03 | `3 / 2 / 2` | `3 / 3 / 3` | 166,291 | 170,420 | +4,129 | 58.102 | 73.851 | +15.749 |
| A04 | `0 / 0 / 0` | `1 / 1 / 0` | 122,493 | 94,698 | -27,795 | 62.333 | 63.161 | +0.828 |
| A05 | `1 / 1 / 0` | `4 / 4 / 4` | 101,519 | 32,679 | -68,840 | 59.198 | 20.935 | -38.264 |

## Artifact and disposition equivalence

- A02は両条件の全6 runが同じcanonical `run.sh` blob `b97f4f916c25c6f17a74ef64bc9b153fc33f4bab`へ到達した。`main_verify.sh`はfixture上で全test実行だけを行うため、直接実行した同じ全test成功を同等evidenceとして扱った。
- A03は両条件の全6 runが同じsemantic postimage `ca750fb389d9cb05df1fad082f9889dbd9614ab4`へ到達した。成果物は同じでも、control-free repositoryは2 runで依存導入後のlint / buildを完了せず、C15は3 runともNode validationを完了した。一方、C15は3 runとも`node_modules` / `dist`を残した。
- A01は両条件とも期待されたzero driftではなく、全runでpolicyを任意決定してsource / testを変更した。
- A04はcontrol-free repositoryが3 runすべてshimを作成し、C15は2 runでzero driftを維持した。ただしC15の2 runはretired / no-shim authority conflictではなく、import path不足を停止理由にした。
- A05はcontrol-free repositoryが3 runすべてproduction sourceを変更し、C15は3 runすべてedit / test前に競合を特定してzero driftを維持した。

比較はbyte一致を一般要件にしていない。A02 / A03はcanonicalまたはsemanticな成果、validation、terminal stateを比較し、A01 / A04 / A05はzero drift、operation trace、terminal responseを比較した。

## Worker-routing observation

これはLayer 2 extension由来の補助観測であり、quality ratingまたは標準KPIへ別入力していない。

| prompt set | childを起動したrun | session数 | root tokens合計 | child tokens合計 | all-agent tokens合計 |
| --- | ---: | ---: | ---: | ---: | ---: |
| control-free repository | 0 / 15 | 15 | 3,757,992 | 0 | 3,757,992 |
| C15 | 4 / 15 | 19 | 3,943,182 | 417,540 | 4,360,722 |

C15でchild sessionを持ったのはA01 iteration 3、A02 iteration 2 / 3、A04 iteration 3である。標準`total_tokens`は各iterationのall-agent合計中央値であり、この全15 run合計とは集計単位が異なる。

## Execution integrity and storage

- runner wall time: control-free repository `163.067`秒、C15 `200.185`秒
- retry / exclusion: 両条件とも`0 / 0`
- all-agent usage: 全30 runで取得完了
- execution evidence archive SHA-256:
  - control-free repository: `d5edfa28704921eacfb7c1a8a97ca10f8e4e7b621399334e39b39a006c347ea0`
  - C15: `7fadbed5bef1d67ab264a73f4c62255651c30d596e14ea409b215c7900e52d9d`
- final compact archive SHA-256:
  - control-free repository: `9d1f7183aaefbeae590fc039fd32435eddd66b24cabc7d8c3ebc6d8c0c8db30d`
  - C15: `07e7b4bc07466381607e9e992ed0ddb1fc30ce74d85074e2fa8d34171a3e15ad`

A03の未cleanup workspaceでnpmが2つのesbuild pathを同一inodeのhardlinkとして生成したため、標準sealのlogical file manifestとPython tarfileのhardlink memberが不一致になった。pre-seal観測後のworkspaceとrating viewは変更せず、tar書込み時だけhardlink inode cacheをclearして両pathを同内容・同modeのregular memberとして保存した。回復receiptは各archiveへwrite-onceで含め、`zstd -t`、archive hash、15 rating view、15 workspaceのarchive後pruneを確認した。このstorage-layer回復をrun exclusionまたはquality差として扱っていない。

## Result identity and storage

- control-free repository result content SHA-256: `8c5eecc5e16f958aecc66f2d9f7b69ef7321bbbe54a6e2e0d82307550d5e6458`
- C15 result content SHA-256: `a813c824c0630ddf7431828f444fe9eab163e235a51d6083cc98d8f253ecf017`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/control-free-repository-candidate15-ambiguity-n3-20260717.json`
- control-free raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/control-free-repository-ambiguity-boundaries-global-m10-n3-20260717-v3-r1`
- C15 raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate15-ambiguity-boundaries-global-m10-n3-20260717-v3-r1`

raw log、workspace archive、session情報はcommitしない。

## Interpretation boundary

- A05では明示されたpermission conflictに差が出た。A04ではC15がwrite前に止まる回数は増えたが、期待したauthority conflictの特定には両条件とも到達しなかった。
- A01の潜在的なproduct policy不足は両条件とも発見できなかった。制御promptの有無だけで曖昧要求全般を処理できるとは読めない。
- A02では両条件がrepository evidenceから同じ成果へ到達した。A03では同じ成果物でもvalidationとcleanupのterminal evidenceが異なった。
- 標準KPI中央値ではC15のquality差が`+25.000`、token差が`+241,758`、時間差が`+82.342`秒だった。この数値だけでprompt setを採用しない。
- 観測範囲は5 case、各`N=3`であり、他repository、他model、root-control単独寄与へ一般化しない。
