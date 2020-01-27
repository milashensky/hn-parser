import os


DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', '27017')
DB_NAME = os.environ.get('DB_NAME', 'posts')

DB_CLIENT = 'mongodb://{host}:{port}/{name}'.format(host=DB_HOST, port=DB_PORT, name=DB_NAME)

URL_TO_PARSE = 'https://news.ycombinator.com/news'
DEFAULT_TIMEOUT = 60
