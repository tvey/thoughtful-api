"""Scrape quotes of selected authors from Goodreads."""

import json
import random
import asyncio

from requests_html import AsyncHTMLSession

BASE_URL = 'https://www.goodreads.com/author/quotes/'

with open('authors.json') as f:
    authors = json.load(f)


async def get_response(asession, url):
    """Get url with async session and return the HTMLResponse."""
    r = await asession.get(url)

    sleep_time = random.random() * 2
    await asyncio.sleep(sleep_time)
    return r


async def gather(urls):
    """Gather tasks."""
    asession = AsyncHTMLSession()
    tasks = (get_response(asession, url) for url in urls)
    return await asyncio.gather(*tasks)


def get_author_thoughts(r) -> list:
    """Collect necessary data from the 1st page of author's quotes."""
    print(r.url)
    thoughts = []
    quote_elems = r.html.find('.quote')

    for quote_elem in quote_elems:
        quote_text_raw = quote_elem.find('.quoteText', first=True)
        quote_text = quote_text_raw.text.split('”\n― ')[0].strip(' “')
        tags_elem = quote_elem.find('.smallText.left a')
        tags = [a.text for a in tags_elem] if tags_elem else []
        thought = {
            'thought': quote_text,
            'tags': tags,
        }
        thoughts.append(thought)

    return thoughts


def main(responses) -> None:
    """Write files for every author; responses are ordered."""

    for author, r in zip(authors, responses):
        thoughts = get_author_thoughts(r)
        name = author['name']

        with open(f'thoughts/{name}.json', 'w', encoding='utf-8') as f:
            json.dump(thoughts, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    urls = [BASE_URL + author['goodreads_slug'] for author in authors]
    responses = asyncio.run(gather(urls))
    main(responses)
