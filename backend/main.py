
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, select
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./todos.db")
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def initialize_db():
    await create_tables()

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class TodoCreate(BaseModel):
    title: str
    completed: bool = False

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

app = FastAPI()

# CORS Middleware
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://todo-app-fastapi-react-git-main-arielll74s-projects.vercel.app/", 
    "https://todo-app-fastapi-0lea.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_startup():
    await initialize_db()

# Dependency to get the database session
async def get_db():
    async with SessionLocal() as db:
        yield db

@app.get("/todos/", response_model=List[dict])
async def read_todos(skip: int = 0, limit: int = 10, completed: bool | None = None, db: AsyncSession = Depends(get_db)):
    query = select(Todo)
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    result = await db.execute(query.offset(skip).limit(limit))
    todos = result.scalars().all()
    return [{"id": todo.id, "title": todo.title, "completed": todo.completed} for todo in todos]

@app.post("/todos/", response_model=dict)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return {"id": db_todo.id, "title": db_todo.title, "completed": db_todo.completed}

@app.get("/todos/{todo_id}", response_model=dict)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).filter(Todo.id == todo_id))
    todo = result.scalars().first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"id": todo.id, "title": todo.title, "completed": todo.completed}

@app.put("/todos/{todo_id}", response_model=dict)
async def update_todo(todo_id: int, todo: TodoUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).filter(Todo.id == todo_id))
    db_todo = result.scalars().first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    await db.commit()
    await db.refresh(db_todo)
    return {"id": db_todo.id, "title": db_todo.title, "completed": db_todo.completed}

@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).filter(Todo.id == todo_id))
    todo = result.scalars().first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    await db.delete(todo)
    await db.commit()
    return {"message": "Todo deleted"}