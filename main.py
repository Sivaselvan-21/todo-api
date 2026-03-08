from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

todos = []
counter = 1

class Todo(BaseModel):
    title: str
    done: Optional[bool] = False

@app.get("/todos")
def get_todos():
    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos")
def create_todo(todo: Todo):
    global counter
    new_todo = {"id": counter, "title": todo.title, "done": todo.done}
    todos.append(new_todo)
    counter += 1
    return {"message": "Todo created", "todo": new_todo}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    for t in todos:
        if t["id"] == todo_id:
            t["title"] = todo.title
            t["done"] = todo.done
            return {"message": "Updated", "todo": t}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return {"message": "Deleted"}