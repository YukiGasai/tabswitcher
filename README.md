# TabSwitcher

TabSwitcher is a simple window for switching between tabs in a browser. It uses the [brotab](https://github.com/balta2ar/brotab) CLI and browser extensions as a foundation.

## Requirements

- Python 3.7 or higher
- BroTab Extension installed in your browser
  - [Firefox](https://addons.mozilla.org/de/firefox/addon/brotab/)
  - [Chrome](https://chromewebstore.google.com/detail/brotab/mhpeahbikehnfkfnmopaigggliclhmnc)
- [fzf](https://github.com/junegunn/fzf) (optional, but recommended for enhanced search)

## Installation

1. Install the TabSwitcher package via pip:

```bash
pip install tabswitcher
```

2. Install the active tab logger task

```bash
tabswitcher --install
```

3. Restart the browser

When using Ubuntu some extra setup is required.

```bash
sudo apt-get install qtbase5-dev libxcb-xinerama0
```

## Usage

Upon opening TabSwitcher, your most recently active tabs will be displayed in the list.

Typing in the input field will initiate a fuzzy search of all your open tabs by title.

You can focus a tab by clicking an item in the list.

Holding Shift while clicking will also bring the browser window into focus.

You can also navigate using Arrow Keys, Tab and Enter.

Tabs can also be selected using the keyboard shortcuts Ctrl + 1-9.

Holding Shift while using these shortcuts will also bring the browser window into focus.

Pressing Backspace on a selected Tab will close it.

### Special Input

Starting a input wiht `>` will search the html code of you open tabs for the input.

Starting a input with `#` will display your bookmarks instead of open tabs.

Starting a input with `?` will open a new tab with the input text in a Google search.

Starting a input with `!` will attempt to open a new tab with the website page (requires a [Redirect Extension](https://addons.mozilla.org/de/firefox/addon/skip-redirect/)).

`Ctrl + ,` will open the settings file.

`Ctrl + q` or `Escape` will close the window.

## Known Issues

- Currently, TabSwitcher only supports Windows and limited on Ubuntu.
