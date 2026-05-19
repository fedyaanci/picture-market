from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

Base = declarative_base()

load_dotenv()  # загрузить данные из .env файла

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)  # должны поместить туда значение DATABASE_URL(которое в файле)

engine = create_async_engine(
    DATABASE_URL
)  # создает асинхронное подключение (async await)

SessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)  # для созданий сессий бд с предуставнеовленными настройками


async def get_db():
    async with SessionLocal() as session:
        yield session
