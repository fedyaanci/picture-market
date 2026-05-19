from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
