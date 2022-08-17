from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def Welcome():
    return 'welcome to here'


