# QueryLens

複雑なSQLクエリをステップごとに分解し、中間テーブルをプレビュー表示する解析ツール。

## セットアップ

**必要なもの**

- Python 3.14+
- Poetry 2.0+

**インストール**

```bash
git clone https://github.com/ryuseim1115/QueryLens.git
cd QueryLens
poetry install
```

## 起動

```bash
cd backend
uvicorn main:app --reload
```
