from dotenv import load_dotenv
import os
import json 
import requests


# Load environment variables from .env file
load_dotenv(dotenv_path='../../.env')

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_URL_BASE = "https://api.weatherapi.com/v1/current.json"


# Define get_weather function 
def get_weather(location = "Melbourne"):
    url = f'{WEATHER_URL_BASE}?key={WEATHER_API_KEY}&q={location}&aqi=no'
    response = requests.get(url)
    print(f"Response: {response.json()}")
    return response.json()





