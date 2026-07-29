@echo off
:: ============================================================
:: DEEPCHAT BUDGET-LAPTOP 3-DAY PRUNE + RESTART (v2.5)
:: For laptops with <=8GB RAM / tight C: drive.
:: 3-day cutoff + VACUUM. Estimated reclaim varies.
:: ============================================================

set "SKILL_DIR=%~dp0.."
set "DC_EXE=C:\Users\LENOVO\AppData\Local\Programs\DeepChat\DeepChat.exe"
set "QUEUE_DIR=%USERPROFILE%\.deepchat\admin_queue"

echo.
echo ============================================================
echo   DEEPCHAT BUDGET-LAPTOP 3-DAY PRUNE v2.5
echo   %date% %time%
echo ============================================================
echo.

:: [0/6] Admin operations
echo [0/6] Queuing admin operations...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SKILL_DIR%\scripts\trigger_admin.ps1" -KillBloat -DisableServices
timeout /t 65 /nobreak >nul
echo        Done.

:: [1/6] Kill DeepChat
echo [1/6] Killing DeepChat...
taskkill /F /IM DeepChat.exe >nul 2>&1
taskkill /F /IM rtk.exe >nul 2>&1
timeout /t 5 /nobreak >nul
echo        Done.

:: [2/6] Budget prune (3-day cutoff + VACUUM + RAM-tuned PRAGMAs)
echo [2/6] Budget laptop prune (3-day cutoff)...
python "%SKILL_DIR%\scripts\agent_db_prune.py" --budget --vacuum
echo        Exit: %ERRORLEVEL%

:: [3/6] Disk cleanup
echo [3/6] Cleaning disk caches...
python "%SKILL_DIR%\scripts\clean_disk.py"
echo        Done.

:: [4/6] Clean WAL/SHM
echo [4/6] Cleaning WAL/SHM...
set "DB=%APPDATA%\DeepChat\app_db\agent.db"
if exist "%DB%-wal" del /f "%DB%-wal" 2>nul
if exist "%DB%-shm" del /f "%DB%-shm" 2>nul
echo        Done.

:: [5/6] Results
echo [5/6] Results:
python -c "import shutil,os; u=shutil.disk_usage('C:'); print(f'  C: {u.free/1024**3:.1f}GB free ({u.free/u.total*100:.1f}%%)'); db=r'%APPDATA%\DeepChat\app_db\agent.db'; print(f'  agent.db: {os.path.getsize(db)/1024**3:.2f}GB' if os.path.exists(db) else '  agent.db: MISSING')"

:: [6/6] Restart
echo [6/6] Restarting DeepChat...
if exist "%DC_EXE%" (
    start "" "%DC_EXE%"
    echo        Launched.
) else (
    echo        ERROR: %DC_EXE% not found
)

echo.
echo ============================================================
echo   BUDGET PRUNE COMPLETE
echo ============================================================
pause
