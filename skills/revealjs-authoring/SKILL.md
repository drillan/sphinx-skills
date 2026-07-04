---
name: revealjs-authoring
description: MyST notation rules for writing presentation slides with sphinx-revealjs. Heading levels define slide structure (h1 = title slide, h2 = section separator, h3 = individual slide). Enforces list-table with 3 columns max, two-column split layouts via nested list-table, literalinclude for code over 5 lines, Mermaid directive usage with sphinx-oceanid supported types, concise admonitions, definition lists, and colon-fence style. MUST trigger when editing or creating .md files under docs/ in a project where docs/conf.py contains sphinx_revealjs in extensions. Complements myst-authoring with slide-specific constraints.
license: MIT
allowed-tools: Read, Grep, Glob
---

## 発火条件

- `docs/conf.py` の extensions に `sphinx_revealjs` を含むプロジェクトで、`docs/` 配下の `.md` を編集・作成する場合
- 「スライドを書いて」「このスライドを直して」「スライドに1枚追加して」

## myst-authoring との棲み分け

- 汎用 MyST 記法 (ディレクティブ・ロール・相互参照・数式等) → `myst-authoring`
- スライドという媒体に固有の制約 (表示領域・スライド分割・レイアウト) → 本スキル
- 両者は同時発火しうる。ルールが矛盾する場合は本スキルのスライド固有ルールを優先する

## スライド構造 — 見出しレベル

見出しレベルがスライド分割を決める:

- `#` — タイトルスライド (文書内で1回のみ)
- `##` — セクション区切りスライド (横方向のスライド)
- `###` — 個別スライド (セクション内の縦方向のスライド)

1スライド1トピック。1つの `###` に複数トピックを詰め込まず、スライドを分割する。

### 禁止パターン

```markdown
### 機能紹介と導入方法と注意点

- 機能A の説明
- 機能B の説明
- インストール手順
- 設定方法
- 利用時の注意点
```

### 正しい記法

```markdown
### 主な機能

- 機能A の説明
- 機能B の説明

### 導入方法

- インストール手順
- 設定方法

### 利用時の注意点
```

## テーブル

- パイプテーブル (`| col1 | col2 |` 形式) は使用禁止。必ず `{list-table}` ディレクティブで記述する
- `:header-rows:` を必ず指定する (ヘッダ行がない場合は `0`)
- `:widths: auto` を基本とする
- **列数は3列以内**。4列以上になる場合はスライドを分割する
- セル内の文字数が多くテーブルでは視認性が悪い場合もスライドの分割を検討する

### 禁止パターン

```markdown
| ツール | 特徴 |
|---|---|
| Spec Kit | テンプレートとプロンプト |
```

### 正しい記法

```markdown
:::{list-table}
:header-rows: 1
:widths: auto

* - ツール
  - 特徴
* - Spec Kit
  - テンプレートとプロンプト
:::
```

### 行単位の比較テーブル

列を横断して1対1で対応する比較項目は、セル内箇条書きではなく独立したテーブル行として記述する。

#### 禁止パターン

```markdown
:::{list-table}
:header-rows: 1
:widths: auto

* - 従来の課題
  - SDD
* - - 曖昧さに気づかない
    - 乖離が発生
  - - 考えが明確化
    - コードを生成
:::
```

#### 正しい記法

```markdown
:::{list-table}
:header-rows: 1
:widths: auto

* - 従来の課題
  - SDD
* - 曖昧さに気づかない
  - 考えが明確化
* - 乖離が発生
  - コードを生成
:::
```

### 太字見出し + 箇条書きグループの表化

太字見出し + 箇条書きのグループが複数並ぶパターンは `{list-table}` に変換する。セル内箇条書きは `* - - item` の3段ネスト (行開始 → セル開始 → 箇条書き項目)、同一セル内の後続項目は4スペースインデントの `    - item`。

#### 禁止パターン

```markdown
**カテゴリA**

- 項目1
- 項目2

**カテゴリB**

- 項目3
- 項目4
```

#### 正しい記法

```markdown
:::{list-table}
:header-rows: 1
:widths: auto

* - カテゴリA
  - カテゴリB
* - - 項目1
    - 項目2
  - - 項目3
    - 項目4
:::
```

## 左右分割レイアウト

