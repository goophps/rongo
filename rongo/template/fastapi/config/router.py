from fastapi import APIRouter
import app.index.router
import app.admin.router
"""
总路由
新增模块时，需把模块路由包含进来(app目录里，比如admin是一个模块，index是一个模块)
每个模块对应一个router.py文件
"""
router = APIRouter()
router.include_router(app.index.router.router)
router.include_router(app.admin.router.router)
