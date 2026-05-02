# QueryLens

## セットアップ

### 必要なもの
- Python 3.14+
- Poetry
- Node.js

### インストール

```bash
# システム依存ライブラリ
sudo apt install -y default-libmysqlclient-dev build-essential python3-dev

# Python 依存パッケージ
poetry install --no-root

# JS/HTML/CSS ツール
cd frontend && npm install
```

## 開発サーバー起動

```bash
cd backend
uvicorn main:app --reload
```

## リント・フォーマット

```bash
# Python（ルートで実行）
poetry run ruff check backend/
poetry run ruff format backend/

# JS/HTML/CSS（frontend/ で実行）
cd frontend
npm run lint
npm run format
```
