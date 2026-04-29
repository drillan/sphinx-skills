---
name: sphinx-theme
description: Install and configure Sphinx HTML themes (Furo, sphinx_rtd_theme, Shibuya). Fetches latest theme documentation to propose accurate theme-specific html_theme_options. Triggers when user asks to change documentation theme, install a theme, or customize theme appearance options like dark mode, sidebar, navigation.
license: MIT
allowed-tools: Bash, WebFetch, Read, Edit
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

依存追加コマンド対応:
- uv: `uv add <pkg> --group docs`
- poetry: `poetry add --group docs <pkg>`
- pipenv: `pipenv install --dev <pkg>`
- plain venv: `pyproject.toml` 手動編集 + `pip install -e ".[docs]"`

検出した PM のコマンドが PATH に無ければ例外送出 (フォールバック禁止)。

## 発火条件

- 「テーマを変えたい」「Furo にして」「Shibuya を使いたい」「ダークモード対応」「サイドバー設定」

## 対応テーマ (初版)

| テーマ | パッケージ | 公式ドキュメント |
|---|---|---|
| Furo | `furo` | https://pradyunsg.me/furo/ |
| Read the Docs | `sphinx-rtd-theme` | https://sphinx-rtd-theme.readthedocs.io/ |
| Shibuya | `shibuya` | https://shibuya.lepture.com/ |

## 責務 (ミニマル)

### 1. テーマインストール

検出した PM で対応コマンドを実行:

```bash
uv add <theme-pkg> --group docs
# poetry: poetry add --group docs <theme-pkg>
# pipenv: pipenv install --dev <theme-pkg>
# plain venv: pyproject.toml 編集 → pip install -e ".[docs]"
```

### 2. html_theme 更新

`sphinx-config` スキルに委譲して `html_theme` の値を更新する。conf.py の安全な編集 (バックアップ・明示的エラー伝播) は `sphinx-config` の責務。

### 3. テーマ固有オプション提案

WebFetch で公式ドキュメントから最新の `html_theme_options` 仕様を取得:

- Furo: `https://pradyunsg.me/furo/customisation/`
- RTD: `https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html`
- Shibuya: `https://shibuya.lepture.com/customisation/`

ユーザー要求 (ダークモード、ロゴ位置等) に合致するオプションを抽出し、`html_theme_options` 反映を `sphinx-config` に委譲。

## 非責務 (明示的に範囲外)

- カスタム CSS / 静的アセット配置 (`_static/` 配下、LLM 一般判断領域)
- ロゴ・favicon 設定 (テーマ非依存の Sphinx 一般機能)
- テーマ間のオプション互換変換 (例: rtd → furo の自動オプション翻訳)

## 関連スキル

- `sphinx-config` (テーマ・オプションの conf.py 反映)
