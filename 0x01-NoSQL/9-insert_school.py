#!/usr/bin/env python3
"""
Write a Python function that inserts a new document in a collection
based on kwargs:

Prototype: def insert_school(mongo_collection, **kwargs):
mongo_collection will be the pymongo collection object
Returns the new _id
"""


def insert_school(mongo_collection, **kwargs):
    """insert a new documents in the given collection"""
    return mongo_collection.insert(kwargs)
