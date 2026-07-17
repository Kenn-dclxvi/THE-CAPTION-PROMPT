# Quality rating contracts

quality ratingの必要条件をrevision別に固定する。結果確認後の変更は新revisionとし、既存resultのscoreをin-placeで読み替えない。

[`owner-producer-quality-v1`](owner-producer-quality-v1.json)は、TaskSpecがcriterion ownerを固定したrunで、ownerに対応するproducer execution identityのresultをquality raterが確認できることをscore `4`の必要条件にする。独立ownerのproducerはactive executorと別execution identityでなければならない。

`scripts/owner_producer_evidence.py`はmodel-visible TaskSpecと実行済みsession metadataからblind evidence viewを作る。このscriptはscoreを決めず、evidenceの利用可否だけを検査する。成果全体の0〜4採点は引き続きquality raterが行う。

現行`evaluation_loop.py rate`はowner付きTaskSpecの採点時にこのevidence viewを必須とする。該当runの`score_4_owner_evidence_eligible`-fieldがtrueでなければscore `4`の保存を拒否する。0〜3のどのscoreにするかはscriptが決めない。
