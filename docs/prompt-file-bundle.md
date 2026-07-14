# Prompt file bundle方式

## 1. 目的

Prompt file bundle方式は、比較対象のprompt setを単一の文字列として渡すのではなく、THE-CAPTION内で使用されるファイル構成と相対pathを保ったまま固定し、実行用fixtureへ配置する方式である。

この方式は、次を目的とする。

- baselineとcandidateを独立したprompt identityとして再現できるようにする
- `AGENTS.md`と参照文書のpath関係を実運用と揃える
- prompt変更とcase fixtureの不具合をGit上で区別する
- 実行後も、どのファイル内容をprompt set A / Bとして使ったか検証できるようにする
- quality raterへprompt identityを開示せず、成果だけをblindで採点できるようにする

本書はprompt setをLayer 2の実行workspaceへ供給する配下機能を定義する。評価基盤の4 Layer、3 KPI、winner schemaは変更しない。

本書はfile bundle方式の設計と実装境界を記録する。exporter、最初のbaseline / candidate、Codex execution adapterは実装済みである。rating viewとblind rater入力境界は未解決であり、artifactが存在しても評価済み、採用済み、本体反映済みであることを示さない。

## 2. 入力の分離

1回の評価runで使用する入力は、少なくとも次の3種類へ分離する。

| 入力 | 内容 | model-visible |
| --- | --- | --- |
| case fixture | 固定commitのTHE-CAPTIONへ`seed.patch`を適用した開始状態 | repositoryの状態として見える |
| prompt bundle | `AGENTS.md`と、それが参照するprompt関連ファイル | 見える |
| case task | Agentへ依頼する作業文 | 見える |

oracle、grader、expected result、quality score、A / Bの勝敗情報は、これらへ含めずAgentから分離する。

`seed.patch`とprompt bundleは用途が異なる。

- `seed.patch`は、固定commitから評価対象の壊れた状態を再現する。
- prompt bundleは、その壊れた状態へどのprompt setで取り組むかを固定する。

## 3. Repository内の保存形

baseline、candidate、releaseは既存の別pathを維持する。評価へ投入するbaselineとcandidateは、どちらも解決済みのfull bundleとして保存する。

```text
THE-CAPTION-PROMPT/
└── prompts/
    ├── baselines/
    │   └── <baseline-id>/
    │       ├── manifest.json
    │       └── files/
    │           ├── AGENTS.md
    │           ├── docs/
    │           │   └── <prompt reference file>
    │           └── prompts/
    │               └── <prompt file>
    ├── candidates/
    │   └── <candidate-id>/
    │       ├── manifest.json
    │       └── files/
    │           ├── AGENTS.md
    │           ├── docs/
    │           │   └── <prompt reference file>
    │           └── prompts/
    │               └── <prompt file>
    └── releases/
        └── <release-id>/
```

`files/`以下は、THE-CAPTIONへ配置するときの相対pathをそのまま表す。

```text
bundle内                              実行workspace内
files/AGENTS.md                    ->  AGENTS.md
files/docs/prompt-guide.md         ->  docs/prompt-guide.md
files/prompts/implement.md         ->  prompts/implement.md
```

Codexは`AGENTS.md`をrepository rootから実行current working directoryまでpath階層に従って発見し、近い階層の指示を後から適用する。したがって、bundle内のファイルを1 directoryへ平坦化しない。root以外の`AGENTS.md`を対象に含める場合も、元の相対pathを維持する。

bundleへ含めるpathは、固定した対象commit上でAgentが参照できるprompt関連ファイルを列挙して決める。作成者の想定だけで参照ファイルを省略しない。

## 4. Full bundle

評価入力には、baselineに対する差分だけでなく、各conditionで使用するファイル一式を保存する。

```text
baseline bundle
├── manifest.json
└── files/          # baselineだけで内容が完結する

candidate bundle
├── manifest.json
└── files/          # candidateだけで内容が完結する
```

