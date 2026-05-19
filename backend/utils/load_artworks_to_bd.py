from core.database_config import SessionLocal
from models.artwork import Artwork
from models.listing import Listing
from sqlalchemy import select

ARTWORK_TITLES = [
    "CosmicCat",
    "DancingRobot",
    "MistyForest",
    "NeonCity",
    "DragonPortrait",
    "AbstractSunset",
    "CloudDreams",
    "CyberSamurai",
    "DeepOcean",
    "FantasyLibrary",
]

EXTRA_ARTWORKS = ["SilentMoon", "ElectricFlower", "NeonDragon"]


async def LoadArtworksBegin():
    async with SessionLocal() as session:
        try:
            existing = await session.execute(select(Artwork).limit(1))

            if existing.scalars().first() is not None:
                return

            artist_id = 38

            for i, title in enumerate(ARTWORK_TITLES):
                artwork = Artwork(
                    title=title.replace(" ", "_"),
                    image_url=f"/uploads/artworks/{title}.jpg",
                    artist_id=artist_id,
                )
                session.add(artwork)
                await session.flush()

                listing = Listing(
                    artwork_id=artwork.id,
                    seller_id=artist_id,
                    price=100.0 + i * 50,
                    is_sold=False,
                )
                session.add(listing)

                await session.commit()

                print("Творчество загружено!")
        except Exception as e:
            print(f"Ошибка: {e}")
            await session.rollback()
            raise


async def seed_artworks_without_listing():
    async with SessionLocal() as session:
        try:
            existing = await session.execute(
                select(Artwork).where(Artwork.title.in_(EXTRA_ARTWORKS))
            )
            if existing.scalars().first():
                print("Дополнительные арты уже существуют")
                return

            artist_id = 38

            for title in EXTRA_ARTWORKS:
                artwork = Artwork(
                    title=title,
                    image_url=f"/uploads/artworks/{title}.jpg",
                    artist_id=artist_id,
                )
                session.add(artwork)

            await session.commit()
            print(f"Добавлено {len(EXTRA_ARTWORKS)} артов БЕЗ листингов")

        except Exception as e:
            print(f"Ошибка: {e}")
            await session.rollback()
            raise
