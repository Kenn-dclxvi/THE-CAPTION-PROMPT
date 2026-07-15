# 共有Python runtime

## 目的

検証workspaceごとに約356MBの`.venv`を複製せず、1つの固定runtimeからPython packageを共有する。各runのpath契約、Git分離、並列実行の独立性は維持する。

## 採用方式

単純なsymlinkは使用しない。THE-CAPTIONのbootstrap contractは、`VIRTUAL_ENV`、`sys.prefix`、`sys.executable`が実行workspace内の`.venv`を指すことを要求するためである。

Layer 2 adapterの`venv_shim` materializationを使用する。

```text
validation environment/
└── .venv/                         # 共有・固定、約356MB
    ├── requirements.freeze.txt    # package identity
    ├── bin/
    └── lib/python3.14/site-packages/
                    ^
                    | read-only shared packages
                    |
<run workspace>/
└── .venv/                         # runごと、実測約124KB
    ├── pyvenv.cfg                 # local sys.prefix
    ├── bin/                       # local activate / Python / console scripts
    └── lib/python3.14/site-packages/
        └── the_caption_shared_runtime.pth
```

shimはworkspace内で`python -m venv --without-pip`を実行して作る。共有runtimeのsite-packagesを`.pth`で追加し、console scriptはlocal Pythonを使う小さなscriptとして配置する。run中のpackage追加はlocal site-packagesへ入り、共有runtimeを更新しない。

## Run capsule

```json
{
  "parameters": {
    "runtime_links": [
      {
        "target": ".venv",
        "source": "/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/environment/.venv",
        "identity_file": "requirements.freeze.txt",
        "identity_sha256": "61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73",
        "materialization": "venv_shim",
        "python_version": "3.14.5"
      }
    ]
  }
}
```

adapterは次をAgent起動前かつ計時対象処理の前に確認する。

1. `identity_file`自体のSHA-256がRun capsuleと一致する。
2. 共有runtimeのPython versionがRun capsuleと一致する。
3. 共有runtimeの`pip freeze --all`が`requirements.freeze.txt`とbyte単位で一致する。
4. shimから`pip`と`pytest`をimportできる。
5. shimの`sys.prefix`と`sys.executable`がworkspace内を指す。
6. `.venv/`がGit-ignoredで、tracked driftを生まない。

## 並列実行

package codeだけを共有し、次はworkspaceごとに分離する。

- `.venv` shimとlocal site-packages
- `.coverage`、`.pytest_cache`、reports、logs
- repository stateとAgent成果
- condition commitと実行証跡

共有runtimeは評価中に更新しない。dependencyを変える場合は新しいruntimeを作り、新しいfreeze identityとしてRun capsuleをrevisionする。既存runtimeをin-place更新して過去runと同じidentityを名乗らせてはならない。

## Qualification

2026-07-15に固定target `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`で確認した。

- local shim size: `124KB`
- Python: `3.14.5`
- focused bootstrap contract: pass
- full gate: `326 passed / 3 skipped`

packageが自身のinstallation directoryへ書き込む特殊なcase、共有pathをsandboxから読めない実行環境、OS / Python minor versionが異なる環境では`copy` materializationへ戻す。
