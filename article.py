# import dataclasses
# import datetime
#
# import requests
# from bs4 import BeautifulSoup
#
#
# def date_formatting(date):
#     split_date = date.split(' ')
#     date = ' '.join(split_date[1:4])
#     time = split_date[-2]
#     final_date = datetime.datetime.strptime(date,
#                                             "%d %b %Y").strftime("%d/%m/%Y")
#     final_time = datetime.datetime.strptime(time, '%H:%M:%S').strftime('%H:%M')
#     public_date = final_date + ' ' + final_time
#     return public_date
#
#
# _SOURCES = []
#
#
# def all_sources():
#     return _SOURCES
#
#
# def news_source(cls):
#     _SOURCES.append(cls)
#
#
# # class Article:
# #     def __init__(self, item):
# #         self._item = item
# #
# #     @staticmethod
# #     def url():
# #         raise NotImplementedError
# #
# #     @staticmethod
# #     def name():
# #         raise NotImplementedError
# #
# #     @classmethod
# #     def read_from_rss(cls):
# #         r = requests.get(cls.url())
# #         soup = BeautifulSoup(r.content, features='html.parser')
# #
# #         items = soup.findAll('item')
# #
# #         return [cls(item) for item in items]
# #
# #     @property
# #     def link(self):
# #         return self._item.find('guid').text
# #
# #     @property
# #     def description(self):
# #         return self._item.find('description').text.replace('\n', '')
# #
# #     @property
# #     def title(self):
# #         return self._item.find('title').text
# #
# #     @property
# #     def publication_date(self):
# #         raw_published = self._item.find('pubdate').text
# #         return date_formatting(raw_published)
# #
# #     @property
# #     def category(self):
# #         return self._item.find('category').text
# #
# #
# # @news_source
# # class LentaArticle(Article):
# #     @staticmethod
# #     def url():
# #         return 'http://lenta.ru/rss'
# #
# #     @staticmethod
# #     def name():
# #         return 'ЛЕНТА'
# #
# #
# # @news_source
# # class KommersantArticle(Article):
# #     @staticmethod
# #     def url():
# #         return 'http://www.kommersant.ru/RSS/news.xml'
# #
# #     @staticmethod
# #     def name():
# #         return 'ЛЕНТА'
# #
# #
# # @news_source
# # class InterfaxArticle(Article):
# #     @staticmethod
# #     def url():
# #         return 'http://www.interfax.ru/rss.asp'
# #
# #     @staticmethod
# #     def name():
# #         return 'ЛЕНТА'
# #
# #
# # @news_source
# # class M24Article(Article):
# #     @staticmethod
# #     def url():
# #         return 'https://www.m24.ru/rss.xml'
# #
# #     @property
# #     def link(self):
# #         return self._item.id.previous_sibling.strip()
# #
# #     @staticmethod
# #     def name():
# #         return 'ЛЕНТА'
#
#
# class NewsSource:
#     def name(self):
#         pass
#
#     @classmethod
#     def read(cls):
#         r = requests.get(cls.url())
#         soup = BeautifulSoup(r.content, features='html.parser')
#
#         items = soup.findAll('item')
#
#         return [Article(
#             title='?',
#             description='?',
#             link=cls.extract_link_from_item(item)
#         ) for item in items]
#
#     @staticmethod
#     def url():
#         return ''
#
#     @staticmethod
#     def extract_link_from_item(item):
#         return item.find('guid').text
#
#
# class M24Source(NewsSource):
#     @staticmethod
#     def extract_link_from_item(item):
#         return ...
#
#
# M24Source.read()
#
#
# class Article:
#     def __init__(self, link, title, description):
#         self.link = link
#         self.description = description
#         self.title = title
