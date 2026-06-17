@echo off
chcp 65001 >nul 2>&1
title Dog Doctor Server

echo ============================================
echo   Dog Doctor - Starting Backend Server...
echo ============================================
echo.

:: Auto-detect project directory (wherever this .bat file is located)
set "PROJECT_DIR=%~dp0"
:: Remove trailing backslash
if "%PROJECT_DIR:~-1%"=="\" set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

echo [INFO] Project directory: %PROJECT_DIR%
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo [ERROR] Please install Python 3.11+ from https://www.python.org/downloads/
    goto end
)

:: Check if port 8000 is already in use
netstat -ano | findstr ":8000 " | findstr "LISTENING" >nul 2>&1
if %errorlevel%==0 (
    echo [INFO] Port 8000 is already in use - server may already be running.
    echo [INFO] Opening browser...
    start http://localhost:8000
    goto end
)

:: Check if dependencies are installed
echo [INFO] Checking dependencies...
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Dependencies not installed!
    echo [INFO] Installing from requirements.txt...
    echo.
    pip install -r "%PROJECT_DIR%\requirements.txt"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies!
        echo [ERROR] Please run manually: pip install -r requirements.txt
        goto end
    )
    echo.
    echo [INFO] Dependencies installed successfully!
    echo.
)

:: Start the backend server
start "Dog Doctor Backend" /min cmd /c "cd /d "%PROJECT_DIR%\backend" && python main.py"

echo.
echo Waiting for server to start...
echo.

:: Wait for server to be ready (max 60 seconds)
set /a count=0
:wait_loop
if %count% gtr 60 goto timeout
timeout /t 1 /nobreak >nul 2>&1
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8000/api/health' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop; exit 0 } catch { exit 1 }" >nul 2>&1
if %errorlevel%==0 goto ready
set /a count+=1
echo Waiting... (%count%/60^)
goto :wait_loop

:ready
echo.
echo ============================================
echo   Server is ready!
echo   Opening browser at http://localhost:8000
echo ============================================
start http://localhost:8000
goto end

:timeout
echo.
echo [!] Server did not respond within 60 seconds.
echo [!] It may still be starting up. Opening browser anyway...
start http://localhost:8000

:end
echo.
echo Press any key to exit this window...
pause >nul
