@echo off
echo === DEEPCHAT ADMIN WATCHER INSTALLER ===
echo.

set "QUEUE=%USERPROFILE%\.deepchat\admin_queue"
mkdir "%QUEUE%" 2>nul

:: 1. Kill stubborn processes
echo [1] Killing processes...
taskkill /F /IM OfficeClickToRun.exe 2>nul && echo   KILLED OfficeClickToRun || echo   OfficeClickToRun not running
taskkill /F /IM MSPCManagerService.exe 2>nul && echo   KILLED MSPCManagerService || echo   MSPCManagerService not running

:: 2. Stop and disable services
echo [2] Stopping services...
sc stop ClickToRunSvc 2>&1 | findstr /i "STOP_PENDING STOPPED SUCCESS"
sc config ClickToRunSvc start= disabled 2>&1 | findstr /i "SUCCESS"
sc failure ClickToRunSvc reset= 86400 actions= "" 2>&1 | findstr /i "SUCCESS"

:: 3. Create permanent SYSTEM watcher
echo [3] Installing DC_Watcher...
schtasks /delete /tn DC_Watcher /f 2>nul
schtasks /create /tn DC_Watcher /tr "powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"C:\Users\LENOVO\.deepchat\skills\bloat-cleanup\scripts\admin_watcher.ps1\"" /sc minute /mo 1 /ru SYSTEM /rl HIGHEST /f

if %ERRORLEVEL% equ 0 (
    echo   SUCCESS: DC_Watcher installed
    
    :: Test signal
    echo {"id":"install_test_%RANDOM%","commands":[{"type":"test","message":"Watcher active %date% %time%"}]} > "%QUEUE%\startup_test.signal"
    echo   Test signal written
) else (
    echo   FAILED to create watcher task
)

echo.
echo === DONE ===
pause
