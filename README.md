# MHXX TA Wiki:RE
モンスターハンターXXの新規タイムアタック記録を集計・掲載する、GitHub Pages用の静的Wikiです。旧Wikiの記録は移植しません。

## 公開

GitHub Pages の公開元を `main` ブランチの `/docs` に設定すると、`docs/index.html` がサイトのトップページになります。

公開前に `docs/assets/site-config.js` のGitHubリポジトリURLとX（Twitter）運用アカウントURLを設定してください。投稿ボタンはこの設定を参照します。

## 記録の投稿

X（Twitter）、GitHub Issue、Pull Requestから投稿できます。詳細は[投稿ガイド](CONTRIBUTING.md)を参照してください。

承認済みの記録は `quest/` 配下に部門別に保存します。`python scripts/build_scores.py` で採点すると、`pages/index.html` の記録一覧が読み込む `pages/data/records.json` が更新されます。

# ガイドライン

[ガイドライン](docs/guidelines.md) を参照。
