# sphinx-skills

Sphinx + MyST ドキュメント開発を支援する Agent Skills パッケージのドキュメントへようこそ。

本パッケージは Claude Code 等のエージェントから `gh skill install` で導入し、Sphinx プロジェクトの初期化・設定・ビルド・MyST 執筆支援を行うスキル群を提供します。

## 提供スキル

| スキル | 用途 |
| --- | --- |
| `sphinx-init` | プロジェクト初期化 (RST/MyST 選択、Makefile セットアップ) |
| `sphinx-config` | `conf.py` の安全な更新 |
| `sphinx-theme` | テーマ管理 (Furo / RTD / Shibuya) |
| `sphinx-build` | Makefile 経由のビルド (HTML / 日本語 PDF / livehtml) |
| `myst-authoring` | MyST 記法支援 |
| `rst-to-myst` | 既存 RST プロジェクトの MyST 移行 |

## クイックスタート

### 前提条件

- [GitHub CLI (`gh`)](https://github.com/cli/cli) がインストール済みであること

### インストール

```bash
cd your-python-project
gh skill install drillan/sphinx-skills sphinx-init --agent claude-code --scope project
```

## 目次

```{toctree}
:maxdepth: 2
:caption: Contents

skills/index
```

## 索引

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
