import requests
from bs4 import BeautifulSoup
import datetime

URL = 'https://www.m24.ru/rss.xml'


# 'http://www.kommersant.ru/RSS/news.xml'

# 'http://www.interfax.ru/rss.asp'


def date_formatting(date):
    split_date = date.split(' ')
    date = ' '.join(split_date[1:4])
    time = split_date[-2]
    final_date = datetime.datetime.strptime(date,
                                            "%d %b %Y").strftime("%d.%m.%Y")
    final_time = datetime.datetime.strptime(time, '%H:%M:%S').strftime('%H:%M')
    public_date = final_date + ' ' + final_time
    return public_date


def website_scrapping(url):
    article_list = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='html.parser')
        # print(soup.prettify())

        articles = soup.findAll('item')
        for article in articles:
            title = article.find('title').text
            link = article.id.previous_sibling.strip()
            raw_description = article.find('description').text
            description = raw_description.replace('\n', '')
            raw_published = article.find('pubdate').text
            published = date_formatting(raw_published)
            category = article.find('category').text
            article = {
                'title': title,
                'link': link,
                'description': description,
                'published': published,
                'category': category
            }
            article_list.append(article)

        print(article_list[:3])
    except Exception as e:
        return f'The scraping job failed. See exception:{e}'


if __name__ == '__main__':
    website_scrapping(URL)
