# sphinx-skills

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://drillan.github.io/sphinx-skills/)

📖 ドキュメント: <https://drillan.github.io/sphinx-skills/>

Sphinx + MyST ドキュメント開発を支援する Agent Skills パッケージ。GitHub の `gh skill install` コマンドで配布可能。

## 提供スキル (6個)

| スキル | 用途 | 自動発火条件 |
|---|---|---|
| [`sphinx-init`](skills/sphinx-init/SKILL.md) | プロジェクト初期化 (RST/MyST 選択、Makefile セットアップ) | 「Sphinx 始めたい」「初期化して」 |
| [`sphinx-config`](skills/sphinx-config/SKILL.md) | conf.py の安全な更新 | 「拡張機能を追加」「conf.py 変更」 |
| [`sphinx-theme`](skills/sphinx-theme/SKILL.md) | テーマ管理 (Furo / RTD / Shibuya) | 「テーマを変えたい」「ダークモード」 |
| [`sphinx-build`](skills/sphinx-build/SKILL.md) | Makefile 経由のビルド (HTML / 日本語 PDF / livehtml) | 「ビルドして」「PDF にして」「ライブリロード」 |
| [`myst-authoring`](skills/myst-authoring/SKILL.md) | MyST 記法支援 | `.md` 編集時 + `myst_parser` 検出 |
| [`rst-to-myst`](skills/rst-to-myst/SKILL.md) | 既存 RST プロジェクトの MyST 移行 | 「RST を MyST に変換」 |

## 対象エージェント

主想定は **Claude Code**。`gh skill install --agent <name>` で claude-code / github-copilot / cursor / codex / gemini / antigravity に対応 (形式互換、発動精度はエージェント依存)。

## インストール

エージェント別に APM の `--target` または gh CLI の `--agent` で配置先を切り替える (Claude Code は `.claude/skills/`、GitHub Copilot は `.github/skills/`、その他もそれぞれの規約)。git で管理することを前提とする。

### 推奨: APM (Agent Package Manager) で一括導入

`--target claude` 指定で 1 コマンド導入。`apm.yml`、`apm.lock.yaml`、`.gitignore` が自動生成され、6 スキルが `.claude/skills/` 配下に配置される。

```bash
cd your-python-project
apm install drillan/sphinx-skills --target claude
git add .claude/skills/ apm.yml apm.lock.yaml .gitignore
git commit -m "chore: install sphinx-skills via APM"
```

`--target` を省略すると `.github/skills/` (Copilot 用レイアウト) に配置される。他エージェントを使う場合は `claude` の部分を `codex` / `copilot` / `cursor` / `gemini` 等に置き換え (複数なら `claude,copilot` のように comma 区切り、全部対応なら `all`)。

生成される `apm.yml` の主要部分:

```yaml
name: your-python-project
dependencies:
  apm:
    - drillan/sphinx-skills
```

別の開発者がリポジトリを clone した後は、引数なしで再現できる。

```bash
apm install   # apm.yml の内容で全依存を復元 (target は既存ディレクトリから auto-detect)
```

CI や production では drift 防止のため tag/SHA で pin することを推奨 (例: `drillan/sphinx-skills#v0.1.0`。リリース後に利用可)。

APM 本体の導入手順は https://github.com/microsoft/apm を参照 (例: `curl -sSL https://aka.ms/apm-unix | sh`)。

#### ユーザースコープに入れる場合

複数プロジェクトで使い回すなら `-g` (`--global`) を付ける。manifest が `~/.apm/` に、スキルが `~/.claude/skills/` に配置される。

```bash
apm install drillan/sphinx-skills --target claude -g
```

user scope の対応状況は target ごとに異なる:

- 完全対応: `claude` / `gemini` / `copilot-cowork`
- 部分対応: `copilot` / `cursor` / `opencode` (一部のプリミティブ非対応)
- 非対応: `codex` (project scope のみ利用可)

