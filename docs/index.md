# sphinx-skills

Sphinx + MyST ドキュメント開発を支援する Agent Skills パッケージのドキュメントへようこそ。

本パッケージは Claude Code 等のエージェント向けに、Sphinx プロジェクトの初期化・設定・ビルド・MyST 執筆支援を行うスキル群を提供します。導入には APM (Agent Package Manager) または GitHub CLI のどちらかを利用できます。

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

### 推奨: APM (Agent Package Manager) で一括インストール

[Microsoft APM](https://github.com/microsoft/apm) を導入してから実行します。

```bash
cd your-python-project
apm install drillan/sphinx-skills --target claude
```

これで 6 スキルすべてが `.claude/skills/` 配下に配置されます。`--target` の値で他エージェントに切り替えできます (`codex` / `copilot` / `cursor` / `gemini` 等、複数指定は `claude,copilot` のように comma 区切り)。複数プロジェクトで使い回す場合は `-g` を追加してユーザースコープにインストールします。

### 代替: GitHub CLI で個別インストール

[GitHub CLI (`gh`)](https://github.com/cli/cli) を導入してから実行します。

```bash
cd your-python-project
gh skill install drillan/sphinx-skills sphinx-init --agent claude-code --scope project
```

6 スキルを一括導入する手順、`apm.yml` の例、`gh CLI` 経由のスキルが既に存在する場合の対処など、詳細は [リポジトリ README のインストール節](https://github.com/drillan/sphinx-skills#インストール) を参照してください。

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
