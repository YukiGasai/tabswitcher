import platform
import subprocess

class WindowFoundException(Exception):
    pass

# The helper function that allows to focus a windwo by title reliable at least on windows 11
def focus_window(title):
    try:
        if platform.system() == "Windows":
            import win32con
            import win32gui
            from pynput.keyboard import Controller, Key

            kbd = Controller()

            # Check if the window title starts with the given title
            def window_enum_callback(hwnd, data):
                if win32gui.GetWindowText(hwnd).startswith(data):
                    raise WindowFoundException(hwnd)

            # Find the window with the given title (starts with)
            def find_window_startswith(title):
                try:
                    win32gui.EnumWindows(window_enum_callback, title)
                except WindowFoundException as ex:
                    return ex.args[0]
                return None

            # Focus the window
            hwnd = find_window_startswith(title)

            # If the window is the TabSwitcher, we need to press alt to focus it properly
            if title == "TabSwitcher":
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                kbd.press(Key.alt)
            try:
                win32gui.SetForegroundWindow(hwnd)
            finally:
                if title == "TabSwitcher":
                    kbd.release(Key.alt)
        else:
            subprocess.call(['xdotool', 'search', '--name', title, 'windowactivate'])
    except Exception as e:
        print("Error in focus_window: " + str(e))