from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import hashlib

# ====== JWT CONFIG ======
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ====== PASSWORD ======
def hash_password(password: str) -> str:
    """
    bcrypt limit = 72 bytes
    sha256().digest() = 32 bytes → безопасно
    """
    sha_bytes = hashlib.sha256(password.encode()).digest()
    return pwd_context.hash(sha_bytes)


def verify_password(password: str, hashed_password: str) -> bool:
    sha_bytes = hashlib.sha256(password.encode()).digest()
    return pwd_context.verify(sha_bytes, hashed_password)


# ====== JWT ======
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)