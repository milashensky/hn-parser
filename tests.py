# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from motor import motor_asyncio as ma

from parser.parser import iteration
from parser import settings
from parser.views import routes


class PostsApiTest(AioHTTPTestCase):

    async def get_application(self):
        app = web.Application()
        settings.DB_NAME = 'tests_parser'
        app.add_routes(routes)
        app.client = ma.AsyncIOMotorClient(settings.DB_CLIENT)
        app.client.drop_database(settings.DB_NAME)
        app.db = app.client[settings.DB_NAME]
        await app.db.posts.insert_one({'title': '1 test', 'url': 'http://test.com/1', 'created': 1580151926})
        await app.db.posts.insert_one({'title': '2 test', 'url': 'http://test.com/2', 'created': 1580171926})
        return app

    @unittest_run_loop
    async def test_posts_get(self):
        resp = await self.client.request("GET", "/posts")
        assert resp.status == 200
        resp = await resp.json()
        assert len(resp) is 2

    @unittest_run_loop
    async def test_posts_limit(self):
        resp = await self.client.request("GET", "/posts?limit=1")
        assert resp.status == 200
        resp = await resp.json()
        assert len(resp) is 1

    @unittest_run_loop
    async def test_posts_ordering(self):
        resp = await self.client.request("GET", "/posts?limit=1&order=title")
        assert resp.status == 200
        resp = await resp.json()
        assert '1 test' in resp[0].get('title')
        resp = await self.client.request("GET", "/posts?limit=1&order=-title")
        assert resp.status == 200
        resp = await resp.json()
        assert '2 test' in resp[0].get('title')

    @unittest_run_loop
    async def test_parser(self):
        collection = self.app.db[settings.DB_NAME].test_posts
        count = await collection.count_documents({})
        assert count is 0
        await iteration(collection)
        count = await collection.count_documents({})
        assert count is 30
