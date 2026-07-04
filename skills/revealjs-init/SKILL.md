---
name: revealjs-init
description: Initialize a dedicated presentation slide project using sphinx-revealjs. Detects the package manager (uv/poetry/pipenv/plain venv), adds dependencies, scaffolds docs/ with a MyST slide template, offers built-in Reveal.js theme selection plus optional sphinx-oceanid (Mermaid) and SCSS custom theme, and installs a Makefile with revealjs/livehtml/serve targets. Triggers when user asks to create presentation slides or start a slide project with Sphinx. Requires a project without an existing docs/ directory.
license: MIT
allowed-tools: Bash, Read, Write, Edit, WebFetch
---

## 前提 — スライド専用プロジェクト

本スキルは「1発表 = 1リポジトリ、`docs/` = スライド」の専用構成を対象とする。既存 Sphinx ドキュメントとの共存 (`slides/` 等の別ディレクトリ追加) は範囲外。

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

- 「スライドを作りたい」「sphinx-revealjs でプレゼン資料を作って」「発表資料のプロジェクトを始めたい」
- `docs/` が存在しないリポジトリで sphinx-revealjs 関連の質問を受けた場合

## 実行フロー

### 1. 前提検証 (失敗時は明示的エラー伝播)

- PM 検出 (上記「パッケージマネージャ検出」セクション参照)
- `pyproject.toml` 存在確認 — 不在なら PM ごとの初期化案内 (uv: `uv init` / poetry: `poetry init` / pipenv: `pipenv install` / venv: `python -m venv .venv`)
- **`docs/` が既に存在する場合は停止**し、「本スキルはスライド専用プロジェクトを対象とする。既存ドキュメントとの共存は範囲外」と報告する。docs/ の削除・上書き等の暗黙処理は行わない

### 2. 依存追加

検出された PM のコマンドで docs グループに追加 (uv 例、PM ごとに動的書き換え):

```bash
uv add sphinx sphinx-revealjs myst-parser sphinx-autobuild --group docs
```

### 3. プロジェクト情報取得

- `PROJECT_NAME`: `pyproject.toml` の `project.name` → 不在時 `basename $PWD`
- `AUTHOR_NAME`: `pyproject.toml` の `authors[0].name` → `git config --get user.name` → `$USER`

### 4. Sphinx プロジェクト作成

```bash
uv run sphinx-quickstart -q -p "$PROJECT_NAME" -a "$AUTHOR_NAME" ./docs
```

生成された `docs/index.rst` は削除する (手順7でスライド雛形 `index.md` に置き換え)。

### 5. テーマ選択

組み込みテーマを選択式で提示 (デフォルト: black):

| テーマ | 特徴 |
|---|---|
| black (デフォルト) | 黒背景・白文字 |
| white | 白背景・黒文字 |
| league | グレー背景 |
| beige | ベージュ背景 |
| night | 黒背景・太字見出し |
| serif | セリフ体 |
| simple | 白背景・ミニマル |
| solarized | Solarized Light 配色 |
| moon | 濃紺背景 |
| blood | 黒背景・赤アクセント |
| sky | 水色グラデーション |

選択値は手順8で `revealjs_style_theme` に反映する。

### 6. オプション選択 (未チェックで提示)

| オプション | 用途 | 選択時の処理 |
|---|---|---|
| `sphinx-oceanid` | Mermaid 図 | `uv add sphinx-oceanid --group docs` + extensions へ `sphinx_oceanid` + `_static/oceanid-revealjs.css` 生成 + `revealjs_css_files` へ追加 + `mermaid-diagram` 外部スキルの案内 |
| SCSS カスタムテーマ | テーマ自作 | extensions へ `sphinx_revealjs.ext.sass` + `_sass/custom.scss` 雛形生成 + sass 関連設定 (下記)。コンパイラ (dart-sass) は初回ビルド時に自動ダウンロードされるため要ネットワーク、追加の Python 依存は不要 |

オプション提示時に、SCSS 非選択の場合はテーブル中央寄せ対処の `_static/table-center.css` を自動生成する旨も合わせて伝える (選択式ではなく既定の対処。SCSS 選択時は `custom.scss` 内の規則が同じ役割を担う)。

以下の生成ファイルに埋め込む値 (`max-height`、`padding`、`pre` 幅、テーブル中央寄せ) は `revealjs-config` の推奨値の複製。変更する際は両スキルを同時に更新する。

sphinx-oceanid 選択時に生成する `docs/_static/oceanid-revealjs.css` (縦長ダイアグラムのはみ出し対策):

```css
/* Constrain sphinx-oceanid diagrams within Reveal.js slides */
.reveal .slides .oceanid-diagram .oceanid-svg-container svg {
  max-height: 500px;
}
```

