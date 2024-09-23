import re

PATH = 'CONTRIBUTORS.md'

def get_contents(path):
    with open(path, 'r') as f:
        return f.read().splitlines()

def get_contributor_lines(contents):
    return [line for line in contents if line and line != '# CONTRIBUTORS']

def extract_user_data(lines):
    user_info = {}
    for line in lines:
        match = re.match(r'\s*-\s*\[(.*?)\]\((.*?)\)', line)
        if match:
            username, url = match.groups()
            user_info[username.strip('@').title()] = url
    return user_info

def sort_users(user_dict):
    with open(PATH, 'w') as f:
        f.write('# CONTRIBUTORS\n\n')
        for user in sorted(user_dict.keys()):
            entry = f'- [@{user}]({user_dict[user]})\n'
            f.write(entry)

contents = get_contents(PATH)
contrib_lines = get_contributor_lines(contents)
user_dict = extract_user_data(contrib_lines)
sort_users(user_dict)
