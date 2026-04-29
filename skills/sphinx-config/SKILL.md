---
name: sphinx-config
description: Safely update docs/conf.py while preserving existing settings. Add or remove Sphinx extensions, MyST optional extensions, theme, project metadata. Triggers when user asks to add an extension, change project name/author/release, modify conf.py, or update Sphinx configuration.
license: MIT
allowed-tools: Read, Edit, Bash
---

## パッケージマネージャ検出

検出優先順位 (該当した時点で確定):

| 優先 | 判定条件 | 採用 |
|---|---|---|
| 1 | `uv.lock` が存在 | uv |
| 2 | `poetry.lock` が存在 | poetry |
| 3 | `Pipfile.lock` が存在 | pipenv |
| 4 | `.venv/` のみ存在 (lockfile なし) | plain venv |
| 5 | 上記すべて該当しない | ユーザー問い合わせ (推奨: uv) |

実行コマンド対応表:

| 操作 | uv | poetry | pipenv | plain venv |
|---|---|---|---|---|
| 依存追加 (docs グループ) | `uv add <pkg> --group docs` | `poetry add --group docs <pkg>` | `pipenv install --dev <pkg>` | `pyproject.toml` 手動編集 + `pip install -e ".[docs]"` |
| サブコマンド実行 | `uv run <cmd>` | `poetry run <cmd>` | `pipenv run <cmd>` | venv 有効化後 `<cmd>` |
| ビルド | `uv run make -C docs <target>` | `poetry run make -C docs <target>` | `pipenv run make -C docs <target>` | `source .venv/bin/activate && make -C docs <target>` |

エラー伝播ポリシー: 検出した PM のコマンドが PATH に無ければ例外送出 + インストール手順提示。デフォルト値による継続処理は禁止。

## 発火条件

- 「拡張機能を追加して」「conf.py を更新」「プロジェクト名を変えたい」「言語設定を変更」
- 他スキル (sphinx-init, sphinx-theme, rst-to-myst) からの委譲呼出

## 拡張カタログ (sphinx-init と共有、配布物の自己完結性のためインライン保持)

### MyST optional extensions

| カテゴリ | 拡張名 | 用途 | 追加パッケージ |
|---|---|---|---|
| 数式 | `amsmath` | LaTeX amsmath 環境 | — |
| 数式 | `dollarmath` | `$..$` / `$$..$$` 数式 | — |
| 属性 | `attrs_inline` | インライン属性 | — |
| 属性 | `attrs_block` | ブロック属性 | — |
| リスト | `deflist` | 定義リスト | — |
| リスト | `tasklist` | チェックボックスリスト | — |
| リスト | `fieldlist` | reST フィールドリスト | — |
| ブロック | `colon_fence` | `:::` ディレクティブ | — |
| ブロック | `html_admonition` | `<div class="admonition">` | — |
| ブロック | `html_image` | `<img>` タグ | — |
| テキスト | `replacements` | 記号自動変換 (©等) | — |
| テキスト | `smartquotes` | 引用符変換 | — |
| テキスト | `strikethrough` | `~~..~~` 取り消し線 | — |
| テキスト | `substitution` | Jinja2 置換 | — |
| リンク | `linkify` | bare URL 自動リンク化 | **`linkify-it-py`** |

### Sphinx 拡張パック

#### 必須

- `sphinx-autobuild` (3rd-party、Makefile livehtml 依存)

#### デフォルト推奨

| 拡張 | 種別 | 用途 |
|---|---|---|
| `sphinx-copybutton` | 3rd-party | コードブロックコピーボタン |
| `sphinx-design` | 3rd-party | カード / タブ / グリッド |
| `sphinx.ext.intersphinx` | built-in | クロスリファレンス |
| `sphinx.ext.napoleon` | built-in | Google/NumPy docstring |

#### オプショナル

| 拡張 | 種別 | 用途 | 連携外部スキル |
|---|---|---|---|
| `sphinx_oceanid` | 3rd-party | Mermaid 図 | `gh skill install drillan/sphinx-oceanid mermaid-diagram` |
| `sphinx.ext.autodoc` | built-in | docstring 自動抽出 | — |
| `sphinx.ext.viewcode` | built-in | ソースコードリンク | — |
| `sphinx.ext.todo` | built-in | TODO ディレクティブ | — |
| `myst-nb` | 3rd-party | Jupyter Notebook 統合 | — |

## 責務

### 1. 既存設定の保持

編集対象セクションのみ変更。コメント、`sys.path` 操作、その他のユーザー設定はそのまま保持する。

### 2. 3rd-party 拡張は自動依存追加

3rd-party 拡張を `extensions` に追加する際は、検出した PM で対応コマンドを実行 (上記 PM 検出セクション参照)。

### 3. MyST 拡張変更

`myst_enable_extensions` リストの追加/削除を行う。`linkify` 追加時は対応 PM で `linkify-it-py` を docs 依存に追加。

### 4. バックアップと明示的エラー伝播

編集失敗時の挙動を厳格に規定:

1. 編集前に必ず `conf.py.bak` を作成
2. **編集失敗時**: `conf.py.bak` から原本を復元したうえで、**元のエラーを必ずユーザーへ例外送出** (復元成功で「正常終了」扱いにしない)
3. **復元処理自体が失敗した場合**: `conf.py.bak` のパスと手動復元手順 (例: `cp conf.py.bak conf.py`) を提示して即時例外送出
4. **編集成功時のみ** `conf.py.bak` を削除

これにより「復元したから OK」というサイレントフェイル実装を仕様レベルで防止する。

## 関連スキル

- `sphinx-theme` (テーマ変更時に html_theme と html_theme_options の更新で連携)
- 委譲元: `sphinx-init` (init 時の conf.py 反映)、`rst-to-myst` (変換後 myst-parser 追加)
