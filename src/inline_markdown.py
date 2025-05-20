import re

#nested [] are considered for the alt text
def extract_markdown_images(markdown_text):
    return re.findall(r"!\[(.*?)\]\(([^\(\)]*)\)", markdown_text)
#nested [] are considered for the link text
def extract_markdown_links(markdown_text):
    return re.findall(r"(?<!!)\[(.*?)\]\(([^\(\)]*)\)", markdown_text)

def extract_title(markdown):
    lines = markdown.split('\n')
    lines_with_hash = list(filter(lambda line: line.startswith('# '), lines))
    lines_stripped = list(map(lambda line: line.strip(), lines_with_hash))
    if len(lines_stripped) > 0:
        title = lines_stripped[0][2:]
        return title
    else:
        raise Exception('No h1 header in markdown')