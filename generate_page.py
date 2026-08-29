import re

CONTRIBUTORS_PATH = './CONTRIBUTORS.md'
INDEX_PATH = './index.html'
REPLACER = '[__CONTENT__]'

MAIN_COLOR = '#4c0ffb'
SECONDARY_COLOR = '#c4094d'

# Reads the CONTRIBUTORS.md files
def read_contributors_file(contributor_path = CONTRIBUTORS_PATH):
    '''
    Reads the CONTRIBUTORS.md files
    '''
    with open(contributor_path, encoding='utf-8') as f:
        text = f.read()
        contributor_links = re.split(r'[\[\]\(\)\s(\n|\n-)]', text)
        contributor_links = list(
            filter(
                lambda x: len(x) > 1 and x.startswith('https'),
                contributor_links)
            )
        f.close()
    return contributor_links

# Extracts and set contributor info data  ( github handle + link + avatar)
def create_contributor_data(links):
    '''
    Extracts and set contributor info data  ( github handle + link + avatar)
    :param links: list of string
    '''
    contributors = list()
    for link in links:
        segments = [segment for segment in re.split(r'/', link) if segment]
        handler = segments[-1]
        contributor = {
            'handler': handler,
            'link': link,
            'avatar': f'https://avatars.githubusercontent.com/{handler}?size=120'
        }
        contributors.append(contributor)
    return contributors

# Create html list items
def create_list_items(contributors):
    """
    Creates html list items
    :param contributors: list 
    """
    list_items = list()
    for contributor in contributors:
        ui_link = "".join(re.split(r'https://|.com|/$', contributor["link"]))
        badge_css = (
            "inline-flex items-center rounded-full px-2 py-1 "
            f"text-xs font-medium text-[{MAIN_COLOR}]/40 "
            f"bg-[{MAIN_COLOR}]/10  inset-ring inset-ring-gray-400/20"
        )

        li = '<li class="relative isolate flex justify-around bg-white h-20 w-80 rounded-lg shadow hover:scale-102 duration-100 ease-in-out">'
        li +=   f'<a href="{contributor["link"]}" target="_blank" class="flex w-full rounded-md justify-around bg-white">'
        li +=     '<div class="flex w-full items-center gap-5 p-4">'
        li +=       '<div class="flex w-full gap-4">'
        li +=           f'<img class="brightness-110 rounded-full h-12 w-12" src="{contributor["avatar"]}" loading="lazy"/>'
        li +=           '<div class="flex flex-col justify-center">'
        li +=               '<h2 class="capitalize text-x1 font-bold">'
        li +=                   f'{contributor["handler"]}'
        li +=               '</h2>'
        li +=               f'<span class="{badge_css}">'
        li +=                   f'{ui_link}'
        li +=               '</span>'
        li +=           '</div>'
        li +=       '</div>'
        li +=      '</div>'
        li +=   '</a>'
        li += '</li>'
        list_items.append(li)
    return list_items


def read_index(index_path=INDEX_PATH):
    '''
    Reads index file
    :param index_path: index.html path
    '''
    with open(index_path, encoding="utf-8") as f:
        html = f.read()
    return html

# Generates content to replace [__CONTENT__] ( with ul, li )
def create_html_content():
    '''
    Generates content to replace [__CONTENT__] ( with ul, li )
    '''

    # Content data
    contributor_links = read_contributors_file()
    contributors = create_contributor_data(contributor_links)

    # HTML content creation
    contributor_list_items = create_list_items(contributors)
    contributor_count = len(contributor_list_items)

    # HTML list content ( ul + li )
    html_content = f'<span title="Currently {contributor_count} contributors" class="text-sm mb-6 flex justify-center italic text-[{SECONDARY_COLOR}]">({contributor_count})</span>'
    html_content += '<ul loading="lazy" class="flex flex-wrap gap-1.5 w-fill justify-center">'
    for li in contributor_list_items:
        html_content += li
    html_content += '</ul>'

    return html_content

# Create page and inject ul and li items
def generate_page(index_path = INDEX_PATH):
    '''
    Create page and inject ul and li items
    :param index_path: index path for html
    '''
    bg_css = (
        "[background-image:repeating-linear-gradient("
        "to_bottom_left,"
        "#090d16_0%,"
        "#581c87_25%,"
        "#1e1b4b_50%,"
        "#090d16_75%"
        ")]"
    )
    base = (
    '<!DOCTYPE html>'
    '<html lang="en">'
    '<head>'
        '<meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Nunito:ital,wght@0,200..1000;1,200..1000&display=swap" rel="stylesheet">'
        '<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>'
        '<title>Contributors</title>'
    '</head>'
    f'<body style="font-family: Nunito" class="text-[{MAIN_COLOR}]">'
        f'<main class="flex flex-col justify-center {bg_css} max-w-screen px-20 py-50">'
        f'<h1 class="relative flex justify-center text-6xl font-extrabold text-[{SECONDARY_COLOR}] text-shadow-md" style="font-family: Montserrat">• Contributors •</h1>'
            '[__CONTENT__]'
        '</main>'
    '</body>'
    )

    contributor_ul = create_html_content()
    base = base.replace(REPLACER, contributor_ul)

    with open(index_path, 'w') as f:
        f.write(base)
        f.close()


if __name__ == '__main__':
    generate_page()