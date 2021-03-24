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
    # date = datetime.datetime.now().timestamp()
    # query = session.query(db.RssFeedCache)[-1]
    #
    # if (int(float(date)) - int(float(query.pubdate))) < 180:
    #     return json.loads(query.news_items)

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
                )
                for article in feed.load(limit=1)
            ],
        )
        for feed in registered_feeds()
    ]


    # cache_news = News(pubdate=date,
    #                   news_items=json.dumps(source_info_per_source))
    # session.add(cache_news)
    # session.commit()
    return rss_feed_outs
