# rst-to-myst

既存の reStructuredText (`.rst`) Sphinx プロジェクトを MyST Markdown (`.md`) に移行するスキルです。`rst-to-myst` ツールを ad-hoc 実行 (依存に追加せず単発実行) し、変換結果を 3 段階で検証してから原本を削除します。実コンテンツを持つ既存プロジェクトが対象であり、`sphinx-quickstart` 生成の最小 `index.rst` は対象外です。

## 発火条件

- 「既存の RST プロジェクトを MyST に変換」「Markdown に移行」「.rst を .md に変える」
- `docs/` 配下に複数の `.rst` ファイルが存在し、移行希望が示された場合
- `sphinx-init` MyST 選択時に `index.rst` 以外の `.rst` を検出した場合 (委譲呼出)

## ad-hoc 実行コマンド (PM 別)

`rst-to-myst` パッケージは依存に含めず単発実行します。

| PM | コマンド |
| --- | --- |
| uv | `uvx --from "rst-to-myst[sphinx]" rst2myst convert <files>` |
| poetry / pipenv / plain venv | `pipx run --spec "rst-to-myst[sphinx]" rst2myst convert <files>` |

`pipx` 不在時はパッケージを一時的に依存追加 → 実行 → 削除する手順を提示します。

## 実行フロー (3段階の段階的検証で原本保護)

### 1. 対象ファイル特定

単一ファイル または `docs/` 配下全体を対象とします。原本 `.rst` のサイズを記録します (検証で参照)。

### 2. ad-hoc 変換実行

検出した PM に対応するコマンドを実行します。

### 3. 変換結果の妥当性検証

以下のすべてを満たす場合のみ「変換成功」とみなします。

- (a) 対応する `.md` ファイルが生成されている (存在確認)
- (b) `.md` ファイルが空でない、かつサイズが原本 `.rst` の 30% 以上
- (c) 変換エラー行 (`<SYSTEM MESSAGE: ...>` 等の rst-to-myst 既知エラーマーカ) を含まない

いずれか不成立の場合は原本 `.rst` を残し、生成された不完全な `.md` を削除し、検証失敗の理由を含む例外を送出します (デフォルト値での継続禁止)。

### 4. 原本削除

上記 3 が「変換成功」の場合のみ `.rst` を削除します。

### 5. conf.py 更新案内

`sphinx-config` スキルへ委譲し `myst-parser` を `extensions` に追加します。

### 6. 執筆移行案内

`myst-authoring` スキルが今後 `.md` 編集時に自動発火する旨を伝えます。

## 用途と非用途

- 対象: 数ファイル以上の実コンテンツを持つ既存 RST プロジェクトの移行
- 非対象: `sphinx-quickstart -q` が生成した最小 `index.rst` 単体 — `sphinx-init` が直接 MyST テンプレートで生成するため本スキルは呼ばれない

## 関連スキル

- 委譲先: `sphinx-config` (myst-parser 追加)
- 後続: `myst-authoring` (変換後の MyST 執筆)
- 委譲元: `sphinx-init` (`index.rst` 以外の `.rst` 検出時)
