# Typed boundary evidence

## 目的

実行開始時などの境界判定で、複数commandのraw stdoutをAgentが位置関係から対応付けるのではなく、実行adapterがread-onlyな観測値を1つのpredicateへbindし、typed evidenceとしてTaskSpecと同時に渡す。

この機能はprompt改善、quality rating、優劣判定、採用判断を行わない。`scripts/evaluation_loop.py`の4 Layer、3 KPI、result schemaも変更しない。既存resultは変更せず、typed evidenceを使うrunは別のexecution compatibility revisionへ固定する。

## 契約

Run capsuleの`parameters.boundary_observations`は、各要素を次の1対1対応に限定する。

```json
{
  "observation_id": "start-head-overlay",
  "operation_identity": "start-identity-check",
  "source": "workspace.git.head_commit",
  "predicate": {
    "operator": "string_equals",
    "expected_context": "prompt_overlay_commit"
  }
}
```

- 1要素は1つの`source`と1つの`predicate`だけを持つ。
- `observation_id`はcapsule内で一意とする。
- predicate operatorはv1では`string_equals`だけとする。
- expected valueはliteralの`expected`、またはadapterが所有する値を参照する`expected_context`のどちらか一方とする。
- observer errorは値を推定せず`unavailable`、観測成功かつpredicate不成立は`failed`、成立は`passed`とする。
- `failed`と`unavailable`をAgent側で別のraw outputから上書きしない。

## Read-only source registry

v1は任意commandをcapsuleから実行できる形にせず、adapterが所有する次のsourceだけを許可する。

| source | 観測対象 |
| --- | --- |
| `workspace.path` | 物理workspace path |
| `workspace.git.branch` | checkoutのbranch名。detached時は空文字列 |
| `workspace.git.head_commit` | `HEAD` commit |
| `workspace.git.parent_commit` | `HEAD^1` commit |
| `workspace.git.status_short` | short status |

source追加はregistryの明示変更として扱う。capsuleからshell文字列や任意argvを受け取らないため、観測interface自体をrepository変更や外部operationの経路にしない。

## Model-visible binding

adapterは観測後に`the-caption-prompt.boundary-evidence/v1`を`layer2/extensions/<run_id>/boundary-evidence/evidence.json`へ保存し、同じobjectを`<adapter-boundary-evidence-json>`としてTaskSpecへ添付する。列挙されたoperationの同一predicateは観測済みであり、Agentはその`status`を使用する。

TaskSpec本文、case revision、prompt bundleは変更しない。TaskSpecが要求するterminal conditionは維持し、typed evidenceが`failed`または`unavailable`ならAgentはその条件に従う。

## Compatibility

typed evidenceを使うcapsuleは次を固定する。

```json
{
  "agent_environment": {
    "adapter_schema_version": "the-caption-prompt.codex-adapter/v4"
  },
  "executor_parameters": {
    "boundary_evidence": {
      "binding_revision": "one-observation-one-predicate/v1",
      "schema_version": "the-caption-prompt.boundary-evidence/v1",
      "source_policy": "adapter_managed_read_only_registry"
    }
  }
}
```

adapterは宣言と実際の`boundary_observations`が片側だけにあるcapsule、またはrevisionが一致しないcapsuleを実行前に拒否する。これにより、raw observationをAgentへ委ねた既存resultとtyped evidence resultを暗黙に混ぜない。

`codex-adapter/v4`の`execution.json`はevidence schemaとcanonical JSON objectのSHA-256を保存する。raw log、session情報、一時workspaceは従来どおりrepositoryへcommitしない。

## 非目標

- case固有のexpected resultやgrader情報をadapterへ入れない。
- predicateをquality scoreやwinnerへ変換しない。
- TaskSpecにないgateを自動追加しない。
- Agentの全commandをadapterへ移さない。
- 既存のevaluation foundation固定点を拡張しない。
