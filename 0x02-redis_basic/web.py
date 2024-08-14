#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching.

Bonus: implement this use case with decorators.
"""
import redis
import requests
from functools import wraps


r = redis.Redis()


def access_count(method):
    """this decorates the get_page function"""
    @wraps(method)
    def wrapper(url):
        """wrapper"""
        key = f"cached:{url}"
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        key_count = f"count:{url}"
        content = method(url)

        # this increment count:url by 1, anf if it does not exists,
        # it initialize it by 1
        r.incr(key_count)
        r.set(key, content)
        r.expire(key, 10)
        return content
    return wrapper


@access_count
def get_page(url: str) -> str:
    """obtain the HTML content of a particular"""
    data = requests.get(url)
    return data.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
