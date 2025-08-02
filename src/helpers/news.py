from dotenv import load_dotenv
from newsapi import NewsApiClient
import os
import json 
import requests
from typing import Dict, Any, List, Optional, Union

# Load environment variables from .env file
load_dotenv()

# Initialize NewsAPI client with error checking
api_key = os.getenv("NEWS_API_KEY")
if not api_key:
    print("Error: NEWS_API_KEY not found in environment variables. Please check your .env file.")
    newsapi = None
else:
    try:
        newsapi = NewsApiClient(api_key=api_key)
        print("NewsAPI client initialized successfully.")
    except Exception as e:
        print(f"Error: Failed to initialize NewsAPI client: {e}")
        newsapi = None


# Define the get_news function
def get_news(query: str, from_: str | None, to: str | None, 
             sortBy: str = "publishedAt") -> List[Dict[str, Any]]:
    """
    Get news articles based on query with optional date filtering and sorting.
    
    Args:
        query: Search query for news articles
        from_: A date for the oldest article allowed (ISO 8601 format)
        to: A date for the newest article allowed (ISO 8601 format)
        sortBy: The order to sort articles in (relevancy, popularity, publishedAt)
        
    Returns:
        A list of news articles
    """
    # Check if newsapi client is available
    if newsapi is None:
        print("Error: NewsAPI client is not initialized. Cannot fetch news articles.")
        return []

    try:
        top_headlines: Dict[str, Any] = newsapi.get_everything(
            q=query,
            from_param=from_,
            to=to,
            sort_by=sortBy
        )
        # Return the list of articles
        return top_headlines['articles']
    except Exception as e:
        print(f"Error fetching news articles: {e}")
        return []

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

def process_news_response(tool_call: Any) -> Dict[str, str]:
    """
    Process news function call and return the result message.
    
    Args:
        tool_call: The tool call object from the API
        
    Returns:
        A dictionary with the result message
    """
    # Parse the function arguments
    arguments = json.loads(tool_call.function.arguments)
    query: str = arguments.get("query", "") 
    from_: str | None = arguments.get("from")
    to: str | None = arguments.get("to")
    sortBy: str = arguments.get("sortBy", "publishedAt")

    print(f"Function call: get_news(query='{query}', from_='{from_}', to='{to}', sortBy='{sortBy}')")

    # Call the function
    result: List[Dict[str, Any]] = get_news(query, from_, to, sortBy)

    print(f"Function result: Found {len(result)} articles")

    # Return the function result message
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "get_news",
        "content": str(result)
    }
