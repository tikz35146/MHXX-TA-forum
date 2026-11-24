# 記録の投稿

新規のMHXX TA記録は、X（Twitter）、GitHub Issue、Pull Requestから受け付けます。掲載前に管理者がガイドライン、レギュレーション、証明を確認します。

同じ部門で自己ベストを更新した場合も、以下の方法で投稿できます。[記録の掲載単位](docs/guidelines.md#記録の掲載単位)

## X（Twitter）

公式運用アカウントのDMまたはリプライへ、クエスト名、武器種・スタイル、タイム、レギュレーション、ハンターネーム、証明URLを送ってください。アカウントは公開時にREADMEとサイトへ設定します。

## GitHub Issue

「TA記録の投稿」テンプレートから投稿してください。データ編集に不慣れな場合はこちらを推奨します。

## Pull Request

`quest/<区分>/<クエスト>/<武器種>/regulation<ルール>/records.json` の配列に新規記録を追加してください。自己ベスト更新時は同じ部門の自分の記録を差し替えます。`python scripts/build_scores.py`（Python 3.8以降、標準ライブラリのみ）で記録一覧を再生成し、入力ファイルと生成された `pages/data/records.json` をまとめてPRに含めてください。

```json
{
  "hunter": "ハンターネーム",
  "time": "3'21\"40",
  "weaponName": "鎧裂鎌ドヒキサキ",
  "style": "ブレイヴ",
  "hunterArts": ["絶対回避【臨戦】"],
  "skills": ["弱点特効", "超会心"],
  "foodSkills": ["ネコの研磨術"],
  "proofUrl": "https://example.com/proof",
  "publishedAt": "2027-01-01"
}
```
