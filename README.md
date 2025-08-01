# AI-Powered CLI Assistant

A modular command-line AI assistant that integrates with OpenAI's GPT-4o-mini model, featuring an extensible tool system for function calling. This project demonstrates modern Python development practices, environment management, and LLM integration.

## Learning Objectives Achieved

- ✅ Applied `uv` for Python project management and dependencies
- ✅ Implemented proper project structure using `src/` layout
- ✅ Practiced Git workflow and version control
- ✅ Used environment variables for secure configuration
- ✅ Applied Python type hints throughout the codebase
- ✅ Integrated OpenAI's function calling capabilities
- ✅ Built a modular, extensible architecture

## Features

- **OpenAI GPT-4o-mini Integration**: Advanced AI chat with function calling support
- **Extensible Tool System**: Registry pattern for dynamic tool discovery and registration
- **Secure Configuration**: Environment variable management with validation
- **Async Operations**: Non-blocking API calls using async/await
- **Beautiful CLI**: Rich-powered interface with formatted messages and interactive commands
- **Type-Safe Codebase**: Comprehensive type hints using modern Python typing features
- **Robust Error Handling**: User-friendly error messages and graceful degradation

## Prerequisites

- **Python 3.9+** (recommended: Python 3.11+)
- **uv** - Modern Python package and environment manager
  ```bash
  # Install uv (if not already installed)
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **OpenAI API Key** - Get one from [OpenAI's platform](https://platform.openai.com/api-keys)

## Quick Start

### 1. Clone and Navigate

```bash
git clone <your-repository-url>
cd tool-calling-chatbot
```

### 2. Install Dependencies with uv

```bash
# Create virtual environment and install dependencies
uv sync

# Install project in editable mode
uv pip install -e .
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional (with defaults)
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000
```

### 4. Run the Assistant

```bash
# Activate the virtual environment (if not already active)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the CLI assistant
python -m src.main
```

## Usage

### Interactive Commands

The assistant supports several special commands:

- `/help` - Show available commands and usage instructions
- `/tools` - List all available tools and their descriptions
- `/clear` - Clear conversation history
- `/exit` or `/quit` - Exit the application gracefully

### Example Conversation

```
🤖 AI Assistant: Hello! I'm your AI-powered CLI assistant. How can I help you today?

You: Calculate the result of 15 * (23 + 7) / 5

🤖 AI Assistant: I'll help you calculate that expression.

🔧 [Calculator Tool] Evaluating: 15 * (23 + 7) / 5
📊 Result: 90.0

The calculation 15 * (23 + 7) / 5 equals 90.

You: What's the weather like in London?

🤖 AI Assistant: I'll check the current weather in London for you.

🌤️ [Weather Tool] Fetching weather for: London
📍 London, UK: 18°C, Partly Cloudy, Humidity: 65%

You: /tools

🤖 AI Assistant: Available tools:
• Calculator - Evaluate mathematical expressions safely
• Weather - Get current weather information for any city
• Movies - Search for movies and get detailed information

You: /exit

