"""Count most popular tags from scraped quotes."""

import json
from collections import Counter


def load_author_thoughts(author_name):
    with open(f'thoughts/{author_name}.json', encoding='utf-8') as f:
        thoughts = json.load(f)
    return thoughts


def get_tags(thoughts):
    tags = []

    for thought in thoughts:
        tags.extend(thought['tags'])

    return tags


def count_tags():
    with open('authors.json') as f:
        authors = [author['name'] for author in json.load(f)]

    all_tags = []

    for author in authors:
        thoughts = load_author_thoughts(author)
        tags = get_tags(thoughts)
        all_tags += tags

    counter = Counter(all_tags)
    common_tags = [i[0] for i in counter.most_common() if i[1] > 3]

    with open('tags.txt', 'w') as f:
        f.write('\n'.join(common_tags))


if __name__ == '__main__':
    count_tags()
