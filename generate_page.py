import re
CONTRIBUTORS_PATH = './CONTRIBUTORS.md'

# Reads CONTRIBUTORS files and get links only
def read_contributors_file():
    with open(CONTRIBUTORS_PATH) as f:
        text = f.read()
        contributor_links = re.split(r'[\[\]\(\)\s(\n|\n-)]', text)
        contributor_links = list(
            filter(
                lambda x: len(x) > 1 and x.startswith('https'),
                contributor_links)
            )
        f.close();
    return contributor_links

# Extract and set contributor info data  ( github handle + link + avatar)
def create_contributor_data(links):
    contributors = list()
    for link in contributor_links:
        handler = re.split(r'//?', link)[-1]
        contributor = {
            'handler': handler,
            'link': link,
            'avatar': f'https://github.com/{handler}.png'
        }
        contributors.append(contributor)
    return contributors

# Create html list items
def create_list_items(contributors):
    list_items = list()
    for contributor in contributors:
        li = '<li><div>'
        li += f'<div><image src="{contributor["avatar"]}"/>'
        li += f'<h2>{contributor["handler"]}</h2>'
        li += '<div/>'
        li += '<div class="separator"></div>'
        li += '<span class="color-grey-100"></span>'
        li += '<div/></li>'
        print(li)
        list_items.append(li)
    return list_items
contributor_links = read_contributors_file()
contributors = create_contributor_data(contributor_links)
contributor_list_items = create_list_items(contributors)

print(contributor_list_items)

