from fastapi import APIRouter
from .controller import Welcome


"""
模块路由
在控制器里，可按fastapi官方文档任意使用路由。  只需包含到这儿来即可。
"""
router = APIRouter(
    prefix="/index",
    tags=["index"],
    responses={404: {"description": "Not found"}},
)
router.include_router(Welcome.router)
