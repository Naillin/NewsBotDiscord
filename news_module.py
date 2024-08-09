import requests
import random
from news_unit import NewsUnit
from newsapi import NewsApiClient

# Получение war новостей
def fetch_war_news(NEWS_API_KEY):
    url = f'https://newsapi.org/v2/top-headlines?country=ru&category=war&language=ru&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    if articles:
        random_article = random.choice(articles)
        return random_article['title']
    return 'Нет доступных новостей.'

# Получение gaming новостей
def fetch_gaming_news(NEWS_API_KEY):
    url = f'https://newsapi.org/v2/top-headlines?country=ru&category=gaming&language=ru&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    if articles:
        random_article = random.choice(articles)
        return random_article['title']
    return 'Нет доступных новостей.'

global top_headlines
def fetch_war_newsAPI(NEWS_API_KEY):
    # Init
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(category='war',
                                              language='ru',
                                              country='ru')
    # /v2/top-headlines/sources
    sources = newsapi.get_sources()

def fetch_gaming_newsAPI(NEWS_API_KEY):
    # Init
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    # /v2/top-headlines
    global top_headlines
    top_headlines = newsapi.get_top_headlines(category='gaming',
                                              language='ru',
                                              country='ru')
    # /v2/top-headlines/sources
    sources = newsapi.get_sources()

def fetch_technology_newsAPI(NEWS_API_KEY):
    # Init
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    # /v2/top-headlines
    global top_headlines
    top_headlines = newsapi.get_top_headlines(category='technology',
                                              language='ru',
                                              country='ru')
    # /v2/top-headlines/sources
    sources = newsapi.get_sources()

def get_NewsUnit():
    global top_headlines
    articles = top_headlines['articles']
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
