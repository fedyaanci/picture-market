import asyncio
from core.database_config import engine, Base


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Все таблицы созданы")


if __name__ == "__main__":
    asyncio.run(init())
