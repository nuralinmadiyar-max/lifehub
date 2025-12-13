from datetime import datetime, timedelta
from jose import jwt

from passlib.context import CryptContext
import hashlib

# ====== НАСТРОЙКИ ======
SECRET_KEY = "super-secret-key"  # для тестов нормально
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ====== PASSWORD ======
def hash_password(password: str) -> str:
    """
    bcrypt имеет лимит 72 байта, поэтому
    сначала делаем sha256
    """
    sha = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha)


def verify_password(password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.verify(sha, hashed_password)


# ====== JWT ======
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt