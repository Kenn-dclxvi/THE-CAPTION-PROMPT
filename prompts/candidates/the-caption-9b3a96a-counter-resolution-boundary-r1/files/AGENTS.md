# THE-CAPTION execution contract

runtime_owner: THE-CAPTION-maintainer-with-merge-authority

## Single root / outcome

このfileをroot execution authorityとし、rootだけがroute、counter、terminalを所有する。各taskは境界と許可が確定したexecute、結論に影響する不足またはresolved execution contractで解消できないinvariantとのauthority conflictを確認してstoppedを返すclarify、TaskSpecまたは対象repositoryのscope外操作だけを拒否するout_of_scope_stopのいずれか一つへ進み、旧processへfallbackしない。execute中のpermission否定、required gateのfailed / unavailable、対象repository内の明示禁止操作はstoppedとして返す。

## Compact TaskSpec

実行前にTaskSpecとしてtarget repository / ref / start identity、task kind / goal / done、許可・禁止変更、validation / non-machine risk、operation別permission、constraint / recoveryを一つのimmutableな論理recordへ固定する。これらを変える入力は新identityとして扱い、旧identityにbindした後段gateを失効させる。

artifact、完了条件、必要なvalidationを変え得る未確定事項は実行前に確認する。安全かつ同一scopeの手段選択は、固定済み境界を変えない範囲で実行側が決めてよい。

## TaskSpec / default resolution

TaskSpecを固定した後、各責務をpre-resolution invariant、TaskSpecの有効な明示値、change-class defaultの順で解決し、一つのresolved execution contractへ固定する。このfile、上位authorityまたはscoped authorityの明示禁止、rootによるroute / counter / terminal所有、identity binding、required gateのfail-closed、許可外drift禁止、workerのnon-mutationはpre-resolution invariantとし、後段で変更しない。TaskSpecで固定したoperation permissionと許可・禁止変更は解決後のscope invariantとなり、defaultまたはworkerが拡張・緩和しない。evidenceの完全性はresolved execution contractがrequiredとしたevidenceだけを対象とする。

pre-resolution invariantに反しないTaskSpecの明示値は、同じ責務のdefaultを置き換える。明示値はsource inputまたはcallerが直接指定した値に限り、rootが推定または補完した値を明示値へ昇格させない。presence、applicability、validityは別に判定する。このfileが非適用を許す責務にTaskSpecが`not_applicable`を明示した場合は、有効な明示状態としてその責務だけをinactiveにし、その責務のpayload domainとdefaultを評価せず、`not_applicable`単独をdomain外値、authority conflictまたは停止理由にしない。inactiveは他の責務、pre-resolution invariant、scope invariant、permission、その責務以外のrequired gate、実行済みgateの`failed / unavailable`を変更せず、それらの停止理由を解消しない。activeな責務ではfieldのtype / domainを満たす`none`、`false`、`0`、空の集合も明示値として未指定扱いしない。activeな責務のdomain外の値またはschema不正な値へdefaultでfallbackせず、defaultのないrequired fieldの不足も推測で補わない。defaultは責務ごとに対応する明示値が存在しない場合だけ適用し、明示値とdefaultの差をauthority conflictにしない。invariantとの矛盾、invalidな明示値、解決不能な不足はauthority入力を読んだresolution中に全件検出し、最初のedit、testまたはexternal side effect前に双方のfieldとauthorityを示して停止する。

resolved execution contractはsource TaskSpecの完全なrecordとidentity、明示値のpresence、適用したinvariant / defaultと各source、最終的なrequired / not_applicable gate、permission、stop / recoveryをlosslessに含むimmutableな論理recordとする。invariant / defaultの分類は結果を見た後に変更しない。rootはaudit / reviewへ要約でなくこのrecord全体、resolution map、resolution identityを渡す。workerはTaskSpecとdefaultの優先順位を再解決せず、新しいrequired conditionを追加しない。

## JIT Context

既定Contextはancestor / scoped AGENTS.md、source TaskSpec、resolved execution contract / resolution map / resolution identity、対象artifact、selected spec / config / test、current diff / resultに限定する。過去run、過去diff、会話履歴、research record、candidate / attempt ID、無関係subtreeは既定入力にしない。

必要になった情報だけをそのgate直前に読む。scoped ruleの明示禁止、canonical artifact、path constraintは対象pathのinvariantとし、一般的な手順またはvalidation commandは同じ責務のTaskSpec明示値がない場合のdefaultとして解決する。scoped ruleはrootのroute、permission、counter、completion、terminalを直接変更しない。

## Ordered gate

gateはboundary / permission、Context / authority、operation、required machine completion、required non-machine completion、drift / final identity、single terminalの順に評価し、statusはpassed、failed、unavailable、not_applicableだけを使う。unknownまたは代替確認をpassへ変換しない。

前段が後段を許可しない場合はそこで停止し、不要な後段を実行しない。完了はrequiredな各gateが許す同一artifact identityだけにbindする。

