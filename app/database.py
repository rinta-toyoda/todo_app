import os
from typing import Any

import psycopg2

#####################################################
##  Database Connection
#####################################################
# database_url
DATABASE_URL = os.environ['DATABASE_URL']

# データベースに接続
def openConnection():
    conn = None
    # Create a connection to the database
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    except Exception as e:
        print("Error opening connection: " + e)
    return conn

# id生成
def generate_id() -> int:
    conn = openConnection()
    if conn is None:
        print("getTasks failed, conn is None")
        return None

    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM Task")
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None or row[0] is None:
        return 1
    return int(row[0]) + 1

# タスクを取得する
def getTasks() -> list[dict[str, Any]]:
    conn = openConnection()
    if conn is None:
        print("getTasks failed, conn is None")
        return None

    result = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Task")
    row = cursor.fetchone()
    if row is None:
        return []
    while row is not None:
        result += [{
            "id": int(row[0]),
            "title": str(row[1]),
            "description": str(row[2]),
            "isDone": bool(row[3])
        }]
        row = cursor.fetchone()
    cursor.close()
    conn.close()

    return result

# タスクを追加する
def addTasks(title: str, description: str) -> dict[str, Any]:
    conn = openConnection()
    if conn is None:
        print("postTasks failed, conn is None")
        return None

    cursor = conn.cursor()
    cursor.execute("INSERT INTO Task VALUES (%s, %s, %s, %s) RETURNING *", (generate_id(), title, description, False))
    row = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()

    if row is None:
        return None

    return {
            "id": int(row[0]),
            "title": str(row[1]),
            "description": str(row[2]),
            "isDone": bool(row[3])
        }

# 特定のタスクを取得する
def getTask(task_id: int) -> dict[str, Any]:
    conn = openConnection()
    if conn is None:
        print("getTask failed, conn is None")
        return None

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Task WHERE id = %s", (task_id, ))
    row = cursor.fetchone()
    if row is None:
        return None
    cursor.close()
    conn.close()

    return {
            "id": int(row[0]),
            "title": str(row[1]),
            "description": str(row[2]),
            "isDone": bool(row[3])
        }

# 特定のタスクを更新する
def updateTask(task_id: int, request_body: dict[str, Any]) -> dict[str, Any]:
    conn = openConnection()
    if conn is None:
        print("getTask failed, conn is None")
        return False

    cursor = conn.cursor()
    cursor.execute("UPDATE Task SET title = %s, description = %s, isDone = %s WHERE id = %s RETURNING *", (request_body["title"], request_body["description"], request_body["isDone"], task_id))
    row = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    if row is None:
        return None
    return {
            "id": int(row[0]),
            "title": str(row[1]),
            "description": str(row[2]),
            "isDone": bool(row[3])
        }

def upsert_ids(task_id: int):
    conn = openConnection()
    if conn is None:
        print("upsert_ids failed, conn is None")
        return False

    target_ids = []
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Task WHERE id>%s", (task_id,))
    row = cursor.fetchone()
    if row is None:
        return
    while row is not None:
        target_ids.append(int(row[0]))
        row = cursor.fetchone()

    for id in target_ids:
        cursor.execute("UPDATE Task SET id = %s WHERE id = %s", (id-1, id))
    cursor.close()
    conn.commit()
    conn.close()

# 特定のタスクを削除する
def deleteTask(task_id: int) -> bool:
    conn = openConnection()
    if conn is None:
        print("deleteTask failed, conn is None")
        return False

    cursor = conn.cursor()
    cursor.execute("DELETE FROM Task WHERE id = %s", (task_id, ))
    isRowDeleted = cursor.rowcount == 1
    cursor.close()
    conn.commit()
    conn.close()

    if isRowDeleted:
        upsert_ids(task_id)
    return isRowDeleted