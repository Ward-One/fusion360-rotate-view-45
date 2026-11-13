@echo off
setlocal

set "SOURCE=%~dp0rotate_view_45deg"
set "DEST=%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\rotate_view_45deg"

echo ========================================================
echo  Installing rotate_view_45deg Add-In for Fusion 360...
echo ========================================================

if not exist "%SOURCE%" (
    echo [ERROR] Could not find the "rotate_view_45deg" folder next to this installer.
    pause
    exit /b 1
)

if exist "%DEST%" (
    echo Removing previous version...
    rmdir /s /q "%DEST%"
)

xcopy "%SOURCE%" "%DEST%\" /E /I /Y >nul

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Add-in installed to:
    echo %DEST%
    echo.
    echo Next steps in Fusion 360:
    echo  1. Press Shift + S to open Scripts and Add-Ins.
    echo  2. Go to the Add-Ins tab and select "rotate_view_45deg".
    echo  3. Check "Run on startup" and click "Run".
) else (
    echo [ERROR] Installation failed. Please check folder permissions.
)

echo.
pause
