#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'parser'))
import asyncio

from aiohttp import web
from motor import motor_asyncio as ma

from parser import settings
from parser.views import routes


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = web.Application()
    app.add_routes(routes)
    app.client = ma.AsyncIOMotorClient(settings.DB_CLIENT)
    app.db = app.client[settings.DB_NAME]
    web.run_app(app)
