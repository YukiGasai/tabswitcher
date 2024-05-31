import subprocess
from fuzzyfinder import fuzzyfinder

def fuzzy_search_py(query, choices):
    if not query:
        return []
    query = query.strip()
    results = fuzzyfinder(query.lower(), choices)
    return list(results)[:10]

# This is not so nice as it requres fzf to be installed but it just works so good
def fuzzy_search_cmd(query, choices):
    if not query:
        return []
    process = subprocess.Popen(['fzf', '-f', query, '-m', '10'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = process.communicate('\n'.join(choices).encode())
    results = stdout.decode().strip().split('\n')
    return results