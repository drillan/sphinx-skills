# sphinx-init

Sphinx ドキュメントプロジェクトを新規作成する初期化スキル。プロジェクトのパッケージマネージャ (uv 推奨、poetry / pipenv / plain venv も対応) を自動検出して依存追加を行い、RST または MyST (Markdown) 記法を選択できる。`livehtml` と `latexpdfja` ターゲットを含むカスタム Makefile も生成する。

## 発火条件

- ユーザーが「Sphinx ドキュメントを始めたい」「初期化して」「ドキュメント環境作って」と発話
- `docs/` が存在しないリポジトリで Sphinx 関連の質問を受けた場合

## パッケージマネージャ検出

| 優先 | 判定条件 | 採用 |
| --- | --- | --- |
| 1 | `uv.lock` が存在 | uv |
| 2 | `poetry.lock` が存在 | poetry |
| 3 | `Pipfile.lock` が存在 | pipenv |
| 4 | `.venv/` のみ存在 | plain venv |
| 5 | 上記すべて該当しない | ユーザー問い合わせ (推奨: uv) |

検出した PM のコマンドが PATH に無ければ例外を送出。デフォルト値による継続処理は行わない。

## 実行フローの要点

1. **前提検証**: `pyproject.toml` 不在なら PM ごとの初期化を案内
2. **記法選択**: MyST (推奨) または RST
3. **プロジェクト情報取得**: `project.name` → ディレクトリ名、`authors[0].name` → `git config user.name` → `$USER`
4. **基本パッケージ追加**: `sphinx` を docs グループに追加
5. **`sphinx-quickstart`** で初期化
6. **MyST 選択時**: `myst-parser` 追加 → `index.rst` を `index.md` に置換 → MyST optional extensions を選択
7. **拡張パック選択**: `sphinx-autobuild` (必須)、`sphinx-copybutton` / `sphinx-design` / `intersphinx` / `napoleon` (推奨)
8. **`conf.py` 反映** は `sphinx-config` に委譲
9. **Makefile カスタマイズ**: `livehtml` (sphinx-autobuild) と `latexpdfja` を追加
10. **テストビルド**: `make html` で動作確認

## MyST optional extensions の推奨セット

`amsmath`, `dollarmath`, `attrs_inline`, `colon_fence`, `deflist`, `html_admonition`, `html_image`, `replacements`, `smartquotes`, `strikethrough`, `substitution`, `tasklist`, `fieldlist`, `linkify`

`linkify` 選択時は `linkify-it-py` を docs 依存に自動追加する。

## 関連スキル

- **委譲先**: `sphinx-config` (conf.py 編集の単一ロジック)、`rst-to-myst` (既存 .rst が複数ある場合の移行)
- **完了後**: `sphinx-build` (動作確認)、`sphinx-theme` (テーマ変更時)、`myst-authoring` (MyST 執筆時)
