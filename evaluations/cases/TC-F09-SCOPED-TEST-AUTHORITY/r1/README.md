# TC-F09-SCOPED-TEST-AUTHORITY r1

## 目的

`tests/AGENTS.md`のfull-suite gateがfocused testへ狭められた状態を復元するscoped-authority caseである。

## 固定条件

- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- seeded fixture commit: `f4e78702f140b4fd5b85c8125cc7c14551b7e054`
- seeded fixture tree: `3dc0da424d291bd48af8b937e255132b6ec5202b`
- source SSOT commit: `1d651a15d3086671a4dbe9d26cc46252d9f40c2f`
- trial input SHA-256: `8fad01aebf0a06f272b5a09b769781267647cf98548bcc5c45aa996bebab9782`
- seed patch SHA-256: `a7c88d5ea4abe9bfb550ee9cff4f3c60a6e365457ec4b8f150a9ea7455361f34`

## Fixture qualification

`seed.patch`は`pytest tests/ -v`の2箇所を単一focused testへ置換する。patch、preimage、postimage、seed commitは再現でき、fixture自体はqualifiedである。

## Execution blocker

現在のbaselineとcandidateは両方とも`tests/AGENTS.md`をprompt bundleの適用対象にしている。通常のadapter順序ではbundle overlayがseeded fileを上書きし、case条件を消してしまう。overlay順を逆にすると評価対象promptそのものをseedで改変するため、A / B比較としても不正になる。

このためstatusは`fixture_qualified_execution_blocked_prompt_target_collision`とする。caseは保管するが、prompt targetとfixture conditionを分離するrevisionを設計するまで実行setへ入れない。
