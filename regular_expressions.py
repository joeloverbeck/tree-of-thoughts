import re


def extract_vote(text):
    pattern = r"best answer is number (\d+)"
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))

    return None
