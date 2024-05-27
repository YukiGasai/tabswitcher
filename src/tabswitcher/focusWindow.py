import os
import subprocess

def focus_window(title):
    try:
        if os.name == 'nt':
            subprocess.call(['powershell', '-Command', f'$wshell = New-Object -ComObject wscript.shell; $wshell.AppActivate("{title}")'])
        elif os.name == 'posix':
            subprocess.call(['xdotool', 'search', '--name', title, 'windowactivate'])
    except:
        pass