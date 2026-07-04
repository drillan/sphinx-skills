# sphinx-build

`docs/Makefile` 経由で Sphinx ドキュメントをビルドするスキルです。HTML、クリーン再ビルド、日本語 PDF (`latexpdfja`)、EPUB、リンクチェック、ライブリロード開発サーバ (`livehtml`)、Reveal.js スライドビルド (`revealjs`) を統一インターフェースで扱います。

## 発火条件

- 「ビルドして」「ドキュメント生成」「HTML 化」「PDF にして」「日本語 PDF」「ライブリロード」「開発サーバ起動」「リンクチェック」
- 「スライドをビルド」「スライドをプレビュー」

## 前提検証

1. `docs/Makefile` が存在すること — 不在なら明示的エラー伝播 + `sphinx-init` 誘導 (Makefile 自動生成等の暗黙処理は行いません)
2. 実行 CWD はプロジェクトルート (`pyproject.toml` のあるディレクトリ) 前提。サブディレクトリから呼ばれた場合はプロジェクトルートへ移動してから実行します
3. PM 検出 (uv / poetry / pipenv / plain venv)

## プロジェクト種別判定

`docs/Makefile` に `revealjs` ターゲットが存在し、かつ `docs/conf.py` の extensions に `sphinx_revealjs` を含む場合はスライドプロジェクトとみなし、ターゲット無指定の「ビルドして」を `revealjs` にマッピングします。`livehtml` は Makefile 側で `-b revealjs` 動作となります。片方のみ該当する場合は不整合として明示的エラー伝播し、ユーザーに確認します。

## ターゲットマッピング

uv 検出時のコマンド例です。他 PM では `uv run` 部分を `poetry run` / `pipenv run` / venv 有効化に置換します。

| ユーザー意図 | コマンド |
| --- | --- |
| HTML ビルド | `uv run make -C docs html` |
| クリーンビルド | `uv run make -C docs clean html` |
| PDF (英文) | `uv run make -C docs latexpdf` |
| PDF (日本語) | `uv run make -C docs latexpdfja` |
| EPUB | `uv run make -C docs epub` |
| ライブリロード | `uv run make -C docs livehtml` |
| ポート指定ライブリロード | `PORT=8003 uv run make -C docs livehtml` |
| リンクチェック | `uv run make -C docs linkcheck` |
| スライドビルド (Reveal.js) | `uv run make -C docs revealjs` |
| ヘルプ | `uv run make -C docs help` |

## エラー解釈パターン

ビルド失敗時、出力を解析して以下のパターンに該当する場合は修正候補を提示します。

| パターン | 対応 |
| --- | --- |
| `WARNING: undefined label` | 参照先ラベル定義箇所を提示、修正候補 |
| `WARNING: document isn't included in any toctree` | toctree 追加提案 |
| `Could not import extension` | `uv add <pkg> --group docs` 提案 |
| `Could not import extension sphinx_revealjs` | `uv add sphinx-revealjs --group docs` 提案 + `revealjs-init` 誘導 |
| LaTeX 系エラー (`latexpdfja` 失敗) | upLaTeX / dvipdfmx インストール手順 (TeX Live 等) |
| ポート競合 (`livehtml`) | `PORT=8003` 等の代替ポート提案 |

## 関連スキル

- 前提: `sphinx-init` (Makefile が無ければ誘導)、`revealjs-init` (スライドプロジェクト未初期化時の誘導)
- 連携: `sphinx-config` (拡張不在エラー時の依存追加)
