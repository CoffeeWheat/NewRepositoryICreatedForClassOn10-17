from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base #建立資料庫的工具
from sqlalchemy.orm import sessionmaker, Session #把模型變成object

app=FastAPI() #init fastAPI

# database
DATABASE_URL="sqlite:///./todos.db"
Base=declarative_base()
engine=create_engine(DATABASE_URL, connect_args={"check_same_thread":False})#建立資料庫連線
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)


#定義模型
#從Base繼承基本模型
class Todo(Base):
    __tablename__="todos"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    description=Column(String, nullable=True)
    complete=Column(Boolean, default=False)

# Initialize Database's Table 建立資料庫
Base.metadata.create_all(bind=engine)



#資料驗證
class TodoBase(BaseModel):
    title:str
    description:str | None=None #None=None 代表可以填空白值
    complete: bool=False

#建立的格式
class TodoCreate(TodoBase):
    pass

#回傳的格式
class TodoResponse(TodoBase):
    id:int

    class Config:
        from_attributes=True

#database injection 讓API保持與DB的連線
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


#api devoloping
@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session=Depends(get_db)):
    db_todo=Todo(**todo.dict()) #建立物件
    db.add(db_todo) #寫入資料庫
    db.commit() #真正寫入資料庫
    db.refresh(db_todo) #更新資料庫
    return db_todo #回傳結果

#取得多個資料 用List
@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session=Depends(get_db)):
    return db.query(Todo).all()

#取得單個資料 用todo_id判斷
@app.get("/todo/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session=Depends(get_db)):
    db_todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    return db_todo

#更新
@app.put("/todo/{todo_id}", response_model=TodoResponse)
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
@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, db: Session=Depends(get_db)):
    db_todo=db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail":"Todo deleted successfully"}