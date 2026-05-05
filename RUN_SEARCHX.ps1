# SEARCHX - Master Start Script
# Runs the Full Functional Stack: Flask Backend + Expo Mobile Frontend

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         SEARCHX: Legal Document Search Engine              " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Start Flask Backend
Write-Host "[1/2] Starting Flask Backend (REST API)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command 'cd backend; python app.py'"

# 2. Start Expo Mobile App
Write-Host "[2/2] Starting React Native Mobile Frontend (Expo)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command 'cd mobile_app; npx expo start -c'"

Write-Host "------------------------------------------------------------" -ForegroundColor Green
Write-Host "Done! Services are starting in separate windows." -ForegroundColor Green
Write-Host "Check the console output for any errors."
Write-Host "------------------------------------------------------------" -ForegroundColor Green
