---
name: rst-to-myst
description: Migrate an existing reStructuredText (.rst) Sphinx documentation project to MyST Markdown (.md) using the rst-to-myst tool. Designed for projects with substantial RST content (multiple files, custom directives, real documentation), NOT for sphinx-quickstart boilerplate. Validates conversion output before deleting originals. Triggers when user asks to migrate RST documentation to MyST, or when the project has multiple .rst files with content beyond the sphinx-quickstart skeleton.
license: MIT
allowed-tools: Bash, Read, Write
---

## パッケージマネージャ検出と一時ツール実行 (ad-hoc)

検出優先順位 (該当した時点で確定):

| 優先 | 判定条件 | 採用 |
|---|---|---|
| 1 | `uv.lock` が存在 | uv |
| 2 | `poetry.lock` が存在 | poetry |
| 3 | `Pipfile.lock` が存在 | pipenv |
| 4 | `.venv/` のみ存在 | plain venv |
| 5 | 上記すべて該当しない | ユーザー問い合わせ (推奨: uv) |

`rst-to-myst` パッケージは依存に含めず単発実行する (ad-hoc)。PM ごとの実行コマンド:

| PM | ad-hoc 実行 |
|---|---|
| uv | `uvx --from "rst-to-myst[sphinx]" rst2myst convert <files>` |
| poetry | `pipx run --spec "rst-to-myst[sphinx]" rst2myst convert <files>` (要 pipx) |
| pipenv | `pipx run --spec "rst-to-myst[sphinx]" rst2myst convert <files>` (要 pipx) |
| plain venv | `pipx run --spec "rst-to-myst[sphinx]" rst2myst convert <files>` または `pip install` で venv に追加 |

`pipx` 不在時はパッケージを一時的に依存追加 → 実行 → 削除する手順を提示する。

## 用途と非用途

### 対象
数ファイル以上の実コンテンツを持つ既存 RST プロジェクトの移行。

### 非対象
`sphinx-quickstart -q` が生成した最小 `index.rst` 単体 — `sphinx-init` が直接 MyST テンプレートで生成するため、本スキルは呼ばれない。

## 発火条件

- 「既存の RST プロジェクトを MyST に変換」「Markdown に移行」「.rst を .md に変える」
- `docs/` 配下に複数の `.rst` ファイルが存在し (sphinx-quickstart 生成 `index.rst` のみではない)、移行希望が示された場合
- `sphinx-init` MyST 選択時に `index.rst` 以外の `.rst` を検出した場合 (sphinx-init からの委譲呼出)

## 実行フロー (3段階の段階的検証で原本保護)

### 1. 対象ファイル特定

- 単一ファイル or `docs/` 配下全体
- 原本 `.rst` のサイズを記録 (検証で参照)

### 2. ad-hoc 変換実行

冒頭の「パッケージマネージャ検出と一時ツール実行」表に従い、検出した PM に対応するコマンドを実行する。

```bash
# uv の例
uvx --from "rst-to-myst[sphinx]" rst2myst convert <files>
```

### 3. 変換結果の妥当性検証

以下の**すべて**を満たす場合のみ「変換成功」とみなす:

- (a) 対応する `.md` ファイルが生成されている (存在確認)
- (b) `.md` ファイルが空でない、かつサイズが原本 `.rst` の **30% 以上**
- (c) 変換エラー行 (`<SYSTEM MESSAGE: ...>` 等の rst-to-myst 既知エラーマーカ) を含まない

いずれか不成立の場合:
- 原本 `.rst` を残す
- 生成された不完全な `.md` を削除
- 検証失敗の理由を含む例外を送出 (デフォルト値での継続禁止)

### 4. 原本削除

上記 3 が「変換成功」の場合のみ `.rst` を削除する。

### 5. conf.py 更新案内

`sphinx-config` スキルへ委譲し `myst-parser` を `extensions` に追加する。

### 6. 執筆移行案内

`myst-authoring` スキルが今後 `.md` 編集時に自動発火する旨を伝える。

## 関連スキル

- 委譲先: `sphinx-config` (myst-parser 追加)
- 後続: `myst-authoring` (変換後の MyST 執筆)
- 委譲元: `sphinx-init` (index.rst 以外の .rst 検出時)
