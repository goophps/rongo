from fastapi import APIRouter

"""
模块路由
在控制器里，可按fastapi官方文档任意使用路由。  只需包含到这儿来即可。
"""
router = APIRouter(
    prefix="/admin",  # 模块名
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

