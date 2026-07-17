# Quality rating contracts

quality ratingの必要条件をrevision別に固定する。結果確認後の変更は新revisionとし、既存resultのscoreをin-placeで読み替えない。

[`owner-producer-quality-v1`](owner-producer-quality-v1.json)は、TaskSpecがcriterion ownerを固定したrunで、ownerに対応するproducer execution identityのresultをquality raterが確認できることをscore `4`の必要条件にする。独立ownerのproducerはactive executorと別execution identityでなければならない。

[`owner-producer-quality-v2`](owner-producer-quality-v2.json)はv1のowner-producer条件を維持し、required validation commandの成功証跡をroot sessionだけでなく、そのrunのall-agent usageにbindされたrecursive descendant sessionまで含める。対象sessionは同一workspaceの全sessionではなく、正確なroot threadから到達できるthread graphだけとする。descendantのfinal responseだけではcommand成功証跡にならない。

[`owner-producer-quality-v3`](owner-producer-quality-v3.json)はv2のevidence scopeを維持し、valid runにcommandまたはowner evidence不足がある場合も0〜3の全体scoreを必ず返す。score `4`の必要条件はv2から変更しない。nullまたはunrateableでLayer 4全体を止めず、不足証跡と成果全体を区別して短い理由へ記録する。

`scripts/owner_producer_evidence.py`はmodel-visible TaskSpecと実行済みsession metadataからblind evidence viewを作る。このscriptはscoreを決めず、evidenceの利用可否だけを検査する。成果全体の0〜4採点は引き続きquality raterが行う。

現行`evaluation_loop.py rate`はowner付きTaskSpecの採点時にowner-producer evidence viewを必須とし、v2 / v3ではさらに`all-agent-command-evidence/v1` artifactを必須とする。該当runの`score_4_owner_evidence_eligible` fieldがtrueでなければscore `4`の保存を拒否する。0〜3のどのscoreにするかはscriptが決めない。v3 profileではvalid runをnullにせず、raterが成果全体から0〜3を付ける。v1 / v2 resultとprofileは履歴として保持し、v3へ読み替えない。
