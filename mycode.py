import requests
from bs4 import BeautifulSoup
import datetime

_SOURCES = []


def all_sources():
    return _SOURCES


def news_source(cls):
    _SOURCES.append(cls)


def date_formatting(date):
    split_date = date.split(' ')
    date = ' '.join(split_date[1:4])
    time = split_date[-2]
    final_date = datetime.datetime.strptime(date,
                                            "%d %b %Y").strftime("%d.%m.%Y")
    final_time = datetime.datetime.strptime(time, '%H:%M:%S').strftime('%H:%M')
    public_date = final_date + ' ' + final_time
    return public_date


class NewSource:
    @classmethod
    def read(cls):
        r = requests.get(cls.url())
        soup = BeautifulSoup(r.content, features='html.parser')

        items = soup.findAll('item')
        return [Article(
            title=cls.extract_title_from_item(item),
            description=cls.extract_description_from_item(item),
            link=cls.extract_link_from_item(item),
            category=cls.extract_category_from_item(item),
            pubdate=cls.extract_pubdate_from_item(item)
        ) for item in items]

    @staticmethod
    def url():
        raise NotImplementedError

    @staticmethod
    def name():
        raise NotImplementedError

    @staticmethod
    def extract_title_from_item(item):
        return item.find('title').text

    @staticmethod
    def extract_description_from_item(item):
        return item.find('description').text.replace('\n', '')

    @staticmethod
    def extract_link_from_item(item):
        return item.find('guid').text

    @staticmethod
    def extract_category_from_item(item):
        return item.find('category').text

    @staticmethod
    def extract_pubdate_from_item(item):
        raw_date = item.find('pubdate').text
        return date_formatting(raw_date)


class Article:
    def __init__(self, title, description, link, category, pubdate):
        self.title = title
        self.description = description
        self.link = link
        self.category = category
        self.pubdate = pubdate


@news_source
class Lenta(NewSource):
    @staticmethod
    def url():
        return 'http://lenta.ru/rss'

    @staticmethod
    def name():
        return 'Лента.ру'


@news_source
class M24(NewSource):
    @staticmethod
    def url():
        return 'https://www.m24.ru/rss.xml'

    @staticmethod
    def name():
        return 'Москва 24'

    @staticmethod
    def extract_link_from_item(item):
        return item.id.previous_sibling.strip()


@news_source
class Interfax(NewSource):
    @staticmethod
    def url():
        return 'http://www.interfax.ru/rss.asp'

    @staticmethod
    def name():
        return 'Интерфакс'


@news_source
class Kommersant(NewSource):
    @staticmethod
    def url():
        return 'http://www.kommersant.ru/RSS/news.xml'

    @staticmethod
    def name():
        return 'Коммерсантъ'
