# Candidate43 / Candidate51 F10 token増加要素の分析

## 結論

Candidate51のF10 token合計がCandidate43より`+48,549`、`+6.91%`だった主因は、prompt candidateではなく、実行時にmodel-visibleだったskill / plugin説明の増加である。

registry上のcompatibility keyは一致するが、Agent環境のmodel-visible入力は一致していない。Candidate43 / Candidate49は7 skillを提示された一方、Candidate51はGitHub、Gmail、Google Drive系を含む拡張後のskill一覧を提示された。Candidate51の1 runには追加のplugin説明も入った。

この差はprofileの`runtime_identity_sha256`に反映されず、現行compatibility keyでも検出されなかった。したがって、Candidate43 / Candidate49 / Candidate51のtoken差はprompt identityだけが異なる互換比較として扱わず、diagnostic-onlyとする。登録済みresultはappend-onlyのまま変更しない。

## Model-visible入力差

root rolloutの先頭入力を直接確認した。

| 項目 | Candidate43 | Candidate51 |
| --- | ---: | ---: |
| `base_instructions` | 17,920文字 | 17,920文字 |
| `base_instructions` SHA-256先頭 | `0d9711441040` | `0d9711441040` |
| 最初のdeveloper message | 5,217文字 | 10,870文字、1 runは11,884文字 |
| 提示skill | 7 | GitHub / Gmail / Google Drive系を追加 |
| candidateを含むuser message | 6,397文字 | 5,389文字 |
| first model input | 15,327〜15,343 token | 16,286〜16,494 token |

Candidate51のroot `AGENTS.md`はCandidate43より`1,507 bytes`小さい。この縮小によりcandidateを含むuser messageは`1,008文字`小さくなった。一方、skill / pluginを含むdeveloper messageは`5,653文字`以上増え、netの初回inputはrunごとに`+943 / +959 / +967 / +959 / +1,167 token`となった。

## F10差の分解

Candidate43のF10 input tokenは`689,536`、Candidate51は`737,406`で、差は`+47,870`だった。

Candidate51の各runについて、同じiterationの初回input差をそのrunのmodel step数へ掛けると、固定model-visible入力の増加は次になる。

| iteration | C51 model step | 初回input差 | 反復input差 |
| ---: | ---: | ---: | ---: |
| 1 | 12 | +959 | +11,508 |
| 2 | 4 | +943 | +3,772 |
| 3 | 4 | +967 | +3,868 |
| 4 | 12 | +959 | +11,508 |
| 5 | 6 | +1,167 | +7,002 |
| 合計 | 38 |  | +37,658 |

`37,658`は観測input差`47,870`の`78.66%`である。

残る`10,212` tokenはmodel step分布と動的contextの差に対応する。

- 12-step run 2件を揃えると、環境差補正後のCandidate51はCandidate43より`-1,878` input tokenだった。
- 4-step run 2件を揃えると、環境差補正後のCandidate51はCandidate43より`-5,335` input tokenだった。
- 残る中間runはCandidate43が5 step、Candidate51が6 stepで、環境差補正後もCandidate51が`+17,425` input tokenだった。
- `-1,878 - 5,335 + 17,425 = +10,212`で残差と一致する。

output token差は`+679`だった。したがってtotal token差`+48,549`は、model-visible環境差`+37,658`、残る1 model stepを中心とする動的input差`+10,212`、output差`+679`へ分解できる。

## 判定

- 事実: C43 / C51でbase instructionsは同一だった。
- 事実: skill / pluginを含むdeveloper入力はCandidate51で大きくなった。
- 事実: その固定差だけでF10 input差の78.66%を説明する。
- 事実: 同じ12-step / 4-step群は環境差補正後にCandidate51の方が小さい。
- 事実: Candidate51にはC43より1 model step多い中間runがあった。
- 判定: `+6.91%`をCandidate51 promptの悪化または`INDEPENDENCE`不足の証拠にしない。
- 判定: Candidate51のroot completion復元効果も、C49とのmodel-visible環境が一致する再試験まで確定しない。

## 次の条件

再試験では、prompt identity以外にmodel-visible skill / plugin catalogのnormalized identityを固定して比較する。少なくとも各runの最初のdeveloper messageから、動的workspace pathを除いたskills / apps / plugins blockのhashを保存し、同一hashだけを互換比較へ含める。

この環境identityを固定するまで、Candidate52や`INDEPENDENCE`復元を追加しない。

## 固定再試験

2026-07-21にapps、plugins、plugin sharingを無効化し、model-visible catalog SHA-256を各runで検査する[`C43 / C51固定再試験`](candidate43-candidate51-catalog-fixed-targeted-n5_2026-07-21.md)を追加した。20 / 20 runが同一catalog identityに一致した。

固定再試験ではCandidate51のF10 tokenがCandidate43より`+22.70%`、model stepが`48 -> 60`だった。Candidate51は5 / 5 runで11 tool callへ分割し、Candidate43には3 / 7 tool callへまとめるrunがあった。同じ11 tool call経路ではCandidate51のinput tokenが`-1.54%`だった。したがって、旧`+6.91%`の環境要因と、新しい固定条件で確認したrouting差を分離する。
