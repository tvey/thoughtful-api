import os
import json
import random

from faker import Faker
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

fake = Faker()


def load_data(file_path):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    return data


def make_tags():
    """Write fixture for tags."""
    with open('data/tags.txt') as f:
        tags = f.read().split('\n')

    fixture = []

    for i, tag in enumerate(tags, start=1):
        obj = {
            'model': 'thoughts.tag',
            'pk': i,
            'fields': {'name': tag},
        }
        fixture.append(obj)

    with open('tags.json', 'w') as f:
        json.dump(fixture, f, indent=4)


def make_authors(extra=10):
    """Write fixture for authors, extra - fake authors."""
    authors = [a['name'] for a in load_data('data/authors.json')]

    if extra:
        start_extra = len(authors) + 1  # start id count after base authors
        end_extra = start_extra + extra
        extra_authors = [f'philo{i}' for i in range(start_extra, end_extra)]
        authors += extra_authors

    fixture = []
    for i, author in enumerate(authors, start=1):
        obj = {
            'model': 'auth.user',
            'pk': i,
            'fields': {
                'username': author,
                'password': os.environ.get('HASHED_PASSWORD'),
            },
        }
        fixture.append(obj)

    with open('authors.json', 'w') as f:
        json.dump(fixture, f, indent=4)


def make_thoughts(extra=100):
    """Write fixture for thoughts, extra - fake thoughts by fake authors."""
    authors = load_data('authors.json')
    real_authors = [
        a for a in authors if not a['fields']['username'].startswith('philo')
    ]
    tags = load_data('tags.json')

    thoughts = []

    for author in real_authors:
        name = author['fields']['username']
        author_data = load_data(f'data/thoughts/{name}.json')
        author_thoughts = []

        for thought in author_data:
            real_thought = {
                'author': author,  # dict
                'text': thought['thought'],
                'tags': [
                    tag['pk']
                    for tag in tags
                    for real_tag in thought['tags']
                    if tag['fields']['name'] == real_tag
                ],
            }
            author_thoughts.append(real_thought)
        thoughts += author_thoughts

    if extra:
        fake_thoughts = []

        for _ in range(extra):
            fake_authors = [
                author
                for author in authors
                if author['fields']['username'].startswith('philo')
            ]
            rand_tag_count = random.randint(0, 5)
            tag_pks = [tag['pk'] for tag in tags]
            fake_thought = {
                'author': random.choice(fake_authors),
                'text': fake.sentence(random.randint(5, 20)),
                'tags': [random.choice(tag_pks) for _ in range(rand_tag_count)],
            }
            fake_thoughts.append(fake_thought)
        thoughts += fake_thoughts

    fixture = []
    for i, thought in enumerate(thoughts, start=1):
        is_editable = False
        if thought['author']['fields']['username'].startswith('philo'):
            is_editable = True

        obj = {
            'model': 'thoughts.thought',
            'pk': i,
            'fields': {
                'author': thought['author']['pk'],
                'text': thought['text'],
                'is_editable': is_editable,
                'tags': thought['tags'],
            },
        }
        fixture.append(obj)

    with open('thoughts.json', 'w') as f:
        json.dump(fixture, f, indent=4)


def main():
    make_tags()
    make_authors()
    make_thoughts()


if __name__ == '__main__':
    make_thoughts(extra=200)
