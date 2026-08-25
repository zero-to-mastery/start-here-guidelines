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


contributor_links = read_contributors_file()
print(contributor_links)
