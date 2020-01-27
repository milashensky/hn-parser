#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'parser'))

from aiohttp import web
from motor import motor_asyncio as ma

from parser import settings
from parser.views import routes


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    app.client = ma.AsyncIOMotorClient(settings.DB_CLIENT)
    app.db = app.client[settings.DB_NAME]
    PORT = os.environ.get('PORT', 8080)
    web.run_app(app, port=PORT)