1スライドに収まらない場合・説明と図を並べる場合・複数トピックを比較する場合は `{list-table}` で左右に分割する。

- `:header-rows: 0` `:widths: 50 50` を基本とする (`60 40` 等で比率調整可)
- ディレクティブのネストはコロンフェンスの段数で表現する (外側 `:::::`、内側 `:::`)

### 禁止パターン

1スライドに収まらない量の説明と図を、分割せずに縦へ積まない:

```markdown
### アーキテクチャ

- 説明の箇条書き1
- 説明の箇条書き2
- 説明の箇条書き3

:::{mermaid}
flowchart TD
  A --> B
:::
```

### 正しい記法

```markdown
:::::{list-table}
:header-rows: 0
:widths: 50 50

* - - 箇条書き項目1
    - 箇条書き項目2
  - :::{mermaid}
    flowchart LR
      A --> B
    :::
:::::
```

## コード

- 外部ファイルに存在するコードは `{literalinclude}` で取り込む。インラインへの複製は禁止
- 説明用の5行以下のコード片のみインラインコードブロックを許容する
- `:language:` を必ず指定する

### 禁止パターン (外部ファイルのコードをインライン複製)

````markdown
```python
def hello():
    print("Hello")
```
````

### 正しい記法

```markdown
:::{literalinclude} examples/hello.py
:language: python
:start-after: # start example
:end-before: # end example
:::
```

## Mermaid ダイアグラム (sphinx-oceanid 導入時のみ)

extensions に `sphinx_oceanid` がある場合に適用する。

- フロー・シーケンス・状態遷移などの図は `{mermaid}` ディレクティブで記述する。罫線文字や ASCII アートによる図は使用禁止
- 対応タイプ: `flowchart` / `graph` (方向: `LR`, `TD`, `TB`, `RL`, `BT`)、`sequenceDiagram`、`stateDiagram-v2`、`classDiagram`、`erDiagram`、`xychart-beta`
- 非対応タイプ (`pie`, `gitGraph`, `mindmap`, `gantt` 等) はビルド時に警告が出るため使用しない
- `:name:` は本文から相互参照する場合のみ付与する
- 縦方向に長い図 (`flowchart TD` 等) はスライドからはみ出しやすい。高さ制約の対処は `revealjs-config` スキル参照

### 禁止パターン

```
┌─────────┐
│ Specify │
└────┬────┘
     ↓
┌─────────┐
│  Plan   │
└─────────┘
```

### 正しい記法

```markdown
:::{mermaid}
flowchart TD
  A[Specify] --> B[Plan]
:::
```

## Admonition

- 重要な情報・注意点・補足は Admonition ディレクティブで記述する。プレーンテキストで「注意:」「ヒント:」と書かない
- 使用可能なタイプ: `note` / `tip` / `warning` / `important` / `seealso`
- スライドの表示領域は狭い。コンテンツは1〜3行に簡潔にまとめる

### 禁止パターン

```markdown
注意: この操作は取り消せません
```

### 正しい記法

```markdown
:::{warning}
この操作は取り消せない
:::
```

## 定義リスト

用語や概念の説明は定義リスト構文で記述する。箇条書きの `- **用語**: 説明` で代用しない。

### 禁止パターン

```markdown
- **SDD**: 仕様駆動開発。仕様書を起点にコードを生成する手法
```

### 正しい記法

```markdown
SDD
: 仕様駆動開発。仕様書を起点にコードを生成する手法
```

## 一般ルール

### コロンフェンスの統一

ディレクティブの囲みにはコロンフェンス (`:::`) を使用する。バッククォートフェンス (` ``` `) でディレクティブを囲まない。

#### 禁止パターン

````markdown
```{note}
バッククォートフェンスで囲んだディレクティブ
```
````

#### 正しい記法

```markdown
:::{note}
コロンフェンスで囲んだディレクティブ
:::
```

### はみ出しの確認

スライドからのはみ出しは目視でしか検出できない。ビルド + プレビュー (`sphinx-build` スキルの revealjs / livehtml) で確認し、はみ出したらスライドを分割する。

## 関連スキル

- **姉妹スキル**: `myst-authoring` (汎用 MyST ルール)
- **連携**: `revealjs-config` (Mermaid の高さ制約等、設定側の対処)、`sphinx-build` (プレビューによるはみ出し確認)
