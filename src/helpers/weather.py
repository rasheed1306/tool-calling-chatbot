from dotenv import load_dotenv
import os
import json 
import requests
from typing import Dict, Any
from openai.types.chat import ChatCompletionToolParam

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")
WEATHER_URL_BASE: str = "https://api.weatherapi.com/v1/current.json"


# Define get_weather function 
def get_weather(location: str = "Melbourne") -> float:    
    """
    Get current weather temperature for a specified location.
    
    Args:
        location: The city or location to get weather for (default: Melbourne)
        
    Returns:
        The current temperature in Celsius
    """
    url: str = f'{WEATHER_URL_BASE}?key={WEATHER_API_KEY}&q={location}&aqi=no'
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print('error', response.status_code)
        return 0.0  # Return a default value in case of error
    
    data: Dict[str, Any] = response.json()
    
    # Explicit type casting
    temp_c: float = float(data['current']['temp_c'])
    return temp_c

# Define the function schema
get_weather_function: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather information for a specified location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or location to get weather for (e.g., 'Melbourne', 'Sydney', 'New York')",
                    "default": "Melbourne"
                }
            },
            "required": []
        }
    }
}

def process_weather_response(tool_call: Any) -> Dict[str, str]:
    """
    Process weather function call and return the result message.
    
    Args:
        tool_call: The tool call object from the API
        
    Returns:
        A dictionary with the result message
    """
    # Parse the function arguments
    arguments = json.loads(tool_call.function.arguments)
    location: str = arguments.get("location", "Melbourne")
    
    print(f"Fetching weather for location: {location}")
    
    # Call the function
    result: float = get_weather(location)
    
    # Return the function result message
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "get_weather",
        "content": str(result)
    }
