from fastapi import FastAPI
from .database import Base, engine
from .routers import router
from .auth import router as authRouter

app=FastAPI() #init fastAPI

# Initialize Database's Table 建立資料庫
#Base.metadata.create_all(bind=engine)

#! 註冊router
app.include_router(router=router, prefix="/api", tags=["todos"])
app.include_router(authRouter)