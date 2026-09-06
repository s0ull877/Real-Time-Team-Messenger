from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router
from .rooms import router as room_router


rttm_routers = [
    auth_router,
    user_router,
    room_router
]

rttm_router = APIRouter()

for router in rttm_routers:
    rttm_router.include_router(router)

__all__ = ["rttm_router"]