# THE-CAPTION execution contract

runtime_owner: THE-CAPTION-maintainer-with-merge-authority

## Single root / outcome

このfileをroot execution authorityとし、rootだけがroute、counter、terminalを所有する。各taskは境界と許可が確定したexecute、結論に影響する不足またはscoped authority conflictを確認してstoppedを返すclarify、TaskSpecまたは対象repositoryのscope外操作だけを拒否するout_of_scope_stopのいずれか一つへ進み、旧processへfallbackしない。execute中のpermission否定、required gateのfailed / unavailable、対象repository内の明示禁止操作はstoppedとして返す。

## Compact TaskSpec

実行前にTaskSpecとしてtarget repository / ref / start identity、task kind / goal / done、許可・禁止変更、validation / non-machine risk、operation別permission、constraint / recoveryを一つのimmutableな論理recordへ固定する。これらを変える入力は新identityとして扱い、旧identityにbindした後段gateを失効させる。

artifact、完了条件、必要なvalidationを変え得る未確定事項は実行前に確認する。安全かつ同一scopeの手段選択は、固定済み境界を変えない範囲で実行側が決めてよい。

## JIT Context

既定Contextはancestor / scoped AGENTS.md、対象artifact、selected spec / config / test、current diff / resultに限定する。過去run、過去diff、会話履歴、research record、candidate / attempt ID、無関係subtreeは既定入力にしない。

必要になった情報だけをそのgate直前に読む。scoped ruleは対象pathにだけ追加適用し、rootのroute、permission、counter、completion、terminalを上書きしない。

## Ordered gate

gateはboundary / permission、Context / authority、operation、required machine completion、required non-machine completion、drift / final identity、single terminalの順に評価し、statusはpassed、failed、unavailable、not_applicableだけを使う。unknownまたは代替確認をpassへ変換しない。

前段が後段を許可しない場合はそこで停止し、不要な後段を実行しない。完了はrequiredな各gateが許す同一artifact identityだけにbindする。

## Python completion

Python変更のrequired gateはrepository rootをcwdとする`bash scripts/dev/main_verify.sh`であり、exit 0、collection / outcome、required report、logging / reporting error 0、expected ignored path / class、未許可tracked / non-ignored drift 0、actual collection / result identityを一つの結果として確認する。

scriptが含む同じtest scopeを別commandで重複実行せず、required resultが得られない場合はそのままfailedまたはunavailableとする。

## Node completion

Node変更は`src/web/market_units_editor/package.json`と`src/web/market_units_editor/package-lock.json`を固定し、`npm ci --ignore-scripts --no-audit --no-fund --include=dev`、`npm run lint`、`npm run build`の順を一つのqualified gateとして扱う。

途中のfailureを後続commandの成功で上書きせず、install後の生成物はdrift分類へ渡す。

## Docs / dependency / mixed completion

docs / AI制御文書の変更はvalid contract auditを要求する。Python dependency familyでは`.in / .txt`のpaired invariantを確認する。mixed changeは該当するrequired gateの和集合を使い、一部がunavailableなら別の成功を代替合格にしない。

変更classに該当しないgateは追加せず、対象artifactとdoneを直接判定する最小のcompletion sourceだけを選ぶ。

## Conditional audit / review

non-machine completionはTaskSpecで固定したcriterionとownerに従う。`prompts/audit.md`のcontract_stopが0のvalid audit停止0の後にだけ、`prompts/review.md`のquality_blocker 0をfreshかつindependentに確認してpassedとする。audit / reviewはpredicate true時だけ起動する。

rootはcandidate prompt path / blob、ordered input manifest、target / head、TaskSpec、diff、machine result、selected spec、session / model / environment、output identityを管理する。auditとreviewはそれぞれactive executorと別execution identityへbindし、禁止inputの除外を確認する。workerはpermission、counter、artifact、gate statusまたはterminalを変更しない。

## Machine rework

machine reworkはTaskSpecのconstraint / recoveryでartifact変更roundが適用対象とされている場合だけ有効とし、適用対象でない場合はcounterを持たずartifact変更roundを開始しない。適用対象の場合だけ、machine_rework_maxはcallerが固定する正整数 Nとする。active executorのinitial implementation後、最初のrequired final gateがtarget_behavior_failureになった場合だけ、artifact変更roundを開始する直前にcountし、各round後はfresh identityでfull required gateを再実行する。N + 1回目は開始しない。

behavior failure以外をこのcountへ混ぜず、上限到達後もrequired gateが通らなければ停止する。

## Environment recovery

environment recoveryはTaskSpecのconstraint / recoveryでenvironment-only repairとrequired commandの再実行が適用対象とされている場合だけ有効とし、適用対象でない場合はcounter、repair、rerunを開始しない。適用対象の場合だけ、environment_recovery_maxはcallerが固定する非負整数 Mとする。environment-only repairと同じrequired commandの再実行だけを一組にし、各action前にcountする。このcycleではtarget artifactを変更しない。M + 1回目は開始せず、回復しなければstopped_failed_or_unverifiedとする。

artifactや期待挙動の変更をenvironment recoveryとして扱わず、別causeの確認を際限なく増やさない。

## Non-machine rework

valid audit停止またはvalid review重大指摘によるnon-machine reworkは、auditとreviewを合わせて同一TaskSpec execution内で共通最大5回とし、initial implementationは数えない。machine reworkはこの5回を消費せず、counterはrootだけが所有し、task中にresetしない。finding identityはclass、固定criterion、artifact / location、defect / causeの意味へbindする。初回出現を再発0、次のfresh confirmationでも同一identityがあれば再発1、さらに連続して同一なら再発2として停止する。chainはfresh confirmationでそのidentityが不在の場合だけ切り、別findingの出現で残存identityをresetせず、auditとreviewのclassを跨いで合算しない。

修正対象は許可scope内の停止またはblockerに限定し、改善や範囲外事項を自動修正へ送らない。

## Operation permission

read / edit / testはTaskSpecの範囲内で扱い、commit、push、mergeはそれぞれ個別明示許可がある場合だけ実行する。scripts/dev/spはAgent executionでは呼び出さない。deploy、外部送信、productionは適用外停止とする。

一つのoperation許可から別operationの許可を推定せず、許可のないexternal side effectを試行しない。

## Drift / final identity

最初のedit前にstart manifest、完了直前にend manifestを取り、pre-existing dirtyとnon-ignored untrackedを保護して無断cleanupしない。mode / rename / delete / contentをartifact class別に比較し、paired invariantとignored outputを分類してfinal artifact identityを固定する。

既存差分を取り込まず、許可scope外の変更または判定不能な差分があれば完了にせず停止する。

## Single terminal

terminal ownerはrootだけとし、outcome、実施内容、変更artifact、validation identity、未実行理由、停止・失敗・未確認、対象外、external side effectを一つの最終結果へまとめる。

同一TaskSpecで完了と停止を併記せず、成果物とvalidationが同じfinal identityを参照することを確認する。

## Invalidation / rollback

TaskSpec-local invalidationとpackage lifecycleを分離する。projection path / blob / ownerが変われば後段結果を無効化し、rollbackは固定preimageに対するprojection commitのrevertまたはpreimage復元後にselected gateを再実行する。repository全体の強制resetまたはhost-local config変更をrollbackにしない。

rollback後も変更pathとfinal identityを確認し、旧authorityと新authorityが混在した状態を成功にしない。
