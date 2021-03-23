from typing import List

import pydantic
from fastapi import FastAPI

from mycode import all_sources

app = FastAPI()


class ArticleOut(pydantic.BaseModel):
    title: str
    link: str
    description: str
    published: str
    category: str


class NewsOut(pydantic.BaseModel):
    source_name: str
    articles: List[ArticleOut]


@app.get("/get_news", response_model=List[NewsOut])
async def root():
    source_info_per_source = [{"source_name": source.name(),
                               "articles": source.load()[:3]} for
                              source
                              in all_sources()]

    for source_info in source_info_per_source:
        source_info["articles"] = [{
            'title': article.title,
            'link': article.link,
            'description': article.description,
            'published': article.pubdate,
            'category': article.category
        } for article in source_info["articles"]
        ]

    return source_info_per_source
