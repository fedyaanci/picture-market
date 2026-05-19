from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# ← Все импорты СТРОГО вверху!
from api.routers.test import router as test_router
from api.routers.user import router as user_router
from api.routers.artworks import router as artworks_router
from api.routers.listing import router as listing_router
from api.routers.order import router as order_router
from api.routers.avatar import router as avatar_router
from api.routers.purchase import router as purchase_router

app = FastAPI(title="API app", swagger_ui_parameters={"persistAuthorization": True})

# === 📦 СТАТИКА: отдача картинок ===
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# 🔥 Абсолютный путь: считаем от ЭТОГО файла (api.py лежит в backend/api/)
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"  # → backend/uploads
UPLOADS_DIR.mkdir(exist_ok=True)

# Монтируем: /uploads/* → файлы в backend/uploads/*
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
# === КОНЕЦ БЛОКА ===



app.include_router(test_router)
app.include_router(user_router)
app.include_router(artworks_router)
app.include_router(listing_router)
app.include_router(order_router)
app.include_router(avatar_router)
app.include_router(purchase_router)
