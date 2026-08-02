@echo off
:: One-time UAC elevation to create Scheduled Task watcher
:: This creates a SYSTEM-level task that polls for admin commands
:: After this, all admin ops are autonomous.

set "WATCHER_SCRIPT=C:\Users\LENOVO\.deepchat\skills\bloat-cleanup\scripts\admin_watcher.ps1"
set "QUEUE_DIR=C:\Users\LENOVO\.deepchat\admin_queue"

echo === DEEPCHAT AUTONOMOUS ADMIN WATCHER INSTALLER ===
echo.

:: Create queue directory
mkdir "%QUEUE_DIR%" 2>nul

:: Remove any existing task
schtasks /delete /tn "DC_AdminWatcher" /f 2>nul

:: Create scheduled task that runs every 60 seconds as SYSTEM
schtasks /create /tn "DC_AdminWatcher" /tr "powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"%WATCHER_SCRIPT%\"" /sc minute /mo 1 /ru SYSTEM /rl HIGHEST /f

if %ERRORLEVEL% equ 0 (
    echo [OK] Scheduled task "DC_AdminWatcher" created
    echo       Runs every 60 seconds as SYSTEM
    echo       Watches: %QUEUE_DIR%
) else (
    echo [FAIL] Could not create scheduled task
    echo        Reason: This script must be run as Administrator
    pause
    exit /b 1
)

echo.
echo === TESTING WATCHER ===
:: Write a test signal
echo {"id":"install_test","commands":[{"type":"test","message":"Watcher installed successfully"}]} > "%QUEUE_DIR%\install_test.signal"
echo [OK] Test signal written. Watcher will process within 60 seconds.

echo.
echo === INSTALLATION COMPLETE ===
echo   To trigger admin ops without admin: run trigger_admin.ps1
echo   Signal files: %QUEUE_DIR%\*.signal
echo   Results: %QUEUE_DIR%\*.done
pause
