# CLI Chat Tool - User Guide

This guide will help you get started with the CLI Chat Tool, a command-line interface for chatting with AI language models.

## Getting Started

### Prerequisites

1. Python 3.7 or higher installed on your system
2. An OpenAI API key (for OpenAI models)
3. A Google Gemini API key (for Gemini models)

### Installation

1. Clone or download the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project directory with your API keys:
   ```
   # OpenAI API key (required for OpenAI models)
   OPENAI_API_KEY=your_openai_api_key_here

   # Gemini API key (required for Gemini models)
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Basic Usage

### Starting the Application

To start the chat application with default settings:

```
python cli_chat.py
```

This will start the application with the default model (gpt-3.5-turbo) and system message. You can also use Gemini models by specifying them with the `--model` option.

### Command-line Options

You can customize the application behavior with these options:

- `--model` or `-m`: Specify the AI model to use
- `--system` or `-s`: Set a system message to provide context
- `--load` or `-l`: Load a conversation from a file

Example:
```
python cli_chat.py --model gpt-4 --system "You are a helpful coding assistant."
```

## Chat Commands

During the chat session, you can use these commands:

### Basic Commands

- `/help`: Display available commands and their descriptions
- `/exit` or `/quit`: Exit the application
- `/clear`: Clear the conversation history

### Conversation Management

- `/save <filename>`: Save the current conversation to a file
  Example: `/save my_chat`

- `/load`: Load a saved conversation
  The application will display a list of available conversation files to choose from.

- `/history`: Show the current conversation history

### Model and System Settings

- `/model <model_name>`: Change the AI model
  Examples:
  - `/model gpt-4` (OpenAI model)
  - `/model gemini-pro` (Gemini model)

- `/models`: List all available AI models

- `/system <message>`: Set a system message to guide the AI's behavior
  Example: `/system You are a helpful assistant that speaks like Shakespeare.`

### Statistics

- `/tokens`: Show token usage statistics for the current conversation

## Tips for Effective Use

1. **Set a clear system message**: Use the system message to guide the AI's behavior and set expectations.

2. **Save important conversations**: Use the `/save` command to preserve valuable conversations.

3. **Monitor token usage**: Keep an eye on token usage with the `/tokens` command to manage API costs.

4. **Clear history when changing topics**: Use `/clear` when starting a new topic to avoid context confusion.

5. **Try different models**: Different models have different capabilities. Use `/models` to see available options and `/model` to switch between them.

## Troubleshooting

### API Key Issues

If you see an error about an invalid API key:
1. Check that your `.env` file exists in the project directory
2. Verify that the appropriate API key is correct and active:
   - For OpenAI models: `OPENAI_API_KEY=your_openai_key_here`
   - For Gemini models: `GEMINI_API_KEY=your_gemini_key_here`
3. Make sure you're using the correct API key for the selected model

### Connection Problems

If the application fails to connect to the API:
1. Check your internet connection
2. Verify that your API key has sufficient quota
3. Try again later as the API might be experiencing high demand

## Support

For issues, questions, or feature requests, please open an issue on the project's GitHub repository.