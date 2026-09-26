from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3


app = FastAPI()


# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Pydantic models
# -----------------------------

class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


class TodoCreate(BaseModel):
    title: str
    description: str


class TodoUpdate(BaseModel):
    completed: bool


# -----------------------------
# Database connection
# -----------------------------

def get_connection():
    connection = sqlite3.connect("todos.db")
    connection.row_factory = sqlite3.Row
    return connection


# -----------------------------
# Initialize database
# -----------------------------

def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    connection.commit()
    connection.close()


initialize_database()


# -----------------------------
# Home endpoint
# -----------------------------

@app.get("/")
def home():
    return {"message": "Todo API is running"}


# -----------------------------
# GET all todos
# -----------------------------

@app.get("/todos", response_model=list[Todo])
def get_todos():
    connection = get_connection()

    cursor = connection.execute(
        "SELECT * FROM todos ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    connection.close()

    todos_list = []

    for row in rows:
        todo = Todo(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            completed=bool(row["completed"])
        )

        todos_list.append(todo)

    return todos_list


# -----------------------------
# POST - create a new todo
# -----------------------------

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO todos (title, description, completed)
        VALUES (?, ?, ?)
        """,
        (todo.title, todo.description, 0)
    )

    connection.commit()

    todo_id = cursor.lastrowid

    connection.close()

    return Todo(
        id=todo_id,
        title=todo.title,
        description=todo.description,
        completed=False
    )


# -----------------------------
# PUT - complete/uncomplete todo
# -----------------------------

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE todos
        SET completed = ?
        WHERE id = ?
        """,
        (int(todo.completed), todo_id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Todo not found")

    cursor = connection.execute(
        """
        SELECT * FROM todos
        WHERE id = ?
        """,
        (todo_id,)
    )

    row = cursor.fetchone()

    connection.close()

    return Todo(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        completed=bool(row["completed"])
    )
