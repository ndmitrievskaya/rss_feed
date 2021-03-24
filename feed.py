import abc

import requests
from bs4 import BeautifulSoup
import datetime

import newspaper


_REGISTERED_FEEDS = []


def registered_feeds():
    return _REGISTERED_FEEDS


def register_custom_feed(cls):
    _REGISTERED_FEEDS.append(cls)
    return cls


def format_date(date):
    split_date = date.split(" ")
    date = " ".join(split_date[1:4])
    time = split_date[-2]
    final_date = datetime.datetime.strptime(date, "%d %b %Y").strftime("%d.%m.%Y")
    final_time = datetime.datetime.strptime(time, "%H:%M:%S").strftime("%H:%M")
    public_date = final_date + " " + final_time
    return public_date


class Article:
    def __init__(self, title, description, link, category, pubdate, image_link, text):
        self.title = title
        self.description = description
        self.link = link
        self.category = category
        self.pubdate = pubdate
        self.image_link = image_link
        self.text = text


class RssFeed(abc.ABC):
    @classmethod
    def load(cls, limit=None):
        resp = requests.get(cls.url())
        soup = BeautifulSoup(resp.content, features="html.parser")
        items = soup.findAll("item")

        if limit is not None:
            items = items[:limit]

        return [cls._article_from_feed_item(item) for item in items]

    @classmethod
    def _article_from_feed_item(cls, item):
        link = cls._extract_link_from_item(item)
        np_article = newspaper.Article(link, language="ru")
        np_article.download()
        np_article.parse()

        text = np_article.text.replace("\n\n", "\n").split("\n")

        return Article(
            title=cls._extract_title_from_item(item),
            description=cls._extract_description_from_item(item),
            link=link,
            category=cls._extract_category_from_item(item),
            pubdate=cls._extract_pubdate_from_item(item),
            image_link=np_article.top_image,
            text=text,
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
        return item.find("title").text

    @staticmethod
    def _extract_description_from_item(item):
        return item.find("description").text.replace("\n", "")

    @staticmethod
    def _extract_link_from_item(item):
        return item.find("guid").text

    @staticmethod
    def _extract_category_from_item(item):
        return item.find("category").text

    @staticmethod
    def _extract_pubdate_from_item(item):
        raw_date = item.find("pubdate").text
        return format_date(raw_date)


@register_custom_feed
class Lenta(RssFeed):
    @staticmethod
    def url():
        return "http://lenta.ru/rss"

    @staticmethod
    def name():
        return "Лента.ру"


@register_custom_feed
class M24(RssFeed):
    @staticmethod
    def url():
        return "https://www.m24.ru/rss.xml"

    @staticmethod
    def name():
        return "Москва 24"

    @staticmethod
    def _extract_link_from_item(item):
        return item.id.previous_sibling.strip()


@register_custom_feed
class Interfax(RssFeed):
    @staticmethod
    def url():
        return "http://www.interfax.ru/rss.asp"

    @staticmethod
    def name():
        return "Интерфакс"


@register_custom_feed
class Kommersant(RssFeed):
    @staticmethod
    def url():
        return "http://www.kommersant.ru/RSS/news.xml"

    @staticmethod
    def name():
        return "Коммерсантъ"
