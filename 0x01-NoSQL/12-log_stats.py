#!/usr/bin/env python3
"""
Write a Python script that provides some stats about Nginx logs
stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the method =
["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
You can use this dump as data sample: dump.zip

get dump.zip like this:
curl -o dump.zip -s "https://s3.amazonaws.com/intranet-projects-files/\
    holbertonschool-webstack/411/dump.zip"
and then unzip dump.zip
and then
mongorestore dump
"""
from pymongo import MongoClient


def main():
    """main function starts here"""

    client = MongoClient()
    db = client['logs']

    x = db.nginx.count_documents({})

    print(x, 'logs')
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        count = db.nginx.count_documents({
            "method": method
        })
        print(f"\tmethod {method}: {count}")

    status_count = db.nginx.count_documents({
        "method": "GET",
        "path": "/status"
    })
    print(f"{status_count} status check")


if __name__ == "__main__":
    main()