アンインストールは `apm uninstall drillan/sphinx-skills -g`。

#### gh CLI 経由のスキルが既に存在する場合

`gh skill install` で配置したスキルは frontmatter の `metadata:` ブロックで識別される。APM はそれを検知して上書きを拒否し、`1 file skipped -- local files exist, not managed by APM` の警告を出す。APM 管理に統一する場合は `--force` で上書きするか、該当スキルを `rm -rf <skill_dir>` で削除してから再 install する。

### 代替: GitHub CLI で一括インストール

APM を導入できない環境では `gh skill install` をシェルループでまとめて実行する。

```bash
cd your-python-project
for s in sphinx-init sphinx-config sphinx-theme sphinx-build myst-authoring rst-to-myst; do
  gh skill install drillan/sphinx-skills "$s" --agent claude-code --scope project
done
git add .claude/skills/ && git commit -m "chore: install sphinx-skills"
```

ユーザースコープに入れる場合は `--scope user`。他エージェントを使う場合は `--agent` の値を `github-copilot` / `cursor` / `codex` / `gemini-cli` / `antigravity` 等に置き換える。Claude Code 以外の多くは `.agents/skills/` を共有する規約なので、`git add` 先もそれに合わせる。各スキルは description の発火条件で Sphinx 不使用プロジェクトでは発動しないため、user スコープでも誤発火しない。

## 典型シナリオ

### A. 新規 Sphinx + MyST プロジェクトを開始

```
User: "このプロジェクトに Sphinx ドキュメントを追加して、MyST で書きたい"
```

→ `sphinx-init` 発火 → uv 検出 → MyST 選択 → MyST extensions 選択 →
   Sphinx 拡張パック選択 → `sphinx-config` 委譲で conf.py 反映 →
   Makefile カスタマイズ (livehtml, latexpdfja) → テストビルド成功

### B. 既存 RST プロジェクトを MyST に移行

```
User: "古い RST のドキュメントを Markdown に移行したい"
```

→ `rst-to-myst` 発火 → `docs/*.rst` を `uvx rst2myst convert` で変換 →
   3段階検証 (存在/サイズ/エラーマーカ) → 成功時のみ原本削除 →
   `sphinx-config` 委譲で myst-parser 追加 → `myst-authoring` が以降自動発火

### C. テーマを Furo から Shibuya に切り替え

```
User: "テーマを Shibuya にしたい、ダークモードもオンにして"
```

→ `sphinx-theme` 発火 → `uv add shibuya --group docs` → WebFetch で Shibuya 公式 →
   ダークモードオプション抽出 → `sphinx-config` 委譲で `html_theme` と
   `html_theme_options` 反映

### D. 日本語 PDF を生成

```
User: "ドキュメントの日本語 PDF を作って"
```

→ `sphinx-build` 発火 → `docs/Makefile` 確認 →
   `uv run make -C docs latexpdfja` 実行 (upLaTeX + dvipdfmx)

### E. ライブリロードで開発

```
User: "開発サーバ立ち上げて、編集したら自動でブラウザ更新されるように"
```

→ `sphinx-build` 発火 → `uv run make -C docs livehtml` (sphinx-autobuild) →
   `http://0.0.0.0:8000` で配信 (PORT=8003 等で上書き可)

## 開発・コントリビュート

### 検証

```bash
uv sync --group dev
uv run pytest tests/ -v                          # validator のテスト
uv run python scripts/validate_skills.py skills  # 全 SKILL.md の frontmatter 検証
uv run ruff check . && uv run ruff format .
uv run mypy scripts tests
```

### CI

`.github/workflows/ci.yml` が PR/push 時に上記検証を全実行する。

### 関連プロジェクト

- [drillan/sphinx-oceanid](https://github.com/drillan/sphinx-oceanid) — Mermaid 図対応の Sphinx 拡張 + 専用 mermaid-diagram スキル

## ライセンス

MIT (`LICENSE` 参照)
