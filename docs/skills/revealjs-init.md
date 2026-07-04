# revealjs-init

sphinx-revealjs によるスライド専用プロジェクトを初期化するスキルです。「1発表 = 1リポジトリ、`docs/` = スライド」の専用構成を前提に、依存追加から docs/ 雛形生成、テーマ選択、Makefile セットアップ、テストビルドまでを一気通貫で行います。

## 発火条件

- 「スライドを作りたい」「sphinx-revealjs でプレゼン資料を作って」「発表資料のプロジェクトを始めたい」
- `docs/` が存在しないリポジトリで sphinx-revealjs 関連の質問を受けた場合

## 実行フロー

1. 前提検証 — PM 検出 (uv / poetry / pipenv / plain venv)、`pyproject.toml` 確認。**`docs/` が既に存在する場合は明示的に停止**します (既存ドキュメントとの共存は範囲外)
2. 依存追加 — `sphinx` `sphinx-revealjs` `myst-parser` `sphinx-autobuild` を docs グループへ
3. `sphinx-quickstart` で docs/ を生成し、`index.rst` をスライド雛形 `index.md` に置き換え
4. テーマ選択 — Reveal.js 組み込みテーマ (black / white / league / beige / night / serif / simple / solarized / moon / blood / sky) から選択
5. オプション選択 — `sphinx-oceanid` (Mermaid 図 + はみ出し対策 CSS)、SCSS カスタムテーマ (`sphinx_revealjs.ext.sass` + libsass + `_sass/custom.scss` 雛形)
6. conf.py 反映 — `sphinx-config` スキルへ委譲 (推奨値: width 1200 / height 700、highlight プラグイン + monokai.css)
7. Makefile 置換 — `revealjs` / `livehtml` (`sphinx-autobuild -b revealjs`) / `serve` ターゲット
8. テストビルド — `uv run make -C docs revealjs`。失敗時は明示的エラー伝播で停止します

## 関連スキル

- 委譲先: `sphinx-config` (conf.py 編集)、知識参照: `revealjs-config`
- 完了後: `sphinx-build` (ビルド)、`revealjs-authoring` (執筆時自動発火)
- 外部スキル: sphinx-oceanid 選択時は `drillan/sphinx-oceanid` の `mermaid-diagram`
