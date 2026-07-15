# Prompt set result registry example

`set.json`と`fixture/`はEvaluation set sourceの最小例である。`run-capsule.template.json`は1 prompt set、1 case、1 iteration用のRun capsule v2を示す。

実利用では`adapter.argv`を実在executorへ置き換え、`prompt_set_identity`とprompt固有`parameters`を対象bundleへ結び付ける。同じcycle内では`prompt_set_identity`と`comparison_conditions`を変更せず、`case_id`と`iteration`だけをslotに合わせる。別prompt setは別cycleで実行し、同じregistryへ`record-result`する。

このexampleはschemaとfixture境界の説明用であり、評価済みresult、採用、release、本体反映を表さない。
