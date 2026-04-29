# sphinx-theme

Sphinx HTML テーマ (Furo / sphinx_rtd_theme / Shibuya) のインストールと設定を行うスキル。テーマ公式ドキュメントを WebFetch で取得し、最新仕様に基づく `html_theme_options` を提案する。

## 発火条件

- 「テーマを変えたい」「Furo にして」「Shibuya を使いたい」「ダークモード対応」「サイドバー設定」

## 対応テーマ (初版)

| テーマ | パッケージ | 公式ドキュメント |
| --- | --- | --- |
| Furo | `furo` | <https://pradyunsg.me/furo/> |
| Read the Docs | `sphinx-rtd-theme` | <https://sphinx-rtd-theme.readthedocs.io/> |
| Shibuya | `shibuya` | <https://shibuya.lepture.com/> |

## 責務 (ミニマル設計)

### 1. テーマインストール

検出した PM で対応コマンドを実行する。

```bash
uv add <theme-pkg> --group docs
```

### 2. `html_theme` 更新

`sphinx-config` スキルに委譲して `html_theme` の値を更新する。`conf.py` の安全な編集 (バックアップ・明示的エラー伝播) は `sphinx-config` の責務。

### 3. テーマ固有オプション提案

WebFetch で公式ドキュメントから最新の `html_theme_options` 仕様を取得し、ユーザー要求 (ダークモード、ロゴ位置等) に合致するオプションを抽出する。反映は `sphinx-config` に委譲。

## 非責務 (明示的に範囲外)

- カスタム CSS / 静的アセット配置 (`_static/` 配下、LLM 一般判断領域)
- ロゴ・favicon 設定 (テーマ非依存の Sphinx 一般機能)
- テーマ間のオプション互換変換 (例: rtd → furo の自動オプション翻訳)

## 関連スキル

- `sphinx-config` (テーマ・オプションの conf.py 反映)
