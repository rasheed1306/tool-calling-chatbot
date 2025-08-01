from dotenv import load_dotenv
from newsapi import NewsApiClient
import os
import json 
import requests

# Load environment variables from .env file
load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
print(os.getenv("NEWS_API_KEY"))


# Define the get_news function
def get_news(query, sources=None, category=None, country=None):
    # Use sources OR category/country, not both
    if sources:
        top_headlines = newsapi.get_top_headlines(q=query, sources=sources)
    elif category or country:
        top_headlines = newsapi.get_top_headlines(q=query, category=category, country=country)
    else: 
        top_headlines = newsapi.get_top_headlines(q=query)
    return top_headlines['articles']

print(get_news(query="Trump", sources='bbc-news'))