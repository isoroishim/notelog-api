# Notelog API

Notelog は、ノートとブログの機能を統合した個人開発向けのアプリケーションです。  
このリポジトリはバックエンド側（API サーバ）を構成しており、Django および Django REST Framework を用いて構築されています。

---

## 技術スタック

| 項目             | 内容                                 |
|------------------|--------------------------------------|
| フレームワーク   | Django 4.x                           |
| API 構築         | Django REST Framework                |
| 認証方式         | JWT（`SimpleJWT` を使用予定または確認済み） |
| データベース     | PostgreSQL（本番予定） |
| 仮想環境         | venv                                |

---

## ディレクトリ構成（抜粋）

```
notelog-api/
├── config/                 # プロジェクト設定モジュール
│   ├── settings.py         # 環境設定
│   ├── urls.py             # URL ルーティング設定
│   └── wsgi.py             # WSGI アプリケーション
├── users/                 # 認証機能アプリケーション
│   ├── models.py           # ユーザーモデル
│   ├── serializers.py      # ユーザーシリアライザ
│   ├── views.py            # 認証用ビュー
│   ├── urls.py             # users アプリ内ルーティング
│   └── tests.py            # 単体テスト
├── manage.py              # 管理コマンド用エントリポイント
├── requirements.txt       # 依存パッケージ一覧
├── .env                   # 環境変数（機密情報は含まない）
```

---

## 現在の実装状況（2025年6月5日時点）

| 機能                   | 状態       | 補足                                          |
|------------------------|------------|-----------------------------------------------|
| プロジェクト初期構成   | 完了       | `config`, `users` アプリ作成済み              |
| JWT 認証の検証         | 済み       | フロントと通信確認のみ、ログイン処理未整備   |
| カスタムユーザーモデル | 未実装     | 今後必要に応じて追加予定                     |
| 投稿モデル             | 未実装     | `posts` アプリ未作成                          |
| API ドキュメント       | 未整備     | Swagger / Redoc 未導入                        |
| テストコード           | 準備中     | tests.py ファイルのみ存在                    |

---

## 今後の実装予定

- JWT 認証の正式導入（`SimpleJWT` で login / refresh API 実装）
- ユーザー登録、ログイン、ログアウト API の整備
- 投稿関連アプリ（`posts`）の新規作成
- 投稿 CRUD API の構築（記事、タグ、コメントなど）
- PostgreSQL への切り替え
- フロントとの本格連携（CORS 設定、JSON 応答確認）
- Swagger または Redoc による API ドキュメント整備

---

## 開発用起動方法

1. 仮想環境作成・起動（初回のみ）

```
python -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
```

2. 依存パッケージのインストール

```
pip install -r requirements.txt
```

3. サーバ起動（デフォルトポート: 8000）

```
python manage.py runserver
```

4. マイグレーション適用（初回のみ）

```
python manage.py migrate
```

---

## 補足情報

- 認証は JWT トークン方式（`Authorization: Bearer <token>`）を使用予定
- 本リポジトリは `notelog` モノレポのバックエンド部分に該当
- データベースは SQLite（開発時） → PostgreSQL（本番）を前提として設計
