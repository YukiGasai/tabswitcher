from .Settings import Settings

# Gets colors by selected theme for ui components 

settings = Settings()
def getTextColor():
    if(settings.get_dark_mode()):
        return "#ffffff"
    return "#161618"

def getBackgroundColor():
    if(settings.get_dark_mode()):
        return "#161618"
    return "#ffffff"

def getSelectedColor():
    if(settings.get_dark_mode()):
        return "#818181"
    return "#818181"

def getWindowBackgroundColor():
    if(settings.get_show_background()):
        if(settings.get_dark_mode()):
            return "#121212"
        return "#dddddd"
    return "transparent"

def getPlaceholderColor():
    if(settings.get_dark_mode()):
        return "#8a8a8b"
    return "#8a8a8b"