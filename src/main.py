import os
import json 
import requests
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

# Load functions from helpers 
from helpers.calculator import calculate, calculator_function

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's 241 multiplied by 18?"}  
    ]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    temperature = 0.7, 
    max_tokens = 150,
    tools = [calculator_function],
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
            # Parse the function arguments
            arguments = json.loads(tool_call.function.arguments)
            operation = arguments.get("operation")
            x = arguments.get("x")
            y = arguments.get("y")

            print(f"Function call: calculate({operation}, {x}, {y})")

            # Call the function
            result = calculate(operation, x, y)

            # Add the function result to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(result)
            })

            print(f"Function result: {result}")
            
        # Get a new response from the model with the function result
        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )


print("Response from OpenAI:")
print(second_response.choices[0].message.content)
