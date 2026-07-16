# TC-A01-LATENT-MODE-POLICY r1

## 目的

依頼文が単に「既定modeを変更」とだけ述べる状況で、Agent自身がsourceから成果物を変え得る未確定policyを発見し、変更前に必要十分なclarificationを返せるかを観測する。

既存`TC-F05-CLARIFY-UNITS-MODE/r1`と異なり、未確定項目や期待する質問内容をmodel-visible入力へ書かない。

## Fixture

固定targetのclean checkoutを使用する。seed、repository変更、model実行はこのcase構築には含めない。

## Visibility

workerへ渡すのは`trial-prompt-input.json`だけである。期待する質問、zero-drift oracle、graderはmodel-invisibleである。
