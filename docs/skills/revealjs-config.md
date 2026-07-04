# revealjs-config

sphinx-revealjs 固有の conf.py 設定に関する知識を提供するスキルです。「何を設定すべきか」の知識のみを持ち、conf.py 編集の実行は `sphinx-config` スキルへ委譲します。

## 発火条件

- extensions に `sphinx_revealjs` があるプロジェクトで conf.py の revealjs 設定変更を求められた場合
- 「スライドの幅を変えたい」「プラグインを追加したい」「コードハイライトが効かない」「Mermaid がスライドからはみ出す」

## 主な知識項目

| 項目 | 要点 |
| --- | --- |
| `revealjs_script_plugins` | **UMD バンドル版必須** (`plugin.js` は ES モジュール形式で動作しない)。highlight / notes / math / search / zoom の指定例を収録 |
| `revealjs_css_files` | highlight.js の色付けは CSS テーマが担当するため、**CSS 未読込だとハイライトが反映されない** |
| `revealjs_script_conf` | width (ワイドスクリーンでは 1200 推奨) / height / slideNumber / hash |
| `revealjs_style_theme` | 組み込みテーマ切り替えとカスタム CSS 指定 |
| sass 拡張 | `sphinx_revealjs.ext.sass`。コンパイラの dart-sass は初回ビルド時に自動取得 (追加の Python 依存は不要)。コードブロック幅最大化の SCSS パターン |
| sphinx-oceanid 連携 | extensions 追加のみで動作。`mermaid_*` 系設定は不要。縦長 SVG のはみ出しは `max-height` CSS で対処 |

設定項目の網羅リストは WebFetch で [sphinx-revealjs 公式ドキュメント](https://sphinx-revealjs.readthedocs.io/en/stable/configurations/) から取得し、スキル記載の落とし穴・推奨値と組み合わせて提案します。

## 関連スキル

- 委譲先: `sphinx-config` (conf.py 編集の実行)
- 前提: `revealjs-init` (未初期化プロジェクトの誘導)
- 連携: `revealjs-authoring` (Mermaid の記法側ルール)
