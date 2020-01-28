from aiohttp import web
from datetime import datetime

from parser import settings

routes = web.RouteTableDef()


@routes.view('/posts')
async def posts(request):
    ordering = request.rel_url.query.get('order')
    offset = abs(int(request.rel_url.query.get('offset', None) or 0))
    limit = abs(int(request.rel_url.query.get('limit', None) or 0))
    if not limit:
        limit = await request.app.db.posts.count_documents({})
    direction = 1
    cursor = request.app.db.posts.find()
    if ordering and ordering.startswith('-'):
        direction = -1
        ordering = ordering[1:]
    if ordering in ['title', 'url', 'id', 'created']:
        if ordering == 'id':
            ordering = '_id'
        cursor.sort(ordering, direction)
    cursor.skip(offset)
    res = await cursor.to_list(length=limit)
    cursor.close()
    return web.json_response(list(map(lambda x: {'id': str(x.pop('_id')), 'created': datetime.fromtimestamp(x.pop('created')).strftime(settings.DATETIME_FORMAT), **x}, res)))
