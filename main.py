import datetime
import json
from pprint import pprint
from typing import List

import pydantic
import yaml
from fastapi import FastAPI

from mycode import all_sources, News, engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()


class ArticleOut(pydantic.BaseModel):
    title: str
    link: str
    image: str
    description: str
    text: list
    published: str
    category: str


class NewsOut(pydantic.BaseModel):
    source_name: str
    articles: List[ArticleOut]


@app.get("/get_news", response_model=List[NewsOut])
async def root():
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    date = datetime.datetime.now().timestamp()
    query = session.query(News)[-1]
    if (int(float(date)) - int(float(query.pubdate))) < 180:
        return json.loads(query.news_items)
    else:
        source_info_per_source = [{"source_name": source.name(),
                                   "articles": source.load(limit=1)} for
                                  source
                                  in all_sources()]
        for source_info in source_info_per_source:
            source_info["articles"] = [{
                'title': article.title,
                'link': article.link,
                'image': article.image_link,
                'description': article.description,
                'text': article.text,
                'published': article.pubdate,
                'category': article.category
            } for article in source_info["articles"]
            ]
        cache_news = News(pubdate=date,
                          news_items=json.dumps(source_info_per_source))
        session.add(cache_news)
        session.commit()
        return source_info_per_source
