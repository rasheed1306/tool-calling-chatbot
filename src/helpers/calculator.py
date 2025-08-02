import json
from typing import Dict, Literal, Any
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam, ChatCompletionToolParam
from rich.console import Console

# Initialize console for rich text output
console = Console()


# Type definitions
OperationType = Literal["add", "subtract", "multiply", "divide"]
NumberType = float | int
ResultType = NumberType | str

# Define a function that performs calculations
def calculate(operation: OperationType, x: NumberType, y: NumberType) -> ResultType:
    """
    Perform a mathematical operation on two numbers.

    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        x: The first number
        y: The second number

    Returns:
        The result of the operation or an error message
    """
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        if y == 0:
            return "Error: Division by zero"
        return x / y
    else:
        return f"Error: Unknown operation '{operation}'"

# Define the function schema
calculator_function: ChatCompletionToolParam= {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform a mathematical operation on two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The mathematical operation to perform"
                },
                "x": {
                    "type": "number",
                    "description": "The first number"
                },
                "y": {
                    "type": "number",
                    "description": "The second number"
                }
            },
            "required": ["operation", "x", "y"]
        }
    }
}

def process_calculator_response(tool_call: Any) -> Dict[str, str]:
    """
    Process calculator function call and return the result message.
    
    Args:
        tool_call: The tool call object from the API
        
    Returns:
        A dictionary with the result message
    """
    # Parse the function arguments
    arguments = json.loads(tool_call.function.arguments)
    operation = arguments.get("operation")
    x = arguments.get("x") 
    y = arguments.get("y")
    
    console.print(f"🧮 [bold]calculate[/bold](operation={operation}, x={x}, y={y})")

    # Call the function with status
    with console.status("[yellow]Calculating...", spinner="dots"):
        result = calculate(operation, x, y)

    console.print(f"[green]✓[/green] Result: {result}")

    # Return the function result message
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": "calculate",
        "content": str(result)
    }