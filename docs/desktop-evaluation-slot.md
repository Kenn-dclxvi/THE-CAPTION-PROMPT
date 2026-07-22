# Desktop評価slot

## 結論

Agent-visibleな広いconcurrencyを必要とする評価では、candidateごとにcloneを増やさない。

固定pathのmanaged workspaceを一つ用意し、run開始前にtarget commit、prompt bundle、runtimeを再materializeする。Codex Desktopにはその固定pathを一度だけproject登録し、同じslotで新しいtaskを順次開始する。

この機能はDesktop実行条件を準備する配下adapterである。Evaluation foundation v3のLayer、KPI、result schemaは変更しない。

## 用語

`Desktop評価slot`は、Codex Desktop taskの開始workspaceとして再利用するisolated Git checkoutである。

slotは`.git/info/the-caption-prompt-desktop-evaluation-slot.json`を管理markerとする。markerがない既存directoryはslotとして採用しない。

## 準備

[`prepare_desktop_evaluation_slot.py`](../scripts/prepare_desktop_evaluation_slot.py)を使う。

```bash
python3 scripts/prepare_desktop_evaluation_slot.py \
  --source-repo /path/to/THE-CAPTION \
  --workspace /path/to/THE-CAPTION-DESKTOP-EVAL-SLOT-01 \
  --target-commit <target-commit> \
  --target-tree <target-tree> \
  --prompt-bundle /path/to/prompt-bundle \
  --bundle-sha256 <bundle-sha256> \
  --runtime-source /path/to/shared/.venv \
  --runtime-target .venv \
  --runtime-identity-file requirements.freeze.txt \
  --runtime-identity-sha256 <runtime-identity-sha256> \
  --runtime-materialization venv_shim \
  --runtime-python-version <python-version>
```

初回だけslotをcloneする。2回目以降は同じpathを使い、cleanなmanaged slotだけを別targetまたは別prompt bundleへ切り替える。

dirtyなslot、管理markerがない既存repo、target identity不一致、bundle identity不一致、runtime identity不一致では変更せず停止する。

## Desktop登録

評価taskへ過去のresultやrepository情報を流入させないため、task開始前にuser configの`memories` featureを無効にする。

`~/.codex/config.toml`:

```toml
[features]
memories = false
```

設定値は次のcommandで確認する。

```bash
codex --strict-config doctor
codex features list
```

`codex features list`で`memories ... false`を確認した後に、新しいDesktop taskを開始する。2026-07-21のpreflightでは、起動中のDesktopを再起動せず、新規taskへ更新後のuser configが読み込まれた。

slot pathは初回だけCodex Desktopへ登録する。

```bash
codex app /path/to/THE-CAPTION-DESKTOP-EVAL-SLOT-01
```

このcommandはproject登録にだけ使う。評価条件としてのmemory除外はuser configと各taskの開始gateで確認する。adapterは通常利用中のDesktopを自動終了してはならない。

登録後の新しいtaskは、このprojectを`local`環境で開始する。`projectless` taskは別directoryを作るため使わない。別workspaceへ後から`cd`する方法も、開始時にcandidateの`AGENTS.md`が注入されないため使わない。

分離`app-server`を`--disable memories`で起動する方法はmemoryを除外できるが、2026-07-20のpreflightではAgent-visible concurrencyがroot込み4だった。31-slot Desktopと同一条件にならないため代替にしない。起動中Desktopへ`codex app --disable memories <slot>`を送る方法も、host側のmemory設定を変えなかったため評価条件の設定方法にしない。

## 開始gate

各runは、調査やworker起動の前に次を確認する。

1. `pwd`がslot markerの`workspace`と一致する。
2. `HEAD`とtreeがmarkerの`prompt_overlay_commit`、`prompt_overlay_tree`と一致する。
3. `git status --short`が空である。
4. 開始時repository instructionsへ対象bundleのroot `AGENTS.md`が注入されている。
5. developer instructionsの`available concurrency slots`がprofileの要求値と一致する。
6. developer instructionsに`## Memory`、memory folder、`MEMORY_SUMMARY`の指示がない。
7. model、reasoning effort、permission、TaskSpecがrun capsuleと一致する。

一つでも不一致なら成果評価を始めず、environment mismatchとして除外する。

## 再利用境界

- 一つのslotではtaskを同時実行しない。
- 実行中taskがあるslotを再materializeしない。
- run終了後にrepository driftがあれば、自動で破棄せず原因を確認する。
- 次candidateは、前runのtask終了とclean stateを確認してから同じslotへmaterializeする。
- resultはprompt set identityとrun条件へappend-onlyで保存する。slot path自体をresult identityにしない。

## 結果回収

Desktop taskのroot thread id、開始・終了時刻、exact workspaceを保存する。同じworkspaceから起動されたrootと全subagent sessionの最終usageを収集し、既存のall-agent token accounting revisionに従って`total_tokens`を算出する。

全sessionの最終usageを取得できないrunはtokenを推定せず、外部計測失敗として除外する。
