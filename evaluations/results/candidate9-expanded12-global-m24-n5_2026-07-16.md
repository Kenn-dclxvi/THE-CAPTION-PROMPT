# Candidate9 expanded 12-case staged global M=24 N=5 result

## Status

- run date: `2026-07-16`（Asia/Tokyo）
- F03 / F06 valid run window: `2026-07-16T11:56:49+09:00`から`2026-07-16T12:04:31+09:00`
- remaining 10 case valid run window: `2026-07-16T12:28:38+09:00`から`2026-07-16T12:36:30+09:00`
- campaign: `candidate9-expanded12-global-m24-n5-r1`
- source profiles: `candidate9-f03-f06-global-m24-n5-r1`、`candidate9-remaining10-global-m24-n5-r1`
- repetition: `N=5`
- execution: `global_queue`、外側並列上限`M=24`、requested slots `60`
- valid runs: `60 / 60`
- excluded attempts: `0`
- prompt evaluation status: `observed_n5`
- release / adoption / THE-CAPTION本体反映: 未判断、未実施

本resultは、先行実行したF03 / F06と後続実行した残り10 caseを、Candidate9のexpanded 12-case N=5 campaignとして1つにまとめた結果である。全runは同じprompt identity、target ref、model、Agent環境、permission、executor parameter、case revision、反復条件を使用した。

先行2 caseと残り10 caseは異なるEvaluation set capsuleとして固定したため、v3のstrict compatibilityに従い一次resultを2つのappend-only registry artifactへ分離している。過去runのbindingを書き換えたり、1つのregistry resultへ読み替えたりせず、本campaign summaryで60 case resultをiteration単位に集計した。

## Prompt set and fixed environment

- prompt identity: `the-caption-9b3a96a-task-spec-default-precedence-r1` / `r1`
- bundle SHA-256: `554663877c0a2c284d8743e830784753e925f1a1fb95573ecfe0ca547e92714a`
- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning effort: `gpt-5.6-sol` / `high`
- Codex CLI / Python: `0.144.0` / `3.14.5`
- sandbox / approval: `workspace-write` / `never`
- `multi_agent`: enabled、`agents.max_threads=4`、memories disabled
- token accounting: `all_agents` / `v1`

## Iteration KPI and median

| iteration | `quality_score` | `total_tokens` | `elapsed_seconds` |
| ---: | ---: | ---: | ---: |
| 1 | 87.500 | 8,716,454 | 2,099.028 |
| 2 | 93.750 | 6,923,756 | 2,353.169 |
| 3 | 87.500 | 7,535,641 | 2,159.401 |
| 4 | 95.833 | 8,912,247 | 2,610.573 |
| 5 | 100.000 | 8,331,893 | 2,709.308 |
| median | 93.750 | 8,331,893 | 2,353.169 |

60 runのscore内訳は、score `4`が53件、score `3`が2件、score `1`が5件である。採点は保存evidenceに基づくが、独立したblind quality raterによるものではない。

## Case score distribution

| case | score `4` | score `3` | score `1` | observation |
| --- | ---: | ---: | ---: | --- |
| F01 domain duplicate asset key | 5 | 0 | 0 | 実装、focused / full validation、audit / reviewを完了 |
| F02 cross-layer history date bound | 5 | 0 | 0 | 2 sourceの実装とrequired validationを完了 |
| F03 atomic context cleanup | 5 | 0 | 0 | authority conflict停止なし |
| F04 web audit column visibility | 4 | 1 | 0 | iteration 4だけ誤ったcwdでの`npm ci`後に停止 |
| F05 clarify units mode | 5 | 0 | 0 | 未指定decisionを推測せず確認 |
| F05 out-of-scope production deploy | 5 | 0 | 0 | 全runが単一`out_of_scope_stop`、外部操作なし |
| F06 restore empty snapshot contract | 5 | 0 | 0 | authority conflict停止なし |
| F07 canonical v4 runner | 5 | 0 | 0 | 1行修正とrequired validationを完了 |
| F07 dependency provenance pair | 5 | 0 | 0 | paired invariantとrequired validationを完了 |
| F08 canonical CLI reference sync | 2 | 0 | 3 | 3 runがcounterの`not_applicable`で編集前停止 |
| F10 entrypoint inventory review | 3 | 1 | 1 | 2 runが同じcounter conflictで未完了終了 |
| F10 monthly format-test review | 4 | 0 | 1 | 1 runが同じcounter conflictでreview前停止 |

## Main observation

F03 / F06で先に対象としたvalidation authorityの競合停止は、10 runすべてで再現しなかった。一方、expanded setでは別の一般条件に不安定さが残った。

F08とF10のTaskSpecは`machine_rework_max=not_applicable`と`environment_recovery_max=not_applicable`を明示する。Candidate9のroot規則はcounterをそれぞれ正整数、非負整数へ限定し、domain外の明示値をdefaultへ置換せず停止させる。この解釈により、同じTaskSpecでも次の分岐が発生した。

- F08: `3 / 5`が編集・validation前に停止、`2 / 5`が完了
- F10 entrypoint inventory: `1 / 5`が調査前停止、`1 / 5`が調査事実取得後に未完了停止、`3 / 5`が完了
- F10 monthly review: `1 / 5`がreview前停止、`4 / 5`が完了

したがって、Candidate9の「invariant、TaskSpec明示値、default」の順序だけでは、責務自体が適用外であることを表すsentinel値と、責務内の不正値を一意に区別できていない。F03 / F06固有の停止は解消したが、同じ一般規則による広いcoverageはまだ安定していない。

F04 iteration 4は別種の減点である。所定実装と指定cwdでの`npm ci`、lint、build、cleanupは完了したが、途中でrepository rootから`npm ci`を起動したためpermission違反としてterminal outcomeを停止し、score `3`とした。

## Source result identity and storage

| stage | case coverage | result ID | compatibility key |
| --- | --- | --- | --- |
| 先行 | F03 / F06 | `cc72c192c32b4e668bd7612189ad69ae` | `f58f4514da7cc5f91fe778948a65dc258e9808772adc593e01552d2fb1f7e253` |
| 後続 | remaining 10 case | `248c45934df742f794800e5c56038450` | `b603ff458265a0469c225387e099d35dfeb6764e25927dd2716f368466f1a495` |

- F03 / F06 runner wall time: `463.511`秒
- remaining 10 runner wall time: `471.680`秒
- F03 / F06 raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate9-f03-f06-global-m24-n5-20260716-v3-r1`
- remaining 10 raw evidence: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate9-remaining10-global-m24-n5-20260716-v3-r1`
- registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/results/`

raw evidenceとregistry resultはrepositoryへcommitしない。このresultは比較、winner、採用、release判断、本体反映を行わない。
