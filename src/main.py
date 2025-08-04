import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import  ChatCompletionMessageParam
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from typing import List, cast

# Load functions from helpers 
from helpers.calculator import calculator_function, process_calculator_response
from helpers.weather import get_weather_function, process_weather_response
from helpers.news import get_news_function, process_news_response

# Load environment variables from .env file
load_dotenv()

# Initialize console for rich text output
console = Console()

def verify_openai_connection() -> OpenAI:
    """Verify OpenAI API connection."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]✗[/red] OPENAI_API_KEY not found in environment variables")
        exit(1)
    
    with console.status("[yellow]Connecting to OpenAI...", spinner="dots"):
        try:
            openai_client = OpenAI(api_key=api_key)
            console.print("[green]✓[/green] OpenAI connected successfully")
            return openai_client
        except Exception as e:
            console.print(f"[red]✗[/red] OpenAI connection failed: {e}")
            exit(1)

# Initialize OpenAI client with verification
client: OpenAI = verify_openai_connection()

# Type annotation for messages
messages: List[ChatCompletionMessageParam] = [
    {"role": "system", "content": "You are a helpful assistant that can answer maths calculations, give news updates and get weather information"},
]


def chat_with_functions(user_input: str) -> None:
    """
    Process user input, get response from OpenAI, and handle any function calls.
    
    Args:
        user_input: The user's message
    """
    # Add user's message to the conversation 
    messages.append({"role": "user", "content": user_input})
    
    # Get the initial response from the model 
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7, 
        max_tokens=150,
        tools=[calculator_function, get_weather_function, get_news_function],
        tool_choice="auto",
    )
    
    # Process the response 
    assistant_message = response.choices[0].message
    messages.append(cast(ChatCompletionMessageParam, assistant_message.model_dump()))

    # Check if the model wants to call a function
    if assistant_message.tool_calls:
        console.print(Rule(style="white"))
        console.print(f"🔧 [bold]Processing {len(assistant_message.tool_calls)} function call(s)[/bold]")
        
        second_response = None
        for tool_call in assistant_message.tool_calls:
            function_name: str = tool_call.function.name

            if function_name == "calculate":
                # Process calculator function call and append the result to messages
                result_message = process_calculator_response(tool_call)
                messages.append(cast(ChatCompletionMessageParam, result_message))
                
            elif function_name == "get_weather":
                # Process weather function call and append the result to messages
                result_message = process_weather_response(tool_call)
                messages.append(cast(ChatCompletionMessageParam, result_message))
            
            elif function_name == "get_news":
                # Process news function call and append the result to messages
                result_message = process_news_response(tool_call)
                messages.append(cast(ChatCompletionMessageParam, result_message))
            
        # Get a new response from the model with the function result
        with console.status("[yellow]Generating final response...", spinner="dots"):
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

        # Response from OpenAI
        content = second_response.choices[0].message.content or "No response content"
        assistant_panel: Panel = Panel(content,title="[bold green]OpenAI Assistant[/bold green]",border_style="green",padding=(0, 1))
        console.print(assistant_panel)


def main() -> None:
    """Main function to demonstrate the chat functionality."""
    # chat_with_functions("What's 241 multiplied by 18?")
    # chat_with_functions("What's the weather in Melbourne?")
    # chat_with_functions("Can you tell me latest news about bitcoin from 2/07/2025?")

    while True:   
        try:
            usr_input = input("\n💬 Enter a prompt (or q to quit): ").strip()
            
            if usr_input.lower() == "q":
                console.print("[bold red]👋 Exiting... Goodbye![/bold red]")
                break
            elif usr_input.lower() == "clear":
                # Reset messages but keep the system message
                global messages
                messages = [
                    {"role": "system", "content": "You are a helpful assistant that can answer maths calculations, give news updates and get weather information"},
                ]
                console.print("[yellow]🗑️ Conversation history cleared[/yellow]")
                continue
            elif not usr_input:
                console.print("[yellow]Please enter a message[/yellow]")
                continue
            
            chat_with_functions(usr_input)
            console.print(Rule(style="white"))
            
        except KeyboardInterrupt:
            console.print("\n[bold red]👋 Goodbye![/bold red]")
            break
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            


if __name__ == "__main__":
    main()
