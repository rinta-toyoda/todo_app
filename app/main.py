from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel

import database

class RequestTask(BaseModel):
    title: str | None = None
    description: str | None = None
    isDone: bool = False

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # どのオリジンからでもアクセスを許可
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETEなど
    allow_headers=["*"],  # 任意のヘッダーを許可
)

# タスク一覧
@app.get("/api/v1/tasks")
def get_tasks():
    tasks = database.getTasks()
    return JSONResponse(content=tasks, status_code=status.HTTP_200_OK)

# タスク追加
@app.post("/api/v1/tasks")
def create_task(reqTask: RequestTask):
    task = database.addTasks(reqTask.title, reqTask.description)
    return JSONResponse(content=task, status_code=status.HTTP_201_CREATED)

# タスク取得
@app.get("/api/v1/tasks/{id}")
def get_task(id: int):
    task = database.getTask(id)
    if task is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=task, status_code=status.HTTP_200_OK)

# タスク更新
@app.put("/api/v1/tasks/{id}")
def update_task(id: int, reqTask: RequestTask):
    task = database.updateTask(id, {"title": reqTask.title, "description": reqTask.description, "isDone": reqTask.isDone})
    if task is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=task, status_code=status.HTTP_200_OK)

# タスク削除
@app.delete("/api/v1/tasks/{id}")
def update_task(id: int):
    isSuccess = database.deleteTask(id)
    if not isSuccess:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
