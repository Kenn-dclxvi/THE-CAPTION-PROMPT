# Candidate43 / Candidate68 independent review operation removal F10 N=5

## 結論

Candidate68はCandidate43を直接sourceとし、`INDEPENDENCE`からF9の「先行result / artifactを対象とする別operationへ固有predicate / owner / producerを実行前に固定する。」一文だけを削除した。root bytesは`3,980 -> 3,860`、`-120`、`-3.02%`である。

F10-only `N=5`は5 / 5でscore `4`、root-only、zero driftを維持した。登録済み3 KPIの中央値は、`quality_score 100.0 -> 100.0`、all-agent `total_tokens 211,070 -> 213,525`、`elapsed_seconds 87.367 -> 110.118`である。token合計も`811,578 -> 812,004`、`+426`、`+0.05%`だった。

事前gateはall-agent token合計がCandidate43以下であることを要求した。Candidate68は426 tokenだけ上回ったためgate不通過とし、A01 / A02、F05 / F10、D01を追加実行しない。Candidate68は`targeted_evaluated / stopped`とし、採用、release、本体反映へ進めない。

## 静的差分

- 直接source: `the-caption-3ce91a4-outcome-authority-boundary-r1`
- Candidate68: `the-caption-3ce91a4-independent-review-operation-removal-r1`
- Candidate43 bundle SHA-256: `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531`
- Candidate68 bundle SHA-256: `d76a223819f36ee38ee9c4fdfa46a31b642cf981c65e55ef0061f7cdfb434a95`
- changed target: root `AGENTS.md`だけ
- label: `SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / METHOD / RECOVERY`を同じ順序で保持
- root bytes: `3,980 -> 3,860`、`-120`、`-3.02%`

Candidate68の全文は、Candidate43からF9一文だけを削除した結果と完全一致する。同じ`INDEPENDENCE`にある「同一predicateを別producerへ再割当てしない。」、Candidate67で削除したcross-label duplicate 2文、`F5 / D6 / R1 / R2`は残した。

## 固定条件

- target commit / tree: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model / reasoning: `gpt-5.6-sol` / `high`
- runtime / Codex CLI: `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` / `0.144.0`
- capability catalog SHA-256: `e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e`
- memories / apps / plugins / plugin sharing: disabled
- token accounting: all-agent / `v1`
- repetition: F10 `N=5`
- Layer 1 identity: `98da7e8c9ea12d91be50bb4d66ac15926b53a4ddee4d2035bc61bace13b01507`
- compatibility key: `cc9fcfebbc698f3f2601439eed2783fd2786082b847bd526f1c31ece4bfce083`
- excluded attempt: 0

Candidate68 profileはCandidate43 profileから`profile_id`と`prompt_set_identity`だけを変更した。

## 3 KPI

保存済みcomparison viewの全iterationを示す。`quality_score`はscore `4`を`100.0`として保存した値である。

| iteration | quality C43 | quality C68 | total_tokens C43 | total_tokens C68 | elapsed C43 | elapsed C68 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100.0 | 100.0 | 216,021 | 75,473 | 96.430秒 | 58.587秒 |
| 2 | 100.0 | 100.0 | 75,527 | 213,922 | 47.334秒 | 110.118秒 |
| 3 | 100.0 | 100.0 | 214,914 | 213,525 | 114.793秒 | 110.881秒 |
| 4 | 100.0 | 100.0 | 211,070 | 95,450 | 87.367秒 | 77.607秒 |
| 5 | 100.0 | 100.0 | 94,046 | 213,634 | 56.615秒 | 111.999秒 |
| 中央値 | 100.0 | 100.0 | 211,070 | 213,525 | 87.367秒 | 110.118秒 |

| KPI中央値 | Candidate43 | Candidate68 | Candidate68 - Candidate43 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.0 | 100.0 | 0.0 |
| all-agent `total_tokens` | 211,070 | 213,525 | +2,455（+1.16%） |
| `elapsed_seconds` | 87.367秒 | 110.118秒 | +22.751秒（+26.04%） |

token合計は`811,578 -> 812,004`、`+426`、`+0.05%`である。品質は両promptとも5 / 5でscore `4`だった。

## 保存traceの実行形

| 診断値 | Candidate43 | Candidate68 | 差 |
| --- | ---: | ---: | ---: |
| top-level tool call | 40 | 40 | 0 |
| reasoning item | 29 | 28 | -1 |
| token_count event | 46 | 45 | -1 |
| shell command | 50 | 50 | 0 |
| root-only | 5 / 5 | 5 / 5 | 0 |
| zero drift | 5 / 5 | 5 / 5 | 0 |

Candidate68のiteration順top-level tool callは`3 / 11 / 11 / 4 / 11`、reasoning itemは`4 / 6 / 6 / 5 / 7`、shell commandは各10件だった。F9削除による追加worker、command増加、成果欠落は観測しなかった。一方、tool cycleはCandidate43から減らず、tokenとelapsedのruntime削減も確認できなかった。

標準`owner-producer-evidence/v1` collectorはCandidate68の5 runを`inadmissible`とした。これはF10-onlyの既知の診断状態であり、5 runは所定response、zero drift、許可範囲を満たしてscore `4`だった。正式owner eligibilityへ読み替えない。

## 判断と次の対象

Candidate68から確定できる範囲は次のとおりである。

1. F9一文を削除しても、F10 `N=5`では成果品質、root-only、zero drift、command集合を維持した。
2. top-level tool callは`40 -> 40`で、F9削除が経路を短縮した証拠はない。
3. 3 KPIのうちqualityは同値、token中央値とelapsed中央値は増えた。token合計も事前上限を426超えた。
4. gateに従いA / F追加scope / Dは未実行である。F9を一般に削除可能とは判断しない。
5. Candidate68へ補助predicateを追加せず、standard14、採用、release、本体反映へ進めない。

次の意味単位を試す場合はCandidate43へ戻り、`F5`の「producer変更は旧bindingを失効し、新identityのTaskSpecで行う。」だけを対象にする。F9、Candidate67の削除、`D6 / R1 / R2`を同じcandidateへ混ぜない。producer変更の正の境界を持つ保存caseを先に選び、F10だけを代理caseにしない。

## 登録証跡

- Candidate43 result ID: `6965832090ad4b1b8507c7c8496dc1c5`
- Candidate68 result ID: `bf759a8f43474ea196495b4d565297af`
- Candidate68 result content SHA-256: `be99e6ff42d75b550e972a0383fcbf8008a982a04d2d5942c24bf49e7e943d42`
- Candidate68 execution archive SHA-256: `d007026ba30cfbb457ae5ed395d82542b0b92bca9b0b2edd8ac9b1c254be7a53`
- comparison view: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3/comparison-views/candidate43-candidate68-independent-review-operation-removal-f10-n5-20260722-r1.json`

Candidate68の採用、release、本体反映は未判断、未実施である。
