@echo off
REM Auto-Mute Watchdog with Sleep/Wake Handling
REM This script monitors auto_mute and restarts it if the system wakes from sleep
REM or if the process crashes

setlocal enabledelayedexpansion

set "SCRIPT_PATH=C:\Auto-Mute"
set "PYTHON_EXE_PATH=%SCRIPT_PATH%\.venv\Scripts\pythonw.exe"
set "PYTHON_EXE_FALLBACK=pythonw.exe"
set "PROCESS_NAME=pythonw.exe"
set "LOG_FILE=%SCRIPT_PATH%\watchdog.log"

REM Create log file in temp location if script directory is not writable
if not exist "%LOG_FILE%" (
    set "LOG_FILE=%TEMP%\auto_mute_watchdog.log"
)

echo [%date% %time%] Watchdog started >> "%LOG_FILE%" 2>nul

:loop
REM Check if pythonw.exe (auto_mute) is running
tasklist /FI "IMAGENAME eq %PROCESS_NAME%" 2>NUL | find /I "%PROCESS_NAME%" >NUL
set "IS_RUNNING=!ERRORLEVEL!"

if "!IS_RUNNING!"=="0" (
    REM Process is running, wait and check again
    timeout /t 30 /nobreak >nul
    goto loop
) else (
    REM Process is not running, restart it
    echo [%date% %time%] Auto-Mute process not found, restarting... >> "%LOG_FILE%" 2>nul
    cd /d "%SCRIPT_PATH%"
    
    REM Determine which Python to use
    if exist "%PYTHON_EXE_PATH%" (
        set "PYTHON_TO_USE=%PYTHON_EXE_PATH%"
    ) else (
        set "PYTHON_TO_USE=%PYTHON_EXE_FALLBACK%"
    )
    
    REM Start the script directly without virtual environment issues
    start "" /B "%PYTHON_TO_USE%" "%SCRIPT_PATH%\auto_mute.py" --tray >nul 2>&1
    
    if !ERRORLEVEL! neq 0 (
        echo [%date% %time%] Failed to start Auto-Mute. Using fallback python... >> "%LOG_FILE%" 2>nul
        start "" /B python "%SCRIPT_PATH%\auto_mute.py" --tray >nul 2>&1
    )
    
    echo [%date% %time%] Restarted Auto-Mute >> "%LOG_FILE%" 2>nul
    
    REM Wait a bit before checking again
    timeout /t 10 /nobreak >nul
    goto loop
)
