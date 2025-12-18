from datetime import timedelta
import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..schemas.entities import AuthRequest, AuthResponse
from ..security.jwt import create_jwt

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


@router.post("/token", response_model=AuthResponse)
async def login(
    credentials: AuthRequest, session: AsyncSession = Depends(get_session)
) -> AuthResponse:
    # Placeholder logic; replace with real credential validation
    if credentials.password != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login")

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_jwt({"sub": credentials.email, "role": "admin"}, expires)
    return AuthResponse(access_token=token, role="admin")
