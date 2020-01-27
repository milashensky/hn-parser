#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'parser'))
import time
import requests
import argparse
import asyncio
from contextlib import suppress
from datetime import datetime
from htmldom import htmldom
from motor import motor_asyncio as ma
from parser import settings
from pymongo.errors import DuplicateKeyError


client = ma.AsyncIOMotorClient(settings.DB_CLIENT)
db = client[settings.DB_NAME]
collection = db.posts
collection.create_index('url', unique=True)



async def iteration():
    response = requests.get(settings.URL_TO_PARSE)
    dom = htmldom.HtmlDom().createDom(response.text)
    for row in dom.find('.itemlist tr.athing'):
        data = {}
        title = row.find('.title a')
        data['url'] = title.attr('href')
        data['title'] = title.text().strip()
        data['created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with suppress(DuplicateKeyError):
            await collection.insert_one(data)
    return True


async def handle(timeout, daemon=False):
    if daemon:
        while True:
            print("parse iteration")
            await iteration()
            print("end iteration, sleep")
            await asyncio.sleep(timeout * 60)
    else:
        print("parse once")
        await iteration()
    print("stop parse")
    return True


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--daemon', help='Run as daemon', action='store_true')
parser.add_argument(
    '-t', '--timeout',
    help='Timeout to use in minutes, defaults to {}'.format(settings.DEFAULT_TIMEOUT),
    default=settings.DEFAULT_TIMEOUT, type=int)
args = parser.parse_args()

loop = asyncio.get_event_loop()
print("Run parse with {}m timeout".format(args.timeout))
loop.run_until_complete(handle(args.timeout, args.daemon))
