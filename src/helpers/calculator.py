# Define a function that performs calculations
def calculate(operation, x, y):
    """
    Perform a mathematical operation on two numbers.

    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        x: The first number
        y: The second number

    Returns:
        The result of the operation
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
calculator_function = {
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