import requests
import random
import datetime
from news_unit import NewsUnit
from newsapi import NewsApiClient

categories = [
    'business',
    'entertainment',
    'general',
    'health',
    'science',
    'sports',
    'technology'
]

global articles_date
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
        The fetched articles are stored in the global variable articles_date.
    """
    # Открываем файл для чтения
    with open('codewords.txt', 'r', encoding='utf-8') as file:
        codewords = []
        for line in file:
            if line:  # Проверяем, что строка не пустая
                codewords.append(line.strip())  # Сохраняем в список, убирая лишние пробелы

    # Init
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    global articles_date  # Объявляем articles_date как глобальную переменную
    articles_date = {'articles': []}  # Инициализируем переменную articles_date
    while not articles_date['articles']:
        d = random.choice(codewords)
        s = random.choice(categories)
        # /v2/top-headlines
        articles_date = newsapi.get_top_headlines(
            q=d,
            category=s,
            language='ru',
            # country='ru'
        )

        if not articles_date['articles']:
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
            articles_date = everything

    # /v2/top-headlines/sources
    sources = newsapi.get_sources()


def get_NewsUnit():
    """
    Retrieves a NewsUnit object containing information about a randomly selected news article.

    Returns:
        NewsUnit: A NewsUnit object containing information about a news article, or a string indicating that no news is available.
    """
    global articles_date
    articles = articles_date['articles']
    if articles:
        random_article = random.choice(articles)
        return NewsUnit(
            random_article['author'],
            random_article['title'],
            random_article['description'],
            random_article['url'],
            random_article['urlToImage']
        )
    else:
        return 'Нет доступных новостей.'
