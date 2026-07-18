# Candidate35 / Candidate38 targeted N=5 token trace analysis

## 結論

Candidate38 - Candidate35の10 run token差`+255,767`は、prompt本体の静的size差ではなく、実行中の追加tool turnと、それに伴うcontext再入力で発生した。

token差の`99.34%`に当たる`+254,073`はinput tokenである。output token差は`+1,694`だった。session数は両setとも20であり、追加worker起動は原因ではない。

増加の`90.50%`はF10 monthly reviewで発生した。F10ではCandidate38がCandidate35より`exec`を8回、`wait`を3回、model stepを10回多く実行した。

## 対象evidence

- Candidate35 result ID: `92cceedd0adf4a489f861fdc15d1566f`
- Candidate38 result ID: `dfad99c8843c431493132cac6cc2a054`
- comparison: [`outcome quality targeted N=5`](candidate35-candidate38-outcome-quality-owner-diagnostic-v9-targeted2-n5_2026-07-19.md)
- 対象: 両setの10 runに保存されたall-agent usage、root / child rollout、tool call、model step
- raw rolloutとsession pathは非公開evidenceとしてrepositoryへ保存しない。

## Token内訳

| token | Candidate35 | Candidate38 | 差 |
| --- | ---: | ---: | ---: |
| input | 2,036,355 | 2,290,428 | +254,073 |
| output | 37,525 | 39,219 | +1,694 |
| total | 2,073,880 | 2,329,647 | +255,767 |
| cached input | 1,701,632 | 1,915,648 | +214,016 |

Candidate38のprompt本体はCandidate35比`+41 bytes`である。仮に1 byteを1 tokenとして全model stepで繰り返し計上しても、静的size差だけでは観測差を説明できない。

## Case別

| case | C35 total | C38 total | 差 | 全差に占める割合 |
| --- | ---: | ---: | ---: | ---: |
| F05 clarification | 692,914 | 717,223 | +24,309 | 9.50% |
| F10 monthly review | 1,380,966 | 1,612,424 | +231,458 | 90.50% |

F10のinput tokenは`1,355,968`から`1,584,971`へ`+229,003`増えた。F10のoutput token差は`+2,455`である。したがって、追加tokenは成果記述量ではなく、途中turnのcontext再入力に使われた。

## 実行経路差

| F10の観測 | Candidate35 | Candidate38 | 差 |
| --- | ---: | ---: | ---: |
| session | 10 | 10 | 0 |
| `spawn_agent` | 5 | 5 | 0 |
| `exec` | 51 | 59 | +8 |
| `wait_agent` | 7 | 10 | +3 |
| tool call合計 | 63 | 74 | +11 |
| model step | 74 | 84 | +10 |

Candidate38のF10 traceでは、rootがfinding、根拠、zero driftを3つの`result unit`として明示的に分けたrunがあった。childは開始identity、authority、diff、source、終了statusを個別に取得した。長いrunではrootもauthorityを読み、その後childが同じauthorityとsourceを再取得していた。

Candidate35は同じowner workerを起動したが、reviewを一つのpredicateとして委譲するrunが多かった。session数と成果内容が同じまま、Candidate38では証拠取得と待機のturnだけが増えた。

## 原因

### 事実

- Candidate38の`SPEC`は、evidenceまたはinvalidation条件が異なるrequired outcomeを最小result unitへ分ける。
- Candidate38の`CONTEXT`は、worker packetへunit別の`direct evidence`を固定する。
- 実traceはF10を3 result unitへ分け、個別commandで証拠を得る経路を含んだ。
- 追加tool turnごとに長い既存contextが再入力され、input tokenが増えた。

### 推測

`result unit`という論理的な判定分割が、実行手段の分割として解釈された可能性が高い。特に、packetへ`direct evidence`を固定する規則は、rootがpacket作成前に証拠を取得し、producer workerが同じ証拠を再取得する動機になる。

N=5には実行経路のばらつきもあるため、全token差をprompt規則だけの決定的因果とは断定しない。ただし、静的size、session数、output量では説明できず、追加tool / model turnとtrace上のresult-unit分割は一致している。

## 必要な制御

次の修正対象はresult unit自体ではなく、result unitと実行回数の境界である。

1. result unitは判定、binding、invalidationの論理単位に限定する。
2. unitごとの別command実行を要求しない。
3. 一つの直接証拠を複数unitへbindできるようにする。
4. worker packetへ固定するのは取得済み`direct evidence`ではなく、必要なevidence identityまたはselectorとする。
5. non-root producerのoperationではrootが証拠を先に取得せず、producerが一度だけ取得する。

この制御により、C34 F05の成立済み成果の保持とC35 F10のlocation直接確認を維持しながら、root / childの重複確認とper-unit tool turnを抑える余地がある。

