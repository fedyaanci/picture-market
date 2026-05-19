import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

load_dotenv()
DB_URL = os.getenv("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql+psycopg2://")
if not DB_URL:
    raise SystemExit("DATABASE_URL не найден в .env")

backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.core.database_config import Base
from backend.models.user import User
from backend.models.artwork import Artwork
from backend.models.listing import Listing

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def seed():
    with Session() as db:
        if db.query(User).first():
            print("База уже заполнена. Пропускаю.")
            return

        print(" Создаю таблицы и генерирую данные...")
        Base.metadata.create_all(bind=engine)

        # Покупатель
        buyer = User(username="test_buyer", password_hash=pwd_context.hash("test123"), balance=5000.0, is_artist=False)
        db.add(buyer)
        db.flush()

        # 3 Художника
        artists_names = ["fedya", "petya", "huilo"]
        artists = [User(username=n, password_hash=pwd_context.hash("artist123"), balance=0.0, is_artist=True) for n in artists_names]
        db.add_all(artists)
        db.flush()

        # 15 работ + листинги
        listing_counter = 0
        for artist in artists:
            for j in range(5):
                listing_counter += 1
                #  Онлайн-картинки: работают у любого без скачивания файлов
                img_url = f"https://picsum.photos/seed/picturemarket_{listing_counter}/400/300"
                
                artwork = Artwork(title=f"Работа #{listing_counter}", image_url=img_url, artist_id=artist.id)
                db.add(artwork)
                db.flush()

                is_sold = (listing_counter <= 5)
                listing = Listing(artwork_id=artwork.id, seller_id=artist.id, price=round(800 + (listing_counter * 120), 2), is_sold=is_sold)
                db.add(listing)

        db.commit()
        print("Готово!")
        print("Покупатель: test_buyer | Пароль: test123 | Баланс: 5000₽")
        print("Художники: fedya, petya, huilo | Пароль: artist123")
        print("Листингов: 15 (5 продано). Картинки подгрузятся автоматически.")

if __name__ == "__main__":
    seed()