# myst-authoring

MyST Markdown による Sphinx ドキュメント執筆を支援するスキルです。ディレクティブ (`{note}`, `{warning}`, `{code-block}`)、ロール (`{ref}`, `{doc}`, `{cite}`)、クロスリファレンス、数式、`sphinx-design` ディレクティブ (`{card}`, `{grid}`, `{tab-set}`) をカバーします。

## 発火条件 (MUST trigger)

- `docs/` 配下の `.md` ファイルを編集または作成する **AND**
- `docs/conf.py` の `extensions` に `myst_parser` が含まれる場合

または以下:

- ユーザーが MyST ディレクティブ・ロール・記法について質問した場合
- MyST + Sphinx プロジェクトでの執筆支援を要求された場合

## 提供知識 (要点)

### ディレクティブ (MyST core)

```{note}
これは note ディレクティブです。
```

```{warning}
警告メッセージ。
```

```{tip}
ヒント。
```

### ロール (MyST core)

| ロール | 用途 | 記法例 |
| --- | --- | --- |
| `{ref}` | 内部参照 | `` {ref}`my-label` `` |
| `{doc}` | ドキュメント参照 | `` {doc}`./other-page` `` |
| `{cite}` | 引用 | `` {cite}`bibkey` `` |
| `{download}` | ダウンロード | `` {download}`./file.zip` `` |
| `{kbd}` | キーボード | `` {kbd}`Ctrl+C` `` |

### 数式 (`dollarmath` / `amsmath`)

インライン: $E = mc^2$

ディスプレイ:

$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

### sphinx-design ディレクティブ

```{card} カードタイトル
カード本文。
```

```{dropdown} クリックで開く
隠された内容。
```

`colon_fence` 拡張が有効な場合は `:::{note}` 形式でも同等に動作します。

### 記法ミス検出パターン

- コロン数の不一致 (3-backtick 形式と `:::` 形式の混在)
- 引用符の不一致 (3-backtick の閉じ忘れ)
- ロールのバッククォート不足 (`{ref}foo` ではなく `` {ref}`foo` ``)
- toctree 内のファイル名拡張子付け間違い (`.md` 不要)

## 最新仕様の参照

公式ドキュメントから最新の記法を WebFetch で取得できます。

- MyST core: <https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html>
- sphinx-design: <https://sphinx-design.readthedocs.io/en/latest/>

## 関連スキル

- **外部スキル**: 図作成 (Mermaid 等) は `drillan/sphinx-oceanid` の `mermaid-diagram` スキルへ委譲
- 連携: `sphinx-build` (執筆後のビルド確認)、`sphinx-config` (新拡張追加時)
