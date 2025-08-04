from dotenv import load_dotenv
import os
import json 
import requests
from typing import Dict, Any
from openai.types.chat import ChatCompletionToolParam
from rich.console import Console 

# Initialize console for rich text output
console = Console()

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

def verify_weather_api() -> bool:
    """Verify Weather API key is available."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        console.print("[red]✗[/red] WEATHER_API_KEY not found in environment variables")
        return False
    console.print("[green]✓[/green] Weather API connected successfully")
    return True

# Verify API and set globals
WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY") if verify_weather_api() else None
WEATHER_URL_BASE: str = "https://api.weatherapi.com/v1/current.json"

WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")
WEATHER_URL_BASE: str = "https://api.weatherapi.com/v1/current.json"


# Define get_weather function 
def get_weather(location: str = "Melbourne") -> str:    
    """
    Get current weather temperature for a specified location.
    
    Args:
        location: The city or location to get weather for (default: Melbourne)
        
    Returns:
        The current temperature in Celsius
    """
    url: str = f'{WEATHER_URL_BASE}?key={WEATHER_API_KEY}&q={location}&aqi=no&alerts=no'
    response = requests.get(url)
        
    # Check if the request was successful
    if response.status_code != 200:
        # return 0.0  # Return a default value in case of error
        console.print(f"[red]Error parsing weather data:[/red] {response.status_code}")
        return f"Error parsing weather data for {location}"
    
    
    
    data: Dict[str, Any] = response.json()
    
    location_info = data['location']
    current = data['current']

    
    # Extract weather information 
    weather_info = {
            'location': f"{location_info['name']}, {location_info['country']}",
            'temperature_c': current['temp_c'],
            'temperature_f': current['temp_f'],
            'humidity': current['humidity'],
            'wind_kph': current['wind_kph'],
            'feels_like_c': current['feelslike_c']
        }
    
    # Explicit type casting
    # temp_c: float = float(data['current']['temp_c'])
    # return temp_c
    
    # Format the output message
    prompt = f"Weather in {weather_info['location']}: {weather_info['temperature_c']}°C ({weather_info['temperature_f']}°F), humidity {weather_info['humidity']}%, wind {weather_info['wind_kph']} km/h, feels like {weather_info['feels_like_c']}°C"
    return prompt


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

    console.print(f"[green]✓[/green] Fetching weather for location: {location}")

    # Call the function
    result: str = get_weather(location)
    
    # Return the function result message
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "get_weather",
        "content": result
    }
