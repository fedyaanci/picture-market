"""
Скрипт для загрузки демо-данных в базу при первом запуске.
Не запускать на проде!
"""

from sqlalchemy import select
from models.user import User
from models.category import Category
from core.database_config import SessionLocal

CATEGORIES = [
    "Портрет",
    "Пейзаж",
    "Абстракция",
    "Фэнтези",
    "Минимализм",
    "Реализм",
    "Сюрреализм",
    "Комиксы",
    "Цифровая живопись",
    "3D-арт",
]


async def LoadDataToTable(obj):
    async with SessionLocal() as session:
        try:
            existing_count = await session.execute(select(User))
            if existing_count.scalars().first() is not None:
                print("Уже загружено")
                return

            for name in CATEGORIES:
                category = Category(name=name)
                session.add(category)

            await session.commit()
            print(f"Успешно добавлено {len(CATEGORIES)} категорий.")

        except Exception as e:
            print(f"Ошибка при загрузке категорий: {e}")
            await session.rollback()
            raise


async def DownloadUsers():
    try:
        async with SessionLocal() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users
    except Exception as e:
        print(f"Ошибка при получении пользователей: {e}")
        return None


# asyncio.run(LoadDataToTable(CATEGORIES))

# async def main():
# users = await DownloadUsers()

# if users:
#     for user in users:
#         print(f"ID: {user.id}, Username: {user.username}, Is Artist: {user.is_artist}")


# asyncio.run(main())
