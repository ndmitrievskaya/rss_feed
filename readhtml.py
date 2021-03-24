from newspaper import Article
import sqlite3
from sqlite3 import Error


class FullArticle:
    def __init__(self, title, image, text):
        self.title = title
        self.image = image
        self.text = text


class NewsItemReader:
    def __init__(self, url):
        self.url = url

    @classmethod
    def parse_article(cls, url):
        item = Article(url, language='ru')
        item.download()
        item.parse()

        return FullArticle(
            title=cls.extract_title_from_article(item),
            image=cls.extract_image_from_article(item),
            text=cls.extract_text_from_article(item)
        )

    @staticmethod
    def extract_title_from_article(item):
        return item.title

    @staticmethod
    def extract_image_from_article(item):
        return item.top_image

    @staticmethod
    def extract_text_from_article(item):
        raw_text = item.text
        return raw_text.replace('\n\n', '\n')

