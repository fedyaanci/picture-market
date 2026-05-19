Write-Host "🚀 Запуск PictureMarket..." -ForegroundColor Cyan

if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Папка venv не найдена. Сначала выполни: .\setup.ps1" -ForegroundColor Red
    exit
}

Write-Host " Запуск Backend (порт 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { .\venv\Scripts\Activate.ps1; uvicorn backend.main:app --reload --port 8000 }"

Start-Sleep -Seconds 3

Write-Host "Запуск Frontend (Flet)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { .\venv\Scripts\Activate.ps1; flet run frontend/main.py }"

Write-Host "Готово! Откроются два окна терминала. Backend: http://localhost:8000" -ForegroundColor Green