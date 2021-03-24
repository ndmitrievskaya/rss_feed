import abc
import dataclasses
import json

import requests
from bs4 import BeautifulSoup
import datetime

import newspaper
import sqlalchemy
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table, \
    DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import sessionmaker

_SOURCES = []


def all_sources():
    return _SOURCES


def news_source(cls):
    _SOURCES.append(cls)
    return cls


def date_formatting(date):
    split_date = date.split(' ')
    date = ' '.join(split_date[1:4])
    time = split_date[-2]
    final_date = datetime.datetime.strptime(date,
                                            "%d %b %Y").strftime("%d.%m.%Y")
    final_time = datetime.datetime.strptime(time, '%H:%M:%S').strftime('%H:%M')
    public_date = final_date + ' ' + final_time
    return public_date


class RssFeed(abc.ABC):
    @classmethod
    def load(cls, limit=None):
        resp = requests.get(cls.url())
        soup = BeautifulSoup(resp.content, features='html.parser')
        items = soup.findAll('item')

        if limit is not None:
            items = items[:limit]

        return [cls._article_from_feed_item(item) for item in items]

    @classmethod
    def _article_from_feed_item(cls, item):
        link = cls._extract_link_from_item(item)
        np_article = newspaper.Article(link,
                                       language='ru')
        np_article.download()
        np_article.parse()

        text = np_article.text.replace('\n\n', '\n').split('\n')

        return Article(
            title=cls._extract_title_from_item(item),
            description=cls._extract_description_from_item(item),
            link=link,
            category=cls._extract_category_from_item(item),
            pubdate=cls._extract_pubdate_from_item(item),
            image_link=np_article.top_image,
            text=text
        )

    @staticmethod
    @abc.abstractmethod
    def url():
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def name():
        raise NotImplementedError

    @staticmethod
    def _extract_title_from_item(item):
        return item.find('title').text

    @staticmethod
    def _extract_description_from_item(item):
        return item.find('description').text.replace('\n', '')

    @staticmethod
    def _extract_link_from_item(item):
        return item.find('guid').text

    @staticmethod
    def _extract_category_from_item(item):
        return item.find('category').text

    @staticmethod
    def _extract_pubdate_from_item(item):
        raw_date = item.find('pubdate').text
        return date_formatting(raw_date)


class Article:
    def __init__(self, title, description, link, category, pubdate, image_link,
                 text):
        self.title = title
        self.description = description
        self.link = link
        self.category = category
        self.pubdate = pubdate
        self.image_link = image_link
        self.text = text


# @dataclasses.dataclass
# class Article:
#     title: str
#     description: str
#     link: str
#     category: str
#     pubdate: str
#     image_link: str
#     text: str


@news_source
class Lenta(RssFeed):
    @staticmethod
    def url():
        return 'http://lenta.ru/rss'

    @staticmethod
    def name():
        return 'Лента.ру'


@news_source
class M24(RssFeed):
    @staticmethod
    def url():
        return 'https://www.m24.ru/rss.xml'

    @staticmethod
    def name():
        return 'Москва 24'

    @staticmethod
    def _extract_link_from_item(item):
        return item.id.previous_sibling.strip()


@news_source
class Interfax(RssFeed):
    @staticmethod
    def url():
        return 'http://www.interfax.ru/rss.asp'

    @staticmethod
    def name():
        return 'Интерфакс'


@news_source
class Kommersant(RssFeed):
    @staticmethod
    def url():
        return 'http://www.kommersant.ru/RSS/news.xml'

    @staticmethod
    def name():
        return 'Коммерсантъ'


# necessary to be done for initializing the table in DB and making first cache in it
engine = create_engine('sqlite:///news.sqlite3', echo=True)
meta = MetaData()
Base = declarative_base()

news_news = Table(
    'news_news', meta,
    Column('id', Integer, primary_key=True),
    Column('pubdate', String),
    Column('news_items', JSON),
)


class News(Base):
    __tablename__ = 'news_news'

    id = Column(Integer, primary_key=True)
    pubdate = Column(String)
    news_items = Column(JSON)


if __name__ == '__main__':
    meta.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    date = datetime.datetime.now().timestamp()
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
