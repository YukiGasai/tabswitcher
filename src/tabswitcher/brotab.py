
import subprocess
import chardet

from .Tab import Tab

def get_tabs(manager):
    output = subprocess.check_output(['bt', '--target', '127.0.0.1:4625', 'list']).decode()
    lines = output.strip().split('\n')
    lines = [line for line in lines if len(line)]
    
    titles = [line.split('\t')[1] for line in lines]

    # Check if there are duplicate titles 
    duplicate_titles = set(title for title in titles if titles.count(title) > 1)

    tabs = {}
    for line in lines:
        id, title, url = line.split('\t')
        # To prevent the same key add the id to dublicate titles 
        if title in duplicate_titles:
            title = f"{id} : {title}"
        tab = Tab(id, title, url, manager)
        tabs[title] = tab
    
    return tabs

def switch_tab(tab_id):
    subprocess.call(['bt', '--target', '127.0.0.1:4625', 'activate', tab_id])

def delete_tab(tab_id):
    subprocess.call(['bt', '--target', '127.0.0.1:4625', 'close', tab_id])


def seach_tab(manager, text):
    _ = subprocess.check_output(['bt', '--target', '127.0.0.1:4625', 'index']).decode()
    output_bytes = subprocess.check_output(['bt', '--target', '127.0.0.1:4625', 'search', text])
        
    if not output_bytes:
        return []
    
    encoding = chardet.detect(output_bytes)['encoding']
    output = output_bytes.decode(encoding)

    lines = output.strip().split('\n')
    lines = [line for line in lines if len(line)]
    
    tabs = []
    for line in lines:
        id, title, content = line.split("\t")
        tab = Tab(id, title, "", manager)
        tabs.append(tab)
    return tabs

def active_tab():
    output = subprocess.check_output(['bt', '--target', '127.0.0.1:4625', 'active']).decode()
    lines = output.strip().split('\n')
    lines = [line for line in lines if len(line)]
    if len(lines) == 0:
        return None
    data = lines[0].split('\t')
    if (len(data) == 5):
        return data[0]
    return None