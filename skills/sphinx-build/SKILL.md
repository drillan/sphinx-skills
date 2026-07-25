---
name: sphinx-build
description: Sphinx ドキュメント・スライドを Makefile 経由でビルドするスキル(HTML・latexpdfja・EPUB・linkcheck・livehtml・revealjs)。ドキュメントやスライドのビルド・プレビュー・開発サーバー起動・リンクチェックを求められたときに使用する。パッケージマネージャ検出とビルドエラーの解釈は本文参照。
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
| 4 | `.venv/` のみ存在 (lockfile なし) | plain venv |
| 5 | 上記すべて該当しない | ユーザー問い合わせ (推奨: uv) |

ビルド (make) 実行コマンド:
- uv: `uv run make -C docs <target>`
- poetry: `poetry run make -C docs <target>`
- pipenv: `pipenv run make -C docs <target>`
- plain venv: `source .venv/bin/activate && make -C docs <target>`

検出した PM のコマンドが PATH に無ければ例外送出 (フォールバック禁止)。

## 発火条件

- 「ビルドして」「ドキュメント生成」「HTML 化」「PDF にして」「日本語 PDF」「ライブリロード」「開発サーバ起動」「リンクチェック」
- 「スライドをビルド」「スライドをプレビュー」

## 前提検証

1. `docs/Makefile` 存在 — 不在なら明示的エラー伝播 + `sphinx-init` 誘導 (Makefile 自動生成等の暗黙処理は行わない)
2. 実行 CWD はプロジェクトルート (`pyproject.toml` のあるディレクトリ) 前提。サブディレクトリから呼ばれた場合はプロジェクトルートへ移動してから実行
3. PM 検出 (上記「パッケージマネージャ検出」セクション参照)

## プロジェクト種別判定

`docs/Makefile` に `revealjs` ターゲットが存在し、かつ `docs/conf.py` の extensions に `sphinx_revealjs` を含む場合、スライドプロジェクトとみなす:

- ターゲット無指定の「ビルドして」は `revealjs` にマッピングする
- `livehtml` は Makefile 側で `-b revealjs` 動作となる (`revealjs-init` が生成)
- 片方のみ該当する場合は不整合として明示的エラー伝播し、どちらを直すかユーザーに確認する (勝手にどちらかへ寄せない)

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
| スライドビルド (Reveal.js) | `uv run make -C docs revealjs` |
| ヘルプ | `uv run make -C docs help` |

PM ごとの実コマンド書き換えは冒頭の「パッケージマネージャ検出」セクションを参照。

## エラー解釈パターン

ビルド失敗時、出力を解析して以下のパターンに該当する場合は修正候補を提示:

- `WARNING: undefined label` → 参照先ラベルの定義箇所を提示、修正候補
- `WARNING: document isn't included in any toctree` → toctree 追加提案
- `Could not import extension` → `uv add <pkg> --group docs` 提案
- `Could not import extension sphinx_revealjs` → `uv add sphinx-revealjs --group docs` 提案。プロジェクトが未初期化なら `revealjs-init` 誘導
- LaTeX 系エラー (`latexpdfja` 失敗) → upLaTeX / dvipdfmx インストール手順 (TeX Live 等)
- ポート競合 (livehtml) → `PORT=8003` 等の代替ポート提案

## 関連スキル

- 前提: `sphinx-init` (Makefile が無ければ誘導)、`revealjs-init` (スライドプロジェクトの初期化)
- 連携: `sphinx-config` (拡張不在エラー時の依存追加)
