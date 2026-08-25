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


contributor_links = read_contributors_file()
contributors = create_contributor_data(contributor_links)
print(contributor_links)
print(contributors)

