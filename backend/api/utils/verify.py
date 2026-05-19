from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 🔥 bcrypt обрезает пароль до 72 байт — делаем это явно, чтобы избежать ошибки
    truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
    return pwd_context.verify(truncated_password, hashed_password)

def get_password_hash(password: str) -> str:
    # То же самое при хешировании новых паролей
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)