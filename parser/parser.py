import requests
from contextlib import suppress
from datetime import datetime
from htmldom import htmldom
from pymongo.errors import DuplicateKeyError
from parser import settings


async def iteration(collection):
    response = requests.get(settings.URL_TO_PARSE)
    dom = htmldom.HtmlDom().createDom(response.text)
    for title in dom.find('.itemlist tr.athing .title a.storylink'):
        data = {}
        data['url'] = title.attr('href')
        data['title'] = title.text().strip()
        data['created'] = int(datetime.now().timestamp())
        with suppress(DuplicateKeyError):
            await collection.insert_one(data)
    return True
