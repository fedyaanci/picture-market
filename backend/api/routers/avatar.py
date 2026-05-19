from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from api.utils.auth import get_current_user
from core.database_config import get_db
import uuid
from pathlib import Path

router = APIRouter(prefix="/avatar", tags=["avatar"])

AVATAR_DIR = Path("uploads/avatar")
AVATAR_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Разрешены только изображения")

    valid_extensions = {"png", "jpg", "jpeg", "gif", "webp"}
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else "jpg"
    if file_ext not in valid_extensions:
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")

    filename = f"{current_user.id}_{uuid.uuid4().hex}.{file_ext}"
    filepath = AVATAR_DIR / filename

    with open(filepath, "wb") as f:
        f.write(await file.read())

    avatar_url = f"/uploads/avatar/{filename}"
    current_user.avatar_url = avatar_url
    await db.commit()

    return {"avatar_url": avatar_url}
