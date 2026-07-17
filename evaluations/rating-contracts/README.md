# Quality rating contracts

quality ratingの必要条件をrevision別に固定する。結果確認後の変更は新revisionとし、既存resultのscoreをin-placeで読み替えない。

[`owner-producer-quality-v1`](owner-producer-quality-v1.json)は、TaskSpecがcriterion ownerを固定したrunで、ownerに対応するproducer execution identityのresultをquality raterが確認できることをscore `4`の必要条件にする。独立ownerのproducerはactive executorと別execution identityでなければならない。

[`owner-producer-quality-v2`](owner-producer-quality-v2.json)はv1のowner-producer条件を維持し、required validation commandの成功証跡をroot sessionだけでなく、そのrunのall-agent usageにbindされたrecursive descendant sessionまで含める。対象sessionは同一workspaceの全sessionではなく、正確なroot threadから到達できるthread graphだけとする。descendantのfinal responseだけではcommand成功証跡にならない。

[`owner-producer-quality-v3`](owner-producer-quality-v3.json)はv2のevidence scopeを維持し、valid runにcommandまたはowner evidence不足がある場合も0〜3の全体scoreを必ず返す。score `4`の必要条件はv2から変更しない。nullまたはunrateableでLayer 4全体を止めず、不足証跡と成果全体を区別して短い理由へ記録する。

[`owner-producer-quality-v4`](owner-producer-quality-v4.json)はv3の採点条件を維持し、all-agent command evidenceをv2へ更新する。command evidence v2はrootのCodex command eventsに加え、all-agent usageへbindされたdescendant rollout内のstructured command arrayと、`write_stdin`でterminalになったcommand continuationを収集する。既存v3 resultは変更しない。

[`owner-producer-quality-v5`](owner-producer-quality-v5.json)はv4の採点条件を維持し、all-agent command evidenceをv3へ更新する。command evidence v3は、command nameと成功結果を一意に対応付けられるcustom `exec` wrapperの`<name>: exit=0`集約行を収集する。sourceに`${r.name}`または`${r.label}`と`${r.exit_code}`がなく、固定command表へnameをbindできないtextは証跡にしない。既存v4 resultは変更しない。

`scripts/owner_producer_evidence.py`はmodel-visible TaskSpecと実行済みsession metadataからblind evidence viewを作る。このscriptはscoreを決めず、evidenceの利用可否だけを検査する。成果全体の0〜4採点は引き続きquality raterが行う。

現行`evaluation_loop.py rate`はowner付きTaskSpecの採点時にowner-producer evidence viewを必須とする。rating v2 / v3は`all-agent-command-evidence/v1`、rating v4は`v2`、rating v5は`v3`を要求する。該当runの`score_4_owner_evidence_eligible` fieldがtrueでなければscore `4`の保存を拒否する。0〜3のどのscoreにするかはscriptが決めない。v3以降のprofileではvalid runをnullにせず、raterが成果全体から0〜3を付ける。既存resultとprofileは履歴として保持し、新revisionへ読み替えない。
