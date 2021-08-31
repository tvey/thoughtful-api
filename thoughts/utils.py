from django.conf import settings
from django.urls import URLPattern, URLResolver


def get_patterns(urlpatterns, acc=None):
    if acc is None:
        acc = []
    if not urlpatterns:
        return
    entry = urlpatterns[0]
    if isinstance(entry, URLPattern):
        yield acc + [str(entry.pattern)]
    elif isinstance(entry, URLResolver):
        yield from get_patterns(entry.url_patterns, acc + [str(entry.pattern)])
    yield from get_patterns(urlpatterns[1:], acc)


def print_urls(url_patterns, depth=0):
    for entry in url_patterns:
        print("  " * depth, entry.pattern)
        if hasattr(entry, 'url_patterns'):
            print_urls(entry.url_patterns, depth + 1)
