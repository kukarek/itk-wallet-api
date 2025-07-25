from fastapi import APIRouter

from src.api.v1.endpoints import auth, wallet

api_router = APIRouter()
api_router.include_router(wallet.router)
api_router.include_router(auth.router)
