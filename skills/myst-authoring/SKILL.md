---
name: myst-authoring
description: Provide MyST Markdown authoring assistance for Sphinx documentation. Covers directives ({note}, {warning}, {code-block}), roles ({ref}, {doc}, {cite}), cross-references, math notation, and sphinx-design directives ({card}, {grid}, {tab-set}). MUST trigger when editing or creating .md files under docs/ in a project where docs/conf.py contains 'myst_parser' in extensions. Also triggers when user asks about MyST syntax, directives, or roles in Sphinx context.
license: MIT
allowed-tools: Read, Edit, WebFetch
---

## 発火条件 (MUST trigger)

- `docs/` 配下の `.md` ファイルを編集または作成する **AND**
- `docs/conf.py` の `extensions` に `myst_parser` が含まれる場合

または以下:

- ユーザーが MyST ディレクティブ・ロール・記法について質問した場合
- MyST + Sphinx プロジェクトでの執筆支援を要求された場合

## 提供知識

### 1. ディレクティブ (MyST core)

````markdown
```{note}
これは note ディレクティブです。
```

```{warning}
警告メッセージ。
```

```{tip}
ヒント。
```

```{code-block} python
def hello():
    return "world"
```

```{toctree}
:maxdepth: 2
:caption: Contents

intro
guide/index
```

```{include} fragment.md
```

```{figure} image.png
:alt: 画像の説明
:width: 400px

キャプション。
```

```{table} 表のキャプション
:widths: auto

| A | B |
|---|---|
| 1 | 2 |
```

```{math}
e^{i\pi} + 1 = 0
```
````

`colon_fence` 拡張が有効な場合は `:::{note}` 形式でも同等に動作する。

### 2. ロール (MyST core)

```markdown
内部参照: {ref}`my-label`
ドキュメント参照: {doc}`./other-page`
引用: {cite}`bibkey`
ダウンロード: {download}`./file.zip`
キーボード: {kbd}`Ctrl+C`
ファイル名: {file}`/path/to/file`
```

### 3. クロスリファレンス

```markdown
(my-label)=
## セクション

参照する側: [](my-label) または {ref}`my-label`
タイトル付き参照: {ref}`セクションへ <my-label>`
```

### 4. 数式 (dollarmath / amsmath 拡張)

````markdown
インライン: $E = mc^2$
ディスプレイ: $$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$

LaTeX 環境 (amsmath 拡張):
```{math}
\begin{align}
a &= b \\
c &= d
\end{align}
```
````

### 5. sphinx-design ディレクティブ (sphinx-design 有効時)

````markdown
```{card} カードタイトル
カード本文。
```

```{grid} 1 2 2 3
:::{grid-item-card} カード 1
:::
:::{grid-item-card} カード 2
:::
```

```{tab-set}
:::{tab-item} タブ 1
内容 1
:::
:::{tab-item} タブ 2
内容 2
:::
```

```{dropdown} クリックで開く
隠された内容。
```
````

### 6. 記法ミス検出

- コロン数の不一致 (3-backtick 形式と `:::` 形式の混在)
- 引用符の不一致 (3-backtick の閉じ忘れ)
- ロールのバッククォート不足 (`{ref}foo` ではなく `` {ref}`foo` ``)
- toctree 内のファイル名拡張子付け間違い (`.md` 不要)

## 最新仕様の参照

公式ドキュメントから最新の記法を WebFetch で取得可能:

- MyST core: https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html
- sphinx-design: https://sphinx-design.readthedocs.io/en/latest/

## 関連スキル

- **外部スキル**: 図作成 (Mermaid 等) は `drillan/sphinx-oceanid` の `mermaid-diagram` スキルへ委譲
- 連携: `sphinx-build` (執筆後のビルド確認)、`sphinx-config` (新拡張追加時)