🤖 AI Assistant: Thank you for using the AI Assistant. Goodbye! 👋
```

## Available Tools

### 1. Calculator Tool ➕

**Purpose**: Safely evaluate mathematical expressions without arbitrary code execution.

- **Function**: `calculate_expression`
- **Parameters**:
  - `expression` (str): Mathematical expression to evaluate
- **Features**:
  - Supports basic arithmetic operations (+, -, \*, /, \*\*, %)
  - Handles parentheses and operator precedence
  - Safe evaluation (no `eval()` - uses `ast.literal_eval`)
  - Input validation and sanitization
- **Example**: `"Calculate 2 + 3 * 4"`

### 2. Weather Tool 🌤️

**Purpose**: Fetch current weather information for any city worldwide.

- **Function**: `get_weather`
- **Parameters**:
  - `location` (str): City name or "City, Country" format
- **Features**:
  - Real-time weather data
  - Temperature, conditions, and humidity
  - Error handling for invalid locations
- **Example**: `"What's the weather in Tokyo?"`

### 3. Movies Tool 🎬

**Purpose**: Search for movies and retrieve detailed information.

- **Function**: `search_movies`
- **Parameters**:
  - `query` (str): Movie title or search term
  - `year` (int, optional): Release year filter
- **Features**:
  - Movie search and details
  - Cast, director, plot summary
  - Ratings and release information
- **Example**: `"Find information about Inception"`

## Project Architecture

### Directory Structure

```
tool-calling-chatbot/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # CLI entry point and main application
│   ├── config.py            # Configuration management with dataclasses
│   ├── assistant.py         # Core AI assistant logic and OpenAI integration
│   ├── tools/               # Tool system directory
│   │   ├── __init__.py      # Tools package initialization
│   │   ├── base.py          # Abstract base classes for tools
│   │   ├── registry.py      # Dynamic tool discovery and registration
│   │   └── implementations/ # Tool implementations
│   │       ├── __init__.py
│   │       ├── calculator.py    # Mathematical expression evaluation
│   │       ├── weather.py       # Weather information tool
│   │       └── movies.py        # Movie search and information
│   ├── calculator.py        # Calculator tool implementation
│   ├── weather.py          # Weather tool implementation
│   └── movies.py           # Movies tool implementation
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_assistant.py    # Assistant core logic tests
│   ├── test_config.py       # Configuration tests
│   └── test_tools/          # Tool-specific tests
│       ├── test_calculator.py
│       ├── test_weather.py
│       └── test_movies.py
│
├── .env.example             # Environment configuration template
├── .env                     # Your environment configuration (gitignored)
├── .gitignore              # Git ignore patterns
├── README.md               # This file
├── pyproject.toml          # Project metadata and dependencies
└── requirements.txt        # Pip requirements (generated from pyproject.toml)
```

### Core Components

#### 1. Configuration Management (`config.py`)

- Dataclass-based configuration with type hints
- Environment variable validation
- Default value handling
- OpenAI API settings management

#### 2. AI Assistant Core (`assistant.py`)

- OpenAI GPT-4o-mini integration
- Async API calls for better performance
- Function calling implementation
- Conversation history management
- Error handling and retry logic

#### 3. Tool System (`tools/`)

- **Base Classes**: Abstract interfaces for tool development
- **Registry Pattern**: Automatic tool discovery and registration
- **Type Safety**: Pydantic models for parameter validation
- **Extensibility**: Easy addition of new tools

#### 4. CLI Interface (`main.py`)

- Rich-powered beautiful terminal UI
- Interactive command processing
- Message formatting and display
- Graceful error handling and user feedback

## Technical Implementation

### Type Hints and Modern Python

This project uses comprehensive type hints following modern Python standards:

```python
# Modern generic syntax (Python 3.9+)
from typing import Any, Protocol, TypeAlias
from collections.abc import Callable, Awaitable

# Type aliases for complex types
MessageHistory: TypeAlias = list[dict[str, Any]]
ToolFunction: TypeAlias = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]

# Protocol classes for interfaces
class ToolProtocol(Protocol):
    name: str
    description: str

    async def execute(self, params: dict[str, Any]) -> dict[str, Any]: ...

# Optional types with union syntax
def process_response(data: str | None = None) -> dict[str, Any]: ...
```

### Async Implementation

The assistant uses async/await for optimal performance:

```python
import asyncio
from openai import AsyncOpenAI

class Assistant:
    async def chat(self, message: str) -> str:
        # Non-blocking OpenAI API calls
        response = await self.client.chat.completions.create(...)

        # Parallel tool execution when needed
        if multiple_tools:
            results = await asyncio.gather(*tool_tasks)

        return formatted_response
```

### Security Considerations

- **Safe Expression Evaluation**: Calculator uses `ast.literal_eval` instead of `eval()`
- **Input Validation**: Pydantic models validate all tool parameters
- **API Key Security**: Environment variables with validation
- **Error Boundaries**: Graceful handling of API failures and invalid inputs

## Development Guide

### Adding a New Tool

1. **Create Tool File**: Add your tool in the appropriate location (`src/tools/` or `src/`)

```python
from typing import Any
from pydantic import BaseModel, Field
from src.tools.base import Tool

class MyToolParams(BaseModel):
    """Parameters for MyTool."""
    input_data: str = Field(..., description="Input data to process")
    optional_param: int = Field(default=42, description="Optional parameter")

class MyTool(Tool):
    """Description of what your tool does."""

    name = "my_tool"
    description = "Detailed description for the AI model"
    parameters_model = MyToolParams

    async def execute(self, params: MyToolParams) -> dict[str, Any]:
        """Execute the tool with validated parameters."""
        # Implement your tool logic here
        result = f"Processed: {params.input_data}"

        return {
            "success": True,
            "result": result,
            "metadata": {"param_used": params.optional_param}
        }
```

2. **Register Tool**: Import in the appropriate `__init__.py` or ensure auto-discovery

3. **Test Tool**: Create corresponding test file in `tests/`

4. **Update Documentation**: Add tool description to this README

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_calculator.py -v
```

### Development Workflow

1. **Feature Branch**: Create a new branch for your feature

   ```bash
   git checkout -b feat/new-awesome-tool
   ```

2. **Development**: Implement your changes with proper type hints

3. **Testing**: Write and run tests for your changes

4. **Documentation**: Update README and docstrings

