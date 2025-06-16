import os
import dotenv
from src.core._shared.infrasctructure.auth_interface import AuthServiceInterface
import jwt

dotenv.load_dotenv()

class JwtAuthService(AuthServiceInterface):
    def __init__(self, token: str = "") -> None:
        raw_public_key = os.getenv("AUTH_PUBLIC_KEY")
        self.public_key = f"-----BEGIN PUBLIC KEY-----\n{raw_public_key}\n-----END PUBLIC KEY-----"
        self.token = token.replace("Bearer ", "", 1)
        
    def _decode_token(self) -> dict:
        try:
            return jwt.decode(
                self.token,
                self.public_key,
                algorithms=["RS256"],
                audience="account"
            )
        except jwt.PyJWTError:
            return {}
        
    def is_authenticated(self) -> bool:
        return bool(self._decode_token())
    
    def has_role(self, role: str) -> bool:
        return role in self._decode_token().get("realm_access", {}).get("roles", [])