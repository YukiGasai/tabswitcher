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


:: Insatll the mediator in the browser
call bt install

:: Get the User ID
for /f "tokens=1* delims= " %%i in ('whoami /user /fo list ^| findstr /B /C:"SID:"') do set "UserID=%%j"

echo "User ID: %UserID%"

for /f "tokens=* USEBACKQ" %%F in (`powershell -Command "(Get-Command tabswitcher).Source"`) do (
   SET commandPath=%%F
)

:: Create a scheduled task to run the Tabswitcher Logger
echo Creating scheduled task for Tabswitcher Logger
set "XML_PATH=%SCRIPT_DIR%/tabswitcher_service.xml"

:: Update the Command and User ID in the XML file
powershell -Command "$xml = [xml](Get-Content '%XML_PATH%'); $xml.Task.Actions.Exec.Command = '%commandPath%'; $xml.Task.Principals.Principal.UserId = '%UserID%'; $xml.Save('%XML_PATH%')"

:: Create the scheduled task
schtasks /Create /XML "%XML_PATH%" /TN "Tabswitcher Logger"

:: Start the Tabswitcher Logger task
echo Starting Tabswitcher Logger
schtasks /Run /TN "Tabswitcher Logger"
