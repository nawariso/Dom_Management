from typing import Iterable, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from .jwt import decode_jwt

security = HTTPBearer(auto_error=False)


class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        authorization: Optional[str] = request.headers.get("Authorization")
        user = None

        if authorization and authorization.lower().startswith("bearer "):
            token = authorization.split()[1]
            try:
                payload = decode_jwt(token)
                user = {"email": payload.get("sub"), "role": payload.get("role", "tenant")}
            except Exception:  # noqa: BLE001
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )

        request.state.user = user
        response = await call_next(request)
        return response


def require_roles(roles: Iterable[str]):
    async def dependency(
        credentials: HTTPAuthorizationCredentials = Depends(security), request: Request | None = None
    ) -> dict:
        _ = credentials
        if request is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request not available")

        user = getattr(request.state, "user", None)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")

        if user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")

        return user

    return dependency
