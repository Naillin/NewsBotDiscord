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
__number_of_requests = 0
__number_of_all_requests = 0
def fetch_news_with_top_headlines(NEWS_API_KEY):
    """
    Fetches news with top headlines using the News API.

    Args:
        NEWS_API_KEY (str): The API key for the News API.

    Returns:
        None

    Notes:
        This function reads codewords from a file, initializes the News API client,
        and fetches top headlines using the API. If no news is found, it attempts to
        fetch news using the get_everything endpoint. The function updates global
        variables to track the number of requests and the articles date.
    """
    # Открываем файл для чтения
    with open('codewords.txt', 'r', encoding='utf-8') as file:
        codewords = []
        for line in file:
            if line:  # Проверяем, что строка не пустая
                codewords.append(line.strip())  # Сохраняем в список, убирая лишние пробелы

    # Init
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    global __number_of_requests
    __number_of_requests = 0
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
        __number_of_requests = __number_of_requests + 1

        if len(__articles_date['articles']) == 0:
            # Если новостей не найдено, ищем их с помощью get_everything
            now = datetime.datetime.now()
            past_7_days = now - datetime.timedelta(days=7)
            # /v2/everything
            everything = newsapi.get_everything(
                q=random.choice(codewords),
                from_param=past_7_days.strftime('%Y-%m-%d'),
                to=now.strftime('%Y-%m-%d'),
                language='ru',
                # country='ru'
            )
            __number_of_requests = __number_of_requests + 1

    # /v2/top-headlines/sources
    # sources = newsapi.get_sources()

    global __number_of_all_requests
    __number_of_all_requests = __number_of_all_requests + __number_of_requests

def fetch_news_everything(NEWS_API_KEY):
    """
    Fetches news using the News API's get_everything endpoint.

    Args:
        NEWS_API_KEY (str): The API key for the News API.

    Returns:
        None

    Notes:
        This function reads codewords from a file, initializes the News API client,
        and fetches news using the get_everything endpoint. It updates global variables
        to track the number of requests and the articles date.
    """
    # Открываем файл для чтения
    with open('codewords.txt', 'r', encoding='utf-8') as file:
        codewords = []
        for line in file:
            if line:  # Проверяем, что строка не пустая
                codewords.append(line.strip())  # Сохраняем в список, убирая лишние пробелы

    # Init
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    global __number_of_requests
    __number_of_requests = 0
    global __articles_date
    __articles_date = {'articles': []}  # Инициализируем переменную articles_date
    while len(__articles_date['articles']) == 0:
        now = datetime.datetime.now()
        past_7_days = now - datetime.timedelta(days=7)
        # /v2/everything
        everything = newsapi.get_everything(
            q=random.choice(codewords),
            from_param=past_7_days.strftime('%Y-%m-%d'),
            to=now.strftime('%Y-%m-%d'),
            language='ru',
            # country='ru'
        )
        __number_of_requests = __number_of_requests + 1

    # /v2/top-headlines/sources
    # sources = newsapi.get_sources()
    global __number_of_all_requests
    __number_of_all_requests = __number_of_all_requests + __number_of_requests

def get_NewsUnit():
    """
    Retrieves a NewsUnit object containing information about a randomly selected news article.

    Returns:
        NewsUnit: A NewsUnit object containing information about a news article, or None if no news is available.
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


def get_number_of_requests():
    """
    Retrieves the current number of requests and the total number of requests made.

    Returns:
        tuple: A tuple containing the current number of requests and the total number of requests.
    """
    global __number_of_requests
    global __number_of_all_requests
    return __number_of_requests, __number_of_all_requests