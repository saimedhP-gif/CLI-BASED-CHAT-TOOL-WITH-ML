# CLI Chat Tool

A command-line interface for chatting with AI language models directly from your terminal.

## Features

- Interactive chat with AI language models
- Support for multiple AI models
- Customizable system messages
- Save conversation history to files
- Rich text formatting in the terminal

## Requirements

- Python 3.7+
- OpenAI API key (for OpenAI models)
- Google Gemini API key (for Gemini models)

## Installation

1. Clone this repository or download the files

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory with your API keys:

```
# OpenAI API key (required for OpenAI models)
OPENAI_API_KEY=your_openai_api_key_here

# Gemini API key (required for Gemini models)
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

Run the application:

```bash
python cli_chat.py
```

You can also specify options when starting:

```bash
python cli_chat.py --model gpt-4 --system "You are a helpful coding assistant."
```

Options:
- `--model` or `-m`: Specify the AI model to use (default: gpt-3.5-turbo)
- `--system` or `-s`: Set a system message to provide context
- `--load` or `-l`: Load a conversation from a file

### Available Commands

Once the chat is running, you can use these commands:

- `/help`: Show help information
- `/exit` or `/quit`: Exit the application
- `/clear`: Clear the conversation history
- `/save <filename>`: Save the conversation to a file
- `/load`: Load a saved conversation
- `/model <model_name>`: Change the AI model
- `/models`: List available AI models
- `/system <message>`: Set a system message
- `/tokens`: Show token usage statistics
- `/history`: Show conversation history

## Supported Models

### OpenAI Models
- gpt-3.5-turbo
- gpt-4
- gpt-4-turbo

### Google Models
- gemini-pro
- gemini-pro-vision

## License

MIT