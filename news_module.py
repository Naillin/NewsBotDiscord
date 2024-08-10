import requests
import random
import datetime
from news_unit import NewsUnit
from newsapi import NewsApiClient

__categories = [
    'business',
    'entertainment',
    'general',
    'health',
    'science',
    'sports',
    'technology'
]

__articles_date = {'articles': []}
def fetch_newsAPI(NEWS_API_KEY):
    """
    Fetches news articles from the News API using the provided API key.

    Args:
        NEWS_API_KEY (str): The API key for the News API.

    Returns:
        None

    Notes:
        This function uses the NewsApiClient to fetch news articles.
        It first tries to fetch top headlines, and if that fails, it tries to fetch everything.
        The fetched articles are stored in the variable articles_date.
    """
    # Открываем файл для чтения
    with open('codewords.txt', 'r', encoding='utf-8') as file:
        codewords = []
        for line in file:
            if line:  # Проверяем, что строка не пустая
                codewords.append(line.strip())  # Сохраняем в список, убирая лишние пробелы

    # Init
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    global __articles_date
    __articles_date = {'articles': []}  # Инициализируем переменную articles_date
    while len(__articles_date['articles']) == 0:
        # /v2/top-headlines
        __articles_date = newsapi.get_top_headlines(
            q=random.choice(codewords),
            category=random.choice(__categories),
            language='ru',
            # country='ru'
        )

        if len(__articles_date['articles']) == 0:
            # Если новостей не найдено, ищем их с помощью get_everything
            now = datetime.datetime.now()
            past_7_days = now - datetime.timedelta(days=7)
            # /v2/everything
            everything = newsapi.get_everything(
                q=d,
                from_param=past_7_days.strftime('%Y-%m-%d'),
                to=now.strftime('%Y-%m-%d'),
                language='ru',
                # country='ru'
            )

    # /v2/top-headlines/sources
    sources = newsapi.get_sources()


def get_NewsUnit():
    """
    Retrieves a NewsUnit object containing information about a randomly selected news article.

    Returns:
        NewsUnit: A NewsUnit object containing information about a news article, or a string indicating that no news is available.
    """
    global __articles_date
    articles = __articles_date['articles']
    if len(articles) != 0:
        random_article = random.choice(articles)
        return NewsUnit(
            random_article['author'],
            random_article['title'],
            random_article['description'],
            random_article['url'],
            random_article['urlToImage']
        )
    else:
        return None