candidate作成中にdiffを利用してもよいが、`evaluation_ready`へ進める前にfull bundleへ解決する。これにより、後からbaselineが変化してもcandidateの実体が変わらず、AとBをそれぞれ単独で再現できる。

## 5. Manifestとidentity

各bundleは`manifest.json`で由来、対象path、ファイルhash、bundle全体のidentityを固定する。

```json
{
  "schema_version": "the-caption-prompt.bundle/v1",
  "prompt_identity": "<prompt identity>",
  "source": {
    "repository": "Kenn-dclxvi/THE-CAPTION",
    "commit": "<source commit>",
    "tree": "<source tree>"
  },
  "files": [
    {
      "target": "AGENTS.md",
      "type": "file",
      "sha256": "<content sha256>"
    },
    {
      "target": "docs/prompt-guide.md",
      "type": "file",
      "sha256": "<content sha256>"
    }
  ],
  "bundle_sha256": "<bundle identity>"
}
```

`files`は`target`で昇順に並べる。現在のexporterは、schema versionと順序を固定した各entry全体をcanonical JSONへ変換して`bundle_sha256`を計算する。通常fileのentryにはtarget、type、mode、Git blob SHA-1、content SHA-256を含め、symlinkのentryにはtarget、type、mode、Git blob SHA-1、link targetを含める。

実行adapterはoverlay前に次を検証する。

1. manifestに記載された全targetが`files/`内に存在する
2. manifestにないファイルが`files/`内に存在しない
3. 各ファイルのSHA-256が一致する
4. 再計算した`bundle_sha256`が一致する
5. targetが絶対pathまたは`..`を含まず、workspace外を指さない

manifestは実行制御用であり、Agentのworkspaceへ配置しない。実際に使用したmanifestはRun capsule側の証跡として固定し、quality raterへは渡さない。

## 6. Layer 2での展開

Layer 1のfixtureはA / Bで共通とする。Layer 2はconditionごとにfixtureをcopyし、そのcopyへ対応するbundleをoverlayする。

```text
Layer 1の固定fixture
固定commit + seed.patch適用済み
            |
            +-----------------+
            |                 |
            v                 v
       A用workspace       B用workspace
            |                 |
     baseline bundle     candidate bundle
       をoverlay            をoverlay
            |                 |
            v                 v
       同一case taskでAgentを実行
```

展開後の概念上のworkspaceは次のようになる。

```text
<run workspace>/
├── .git/
├── AGENTS.md                         # bundleから配置
├── docs/                             # bundle対象pathを配置
├── prompts/                          # bundle対象pathを配置
├── src/
│   └── domain/
│       └── market_units_snapshot.py  # seed.patchで壊した対象
└── tests/
```

Run capsuleの`parameters`には、基盤が解釈しないopaque parameterとしてbundle pathと期待するidentityを持たせる。

```json
{
  "parameters": {
    "prompt_bundle": "/absolute/path/to/<bundle-id>",
    "prompt_identity": "<prompt identity>",
    "bundle_sha256": "<expected bundle sha256>"
  }
}
```

adapterは期待identityを検証した後だけoverlayする。同じconditionの全caseと全repetitionでは、同じ`prompt_identity`と`bundle_sha256`を使用する。

## 7. Git状態の分離

bundleを単純にoverlayしただけでは、Agentからprompt変更とcase seedが同じ未commit変更に見える可能性がある。

```text
 M AGENTS.md
 M docs/prompt-guide.md
 M src/domain/market_units_snapshot.py
```

これを避けるため、Agent実行前に次を行う。

1. bundleを検証してoverlayする
2. bundleのtarget pathだけをstageする
3. 固定したauthor、committer、timestamp、messageでcondition commitを作る
4. bundleに変更がないconditionでも同じ手順にできるよう、必要ならempty commitを許可する
5. `seed.patch`による変更はstageせず、壊れた作業状態として残す

実行開始時の`git status --short`は、原則としてseed対象だけを示す。

