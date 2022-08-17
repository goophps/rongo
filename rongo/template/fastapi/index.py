from fastapi import FastAPI
from config.router import router


run = FastAPI()
# 自动加载所有路由
run.include_router(router)



