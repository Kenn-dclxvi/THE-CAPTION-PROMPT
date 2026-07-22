# TC-A06 C43 max slot31 memory-off N=1 diagnostic

## 結論

C43、`gpt-5.6-sol`、reasoning effort `max`、root込み31 slot、Memory指示なし、`N=1`でA06を実行した。

開始gateは全項目通過した。最終監査は`NONCONFORMING`で、確認済み不適合を12件報告した。重大度内訳は高7件、中5件である。

このrunではrootが監査operationの唯一のproducerになり、workerを起動しなかった。sessionは1、tool callは72、model stepは74、all-agent `total_tokens`は`9,415,805`、root task durationは`1,352.530`秒だった。

過去の`ultra` runとはreasoning effortとAgent環境が異なるため、互換KPI比較へ混ぜない。blind quality rating、Layer 4登録、winner、採用、release、本体反映は行っていない。

## 固定条件

| 項目 | 値 |
| --- | --- |
| case | `TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1` |
| target commit | `eebc1c6c106f504978482238fd760fb73f5fff36` |
| target tree | `6366adbb7eaf9db55763e39797b5e070905ede16` |
| prompt identity | `the-caption-3ce91a4-outcome-authority-boundary-r1` |
| bundle sha256 | `b6455c1774c32e0bc9cb5bfe2257d35911b6797ecd5b2f3b77bbf41e4bcca531` |
| prompt overlay commit | `a1d5945332bac14972d037b3676fe2ed6f7d5580` |
| prompt overlay tree | `6366adbb7eaf9db55763e39797b5e070905ede16` |
| model / reasoning | `gpt-5.6-sol` / `max` |
| Agent-visible concurrency | root込み`31` |
| Memory instructions | `absent` |
| runtime | Python `3.14.5` / `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` |
| workspace | `/Users/kenn/repos/THE-CAPTION-DESKTOP-EVAL-SLOT-01` |
| root thread | `019f834c-b138-7031-a7f2-a37c5592029f` |
| start gate | pass |
| end drift | none |
| comparison status | `diagnostic_only / max / memory_off / N=1` |

## 診断値

`tool call`はroot rolloutの`custom_tool_call`を数えた。`model step`は`token_count` eventを数えた。tokenは最終usageを用いた。workerがないためroot値とall-agent値は同一である。

| 診断値 | 値 |
| --- | ---: |
| session | 1 |
| worker | 0 |
| tool call | 72 |
| model step | 74 |
| context compaction | 1 |
| root task duration seconds | 1,352.530 |
| all-agent `total_tokens` | 9,415,805 |
| input tokens | 9,373,669 |
| cached input tokens | 8,878,848 |
| output tokens | 42,136 |
| reasoning output tokens | 26,409 |

tool callは72件すべて`exec`だった。`spawn_agent`、`wait_agent`、`send_message`は0件だった。

## 確認済み不適合

1. 高: `docs/reference/logic.md`が要求する資産1件以上かつ正の合計額を`src/domain/guard_rail.py`が検査せず、空または合計0の台帳を通常配信してCompletionLockを更新できる。
2. 高: Accepted `ADR-0004`がMonexを非blocking監査へ隔離する一方、`src/lib/utils.py`はMonex / IMAP資格情報がないとv4開始前に停止し、`src/app/v4_engine.py`にはMonex監査呼出しがない。
3. 高: `src/domain/universal_ingester.py`が米国終値確認へJP側`target_date`を渡し、18:45 JST時点で確定済みの前日終値を`PRE`等から`STALE`へ降格できる。
4. 高: Finalized ShadowLedger、daily metrics、market snapshot、月次Chronicle、CompletionLockの保存失敗を送信停止へ伝播せず、送信とlock処理を継続できる。
5. 高: 日次State分類が規約上の`total_diff_pct`、Safe Ratio、pricing status、`Share x Diff`を使わず、実質3状態と単純変動額順で処理する。
6. 中: 日次が月次再蒸留用`archive_context`を保存せず、因果ベクトル、regime、FX、VIX、tagが月次へ届かない。
7. 中: 日次HTMLに必須のShield phaseがなく、確定済みIron Bankの`DAY +0 / +0.00%`も`STATIC FACT`へ置換して非表示にする。
8. 中: 暫定メールにAppraisalを表示しても`last_displayed_date`を保存せず、7日制限内で再表示できる。
9. 高: 日次は単一`data/v4_shadow_ledger.json`を上書きする一方、月次は日付別履歴を要求する。単一fileだけを月初と月末に使い、正しいdaily metrics推移をゼロ変動で上書きできる。
10. 中: 月次data qualityが`pricing_stale_count`を集約せず、`(Market data unavailable)`も非空文字列として欠損日に数えない。
11. 高: 現行v4日次が生成しない旧`ledger_YYYYMMDD.json`を週次が必須とし、月次fallbackも同じ旧Ledger不在時に停止する。
12. 中: `src/domain/universal_ingester.py`と`src/domain/collection_history_updater.py`がfile I/O、HTTP、CSV保存を直接所有し、`src/AGENTS.md`のdomain / infra境界に反する。

## 検証結果

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q`: `326 passed, 3 skipped`
- `.venv/bin/python -m pip check`: `No broken requirements found`
- TypeScript typecheck: `node_modules`とglobal `tsc`がなく、依存導入は変更禁止条件に反するため未実行
- end identity: HEADとtreeは開始時と同一
- `git status --short`、通常diff、cached diff: empty
- repository edit、application実行、commit、外部送信: なし

Python test成功は適合証明に使わない。Shield欠落を期待するtestと、現行v4に生成元がない旧Ledgerをmock注入する週次testが含まれる。

過去の製造過程は、各変更をTaskSpec、producer identity、terminal resultへ結び付けるrepository内証跡がない。現物の不適合とは分け、過去processの適合・不適合はどちらも証明不能とした。

## 解釈

- 事実: current developer / repository controlの下では、C43はA06全体をroot producer 1件として実行し、31 slotをworkerへ使わなかった。
- 事実: authority、implementation path、reachable behaviorを結び付けた12件を最終報告した。
- 事実: no-driftとread-only条件を満たした。
- 未確定: blind ratingでscore `4`を維持するか。
- 未確定: 同じ`max`条件を反復した場合もroot-only routingが再現するか。

`N=1`からrouting一般則、efficiency、winner、採用、release、本体反映を判断しない。
