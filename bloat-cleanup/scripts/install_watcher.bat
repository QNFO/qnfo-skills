@echo off
:: DeepChat SYSTEM Admin Watcher — one-time installer
:: Creates a scheduled task that runs every 60 seconds as SYSTEM
:: After this runs, use trigger_admin.ps1 to queue admin commands without admin.
::
:: USAGE: Run this file directly (will trigger UAC prompt)
:: This is the ONLY time admin/UAC is needed.
::
:: After installation:
::   powershell -File trigger_admin.ps1 -KillBloat
::   powershell -File trigger_admin.ps1 -DisableServices

set "WATCHER_SCRIPT=%~dp0admin_watcher.ps1"
set "QUEUE_DIR=%USERPROFILE%\.deepchat\admin_queue"

mkdir "%QUEUE_DIR%" 2>nul

:: Delete old watcher if exists
schtasks /delete /tn "DC_Watcher" /f 2>nul

:: Create permanent SYSTEM watcher that runs every 60 seconds
:: Key: /ru SYSTEM /rl HIGHEST — this is what makes it autonomous
schtasks /create ^
    /tn "DC_Watcher" ^
    /tr "powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"%WATCHER_SCRIPT%\"" ^
    /sc minute /mo 1 ^
    /ru SYSTEM /rl HIGHEST ^
    /f

if %ERRORLEVEL% equ 0 (
    echo ========================================
    echo   DC_Watcher installed successfully!
    echo   Runs every 60s as SYSTEM
    echo   Queue dir: %QUEUE_DIR%
    echo ========================================
    
    :: Quick test: write a signal
    echo {"id":"install_test_%RANDOM%","commands":[{"type":"test","message":"Watcher installed and active"}]} > "%QUEUE_DIR%\test.signal"
    echo   Test signal written — check for test.done in 60s
    
    timeout /t 3 >nul
) else (
    echo ERROR: Failed to create scheduled task.
    echo Run this file as Administrator (right-click, Run as Administrator)
    pause
)
