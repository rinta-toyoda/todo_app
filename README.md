<div id="top"></div>

## 使用技術一覧

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <!-- バックエンドのフレームワーク一覧 -->
  <img src="https://img.shields.io/badge/-FastAPI-00968.svg?logo=fastapi&style=for-the-badge">
  <!-- バックエンドの言語一覧 -->
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <!-- ミドルウェア一覧 -->
  <img src="https://img.shields.io/badge/-PostgreSQL-4479A1.svg?logo=postgreSQL&style=for-the-badge&logoColor=white">
  <!-- インフラ一覧 -->
  <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
</p>

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [環境構築](#環境構築)

<!-- プロジェクトについて -->

## プロジェクトについて

Docker、FastAPI、PostgreSQL を使用したTODOアプリ

<p align="right">(<a href="#top">トップへ</a>)</p>

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.10       |
| FastAPI               | 0.100.0    |
| PostgreSQL            | 15.0       |

その他のパッケージのバージョンは requirements.txt を参照してください

<p align="right">(<a href="#top">トップへ</a>)</p>

## ディレクトリ構成

<!-- Treeコマンドを使ってディレクトリ構成を記載 -->
```
│   .env
│   docker-compose.yml
│   Dockerfile
│   README.md
│   swagger.yaml
│
├───app
│       database.py
│       main.py
│       requirements.txt
│
├───config
│       postgresql.conf
│
└───initdb
        setup.sql
```

### .env
環境変数を記載

### docker-compose.yml
作成するコンテナの内容

### Dockerfile

appディレクトリをtodo_appコンテナに作成
```
WORKDIR /app
```

localのappディレクトリにあるファイルをコンテナのappディレクトリにコピー
```
COPY ./app /app
```

requirements.txtから必要なライブラリをinstall
```
RUN pip install --no-cache-dir -r /app/requirements.txt
```

uvicornでFastAPIアプリケーションを起動
```
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### app/database.py
データベースを直接操作するメソッドとその際に必要なメソッドを記載

### app/main.py
APIの処理を記載

### app/requirements.txt
Pythonで使用するライブラリを記載

### config/postgresql.conf
postgreSQLのコンテナがtodo_appのコンテナからアクセスできるように、以下を記載
```
listen_addresses = '*'
```

### initdb/setup.sql
コンテナを初めて作成するときに実行されるsqlを記載。Taskテーブルを作成する

<p align="right">(<a href="#top">トップへ</a>)</p>

## 環境構築

docker-compose.ymlがあるディレクトリで以下のコマンドを実行
```
$ docker-compose up --build
```
