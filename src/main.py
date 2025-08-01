import os
import json 
import requests
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}  
    ],
    temperature = 0.7, 
    max_tokens = 150
)

print("Response from OpenAI:")
print(response.choices[0].message.content)