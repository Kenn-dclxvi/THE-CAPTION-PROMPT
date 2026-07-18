# Quality rating contracts

quality ratingの必要条件をrevision別に固定する。結果確認後の変更は新revisionとし、既存resultのscoreをin-placeで読み替えない。

[`owner-producer-quality-v1`](owner-producer-quality-v1.json)は、TaskSpecがcriterion ownerを固定したrunで、ownerに対応するproducer execution identityのresultをquality raterが確認できることをscore `4`の必要条件にする。独立ownerのproducerはactive executorと別execution identityでなければならない。

[`owner-producer-quality-v2`](owner-producer-quality-v2.json)はv1のowner-producer条件を維持し、required validation commandの成功証跡をroot sessionだけでなく、そのrunのall-agent usageにbindされたrecursive descendant sessionまで含める。対象sessionは同一workspaceの全sessionではなく、正確なroot threadから到達できるthread graphだけとする。descendantのfinal responseだけではcommand成功証跡にならない。

[`owner-producer-quality-v3`](owner-producer-quality-v3.json)はv2のevidence scopeを維持し、valid runにcommandまたはowner evidence不足がある場合も0〜3の全体scoreを必ず返す。score `4`の必要条件はv2から変更しない。nullまたはunrateableでLayer 4全体を止めず、不足証跡と成果全体を区別して短い理由へ記録する。

[`owner-producer-quality-v4`](owner-producer-quality-v4.json)はv3の採点条件を維持し、all-agent command evidenceをv2へ更新する。command evidence v2はrootのCodex command eventsに加え、all-agent usageへbindされたdescendant rollout内のstructured command arrayと、`write_stdin`でterminalになったcommand continuationを収集する。既存v3 resultは変更しない。

[`owner-producer-quality-v5`](owner-producer-quality-v5.json)はv4の採点条件を維持し、all-agent command evidenceをv3へ更新する。command evidence v3は、command nameと成功結果を一意に対応付けられるcustom `exec` wrapperの`<name>: exit=0`集約行を収集する。sourceに`${r.name}`または`${r.label}`と`${r.exit_code}`がなく、固定command表へnameをbindできないtextは証跡にしない。既存v4 resultは変更しない。

[`owner-producer-quality-v6`](owner-producer-quality-v6.json)はv5の採点条件とcommand / producer evidence revisionを維持し、F05 clarificationのresponse evidenceだけをsemantic marker groupへ更新する。`daily`、`strict`に加え、live CSV fallback policyは英字`fallback`または日本語`フォールバック`のどちらでも同じ概念証拠として扱う。Unicode NFKCとcasefold後に各概念groupの少なくとも1表現を要求する。既存v5 resultは変更せず、v6 resultと互換比較へ混ぜない。

[`owner-producer-quality-v7`](owner-producer-quality-v7.json)はv6の採点条件とresponse / producer evidenceを維持し、all-agent command evidenceをv4へ更新する。command evidence v4は、custom `exec` wrapperが出力する`### <name>`直後の`exit_code=0`を、source側の`${r.name}`と`${r.exit_code}`および固定name-command表へ一意にbindできる場合だけ成功証跡へ含める。process開始失敗、`exit_code`欠落、固定nameへbindできないtextは成功証跡にしない。既存v6 resultは変更しない。

[`owner-producer-quality-v8`](owner-producer-quality-v8.json)は採点anchorとresponse / producer evidenceを維持し、all-agent command evidenceをv5へ更新する。v5はattempted、successful、failed、protocol violationを別配列へ保存する。required command callがない場合とmachine-boundな非zero exitはtask outcomeとして採点する。callはあるがzero / nonzero exitのどちらもbindできない場合は`command_evidence_incomplete`のexternal failureとして除外し、同じslotを再試行する。format違反とadapter-owned cleanup試行は診断へ保存するがquality KPIへ入れない。既存v7 resultは変更しない。

[`outcome-quality-owner-diagnostic-v9`](outcome-quality-owner-diagnostic-v9.json)はv8のresponse evidence、command evidence、0〜4 anchorを維持し、成果・boundary・required validationを`quality_score`の対象にする。owner-producer evidenceは同じcollectorで必ず保存するが、独立worker経路の成立可否をdiagnostic observationへ分離し、quality scoreを変更しない。既存v8 resultは変更せず、新profile revisionとして実行する。

`scripts/owner_producer_evidence.py`はmodel-visible TaskSpecと実行済みsession metadataからblind evidence viewを作る。このscriptはscoreを決めず、evidenceの利用可否だけを検査する。成果全体の0〜4採点は引き続きquality raterが行う。

現行`evaluation_loop.py rate`はowner付きTaskSpecの採点時にowner-producer evidence viewを必須とする。rating v2 / v3は`all-agent-command-evidence/v1`、rating v4は`v2`、rating v5 / v6は`v3`、rating v7は`v4`、rating v8 / v9は`v5`を要求する。v8 / v9のmeasurement-incomplete runはLayer 2で除外されるためLayer 3へ渡さない。v1〜v8は該当runの`score_4_owner_evidence_eligible` fieldがtrueでなければscore `4`の保存を拒否する。v9は同fieldを診断へ保持し、outcome qualityのscore `4`を拒否するgateには使わない。既存resultとprofileは履歴として保持し、新revisionへ読み替えない。
