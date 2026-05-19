"""
Точка входа в backend-приложение PictureMarket.

Запускает FastAPI-сервер с подключёнными роутерами,
CORS, статическими файлами и middleware.
"""

import uvicorn
from api.api import app
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import os

UPLOADS_DIR = Path(__file__).parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# asyncio.run(LoadArtworksBegin())

# asyncio.run(seed_artworks_without_listing())