## Python completion default

TaskSpecにPythonのrequired machine completionが明示されていない場合、change-class defaultはrepository rootをcwdとする`bash scripts/dev/main_verify.sh`とし、exit 0、collection / outcome、required report、logging / reporting error 0、expected ignored path / class、未許可tracked / non-ignored drift 0、actual collection / result identityを一つの結果として確認する。

TaskSpecがrequired command、順序、包含・重複、equivalenceまたはevidence条件を明示した場合は、重複して見えるgateも含めてそのplanを一体として保持し、同じ責務のdefault commandを追加または置換しない。defaultを使う場合はscriptが含む同じtest scopeを別commandで重複実行しない。明示値またはdefaultから選定したrequired gateがfailed / unavailableなら、別commandの成功を代替合格にしない。

## Node completion default

Node dependency変更では`src/web/market_units_editor/package.json`と`src/web/market_units_editor/package-lock.json`のpairをartifact invariantとして固定する。TaskSpecにNodeのrequired machine completionが明示されていない場合、change-class defaultは`npm ci --ignore-scripts --no-audit --no-fund --include=dev`、`npm run lint`、`npm run build`の順を一つのqualified gateとして扱う。

途中のfailureを後続commandの成功で上書きせず、install後の生成物はdrift分類へ渡す。

## Docs / dependency / mixed completion defaults

Python dependency familyの`.in / .txt` pairはartifact invariantとする。TaskSpecに責務ごとに対応するcompletionが明示されていない場合、change-class defaultとしてdocs / AI制御文書の変更はvalid contract auditを要求する。mixed changeは責務ごとに適用されたdefaultとTaskSpec明示値から得たrequired gateの和集合を使い、一部がfailed / unavailableなら別の成功を代替合格にしない。

TaskSpecが明示したgateは重複して見えても保持する。executorが自発的に加えるdefaultだけを対象artifactとdoneを直接判定する最小範囲に限定し、変更classに該当しないdefault gateは追加しない。

## Conditional audit / review

non-machine completion routeのdomainは`none`、`audit`、`review`、`audit+review`とする。明示routeをresolved execution contractのcriterion、ownerとともに保持し、`none`はworkerなし、`audit`はvalid auditのcontract_stop 0、`review`はfresh reviewのquality_blocker 0、`audit+review`はcontract_stop 0のvalid audit後にfreshかつindependentなreviewのquality_blocker 0を要求する。TaskSpecにrouteの明示がなくpredicate trueの場合のdefaultは`audit+review`、predicate falseの場合は`none`とし、resolved routeが要求するworkerだけを起動する。

rootはcandidate prompt path / blob、ordered input manifest、target / head、source TaskSpecの完全なrecord / identity、resolved execution contract / resolution map / resolution identity、diff、machine result、selected spec、session / model / environment、output identityを管理する。auditとreviewはそれぞれactive executorと別execution identityへbindし、明示値をmissingへ変換する省略・要約がないことと禁止inputの除外を確認する。workerはpermission、counter、artifact、gate statusまたはterminalを変更しない。

## Machine rework

TaskSpecが`machine_rework_max=not_applicable`を明示した場合、machine rework責務だけをinactiveにし、counterを持たずartifact変更roundを開始しない。machine rework責務がapplicableな場合だけ、machine_rework_maxはcallerが固定する正整数 Nとする。active executorのinitial implementation後、最初のrequired final gateがtarget_behavior_failureになった場合だけ、artifact変更roundを開始する直前にcountし、各round後はfresh identityでfull required gateを再実行する。N + 1回目は開始しない。

behavior failure以外をこのcountへ混ぜず、上限到達後もrequired gateが通らなければ停止する。

## Environment recovery

TaskSpecが`environment_recovery_max=not_applicable`を明示した場合、environment recovery責務だけをinactiveにし、counter、environment-only repair、同じrequired commandの再実行を持たない。environment recovery責務がapplicableな場合だけ、environment_recovery_maxはcallerが固定する非負整数 Mとする。environment-only repairと同じrequired commandの再実行だけを一組にし、各action前にcountする。このcycleではtarget artifactを変更しない。M + 1回目は開始せず、回復しなければstopped_failed_or_unverifiedとする。

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

同一resolved execution contractで完了と停止を併記せず、成果物とvalidationが同じresolution identityとfinal identityを参照することを確認する。

## Invalidation / rollback

TaskSpec-local invalidationとpackage lifecycleを分離する。source TaskSpec、resolved execution contract、projection path / blob / ownerのidentityが変われば後段結果を無効化し、rollbackは固定preimageに対するprojection commitのrevertまたはpreimage復元後にselected gateを再実行する。repository全体の強制resetまたはhost-local config変更をrollbackにしない。

rollback後も変更pathとfinal identityを確認し、旧authorityと新authorityが混在した状態を成功にしない。
