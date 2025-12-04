*Read this in other languages: [English](README.md)*

# NoMoney

NoMoneyはDjangoで作られたシンプルな家計簿です。(妻のために作りました。)

複式簿記の考え方が取り入れられています。
(素人なので、何かが間違っているかもしれません。)

![Screenshot](docs/img/screenshots/report-lg-en.png)

## 要件

* Python 3.12+
* Django 5.2
* PostgreSQL 18+

## インストール

### Docker Compose

1. NoMoneyをクローンまたはコピーします。
2. `docker compose build` を実行して、Dockerイメージをビルドします。
3. 静的ファイルとメディアを保存するディレクトリを作成します。
```bash
groupadd -r nomoney
mkdir -p /var/opt/
install -g nomoney -m 775 -d /var/opt/nomoney/app/{staticfiles,media}
```
4. 以下のコマンドを実行し、設定ファイルをコピーし、必要に応じて修正します。
```bash
cp extra/docker/env.tmpl .env
cp extra/docker/compose.override.yaml.tmpl compose.override.yaml
```
5. `docker compose up -d` を実行して、NoMoneyを起動します。
6. 静的ファイルをコピーします。
```bash
docker compose exec app python3 manage.py collectstatic
```

以下にアクセスしましょう。
http://example.com/n/money/

## 使い方

### 科目の設定

まずは管理画面から科目を追加します。例えば、以下のように追加しましょう。

| 名前             | 科目 |
|------------------|------|
| 給料             | 収入 |
| 現金             | 資産 |
| クレジットカード | 負債 |
| 食費             | 支出 |
| 衣服・美容       | 支出 |
| ...              | ...  |

### 記録

お金のやりとりが発生したら、
「新しい記録」をクリックして、データを入力します。

### レポート

まとめが知りたくなったら、「レポート」ページを開いてください。

## ライセンス

[MIT](LICENSE)

## 作者

なかむら たけし
