---
name: sphinx-init
description: Initialize a new Sphinx documentation project. Detects the project's package manager (uv recommended; supports poetry, pipenv, plain venv) and uses it for dependency installation. Supports RST or MyST (Markdown) syntax selection. Triggers when user asks to start, create, or initialize Sphinx documentation in a Python project. Sets up MyST optional extensions, popular Sphinx extensions, and a customized Makefile with livehtml and latexpdfja targets.
license: MIT
allowed-tools: Bash, Read, Write, Edit, WebFetch
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

- ユーザーが「Sphinx ドキュメントを始めたい」「初期化して」「ドキュメント環境作って」と発話
- `docs/` が存在しないリポジトリで Sphinx 関連の質問を受けた場合

## 実行フロー

### 1. 前提検証 (失敗時は明示的エラー伝播)

- パッケージマネージャ検出 (上記「パッケージマネージャ検出」セクション参照)
- `pyproject.toml` 存在確認 — 不在なら PM ごとの初期化案内
  - uv: `uv init` / poetry: `poetry init` / pipenv: `pipenv install` / venv: `python -m venv .venv`

### 2. 記法選択

ユーザーに以下を提示:

> 記法を選択してください:
> - **MyST** (Markdown ベース、推奨) — `.md` で執筆
> - **RST** (reStructuredText) — `.rst` で執筆

デフォルトは MyST。

### 3. プロジェクト情報取得

- `PROJECT_NAME`: `pyproject.toml` の `project.name` → 不在時 `basename $PWD`
- `AUTHOR_NAME`: `pyproject.toml` の `authors[0].name` → `git config --get user.name` → `$USER`

### 4. Sphinx 基本パッケージ追加

検出された PM のコマンドで `sphinx` を docs グループに追加:

```bash
uv add sphinx --group docs
# poetry: poetry add --group docs sphinx
# pipenv: pipenv install --dev sphinx
# plain venv: pyproject.toml の [project.optional-dependencies] に追加 → pip install -e ".[docs]"
```

### 5. Sphinx プロジェクト作成

```bash
uv run sphinx-quickstart -q -p "$PROJECT_NAME" -a "$AUTHOR_NAME" ./docs
```

### 6. MyST 選択時の処理

- `uv add myst-parser --group docs` で myst-parser を追加
- **`docs/index.rst` を削除し、最小 MyST テンプレートを `docs/index.md` として書き出す** (生成失敗時は明示的エラー伝播):

````markdown
# Welcome to {{ PROJECT_NAME }}'s documentation!

```{toctree}
:maxdepth: 2
:caption: Contents:
```

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
````

- 既存 `.rst` (index.rst 以外) を検出した場合:
  ユーザーに「他の RST ファイルも MyST に変換しますか?」と問い合わせ、希望時は `rst-to-myst` スキルへ委譲。

- **MyST optional extensions 選択** (15個、カテゴリ別提示):

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

  推奨セット (チェック済みで提示、オプトアウト可): `amsmath`, `dollarmath`, `attrs_inline`, `colon_fence`, `deflist`, `html_admonition`, `html_image`, `replacements`, `smartquotes`, `strikethrough`, `substitution`, `tasklist`, `fieldlist`, `linkify`。

  `linkify` 選択時は `uv add linkify-it-py --group docs` (PM ごとに動的書き換え) を自動実行。最新拡張一覧は WebFetch で `https://myst-parser.readthedocs.io/en/latest/syntax/optional.html` から取得し新規追加分を取り込む。

### 7. Sphinx 拡張パック選択

#### 必須インストール (Makefile livehtml ターゲット依存)

- `sphinx-autobuild` (3rd-party) — `extensions` への追加は不要、dev 依存として `uv add sphinx-autobuild --group docs`

#### デフォルト推奨 (チェック済みで提示、オプトアウト可)

| 拡張 | 種別 | 用途 |
|---|---|---|
| `sphinx-copybutton` | 3rd-party | コードブロックコピーボタン |
| `sphinx-design` | 3rd-party | カード / タブ / グリッド / ドロップダウン |
| `sphinx.ext.intersphinx` | built-in | クロスリファレンス |
| `sphinx.ext.napoleon` | built-in | Google/NumPy docstring |

#### オプショナル (未チェックで提示、選択時にチェック)

| 拡張 | 種別 | 用途 | 連携外部スキル |
|---|---|---|---|
| `sphinx_oceanid` | 3rd-party | Mermaid 図 | `gh skill install drillan/sphinx-oceanid mermaid-diagram --scope project` |
| `sphinx.ext.autodoc` | built-in | docstring 自動抽出 | — |
| `sphinx.ext.viewcode` | built-in | ソースコードリンク | — |
| `sphinx.ext.todo` | built-in | TODO ディレクティブ | — |
| `myst-nb` | 3rd-party | Jupyter Notebook 統合 | — |

選択された 3rd-party 拡張は検出した PM のコマンドで自動依存追加 (例 uv: `uv add <pkg> --group docs`)。`sphinx_oceanid` 選択時は対応する外部スキルのインストール案内を表示。

### 8. conf.py 反映 — sphinx-config スキルへ委譲

`sphinx-config` スキルへ以下を渡して委譲:
- 選択された extensions
- 選択された myst_enable_extensions
- 検出された language (`$LANG` が `ja_JP*` または既存 language が空 → `language = "ja"` を提案)

これにより conf.py 編集の単一ロジック (バックアップ・復元・明示的エラー伝播) は `sphinx-config` のみが保持。

### 9. Makefile カスタマイズ

`sphinx-quickstart` 生成 Makefile を以下で**置換**:

```makefile
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
PORT          ?= 8000

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "  latexpdfja  to make LaTeX files and run them through upLaTeX/dvipdfmx"
	@echo "  livehtml    to start sphinx-autobuild dev server (PORT=$(PORT))"

.PHONY: help Makefile latexpdfja livehtml

latexpdfja:
	@$(SPHINXBUILD) -M latexpdfja "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" \
		--host 0.0.0.0 --port $(PORT) $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

`SPHINXBUILD` は `sphinx-build` のまま (PM 非依存)。`PORT=8003` 等で上書き可。

### 10. テストビルド

```bash
uv run make -C docs html
```

失敗時は明示的エラー伝播し処理停止 (生成済みファイルは手動修正を要求)。以後のビルドは `sphinx-build` スキルへ委譲する旨を案内。

## 関連スキル

- **委譲先**: `sphinx-config` (conf.py 編集の単一ロジック)、`rst-to-myst` (既存 .rst が複数ある場合の移行)
- **完了後**: `sphinx-build` (動作確認)、`sphinx-theme` (テーマ変更時)、`myst-authoring` (MyST 選択時の執筆時自動発火)
- **外部スキル**: `sphinx_oceanid` 選択時は `drillan/sphinx-oceanid` の `mermaid-diagram` を別途インストール
