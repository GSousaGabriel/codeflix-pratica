import os
import jwt
import dotenv
import time

dotenv.load_dotenv()

class JwtGenerator:
    def encode_jwt(self):
        encoded_jwt = jwt.encode(
          {
            "exp": int(time.time()) + 3600,
            "aud": "account",
            "typ": "Bearer",
            "azp": "codeflix-frontend",
            "acr": "1",
            "realm_access": {
              "roles": [
                "offline_access",
                "uma_authorization",
                "admin",
                "default-roles-codeflix"
              ]
            },
          },
            os.getenv("TEST_PRIVATE_KEY").replace("\\n", "\n"),
            algorithm="RS256",
        )
        
        self.encoded_jwt = encoded_jwt
        
    def decode_jwt(self):
        decoded_jwt = jwt.decode(
            self.encoded_jwt,
            os.getenv("TEST_PUBLIC_KEY"),
            algorithms=["RS256"],
            audience="account"
        )
        
        self.decoded_jwt = decoded_jwt