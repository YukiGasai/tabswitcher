import subprocess
from fuzzywuzzy import process, fuzz

# This is the better idea to use a python fzf but it is not working as good
def scorer(query, choice):
    if choice.startswith(query):
        return 100
    else:
        return fuzz.ratio(query, choice)

def fuzzy_search_py(query, choices):
    if not query:
        return []
    results = process.extract(query, choices, limit=10, processor=lambda x: x.lower())
    results = [result[0] for result in results if result[1] > 30]
    return results

# This is not so nice as it requres fzf to be installed but it just works so good
def fuzzy_search_cmd(query, choices):
    if not query:
        return []
    process = subprocess.Popen(['fzf', '-f', query, '-m', '10'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = process.communicate('\n'.join(choices).encode())
    results = stdout.decode().strip().split('\n')
    return results