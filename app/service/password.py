from typing import Any, Dict, List, ByteString
from bcrypt import hashpw, gensalt, checkpw


from pydantic import SecretStr


class PasswordMixin:
    _password: Any
    password: SecretStr

    async def hach_password(self):
        self._password = hashpw(
            self.password.get_secret_value().encode("utf-8"), gensalt()
        )

    async def check_password(self, password: SecretStr) -> bool:
        return checkpw(password.get_secret_value().encode("utf-8"), self._password)
