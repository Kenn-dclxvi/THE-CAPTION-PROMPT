# Candidate16〜19 evidence boundary targeted checks

## 目的と範囲

Candidate15の連続試験でscore `4`未満が残ったF04 web audit columnとF10 monthly format-test reviewに対し、個別case、path、commandの例外を追加せず、TaskSpec、operation identity、evidence、gate statusの所有境界を既存section内で再編したcandidateを確認する。

この文書はpartial setのdiagnostic evidenceであり、expanded 12 caseのLayer 4 resultへ登録しない。採用、release、THE-CAPTION本体反映は未判断、未実施である。

## 共通条件

- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- Codex CLI: `0.144.0`
- Python: `3.14.5`
- permission: `workspace-write` / `never`
- memories: disabled
- `agents.max_threads`: `4`
- token accounting: `all_agents` / `v1`
- Evaluation set、fixture、TaskSpec、required commandはCandidate15連続試験から変更しない。

## Candidate lineage

| candidate | direct source | 変更原則 | `AGENTS.md` o200k tokens | bundle SHA-256 |
| --- | --- | --- | ---: | --- |
| Candidate15 | Candidate14 | selected role control input boundary | 2,590 | `1a2ef9…6db8` |
| Candidate16 | Candidate15 | bind済みevidenceだけでgate statusを変更 | 2,587 | `97086d…1c1162` |
| Candidate17 | Candidate16 | constraint / terminalもoperation identityごとに限定 | 2,587 | `4c492d…740d4a` |
| Candidate18 | Candidate17 | operation開始時にevidence対応を固定 | 2,590 | `cb9cf7…b39f4ef` |
| Candidate19 | Candidate18 | 1 resultを1 predicateだけへbind | 2,585 | `0580e6…342ae7b3` |

新sectionは追加していない。Candidate16は`Compact TaskSpec`、`Ordered gate`、`Operation permission`の既存記述を置換・統合し、Candidate17〜19も同じ既存記述内の修正に限定した。

## Targeted observations

| candidate | case / repetition | score分布 | 観測 |
| --- | --- | --- | --- |
| Candidate16 | F04 / `N=5` | `4`: 4、`3`: 1 | Node validation後のcleanup停止が1件再発した。 |
| Candidate16 | F10 / `N=5` | `4`: 5 | この5回では開始identity誤認なし。 |
| Candidate17 | F04 / `N=90` | `4`: 90 | cleanup未完了は0件。 |
| Candidate17 | F10 / `N=90` | `4`: 88、`1`: 2 | aggregate result内の`HEAD`と`HEAD^`の対応を逆に読んだ停止が2件残った。 |
| Candidate18 | F10 / `N=10` | `4`: 8、`1`: 2 | evidence対応をoperation開始時に固定しても同じ誤認が再発し、連続実行を打ち切った。 |
| Candidate19 | F10 / `N=10` | `4`: 8、`1`: 2 | 1 result / 1 predicateの正規化後もaggregate invocationが選択され、連続実行を打ち切った。 |

Candidate17の180 runは18 batchを逐次実行し、すべてrateableだった。別に試したparallel batchで1件、`npm` command自体がPATHにないenvironment-only runが出たため、そのbatch全体を上記180 runから除外し、raw evidenceだけを保持した。

## Candidate15 / Candidate17の同一case比較

| case | Candidate15 | Candidate17 | score `4`差 | Candidate15 tokens | Candidate17 tokens |
| --- | --- | --- | ---: | ---: | ---: |
| F04 web audit column | `4`: 88、`3`: 2 | `4`: 90 | +2 | 45,955,820 | 46,832,263 |
| F10 monthly review | `4`: 84、`1`: 6 | `4`: 88、`1`: 2 | +4 | 8,032,740 | 8,526,473 |
| 合計 | `4`: 172、`3`: 2、`1`: 6 | `4`: 178、`1`: 2 | +6 | 53,988,560 | 55,358,736 |

Candidate17のall-agent `total_tokens`合計はCandidate15比`+1,370,176`、`+2.54%`だった。case別中央値はF04が`508,505.5` → `515,578.0`、F10が`84,531.5` → `88,727.5`である。これらは観測値であり、自動的な優劣判定へ変換しない。

## 結論

- operationごとにconstraint / terminalのbind先を限定するCandidate17で、F04のcleanup停止は観測90回中0件だった。
- F10の開始identity誤認はCandidate15の6 / 90からCandidate17の2 / 90に変化したが、0ではない。
- Candidate18 / 19でevidence生成規則を強めても再発した。これ以上promptで具体的なinvocation shapeを固定すると、一般境界ではなくtool-call実装の指示になるため、この系統のprompt追加はCandidate17までで打ち切る。
- Candidate17のexpanded 12 case回帰、採用、release、runtime projectionは未実施である。

## Raw evidence

- Candidate16: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate16-gate-evidence-binding-targeted-f04-f10-n5-b18-20260717`
- Candidate17: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate17-operation-qualified-evidence-targeted-f04-f10-n5-b18-20260717`
- Candidate18: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate18-explicit-evidence-binding-f10-n5-b18-20260717`
- Candidate19: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate19-single-predicate-evidence-f10-n5-b18-20260717`

raw evidence、session情報、一時workspaceはrepositoryへcommitしない。