```text
 M src/domain/market_units_snapshot.py
```

condition commitへstageできるpathはmanifest記載pathだけとし、seed対象やAgentの成果を混入させない。condition commitのcommit / tree identityはRun capsuleの証跡へ記録する。

## 8. Model-visibleとmodel-invisibleの境界

bundleの`files/`以下はmodel-visibleである。次はmodel-invisibleとしてworkspaceへ置かない。

```text
model-visible
├── bundleのfiles/以下
├── case task
└── case fixtureの作業状態

model-invisible
├── manifestとA / B binding
├── seed.patchそのもの
├── private case data
├── oracle
├── grader prompt
├── expected result
├── quality score
└── winner情報
```

Agentは配置されたpromptを読むことができるが、それがbaseline、candidate、A、Bのどれであるかを示すlabelは受け取らない。

## 9. Blind rating用の成果表示

実行後の完全なworkspaceには、conditionごとに異なるpromptファイルが残る。完全なworkspaceをそのままquality raterへ渡すと、prompt内容からconditionを推測できる可能性がある。

推奨案は、完全な実行証跡とは別にblind rating用の成果表示を生成することである。

```text
layer2/evidence/<run_id>/
├── workspace/               # 完全な実行証跡
├── rating-view/
│   ├── result.diff          # bundle targetを除外した成果差分
│   ├── validation.json      # test commandと結果
│   └── final-response.txt   # Agentの最終応答
├── usage.json
└── execution.json
```

`result.diff`から除外するのはmanifestに記載されたbundle targetだけとする。Agentが変更した実装、test、その他の成果pathは残す。

推奨案では、quality raterへ渡す範囲を該当caseのmodel-visible taskと`rating-view/`に限定する。`manifest.json`、Run capsule、bindings、完全なworkspaceは渡さない。採点後も完全なworkspaceは監査用証跡として保持する。

このrating viewはLayer 2が作る実行証跡の配下機能であり、新しいLayerまたはKPIを追加するものではない。

ただし、現在の`docs/evaluation-loop-manual.md`はquality raterへ`evidence/<run_id>/`を渡し、その中に`workspace/`を含める契約である。したがって、上記の推奨案をそのまま採用すると、固定manualのrater入力境界と一致しない。

この不一致を暗黙に処理しない。file bundleを使った正式runの前に、次を明示的に決める必要がある。

1. 固定manualを要件変更として改訂し、rater入力を`rating-view/`へ限定する
2. 固定manualを維持できる別の遮蔽方法を設計する

この判断が完了するまで、file bundleを使ったrunをblind quality rating済みの正式evidenceとして扱わない。

## 10. 実行時directoryの全体像

次はSection 9のrating view案を採用した場合のdirectory案であり、現在の固定schemaではない。

```text
<cycle>/
├── layer1/
│   ├── set.json
│   └── fixtures/
│       └── <case id>/               # A / B共通の壊れたfixture
├── layer2/
│   ├── evidence/
│   │   └── <blind run id>/
│   │       ├── workspace/           # bundle適用後の完全なrun
│   │       ├── rating-view/         # blind採点へ渡す成果
│   │       ├── usage.json
│   │       └── execution.json
│   ├── capsules/
│   │   └── <blind run id>.json      # bundle identityを含む。raterへ渡さない
│   ├── bindings/
│   │   └── <blind run id>.json      # A / B binding。raterへ渡さない
│   └── extensions/
│       └── <blind run id>/
├── layer3/
│   └── ratings/
└── layer4/
    └── decision.json
```

## 11. Bundleへ含めるものと含めないもの

bundleへ含めるものは、Agentの行動へ影響するprompt setの構成要素に限定する。

| 含める | 含めない |
| --- | --- |
| root `AGENTS.md` | case fixture |
| 対象にする階層別`AGENTS.md` | `seed.patch` |
| `AGENTS.md`から参照される指示文書 | case task |
| promptとして読み込ませるfile | oracle / grader |
| prompt set identityに含めるmodel-visible設定file | expected result |
| 必要なsymlinkとそのlink target | run log / score / winner |

