# Candidate35 B18 v8 saved-evidence replay

## 結論

Candidate35 B18の保存済みv7 evidence 1,080 runを、修正したcommand collectorと採点policyで診断replayした。projected score分布は`4 / 3 / 2 / 1 = 1075 / 5 / 0 / 0`、全run合算qualityは`99.8843%`である。

これは新しい公式resultではない。v7 resultを変更せず、F04 r2を含むv8 profileの新規実行前に、試験側の誤判定と残存するcandidate側観測を分離する診断artifactである。

## Replay delta

| 修正対象 | v7観測 | v8 replay | 件数 |
| --- | --- | --- | ---: |
| command evidence収集 | successful commandのformat差を欠落扱い | quoted key、`exit_status`、固定配列loop、明示statusを一意にbind | Score 3から4へ24件 |
| changed path判定 | source-only固定一覧にない許可済みtest fileを不一致扱い | adapterの`unexpected_changed_paths=[]`を許可上限のSSOTとし、必須source pathだけ確認 | Score 2から4へ6件 |
| F10 review判定 | 正しいmajor findingの1行ずれをreview未実施扱い | finding内容と位置精度を分離 | Score 1から3へ1件 |
| F04 cleanup | modelが削除できなかったtemporary outputをcandidate qualityへ算入 | 保存済みr1は変更せずScore 3を維持。新規F04 r2ではadapter-owned teardownへ移管 | replay上の移動なし2件 |

## 残るScore 3

- `9e984e990eb542e9a9ea3ad6877b75ac`: `git diff --name-only`の出力はあるが、保存済みtextにcommandと成功exitを一意にbindできない。過去v7 replayではScore 3を維持する。新規v8 runで同型が発生した場合は`command_evidence_incomplete`として除外・再試行し、Scoreへ入れない。
- `a006fe87ae86408a8155b53c1a71b468`: `bash -n run.sh`の実行証跡そのものがない。
- F04 r1の2件: cleanup責務を含む過去case revisionのため、replayで採点条件を書き換えない。
- `46c2e073ff3248f5830bb610ee4b6763`: `format_test=args.force`というmajor findingは正しいが、報告位置が`:26`で実変更行`:25`と1行ずれた。

## Path判定の根拠

旧Score 2の6件はすべて、必須source pathに加えてTaskSpecが許可したtest pathを変更していた。各runのadapter validationは`unexpected_changed_paths=[]`だった。Layer 3のsource-only固定一覧が同じ許可境界を再定義したことが誤判定の原因である。

## Diagnostic replay

旧command関連Score 3の26件をattempt / exit分離policyでreplayすると、`successful=24`、`evidence_incomplete=1`、`not_attempted=1`へ分離できた。旧F04 cleanup 2 runは、tool開始前にcleanup commandが拒否されたというmodel reportを両runから検出できた。新規runではこれらを`command-protocol-audit`と`evaluation-diagnostics`へ保存する。

## 新規runの固定条件

新しいprofileは`candidate35-root-control-only-owner-producer-v8-expanded12-f04r2-global-m24-n5-r1`である。prompt identityはv7と同じで、変更するのはEvaluation setとrating / evidence protocolだけである。

- required commandは1 commandずつ実行し、structured `exit_code`を保存する。
- callなし、非zero exit、exit収集不能を別statusへ分離する。exit収集不能だけをexternal failureとして再試行する。
- F04の`node_modules/`と`dist/`はadapterが宣言済みpathだけを削除する。
- teardown失敗は`adapter_owned_teardown_failed`としてrunを除外する。
- format違反とmodelによるadapter-owned cleanup試行をdiagnostic observationへ保存する。
- Layer 3はadapterの許可path判定を再定義しない。
- F10はfinding内容と正確な変更位置を別の証跡として扱う。

採用、release承認、THE-CAPTION本体反映は行っていない。
