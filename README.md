# AI Tool-Calling Chatbot

A powerful command-line AI assistant that integrates with OpenAI's GPT-4o models and features function calling capabilities. This chatbot can perform calculations, fetch weather information, and get news updates through integrated APIs.

## ✨ Features

- **🤖 OpenAI Integration**: Uses GPT-4o and GPT-4o-mini models with function calling
- **🧮 Calculator Tool**: Safe mathematical expression evaluation
- **🌤️ Weather API**: Real-time weather information for any location
- **📰 News API**: Latest news articles with date filtering and search
- **🎨 Rich CLI Interface**: Beautiful terminal UI with colors and formatting
- **💬 Interactive Chat**: Continuous conversation with context memory
- **🔧 Function Calling**: Automatic tool selection based on user queries

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **uv** - Modern Python package manager
- **OpenAI API Key** - From [OpenAI Platform](https://platform.openai.com/api-keys)
- **WeatherAPI Key** - From [WeatherAPI](https://www.weatherapi.com/)
- **NewsAPI Key** - From [NewsAPI](https://newsapi.org/)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/rasheed1306/tool-calling-chatbot.git
   cd tool-calling-chatbot
   ```

2. **Install dependencies with uv**

   ```bash
   uv sync
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your API keys:

   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   WEATHER_API_KEY=your-weatherapi-key-here
   NEWS_API_KEY=your-newsapi-key-here
   ```

4. **Run the chatbot**
   ```bash
   uv run python src/main.py
   ```

## 🎯 Usage

### Interactive Commands

- **Regular chat**: Ask questions or make requests naturally
- **`clear`**: Clear conversation history
- **`q`**: Quit the application

## 📁 Project Structure

```
tool-calling-chatbot/
├── src/
│   ├── main.py              # Main application and CLI interface
│   └── helpers/             # Tool implementations
│       ├── __init__.py      # Package initialization
│       ├── calculator.py    # Mathematical calculations
│       ├── weather.py       # Weather API integration
│       └── news.py          # News API integration
├── .env.example             # Environment template
├── .env                     # Your API keys (gitignored)
├── .gitignore              # Git ignore patterns
├── pyproject.toml          # Project dependencies and metadata
├── uv.lock                 # Dependency lock file
└── README.md               # Project documentation
```

---

**Built with ❤️ using modern Python and AI technologies**
