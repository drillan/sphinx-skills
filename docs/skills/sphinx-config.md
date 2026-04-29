# sphinx-config

`docs/conf.py` を既存設定を保持したまま安全に更新するスキルです。Sphinx 拡張、MyST optional extensions、テーマ、プロジェクトメタデータの追加・削除を担います。本スキルは `conf.py` 編集の単一ロジックを保持する役割であり、他スキル (`sphinx-init`, `sphinx-theme`, `rst-to-myst`) からの委譲先となります。

## 発火条件

- 「拡張機能を追加して」「conf.py を更新」「プロジェクト名を変えたい」「言語設定を変更」
- 他スキル (`sphinx-init`, `sphinx-theme`, `rst-to-myst`) からの委譲呼出

## 責務

### 1. 既存設定の保持

編集対象セクションのみ変更します。コメント、`sys.path` 操作、その他のユーザー設定はそのまま保持します。

### 2. 3rd-party 拡張は自動依存追加

3rd-party 拡張を `extensions` に追加する際は、検出した PM で対応コマンドを実行します。

### 3. MyST 拡張変更

`myst_enable_extensions` リストの追加/削除を行います。`linkify` 追加時は対応 PM で `linkify-it-py` を docs 依存に追加します。

### 4. バックアップと明示的エラー伝播

編集失敗時の挙動を厳格に規定します。

1. 編集前に必ず `conf.py.bak` を作成
2. 編集失敗時: `conf.py.bak` から原本を復元したうえで、元のエラーを必ず例外送出する (復元成功で「正常終了」扱いにしない)
3. 復元処理自体が失敗した場合: `conf.py.bak` のパスと手動復元手順を提示して即時例外送出
4. 編集成功時のみ `conf.py.bak` を削除

これにより「復元したから OK」というサイレントフェイル実装を仕様レベルで防止します。

## 拡張カタログ (sphinx-init と共有)

カタログは配布物の自己完結性のため `sphinx-init` と本スキルで重複保持されます。

### MyST optional extensions

数式系 (`amsmath`, `dollarmath`)、属性系 (`attrs_inline`, `attrs_block`)、リスト系 (`deflist`, `tasklist`, `fieldlist`)、ブロック系 (`colon_fence`, `html_admonition`, `html_image`)、テキスト系 (`replacements`, `smartquotes`, `strikethrough`, `substitution`)、リンク系 (`linkify` — `linkify-it-py` 必要)。

### Sphinx 拡張パック

- 必須: `sphinx-autobuild` (Makefile `livehtml` 依存)
- 推奨: `sphinx-copybutton`, `sphinx-design`, `sphinx.ext.intersphinx`, `sphinx.ext.napoleon`
- オプショナル: `sphinx_oceanid` (Mermaid)、`sphinx.ext.autodoc`、`sphinx.ext.viewcode`、`sphinx.ext.todo`、`myst-nb`

## 関連スキル

- `sphinx-theme` (テーマ変更時に `html_theme` と `html_theme_options` の更新で連携)
- 委譲元: `sphinx-init` (init 時の conf.py 反映)、`rst-to-myst` (変換後 myst-parser 追加)
