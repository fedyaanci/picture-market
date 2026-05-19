# PictureMarket
> Маркетплейс цифрового искусства. Бэкенд на FastAPI, фронтенд на Flet, БД PostgreSQL.  
> Полный цикл: каталог, фильтрация, покупка, профили художников, рейтинги.

##  Стек
| Компонент | Технологии |
|-----------|------------|
| **Backend** | FastAPI, SQLAlchemy (Async), Uvicorn, Passlib+Bcrypt, Python-Jose |
| **Frontend** | Flet (Python UI framework) |
| **Database** | PostgreSQL |
| **Dev/Tools** | Faker, Picsum (демо-картинки), PowerShell scripts |

## Требования
- Python 3.10+
- **PostgreSQL** (должен быть запущен локально, порт `5432`)
- Git

## Быстрый старт (Windows)

### 1. Клонирование и настройка окружения.
```powershell
git clone https://github.com/ТВОЙ_НИК/picturemarket.git
cd picturemarket
.\setup.ps1
```
### 2. Настройка подключения к БД.
Откройте файл .env в корне проекта и укажите ваши данные PostgreSQL:

```env
DATABASE_URL=postgresql+asyncpg://postgres:ВАШ_ПАРОЛЬ@localhost:5432/picturemarket
SECRET_KEY=your_super_secret_key_change_this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Затем надо локально создать бд
```
psql -U postgres -c "CREATE DATABASE picturemarket;"
```
### 3. Заполнение тестовыми данными.

```powershell
python seed_db.py
```

### 4. Запуск приложения 

```
.\start.ps1
```