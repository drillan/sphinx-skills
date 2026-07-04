# スキル一覧

`sphinx-skills` が提供する 9 つのスキルの個別ドキュメントです。各ページは元の `SKILL.md` の主要部分を抜粋しています。完全な仕様は GitHub リポジトリの `skills/<name>/SKILL.md` を参照してください。

```{toctree}
:maxdepth: 1

sphinx-init
sphinx-config
sphinx-theme
sphinx-build
myst-authoring
rst-to-myst
revealjs-init
revealjs-config
revealjs-authoring
```

## ワークフロー全体像

スキルは互いに委譲しあう設計です。代表的な呼び出し関係は以下の通りです。

| 起点 | 委譲先 |
| --- | --- |
| `sphinx-init` | `sphinx-config` (conf.py 反映)、`rst-to-myst` (既存 .rst 検出時) |
| `sphinx-theme` | `sphinx-config` (html_theme / html_theme_options 反映) |
| `rst-to-myst` | `sphinx-config` (myst-parser 追加) |
| `sphinx-build` | `sphinx-config` (拡張不在エラー時の依存追加)、`revealjs-init` (スライドプロジェクト未初期化時の誘導) |
| `revealjs-init` | `sphinx-config` (conf.py 反映)、`revealjs-config` (設定値の知識)、`sphinx-build` (テストビルド以後) |
| `revealjs-config` | `sphinx-config` (revealjs_* 設定の反映) |

`conf.py` への変更はすべて `sphinx-config` の単一責務に集約されており、バックアップと明示的エラー伝播もここで一元化されます。