README、説明用sample、履歴文書などがAgentから読める場所に存在しても、それがprompt setの一部でない場合はbundleへ自動的に含めない。含めるpathの判断はmanifest revisionとして明示する。

## 12. Failure条件

次の場合はAgentを起動せず、runを正式評価へ使用しない。

- manifestまたはfile hashが一致しない
- bundleに未記載fileがある
- unsafeなtarget pathがある
- overlay後の内容がmanifestと一致しない
- condition commitへmanifest外の変更が混入した
- seed対象以外の予期しない未commit変更が実行前にある
- A / Bでcase fixture、case task、model、permission、反復条件が一致しない
- rating viewへbundle targetまたはA / B identityが漏れた

Codex adapterが既知の外部要因をstderrの客観的signatureから検出した場合、`EVAL_RUN_STATUS_FILE`へ`status: excluded`、`category: external_failure`、安定した`reason_code`を出力する。Layer 2はraw artifactと`exclusion.json`を保持し、このattemptを採点・KPI比較・有効反復数から除外する。同じcondition / case / repetitionは再実施してA / Bの有効回数を揃える。Agentの自己申告だけでは除外しない。

現在自動検出するsignatureは`collab spawn failed: no thread with id:`で、reason codeは`codex_collab_parent_thread_missing`である。`timeout_ms must be at least 10000`などAgentによる不正なtool parameter、analytics送信失敗、ephemeral sessionのhook transcript警告、backgroundのmodel refresh失敗は、このsignatureだけではrun経路が無効になったと確定できないため自動除外しない。

multi-agent実行では親threadをCodexのthread storeから解決できる必要がある。`codex exec --ephemeral`では親thread欠落が3attempt連続で再現したため、Codex adapterはsessionを既定のlocal storeへpersistする。session fileは非公開のlocal run evidenceであり、repositoryへcommitしない。A / Bは同じsession modeで実行し、mode変更後は新しいcycleとenvironment revisionとして扱う。

## 13. 現在の実装境界

現在の実装状態は次のとおりである。

| 項目 | 状態 |
| --- | --- |
| 明示pathからのbaseline export | 実装済み |
| baselineのbit-identicalなcandidate複製 | 実装済み |
| manifest、file identity、bundle hash検証 | 実装済み |
| symlinkを保ったfull bundle | 実装済み |
| fixtureへのoverlay | 実装済み |
| deterministicなcondition commit | 実装済み |
| `codex exec`実行と`total_tokens`取得 | 実装済み |
| Codex collaborationの親thread欠落を自動検出し、attemptを除外して同じslotを再実施可能にする | 実装済み |
| multi-agent用のpersisted parent session | 実装済み。ephemeral modeは親thread欠落が再現したため不採用 |
| 固定commitからのprompt path自動発見 | 未実装。最初のbundleは17 pathを明示指定 |
| blind rater入力と固定manualの不一致に対する判断 | 未決定 |
| rating viewまたは代替遮蔽機能 | 未実装 |
| A / B、全case、`1..N`のrun生成・実行automation | 未実装 |
| case qualification | `r1`は`case_revision_not_qualified`、`r2`は`execution_qualified_null_calibration_failed` |

最初のbundleとnull calibrationの結果は`evaluations/results/TC-F01-r1_identical-bundle-pilot_2026-07-15.md`、`evaluations/results/TC-F01-r2_identical-bundle-pilot_2026-07-15.md`、`evaluations/results/TC-F01-r2_identical-bundle-n10_2026-07-15.md`を参照する。

## 14. 関連文書

- `docs/repository-contract.md`
- `docs/prompt-comparison-workflow.md`
- `docs/evaluation-loop-manual.md`
- [CodexのAGENTS.md仕様](https://learn.chatgpt.com/docs/agent-configuration/agents-md.md)
