from dotenv import load_dotenv
from newsapi import NewsApiClient
import os
import json 
import requests

# Load environment variables from .env file
load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


# Define the get_news function
def get_news(query, from_=None, to=None, sortBy="publishedAt"):
    # Convert string 'None' to actual None
    if from_ == 'None':
        from_ = None
    if to == 'None':
        to = None

    top_headlines = newsapi.get_everything(
        q=query,
        from_param=from_,
        to=to,
        sort_by=sortBy
    )

    # Return the list of articles
    return top_headlines['articles']

# Define the function schema
get_news_function = {
    "type": "function",
    "function": {
        "name": "get_news",
        "description": "Get news articles based on query with optional date filtering and sorting",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for news articles (e.g., 'bitcoin', 'AI', 'climate change')"
                },
                "from": {
                    "type": "string",
                    "description": "A date and optional time for the oldest article allowed. This should be in ISO 8601 format (e.g. 2025-08-02 or 2025-08-02T11:04:42)"
                },
                "to": {
                    "type": "string", 
                    "description": "A date and optional time for the newest article allowed. This should be in ISO 8601 format (e.g. 2025-08-02 or 2025-08-02T11:04:42)"
                },
                "sortBy": {
                    "type": "string",
                    "enum": ["relevancy", "popularity", "publishedAt"],
                    "description": "The order to sort articles in. relevancy = articles more closely related to query come first. popularity = articles from popular sources come first. publishedAt = newest articles come first. Default: publishedAt"
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
    from_ = arguments.get("from")
    to = arguments.get("to")
    sortBy = arguments.get("sortBy", "publishedAt")

    print(f"Function call: get_news(query='{query}', from_='{from_}', to='{to}', sortBy='{sortBy}')")

    # Call the function
    result = get_news(query, from_, to, sortBy)

    print(f"Function result: Found {len(result)} articles")

    # Return the function result message
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "get_news",
        "content": str(result)
    }



