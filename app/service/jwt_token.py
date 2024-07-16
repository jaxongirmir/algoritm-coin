from os import getenv
from datetime import datetime, timedelta
from typing import Any, Optional


from jose import jwt, ExpiredSignatureError
from fastapi import HTTPException, status

SECRET_KEY = getenv("SECRET_KEY")


class TokenMixin:
    id: Any

    async def generate_token(self) -> str:
        # "exp": datetime.now() + timedelta(seconds=expires_in),
        payload = {
            "sub": str(self.id),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")  # type: ignore
        return token

    async def verify_token(self, token: str) -> Optional[bool]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # type: ignore
            self.id = payload["sub"]
            return True
        except ExpiredSignatureError:
            raise HTTPException(
                detail="Qaytadan kiring", status_code=status.HTTP_401_UNAUTHORIZED
            )
