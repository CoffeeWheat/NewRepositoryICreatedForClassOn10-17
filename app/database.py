from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base #建立資料庫的工具
from sqlalchemy.orm import sessionmaker #把模型變成object


# database
DATABASE_URL="sqlite:///./todos.db"
Base=declarative_base()
engine=create_engine(DATABASE_URL, connect_args={"check_same_thread":False})#建立資料庫連線
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
