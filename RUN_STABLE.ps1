
# TOTAL CLEANUP
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# ENSURE SPACE IS CLEARED ON C: (Temporary files only)
Remove-Item $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue

# REDIRECT TO D:
$env:TEMP = "D:\SEARCHX_TEMP"
$env:TMP = "D:\SEARCHX_TEMP"
$env:npm_config_cache = "D:\NPM_CACHE"
mkdir D:\SEARCHX_TEMP -ErrorAction SilentlyContinue
mkdir D:\NPM_CACHE -ErrorAction SilentlyContinue

# 1. RUN BACKEND
Start-Process powershell -ArgumentList "-NoExit -Command cd d:\SEARCHX\backend; python app.py"

# 2. RUN FRONTEND (LAN Mode - ensure same Wi-Fi)
cd d:\SEARCHX\mobile_app
npm cache clean --force
npm start
