PATH = 'CONTRIBUTORS.md'

def get_contents(path):
    with open(path, 'r') as f:
        contents = f.read().splitlines()
    return contents

def get_contributor_lines(contents):
    lines = []
    for line in contents:
        if line != '' and line != '# CONTRIBUTORS':
            lines.append(line)
    return lines

def get_user_list(lines):
    username_list = []
    for line in lines:
        username_chars = []
        start_chars = ['-', ' ', '[', '@']
        for letter in line:
            if letter not in start_chars:
                if letter == ']':
                    break
                username_chars.append(letter)
        username = ''.join(username_chars)
        username_list.append(username)
    return username_list

def get_url_list(lines):
    url_list = []
    for line in lines:
        url_chars = []
        copy_state = False
        for letter in line:
            if letter == '(':
                copy_state = True
                continue
            elif letter == ')':
                break
            if copy_state:
                url_chars.append(letter)
        url = ''.join(url_chars)
        url_list.append(url)
    return url_list

def create_user_dict(user_list, url_list):
    user_info = {}
    for i in range(len(user_list)):
        # Store usernames as lowercase to ensure case-insensitive duplicate removal
        user_info[user_list[i].lower()] = url_list[i]
    return user_info

def sort_users(user_dict):
    with open(PATH, 'w') as f:
        f.write('# CONTRIBUTORS\n\n')
        # Sort the dictionary keys in a case-insensitive manner
        for user in sorted(user_dict.keys(), key=str.lower):
            entry = f'- [@{user}]({user_dict[user]})\n\n'
            f.write(entry)

def remove_dupes(user_dict):
    # Remove duplicates and normalize username casing
    unique_users = {}
    for user, url in user_dict.items():
        # Title case for usernames in the final output for consistency
        unique_users[user.title()] = url
    return unique_users

contents = get_contents(PATH)
contrib_lines = get_contributor_lines(contents)
user_list = get_user_list(contrib_lines)
url_list = get_url_list(contrib_lines)
user_dict = create_user_dict(user_list, url_list)
user_dict_filtered = remove_dupes(user_dict)
sort_users(user_dict_filtered)