5. **Commit**: Use meaningful commit messages

   ```bash
   git commit -m "feat: add awesome new tool for X functionality"
   ```

6. **Pull Request**: Submit PR with clear description

## Configuration Reference

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# OpenAI Configuration (Required)
OPENAI_API_KEY=sk-your-secret-api-key-here

# OpenAI Settings (Optional - with defaults)
OPENAI_MODEL=gpt-4o-mini           # AI model to use
OPENAI_TEMPERATURE=0.7             # Response creativity (0.0-2.0)
OPENAI_MAX_TOKENS=1000             # Maximum response length
OPENAI_TIMEOUT=30                  # API timeout in seconds

# Application Settings (Optional)
LOG_LEVEL=INFO                     # Logging level
DEBUG=false                        # Enable debug mode
```

### pyproject.toml Dependencies

The project uses modern Python packaging with these key dependencies:

```toml
dependencies = [
    "openai>=1.0.0",              # OpenAI API client
    "python-dotenv>=1.0.0",       # Environment variable management
    "rich>=13.0.0",               # Beautiful terminal UI
    "pydantic>=2.0.0",            # Data validation and settings
    "httpx>=0.24.0",              # HTTP client for API calls
    "asyncio-compat",             # Async compatibility utilities
]
```

## Troubleshooting

### Common Issues

#### 1. OpenAI API Key Issues

```bash
Error: OpenAI API key not found or invalid
```

**Solution**:

- Ensure `.env` file exists with valid `OPENAI_API_KEY`
- Check that your API key has sufficient credits
- Verify the key format (should start with `sk-`)

#### 2. Import Errors

```bash
ModuleNotFoundError: No module named 'src'
```

**Solution**:

- Install project in editable mode: `uv pip install -e .`
- Ensure you're in the project root directory
- Check that virtual environment is activated

#### 3. uv Command Not Found

```bash
bash: uv: command not found
```

**Solution**:

- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart your terminal or source your shell profile
- Alternative: Use pip instead: `pip install -e .`

#### 4. Tool Registration Issues

```bash
Warning: No tools found in registry
```

**Solution**:

- Check that tool files are properly imported
- Verify tool classes inherit from base `Tool` class
- Ensure `__init__.py` files exist in tool directories

### Debug Mode

Enable debug logging for troubleshooting:

```env
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG
```

Run with verbose output:

```bash
python -m src.main --debug
```

## Performance Considerations

### Async Operations

- All OpenAI API calls are non-blocking
- Multiple tool calls can execute in parallel
- Conversation history is managed efficiently

### Memory Management

- Conversation history is limited to prevent memory issues
- Large tool outputs are truncated appropriately
- Connection pooling for HTTP requests

### Rate Limiting

- Built-in respect for OpenAI API rate limits
- Automatic retry with exponential backoff
- Graceful degradation on API failures

## Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/amazing-feature`
3. Make your changes with proper type hints and tests
4. Run the test suite: `uv run pytest`
5. Update documentation as needed
6. Submit a pull request

### Code Standards

- **Type Hints**: All functions must have type annotations
- **Docstrings**: Use Google-style docstrings for all public functions
- **Testing**: Maintain >90% test coverage
- **Formatting**: Use `black` and `isort` for code formatting
- **Linting**: Pass `flake8` and `mypy` checks

### Commit Messages

Follow conventional commit format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring

## Roadmap

### Planned Features

- [ ] **Plugin System**: External tool loading from packages
- [ ] **Conversation Persistence**: Save/load chat history
- [ ] **Multi-Model Support**: Support for Claude, Gemini, etc.
- [ ] **Web Interface**: Optional web UI alongside CLI
- [ ] **Tool Marketplace**: Community-contributed tools
- [ ] **Configuration UI**: Interactive setup and configuration
- [ ] **Voice Integration**: Speech-to-text and text-to-speech

### Performance Improvements

- [ ] **Caching**: Tool result caching for repeated queries
- [ ] **Streaming**: Real-time response streaming
- [ ] **Batch Processing**: Multiple query handling
- [ ] **Background Processing**: Long-running task support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- **OpenAI** for providing the GPT-4o-mini model and excellent API
- **Astral** for the amazing `uv` package manager
- **Pydantic** team for robust data validation
- **Rich** library for beautiful terminal interfaces
- **Python community** for the extensive ecosystem

## Support and Community

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/your-username/tool-calling-chatbot/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/your-username/tool-calling-chatbot/discussions)
- **Documentation**: Comprehensive docs available in the `/docs` directory
- **Examples**: See `/examples` directory for advanced usage patterns

---

**Built with ❤️ using modern Python practices and OpenAI's powerful language models.**

_Happy coding! 🚀_
