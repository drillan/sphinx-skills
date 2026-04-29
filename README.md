# sphinx-skills

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

## インストール (推奨: プロジェクトスコープ)

プロジェクトに追従する形で `.claude/skills/` 配下に配置し、git で管理することを推奨。

```bash
cd your-python-project
gh skill install drillan/sphinx-skills sphinx-init --agent claude-code --scope project
gh skill install drillan/sphinx-skills sphinx-config --agent claude-code --scope project
gh skill install drillan/sphinx-skills sphinx-theme --agent claude-code --scope project
gh skill install drillan/sphinx-skills sphinx-build --agent claude-code --scope project
gh skill install drillan/sphinx-skills myst-authoring --agent claude-code --scope project
gh skill install drillan/sphinx-skills rst-to-myst --agent claude-code --scope project

git add .claude/skills/ && git commit -m "chore: install sphinx-skills"
```

### 個人で多数プロジェクト向け (補足: ユーザースコープ)

```bash
gh skill install drillan/sphinx-skills sphinx-init --agent claude-code --scope user
# (他のスキルも同様)
```

各スキルは description の発火条件で Sphinx 不使用プロジェクトでは発動しないため、user スコープでも誤発火しない。

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
