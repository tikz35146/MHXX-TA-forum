# 記録一覧の更新

`build_scores.py` は、`quest/` 配下の記録を部門ごとに採点し、サイトの記録一覧を再生成します。Python 3.8 以降の標準ライブラリで動作します。以下のコマンドはリポジトリのルートで実行します。

## 記録を追加・更新する

`quest/<区分>/<クエスト>/<武器種>/regulation<ルール>/records.json` の JSON 配列を編集します。新しい走者は配列に追加し、自己ベスト更新時は同じ部門の既存記録を差し替えます。[青電主・太刀・レギュレーションAの入力例](../quest/超特殊許可/青電主/太刀/regulationA/records.json)

採点に使う項目は走者名 `hunter` とタイム `time` です。たとえば4分52秒30は JSON で `"time": "4'52\"30"` と記入します。秒と百分の一秒はそれぞれ2桁に揃えます。スタイルや証明URLなどの掲載項目は[投稿ガイド](../CONTRIBUTING.md)を参照してください。

## 採点する

```sh
python scripts/build_scores.py
```

Windows の PowerShell で `python` が見つからず、Codex 同梱の Python を使う場合は、リポジトリのルートで次を実行します。

```powershell
$wikiPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $wikiPython scripts/build_scores.py
```

端末に処理した記録数と出力先が表示されます。出力の [pages/data/records.json](../pages/data/records.json) には、部門別の得点 `score` と、同じ走者の同一クエストで最高得点の1件を示す `scoreCounted` が入ります。記録の修正は入力側の `quest/` で行い、再度コマンドを実行してください。[採点式](../docs/rating.md)

## ブラウザで確認する

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory pages
```

上で `$wikiPython` を設定した PowerShell では、同じ端末で次を実行します。

```powershell
& $wikiPython -m http.server 8000 --bind 127.0.0.1 --directory pages
```

[ローカルの記録一覧](http://127.0.0.1:8000/#records)で、更新した部門のタイムとスコアを確認します。確認後は端末で Ctrl+C を押してサーバーを終了します。
