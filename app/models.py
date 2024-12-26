from sqlalchemy import Column, Integer, String, Boolean, Date
from .database import Base #! 從同資料夾內的main.py引入Base


#定義模型
#從Base繼承基本模型
class Todo(Base):
    __tablename__="todos"

    # column名稱=Column(資料型態, 其他參數)
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String(100), nullable=False) # String(100) 限制字元數量
    description=Column(String, nullable=True)
    complete=Column(Boolean, default=False)
    # below is added on 12-5
    due_date=Column(Date, nullable=True)
    priority=Column(Integer, nullable=False)


class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, nullable=False)
    password=Column(String, nullable=False)
    email=Column(String, unique=True, nullable=False)