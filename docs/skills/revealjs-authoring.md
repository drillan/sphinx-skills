# revealjs-authoring

sphinx-revealjs スライドを執筆する際の MyST 記法ルールを提供するスキルです。`docs/conf.py` に `sphinx_revealjs` を含むプロジェクトで `.md` を編集すると自動発火します。汎用 MyST ルールは `myst-authoring` が担当し、本スキルはスライドという媒体に固有の制約のみを扱います (矛盾時は本スキルを優先)。

## 主なルール

| カテゴリ | ルール |
| --- | --- |
| スライド構造 | `#` = タイトル、`##` = セクション区切り、`###` = 個別スライド。1スライド1トピック |
| テーブル | `{list-table}` 必須 (パイプテーブル禁止)。`:header-rows:` 必須、**3列以内** (超えたらスライド分割) |
| 左右分割 | `{list-table}` `:widths: 50 50`。ネストはコロンフェンス段数で表現 (外側 `:::::`、内側 `:::`) |
| コード | 5行超・外部ファイルは `{literalinclude}` + `:language:` 必須 |
| Mermaid | `{mermaid}` ディレクティブ (ASCII アート禁止)。対応タイプ: flowchart / sequenceDiagram / stateDiagram-v2 / classDiagram / erDiagram / xychart-beta |
| Admonition | note / tip / warning / important / seealso を1〜3行で簡潔に |
| 定義リスト | 「用語: 説明」は定義リスト構文。箇条書きで代用しない |
| 一般 | ディレクティブはコロンフェンス `:::` 統一。はみ出したらプレビューで確認して分割 |

各ルールは SKILL.md 内で「正しい記法」と「禁止パターン」の対で例示されています。

## 関連スキル

- 姉妹スキル: `myst-authoring` (汎用 MyST ルール)
- 連携: `revealjs-config` (設定側の対処)、`sphinx-build` (プレビュー確認)
