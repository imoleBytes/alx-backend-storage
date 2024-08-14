#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of the Redis
client as a private variable named _redis (using redis.Redis()) and flush
the instance using flushdb.
Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the input
data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str, bytes,
int or float.
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """ a decorator function to count calls of method"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wraper for deco fn"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs

    In this task, we will define a call_history decorator to store the history
    of inputs and outputs for a particular function.

    Everytime the original function will be called, we will add its input
    parameters to one list in redis, and store its output into another list.

    In call_history, use the decorated function’s qualified name and append
    ":inputs" and ":outputs" to create input and output list keys,
    respectively.
    call_history has a single parameter named method that is a Callable and
    eturns a Callable.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorated function"""
        input_value = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_value)
        output_value = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_value)
        return output_value

    return wrapper


class Cache:
    """An cache of Redis engine"""
    def __init__(self) -> None:
        """initialize an instance of Redis Client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """data is stored to the redis database and a key returned"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)

        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        get method that take a key string argument and an optional
        Callable argument named fn that convert the bytes given
        by redis to the desired type[format]
        """
        v = self._redis.get(key)
        if fn:
            v = fn(v)
        return v

    def get_str(self, key: str) -> str:
        """covert the return value to string of utf-8 format"""
        v = self._redis.get(key)
        v = v.decode("utf-8")
        return v

    def get_int(self, key: str) -> int:
        """covert the return value to int"""
        v = self._redis.get(key)
        try:
            v = int(v.decode("utf-8"))
        except Exception:
            v = 0
        return v


# if __name__ == "__main__":
# This test task 0
#     cache = Cache()

#     data = b"hello"
#     key = cache.store(data)
#     print(key)

#     local_redis = redis.Redis()
#     print(local_redis.get(key))


# Test task 1
    # cache = Cache()

    # TEST_CASES = {
    #     b"foo": None,
    #     123: int,
    #     "bar": lambda d: d.decode("utf-8")
    # }

    # for value, fn in TEST_CASES.items():
    #     key = cache.store(value)
    #     assert cache.get(key, fn=fn) == value
