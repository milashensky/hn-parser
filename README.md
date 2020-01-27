# hn-parser


Parses https://news.ycombinator.com/news with setted interval and provides endpoint with results


## Setup

```
pip install -Ur ./requirements/base.txt
```
or you can use docker-compose
```
docker-compose up
```

## Run parser

```
python ./parse.py -d -t 10
```

will run parser of https://news.ycombinator.com/news as daemon with an interval of 10 minutes

## Run api

```
python ./main.py
```
Will provide endpoint `/posts` with parsed pages.
Supports ordering (asc and desc), offset and limit.

###Ordering
```
localhost:8080/posts?order=title

```
will return all posts, ordered by title.
Ordering supports `id`, `url`, `title` and `created` fields.


Desc ordering:
```
localhost:8080/posts?order=-title

```

###Limiting

```
localhost:8080/posts?limit=10

```
will return 10 posts


###Offset

```
localhost:8080/posts?offset=10

```
will return posts, skipping first 10
