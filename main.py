import datetime
import json
from typing import List

import pydantic
from fastapi import FastAPI, Depends

import db
from feed import registered_feeds
from sqlalchemy.orm import Session

app = FastAPI()


class ArticleOut(pydantic.BaseModel):
    title: str
    link: str
    image: str
    description: str
    text: list
    published: str
    category: str


class RssFeedOut(pydantic.BaseModel):
    name: str
    articles: List[ArticleOut]


def get_session():
    session = db.make_session()
    try:
        yield session
    finally:
        session.close()


@app.get("/get_news", response_model=List[RssFeedOut])
def root(session: Session = Depends(get_session)):
    date = datetime.datetime.now().timestamp()
    cache_entry = session.query(db.RssFeedCache).order_by(
        db.RssFeedCache.timestamp.desc()).first()

    x = datetime.timedelta(minutes=3).total_seconds()

    if cache_entry is not None:
        if int(float(date)) - int(float(cache_entry.timestamp)) < x:
            return json.loads(cache_entry.snapshot)

    rss_feed_outs = [
        RssFeedOut(
            name=feed.name(),
            articles=[
                ArticleOut(
                    title=article.title,
                    link=article.link,
                    image=article.image_link,
                    description=article.description,
                    text=article.text,
                    published=article.pubdate,
                    category=article.category,
                ) for article in feed.load(limit=3)
            ],
        ) for feed in registered_feeds()
    ]

    snapshot = json.dumps(
        [rss_feed_out.dict() for rss_feed_out in rss_feed_outs])

    new_cache_entry = db.RssFeedCache(timestamp=date, snapshot=snapshot)
    session.add(new_cache_entry)
    session.commit()
    return rss_feed_outs
