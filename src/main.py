import os
import json 
import requests
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

# Load functions from helpers 
from helpers.calculator import calculator_function, process_calculator_response
from helpers.weather import get_weather_function, process_weather_response
from helpers.news import get_news, get_news_function, process_news_response

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
        {"role": "system", "content": "You are a helpful assistant that can answer maths calculations, give news updates and get weather information"},
    ]


def chat_with_functions(user_input):
    # Add user's message to the conversation 
    messages.append({"role": "user", "content": user_input})
    
    # Get the initial response from the model 
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature = 0.7, 
        max_tokens = 150,
        tools = [calculator_function, get_weather_function, get_news_function],
        tool_choice = "auto",
        )
    
    # Process the response 
    assistant_message = response.choices[0].message
    messages.append(assistant_message.model_dump())

    # Check if the model wants to call a function 
    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name

            if function_name == "calculate":
                # Process calculator function call and append the result to messages
                result_message = process_calculator_response(tool_call)
                messages.append(result_message)
                
            elif function_name == "get_weather":
                # Process weather function call and append the result to messages
                result_message = process_weather_response(tool_call)
                messages.append(result_message)
            
            elif function_name == "get_news":
                # Process news function call and append the result to messages
                result_message = process_news_response(tool_call)
                messages.append(result_message)
            
            
            # Get a new response from the model with the function result
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

        print("Response from OpenAI:")
        print(second_response.choices[0].message.content)



def main(): 
    # chat_with_functions("What's 241 multiplied by 18?")
    # chat_with_functions("What's the weather in Melbourne?")
    chat_with_functions("Can you tell me latest news about bitcoin from 2/07/2025?")
  
  
if __name__ == "__main__":
    main()