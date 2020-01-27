#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'parser'))

import argparse
import asyncio
from motor import motor_asyncio as ma
from parser import settings
from parser.parser import iteration


client = ma.AsyncIOMotorClient(settings.DB_CLIENT)
db = client[settings.DB_NAME]
collection = db.posts
collection.create_index('url', unique=True)


async def handle(timeout, daemon=False):
    if daemon:
        while True:
            print("parse iteration")
            await iteration(collection)
            print("end iteration, sleep")
            await asyncio.sleep(timeout * 60)
    else:
        print("parse once")
        await iteration(collection)
    print("stop parse")
    return True


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--daemon', help='Run as daemon', action='store_true')
parser.add_argument(
    '-t', '--timeout',
    help='Timeout to use in minutes, defaults to {}'.format(settings.DEFAULT_TIMEOUT),
    default=settings.DEFAULT_TIMEOUT, type=int)


if __name__ == '__main__':
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    print("Run parse with {}m timeout".format(args.timeout))
    loop.run_until_complete(handle(args.timeout, args.daemon))
