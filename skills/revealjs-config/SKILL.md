---
name: revealjs-config
description: Configuration knowledge for sphinx-revealjs in conf.py. Covers revealjs_script_plugins (UMD bundles required, ES module plugin.js does not work), revealjs_css_files (a highlight CSS theme is mandatory for visible syntax highlighting), revealjs_script_conf (slide width/height/slideNumber), theme switching via revealjs_style_theme, SCSS setup with sphinx_revealjs.ext.sass, table centering (the bundled reveal.css left-aligns tables with a rule more specific than any theme's margin auto), and sphinx-oceanid (Mermaid) integration including SVG max-height constraints. Triggers when user wants to change slide width, plugins, highlighting, themes, fix left-aligned tables, or fix Mermaid overflow in a sphinx-revealjs project. Delegates conf.py editing to sphinx-config.
license: MIT
allowed-tools: Bash, Read, WebFetch
---

## 発火条件

- extensions に `sphinx_revealjs` があるプロジェクトで conf.py の revealjs 設定変更を求められた場合
- 「スライドの幅を変えたい」「プラグインを追加したい」「コードハイライトが効かない」「Mermaid がスライドからはみ出す」「スライドのテーマを変えたい」

## 前提検証

`docs/conf.py` の extensions に `sphinx_revealjs` が無い場合は明示的エラー伝播し、`revealjs-init` への誘導を案内する。

## 責務

本スキルは「何を設定すべきか」の知識のみを持つ。conf.py 編集の実行 (バックアップ・復元・明示的エラー伝播) は `sphinx-config` スキルへ委譲する。

## プラグイン設定 (`revealjs_script_plugins`)

- `src` パスに `_static/` プレフィックスは不要 (ビルダーが自動付加する)
- Reveal.js プラグインには2種類のファイルが存在する:
  - `plugin.js` — ES モジュール形式 (`import` 文を使用)。`<script>` タグでは動作しない
  - `highlight.js` 等 — UMD バンドル形式。`<script>` タグで読み込み可能
- `src` には必ず UMD バンドル版を指定する
- `name` は Reveal.js が認識するグローバル名を指定する

### 利用可能なプラグイン

```python
# シンタックスハイライト
{"src": "revealjs/plugin/highlight/highlight.js", "name": "RevealHighlight"}
# スピーカーノート
{"src": "revealjs/plugin/notes/notes.js", "name": "RevealNotes"}
# 数式
{"src": "revealjs/plugin/math/math.js", "name": "RevealMath"}
# スライド内検索
{"src": "revealjs/plugin/search/search.js", "name": "RevealSearch"}
# ズーム
{"src": "revealjs/plugin/zoom/zoom.js", "name": "RevealZoom"}
```

## ハイライト CSS テーマ (`revealjs_css_files`)

highlight.js は JS 側でコード構造を解析するのみで、色付けは CSS テーマが担当する。CSS テーマを読み込まないとハイライトは視覚的に反映されない。

```python
revealjs_css_files = [
    "revealjs/plugin/highlight/monokai.css",  # ダーク背景
]
```

同梱テーマ: `monokai.css` (ダーク背景)、`zenburn.css` (ダーク背景・低コントラスト)

## スライドテーマ (`revealjs_style_theme`)

組み込みテーマ名またはカスタム CSS ファイル名を指定する。

```python
revealjs_style_theme = "black"        # 組み込みテーマ
revealjs_style_theme = "custom.css"   # revealjs_static_path 配下のカスタム CSS
```

組み込みテーマ: black (デフォルト) / white / league / beige / night / serif / simple / solarized / moon / blood / sky

## 表示領域の最適化 (`revealjs_script_conf`)

Reveal.js のデフォルトスライド幅は 960px で、ワイドスクリーンでは左右に余白が生まれる。

```python
revealjs_script_conf = {
    "width": 1200,        # デフォルト: 960。ワイドスクリーンでは 1200 推奨
    "height": 700,        # デフォルト: 700
    "slideNumber": "c/t", # 現在/総数 形式のページ番号
    "hash": True,         # URL にスライド位置を反映 (リロード・共有に強い)
}
```

## テーブルの中央寄せ

同梱 reveal.js (5.x) の `dist/reveal.css` には次の規則があり、テーブルとコードブロックの margin を 0 にする:

```css
html:not(.print-pdf) .reveal pre,
html:not(.print-pdf) .reveal table { margin-left: 0; margin-right: 0 }
```

この詳細度は (0,2,2)。テーマ側 (組み込み・カスタムとも) の `.reveal table { margin: auto }` は (0,1,1) で、CSS では読み込み順より詳細度が優先されるため、テーマの選択に関係なく**対策しない限りテーブルは常に左寄せで表示される**。

`.reveal .slides section table` で上書きすると詳細度 (0,2,2) の同点になり、テーマ CSS・追加 CSS は reveal.css より後に読み込まれるため上書き側が勝つ。

SCSS カスタムテーマ使用時は `_sass/custom.scss` に追記する:

```scss
.reveal {
  .slides section table {
    margin-left: auto;
    margin-right: auto;
  }
}
```

組み込みテーマのみの場合は `_static/table-center.css` を作成し、`revealjs_css_files` で読み込む:

```css
/* Center tables within Reveal.js slides */
.reveal .slides section table {
  margin-left: auto;
  margin-right: auto;
}
```

```python
revealjs_css_files = [
    "revealjs/plugin/highlight/monokai.css",
    "table-center.css",
]
```

なお同じ reveal.css の規則で `pre` の margin も 0 になるが、こちらは「コードブロックの幅最大化」の推奨値 (`width: 100%`) と整合するため上書きしない。

## SCSS カスタムテーマ (`sphinx_revealjs.ext.sass`)

extensions に `sphinx_revealjs.ext.sass` を加えると SCSS からテーマをビルドできる。コンパイラは dart-sass バイナリで、初回ビルド時に GitHub Releases から自動ダウンロードされる (要ネットワークアクセス)。追加の Python 依存 (libsass 等) は不要。

```python
extensions = [
    "sphinx_revealjs",
    "sphinx_revealjs.ext.sass",
]
revealjs_sass_src_dir = "_sass"      # SCSS ソース
revealjs_sass_out_dir = "_static"    # コンパイル先
revealjs_sass_auto_targets = True    # _sass 配下を自動検出
revealjs_style_theme = "custom.css"  # _sass/custom.scss のコンパイル結果
revealjs_static_path = ["_static"]
```

### コードブロックの幅最大化 (SCSS)

Reveal.js ベーステーマの `pre` はデフォルトで `width: 90%`、`margin: auto`。コンテンツ領域を最大化するには以下を上書きする:

```scss
.reveal {
  .slides section {
    padding: 10px;  // デフォルトは 20px 程度
  }

  pre {
    width: 100%;
    margin-left: 0;
    margin-right: 0;
    box-sizing: border-box;
  }
}
```

## Mermaid ダイアグラム連携 (sphinx-oceanid)

### クライアントサイド遅延レンダリング

sphinx-oceanid は beautiful-mermaid (ELK.js ベースレイアウト) によるクライアントサイドレンダリングを使用する。Reveal.js の非表示スライド問題は IntersectionObserver と `slidechanged` イベントによる遅延レンダリングで自動的に解決される。

conf.py に `"sphinx_oceanid"` を追加するだけで動作し、追加設定は不要。

```python
extensions = [
    "sphinx_oceanid",
    "sphinx_revealjs",
]
```

### 不要な設定 (サーバーサイドレンダリング関連)

sphinx-oceanid では以下の設定・ファイルは不要:

- `mermaid_output_format`, `mermaid_cmd`, `mermaid_params` 等の `mermaid_*` 設定
- `puppeteer-config.json` (Puppeteer は使用しない)
- `mermaid-config.json` (beautiful-mermaid がテーマを内包)
- CI での日本語フォントインストール (クライアントサイドレンダリングのため閲覧者のブラウザ環境に依存)

### SVG の高さ制約

sphinx-oceanid の SVG はデフォルトで `height: auto` のため、縦方向に長いダイアグラム (`flowchart TD` 等) がスライドからはみ出す。`_static/oceanid-revealjs.css` で `max-height` を設定し、`revealjs_css_files` で読み込む。

```css
/* _static/oceanid-revealjs.css */
.reveal .slides .oceanid-diagram .oceanid-svg-container svg {
  max-height: 500px;
}
```

```python
revealjs_css_files = [
    "revealjs/plugin/highlight/monokai.css",
    "oceanid-revealjs.css",
]
```

## 設定例

```python
# conf.py — sphinx-revealjs + sphinx-oceanid 構成例
extensions = [
    "myst_parser",
    "sphinx_revealjs",
    "sphinx_oceanid",
]

revealjs_style_theme = "black"
revealjs_static_path = ["_static"]
revealjs_script_conf = {
    "width": 1200,
    "height": 700,
    "slideNumber": "c/t",
    "hash": True,
}
revealjs_css_files = [
    "revealjs/plugin/highlight/monokai.css",
    "oceanid-revealjs.css",
]
revealjs_script_plugins = [
    {
        "src": "revealjs/plugin/highlight/highlight.js",
        "name": "RevealHighlight",
    },
]
```

## 情報の鮮度維持

設定項目の網羅リストは WebFetch で公式ドキュメント <https://sphinx-revealjs.readthedocs.io/en/stable/configurations/> から取得し、本スキル記載の知識 (落とし穴・推奨値) と組み合わせて提案する。

## 関連スキル

- **委譲先**: `sphinx-config` (conf.py 編集の実行)
- **前提**: `revealjs-init` (プロジェクト未初期化なら誘導)
- **連携**: `revealjs-authoring` (Mermaid の記法側ルール)