SCSS 非選択時に生成する `docs/_static/table-center.css` (同梱 reveal.css がテーマより詳細度の高い規則でテーブルを左寄せにするため。根拠は `revealjs-config` の「テーブルの中央寄せ」参照):

```css
/* Center tables within Reveal.js slides */
.reveal .slides section table {
  margin-left: auto;
  margin-right: auto;
}
```

SCSS 選択時に生成する `docs/_sass/custom.scss`:

```scss
// Reveal.js カスタムテーマ雛形
@import "template/mixins";
@import "template/settings";

// テーマ変数の上書きはここに書く
// (変数一覧は Reveal.js の css/theme/template/settings.scss を参照)
// $mainFontSize: 36px;
// $backgroundColor: #fdf6e3;

@import "template/theme";

// コンテンツ領域の最大化
.reveal {
  .slides section {
    padding: 10px;
  }

  pre {
    width: 100%;
    margin-left: 0;
    margin-right: 0;
    box-sizing: border-box;
  }

  // 同梱 reveal.css がテーマより詳細度の高い規則でテーブルを左寄せにするため中央に戻す
  .slides section table {
    margin-left: auto;
    margin-right: auto;
  }
}
```

SCSS 選択時の追加設定 (手順8に合流):

```python
revealjs_sass_src_dir = "_sass"
revealjs_sass_out_dir = "_static"
revealjs_sass_auto_targets = True
revealjs_style_theme = "custom.css"  # 手順5の選択より優先
```

### 7. スライド雛形 index.md 生成

発表タイトル・イベント名・発表日をユーザーに確認し、`docs/index.md` を生成する (`{{ }}` は確認した値で置換):

```markdown
# {{ 発表タイトル }}

- {{ イベント名 }}
- {{ 発表日 }}
- {{ AUTHOR_NAME }}

## はじめに

### 自己紹介

- 名前
- 所属

## 本編

### スライドの書き方

- `##` がセクション区切り、`###` が個別スライドになる
- 1スライド1トピックで書く
- 詳細な記法ルールは `revealjs-authoring` スキルが提供する
```

### 8. conf.py 反映 — sphinx-config スキルへ委譲

以下を渡して委譲する (設定値の根拠・落とし穴は `revealjs-config` スキル参照):

```python
extensions = [
    "myst_parser",
    "sphinx_revealjs",
    # sphinx-oceanid 選択時: "sphinx_oceanid"
    # SCSS 選択時: "sphinx_revealjs.ext.sass"
]
myst_enable_extensions = ["colon_fence", "deflist", "tasklist"]
revealjs_style_theme = "black"  # 手順5の選択値
revealjs_static_path = ["_static"]
revealjs_script_conf = {
    "width": 1200,
    "height": 700,
    "slideNumber": "c/t",
    "hash": True,
}
revealjs_css_files = [
    "revealjs/plugin/highlight/monokai.css",
    # sphinx-oceanid 選択時: "oceanid-revealjs.css"
    # SCSS 非選択時: "table-center.css"
]
revealjs_script_plugins = [
    {
        "src": "revealjs/plugin/highlight/highlight.js",
        "name": "RevealHighlight",
    },
]
```

### 9. Makefile 置換

`sphinx-quickstart` 生成の Makefile を以下で置換する:

```makefile
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
PORT          ?= 8000

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "  serve       to serve built slides at http://localhost:$(PORT)"
	@echo "  livehtml    to start sphinx-autobuild dev server for slides (PORT=$(PORT))"

.PHONY: help Makefile revealjs serve livehtml

revealjs: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

serve: revealjs
	@echo "Serving at http://localhost:$(PORT) - press Ctrl+C to stop"
	python -m http.server -d "$(BUILDDIR)/revealjs" $(PORT)

livehtml:
	sphinx-autobuild -b revealjs "$(SOURCEDIR)" "$(BUILDDIR)/revealjs" \
		--host 0.0.0.0 --port $(PORT) $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

`SPHINXBUILD` は `sphinx-build` のまま (PM 非依存)。`PORT=8003` 等で上書き可。

### 10. テストビルド

```bash
uv run make -C docs revealjs
```

失敗時は明示的エラー伝播で停止 (生成済みファイルの自動削除・自動修正はしない)。成功時は `docs/_build/revealjs/index.html` を案内し、以後のビルド・プレビューは `sphinx-build` スキルへ委譲する旨を伝える。

## 関連スキル

- **委譲先**: `sphinx-config` (conf.py 編集の単一ロジック)
- **知識参照**: `revealjs-config` (sphinx-revealjs 固有設定の根拠と落とし穴)
- **完了後**: `sphinx-build` (revealjs ビルド・プレビュー)、`revealjs-authoring` (スライド執筆時に自動発火)
- **外部スキル**: sphinx-oceanid 選択時は `drillan/sphinx-oceanid` の `mermaid-diagram` を別途インストール
