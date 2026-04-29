---
name: sphinx-build
description: Build Sphinx documentation via Makefile targets. Supports HTML, clean rebuild, Japanese PDF (latexpdfja), EPUB, link checking, and live-reload development server (livehtml). Detects the project's package manager (uv/poetry/pipenv/plain venv) and uses the appropriate run command. Interprets common build errors and suggests fixes. Triggers when user asks to build documentation, generate HTML/PDF/EPUB, run dev server with live reload, or check links.
license: MIT
allowed-tools: Bash, Read
---

## パッケージマネージャ検出

検出優先順位 (該当した時点で確定):

| 優先 | 判定条件 | 採用 |
|---|---|---|
| 1 | `uv.lock` が存在 | uv |
| 2 | `poetry.lock` が存在 | poetry |
| 3 | `Pipfile.lock` が存在 | pipenv |
| 4 | `.venv/` のみ存在 | plain venv |
| 5 | 上記すべて該当しない | ユーザー問い合わせ (推奨: uv) |

ビルド (make) 実行コマンド:
- uv: `uv run make -C docs <target>`
- poetry: `poetry run make -C docs <target>`
- pipenv: `pipenv run make -C docs <target>`
- plain venv: `source .venv/bin/activate && make -C docs <target>`

検出した PM のコマンドが PATH に無ければ例外送出 (フォールバック禁止)。

## 発火条件

- 「ビルドして」「ドキュメント生成」「HTML 化」「PDF にして」「日本語 PDF」「ライブリロード」「開発サーバ起動」「リンクチェック」

## 前提検証

1. `docs/Makefile` 存在 — 不在なら明示的エラー伝播 + `sphinx-init` 誘導 (Makefile 自動生成等の暗黙処理は行わない)
2. 実行 CWD はプロジェクトルート (`pyproject.toml` のあるディレクトリ) 前提。サブディレクトリから呼ばれた場合はプロジェクトルートへ移動してから実行
3. PM 検出 (上記「パッケージマネージャ検出」セクション参照)

## 責務 — make ターゲットへのマッピング

| ユーザー意図 | 実行コマンド (uv 例、PM ごとに動的書き換え) |
|---|---|
| HTML ビルド | `uv run make -C docs html` |
| クリーンビルド | `uv run make -C docs clean html` |
| PDF (英文) | `uv run make -C docs latexpdf` |
| **PDF (日本語)** | `uv run make -C docs latexpdfja` |
| EPUB | `uv run make -C docs epub` |
| ライブリロード | `uv run make -C docs livehtml` |
| ポート指定ライブリロード | `PORT=8003 uv run make -C docs livehtml` |
| リンクチェック | `uv run make -C docs linkcheck` |
| ヘルプ | `uv run make -C docs help` |

PM ごとの実コマンド書き換えは冒頭の「パッケージマネージャ検出」セクションを参照。

## エラー解釈パターン

ビルド失敗時、出力を解析して以下のパターンに該当する場合は修正候補を提示:

- `WARNING: undefined label` → 参照先ラベルの定義箇所を提示、修正候補
- `WARNING: document isn't included in any toctree` → toctree 追加提案
- `Could not import extension` → `uv add <pkg> --group docs` 提案
- LaTeX 系エラー (`latexpdfja` 失敗) → upLaTeX / dvipdfmx インストール手順 (TeX Live 等)
- ポート競合 (livehtml) → `PORT=8003` 等の代替ポート提案

## 関連スキル

- 前提: `sphinx-init` (Makefile が無ければ誘導)
- 連携: `sphinx-config` (拡張不在エラー時の依存追加)
