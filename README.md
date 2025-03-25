<div id="top"></div>

## Used Frameworks and Languages

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

## Table of Contents

1. [About this project](#プロジェクトについて)
2. [Environment](#環境)
3. [Directory Structure](#ディレクトリ構成)
4. [Building Environment](#環境構築)

<!-- プロジェクトについて -->

## About this project

TODO app that uses Docker、FastAPI、PostgreSQL

<p align="right">(<a href="#top">Top</a>)</p>

## Environment

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| Language and Framework | Version |
|------------------------|---------|
| Python                 | 3.10    |
| FastAPI                | 0.100.0 |
| PostgreSQL             | 15.0    |

Refer to requirements.txt for more information on the versions of libraries used.

<p align="right">(<a href="#top">トップへ</a>)</p>

## Directory Structure

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
Environment Variables

### docker-compose.yml
Docker compose file

### Dockerfile

create app directory in todo app container
```
WORKDIR /app
```

copy local app directory to todo app container
```
COPY ./app /app
```

install libraries in requirements.txt
```
RUN pip install --no-cache-dir -r /app/requirements.txt
```

start FastAPI server with uvicorn
```
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### app/database.py
Includes methods for connecting to the database and executing SQL

### app/main.py
Writes about the API methods.

### app/requirements.txt
Requirements for the libraries used in the project

### config/postgresql.conf
Has the line below so that the postgreSQL container can be accessed from the todo_app container
```
listen_addresses = '*'
```

### initdb/setup.sql
SQL to be executed when creating the container for the first time. Create the Task table

<p align="right">(<a href="#top">トップへ</a>)</p>

## Building Environment
In the directory that docker-compose.yml is located, run the following command
```
$ docker-compose up --build
```
