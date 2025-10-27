"""Pre review script: provides review on Pull Requests"""

import sys
import json
import re


EXPECTED_FILE_CHANGED = 'CONTRIBUTORS.md'
ERROR_FILE_WORD = "archived"
README_LINK_MD = '[README.md](https://github.com/zero-to-mastery/start-here-guidelines/blob/master/README.md)'

# ---------------------------------- HELPERS --------------------------------- #
def get_pr_info():
    """Gets changed files into the correct format"""
    _, changed_files, contributor = sys.argv
    changed_files = changed_files.split("\\n")
    return changed_files, contributor

def get_check_patterns(contributor):
    """Provides patterns criterions"""
    expected_url = f"https://github.com/{contributor}"

    # Only match extra params (exclude exact URL)
    param_pattern = rf"{re.escape(expected_url)}/[^\s\)]+"

    # Loose pattern: match either clean or with param (for general detection)
    loose_link_md_pattern = rf"\[\s*@?{re.escape(contributor)}\s*\]\(\s*https://github\.com/{re.escape(contributor)}(?:/[^\s\)]*)?\s*\)"

    # Strict link pattern: matches only clean profile link
    strict_link_md_pattern = rf"\[\s*@{re.escape(contributor)}\s*\]\(\s*{re.escape(expected_url)}\/?\s*\)"


    # List item and full line contexts
    list_item_link_md_pattern = rf"^\s*-\s*\[\s*@?{re.escape(contributor)}\s*\]\(\s*{re.escape(expected_url)}(?:/[^\s\)]*)?\s*\)\s*$"

    strict_line_md_pattern = rf"^\s*-\s*{strict_link_md_pattern}\s*$"


    return {
        "strict": strict_link_md_pattern,
        "loose": loose_link_md_pattern,
        "param": param_pattern,
        "list_item": list_item_link_md_pattern,
        "strict_line": strict_line_md_pattern,
    }

def match_pattern( pattern, content ):
    """Regexp search operation"""
    return re.search(pattern, content, re.IGNORECASE | re.MULTILINE)

def push_feedback(base_message, action_message, review_list, is_inline = False):
    """Format message and push to the provided list"""
    message_separator = "\n\t - " if not is_inline else ' '
    review_list.append(f'- [ ] {base_message}:{message_separator}{action_message}.')

# -------------------------------- LOGIC UTILS ------------------------------- #

def review_insertion( file_content, contributor ):
    """Review CONTRIBUTORS.md for the github author"""
    # Format contributor to lowercase for checks
    contributor = contributor.lower()
    file_content = file_content.lower()
    patterns = get_check_patterns(contributor)

    # Get pattern checks
    link_with_param = patterns["param"]
    loose_link_md_pattern = patterns["loose"]
    list_item_link_md_pattern = patterns["list_item"]
    strict_line_md_pattern = patterns["strict_line"]


    # Loosest to stricter match check 
    has_link_param          = match_pattern( link_with_param, file_content )
    has_md_loose_link       = match_pattern( loose_link_md_pattern, file_content )
    has_md_list_item_link   = match_pattern( list_item_link_md_pattern, file_content )
    has_md_valid_insertion  = match_pattern( strict_line_md_pattern, file_content )

    # Various insertion issues possible
    reviews = []
    if not has_md_valid_insertion:
        # [ CASE ] Param in github link
        if has_md_loose_link and has_link_param:
            base_message = 'Link has extra params'
            action = 'remove the url param from your link'
            push_feedback(base_message, action, reviews)

        # [ CASES ] Link detected but with errors
        if has_md_loose_link:

            # [ CASE ] Text link ( username text ) is missing `@`
            if '@' not in has_md_loose_link.group(0):
                base_message = 'Missing `@` before the github user name'
                action = 'prefix your github name with `@`'
                push_feedback(base_message, action, reviews)

            # [ CASE ] Missing list item markdown bullet
            if not has_md_list_item_link:
                base_message = 'Missing hyphen (`-`) at the start of the line'
                action = 'prepend the line with an hyphen'
                push_feedback(base_message, action, reviews)

        # [ CASES ] Insertion incorrect ( ex wrong protocol https, a typo, ... )
        else:
            base_message = 'Invalid insertion'
            action = 'review your line for any typos'
            push_feedback(base_message, action, reviews, True)

    return reviews

def review_overall_contribution( changed_files ):
    """Checks PR requirements"""

    messages = []

    # [ CASE ] Incorrect changes: missing changes int expected file
    if EXPECTED_FILE_CHANGED not in changed_files:
        push_feedback(
            "Missing required contribution",
            "add your github profile link to the contributors file",
            messages
        )


    # [ CASES ] Incorrect changes detected in other file(s)
    for file in changed_files:
        # other file than CONTRIBUTORS.md touched
        base_message = "Incorrect changes"
        action_message = f"remove any changes in the `{file}` file"

        # "archived file touched"
        if ERROR_FILE_WORD in file:
            push_feedback(base_message, f"archived file:{action_message}", messages)
            break
        elif file != EXPECTED_FILE_CHANGED and file not in messages:
            push_feedback(base_message, action_message, messages)



    # Title list of review
    if messages:
        messages = [
            f"> [!TIP] \n> _You can refer to {README_LINK_MD} for additional guidance._",
            "\n ## Overall feedback",
            *messages
        ]

    return messages or []

def review_contributors_file( changed_files, contributor ):
    """Reads CONTRIBUTORS.md file and checks insertion in CONTRIBUTORS.md"""
    if EXPECTED_FILE_CHANGED not in changed_files:
        return []


    # Gets file content
    content = ''
    with open(EXPECTED_FILE_CHANGED, 'r', encoding = 'utf-8') as f:
        content =  f.read()
    
    reviews = review_insertion( content, contributor )

    if reviews:
        reviews = [
            f'## `{EXPECTED_FILE_CHANGED}` addition feedback',
            '> [!TIP]',
            '> Check how others set their links to adjust yours if needed',
            *reviews
        ]

    return reviews or []

# -------------------------------- MAIN LOGIC -------------------------------- #
def run():
    """Main code"""
    changed_files, contributor = get_pr_info()

    # Feedback for other files changes
    overall_reviews = review_overall_contribution(changed_files)
 
    # Feedback regarding the expected line insertion
    insertion_reviews = review_contributors_file(changed_files, contributor)

    reviews = [*overall_reviews, *insertion_reviews]
    if reviews:
        reviews =  [
            "\nBefore we can merge your PR, address the bellow feedback.",
            '\n'.join([*overall_reviews, *insertion_reviews])
        ]
    else:
        reviews = [
            "\n🎉 Your submission meets all pre-review requirements!",
            "It’s now awaiting final validation from a maintainer."
        ]

    messages = [
        f"Aloha @{contributor} 🙌",
        "Thanks for your contribution!",
        *reviews
    ]
    message = '\n'.join(messages)
    print(message)

run()
