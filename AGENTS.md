# リポジトリガイドライン

## プロジェクト概要

このリポジトリは Django 製の todo アプリケーションです。メインアプリは `todo/`、プロジェクト設定は `config/` にあります。

## 開発コマンド

- 依存パッケージのインストール: `pip install -r requirements.txt`
- 開発サーバーの起動: `python3 manage.py runserver`
- テストの実行: `python3 manage.py test`
- CI と同じ基本的な lint チェック:
  - `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
  - `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`

## コーディングメモ

- Django の view、model、template、test は、明確な理由がない限り既存の `todo/` アプリ内に置いてください。
- ユーザーから見える動作を変更する場合は、`todo/tests.py` にテストを追加または更新してください。
- コミットは小さく、目的を絞ってください。関係のない整形変更は避けてください。
- このプロジェクトのタイムゾーンは `Asia/Tokyo`、言語設定は日本語です。

## プルリクエストの確認事項

- プルリクエストを作成する前に、`python3 manage.py test` が通ることを確認してください。
- migration、新しい依存パッケージ、デプロイに影響する変更がある場合は、PR の説明に書いてください。
