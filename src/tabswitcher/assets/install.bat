@echo off

set "SCRIPT_DIR=%~dp0"

:: Check for administrator privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "%*", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:: Create a scheduled task to run the BroTab Service
echo Creating scheduled task for BroTab Service
set "XML_PATH=%SCRIPT_DIR%/brotab_service.xml"
schtasks /Create /XML "%XML_PATH%" /TN "BroTab Service"

:: Start the BroTab Service task
echo Starting BroTab Service
schtasks /Run /TN "BroTab Service"

:: Create a scheduled task to run the Tabswitcher Logger
echo Creating scheduled task for BroTab Service
set "XML_PATH=%SCRIPT_DIR%/tabswitcher_service.xml"
schtasks /Create /XML "%XML_PATH%" /TN "Tabswitcher Logger"

:: Start the Tabswitcher Logger task
echo Starting Tabswitcher Logger
schtasks /Run /TN "Tabswitcher Logger"