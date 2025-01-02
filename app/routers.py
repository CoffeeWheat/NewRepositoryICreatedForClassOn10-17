from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session #把模型變成object

# from .main import app <- 這樣會出錯
from .schemas import TodoCreate, TodoResponse
from .models import Todo
from .database import SessionLocal
from .auth import getCurrentUser


router = APIRouter()


#database injection 讓API保持與DB的連線
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


#api devoloping
@router.post("/todos", response_model=TodoResponse)
def create_todo(
        todo: TodoCreate,
        db: Session=Depends(get_db),
        current_user: dict = Depends(getCurrentUser)):
    db_todo=Todo(**todo.dict()) #建立物件
    db.add(db_todo, ) #寫入資料庫
    db.commit() #真正寫入資料庫
    db.refresh(db_todo) #更新資料庫
    return db_todo #回傳結果

#取得多個資料 用List
@router.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session=Depends(get_db)):
    return db.query(Todo).all()

#取得單個資料 用todo_id判斷
@router.get("/todo/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session=Depends(get_db)):
    db_todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    return db_todo

#更新
@router.put("/todo/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: Session=Depends(get_db)):
    db_todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

#刪除
@router.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, db: Session=Depends(get_db)):
    db_todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail":"Todo deleted successfully"}