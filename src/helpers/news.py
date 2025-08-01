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

    # Return the list of articles
    return top_headlines['articles']

# Define the function schema
get_news_function = {
    "type": "function",
    "function": {
        "name": "get_news",
        "description": "Get top news headlines based on query, sources, category, or country",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for news articles (e.g., 'bitcoin', 'AI', 'climate change')"
                },
                "sources": {
                    "type": "string",
                    "description": "Comma-separated news sources (e.g., 'bbc-news', 'cnn', 'reuters'). Cannot be used with category/country."
                },
                "category": {
                    "type": "string",
                    "enum": ["business", "entertainment", "general", "health", "science", "sports", "technology"],
                    "description": "News category. Cannot be used with sources parameter."
                },
                "country": {
                    "type": "string",
                    "enum": ["us", "gb", "ca", "au", "de", "fr", "jp", "in"],
                    "description": "Country code for news (e.g., 'us', 'gb', 'ca'). Cannot be used with sources parameter."
                }
            },
            "required": ["query"]
        }
    }
}

def process_news_response(tool_call):
    """Process news function call and return the result message"""
    # Parse the function arguments
    arguments = json.loads(tool_call.function.arguments)
    query = arguments.get("query")
    sources = arguments.get("sources")
    category = arguments.get("category")
    country = arguments.get("country")

    print(f"Function call: get_news(query='{query}', sources='{sources}', category='{category}', country='{country}')")

    # Call the function
    result = get_news(query, sources, category, country)

    print(f"Function result: Found {len(result)} articles")

    # Return the function result message
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "get_news",
        "content": str(result)
    }



