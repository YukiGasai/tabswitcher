Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd.exe /c tabswitcher --startlogger", 0, True
Set WshShell = Nothing