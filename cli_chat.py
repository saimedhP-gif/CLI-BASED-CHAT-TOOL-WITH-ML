#!/usr/bin/env python3
"""
CLI Chat Tool - A command-line interface for chatting with AI language models
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

# Import our modules
from chat_engine import ChatEngine
from config import Config
from cli_interface import CLIInterface
from conversation import ConversationManager
from ml_models import ModelFactory

# Initialize typer app
app = typer.Typer(help="CLI Chat Tool - Chat with AI language models from your terminal")

# Load environment variables
load_dotenv()

# Initialize configuration
config = Config()

# Initialize console
console = Console()

# Initialize CLI interface
cli = CLIInterface()


@app.command()
def chat(
    model: str = typer.Option(config.default_model, "--model", "-m", help="AI model to use"),
    system_message: str = typer.Option(
        config.default_system_message, "--system", "-s", help="System message to set context"
    ),
    load_conversation: str = typer.Option(
        None, "--load", "-l", help="Load a conversation from a file"
    ),
):
    """Start an interactive chat session with an AI language model"""
    # Display welcome message
    cli.display_welcome()
    
    # Initialize chat engine with the specified model
    chat_engine = ChatEngine(model=model, system_message=system_message)
    
    # Initialize conversation manager
    conversation_manager = ConversationManager(chat_engine, console)
    
    # Load conversation if specified
    if load_conversation:
        if os.path.exists(load_conversation):
            if conversation_manager.load_conversation(load_conversation):
                cli.display_info(f"Loaded conversation from {load_conversation}")
            else:
                cli.display_error(f"Failed to load conversation from {load_conversation}")
        else:
            cli.display_error(f"File not found: {load_conversation}")
    
    # Register command handlers
    cli.register_command("/clear", lambda _: (chat_engine.clear_history(), cli.display_info("Conversation history cleared")))
    cli.register_command("/save", lambda args: save_conversation(conversation_manager, args))
    cli.register_command("/load", lambda _: load_conversation_interactive(conversation_manager))
    cli.register_command("/model", lambda args: change_model(chat_engine, args))
    cli.register_command("/system", lambda args: (chat_engine.set_system_message(args), cli.display_info("System message updated")))
    cli.register_command("/tokens", lambda _: display_token_usage(chat_engine))
    cli.register_command("/history", lambda _: display_history(chat_engine))
    cli.register_command("/models", lambda _: list_available_models())
    
    # Main chat loop
    while True:
        # Get user input
        user_input = cli.get_user_input()
        
        # Process commands
        if user_input.startswith("/"):
            if cli.process_command(user_input):
                break
            continue
        
        # Process regular message
        try:
            # Show thinking indicator
            with cli.display_thinking():
                response = chat_engine.send_message(user_input)
            
            # Display the response
            cli.display_ai_response(response)
        except Exception as e:
            cli.display_error(str(e))


def save_conversation(conversation_manager: ConversationManager, filename: str) -> None:
    """Save the current conversation
    
    Args:
        conversation_manager: The conversation manager instance
        filename: The filename to save to (optional)
    """
    try:
        filepath = conversation_manager.save_conversation(filename if filename else None)
        cli.display_info(f"Conversation saved to {filepath}")
    except Exception as e:
        cli.display_error(f"Failed to save conversation: {str(e)}")


def load_conversation_interactive(conversation_manager: ConversationManager) -> None:
    """Interactively load a conversation
    
    Args:
        conversation_manager: The conversation manager instance
    """
    try:
        selected_file = conversation_manager.interactive_load()
        if selected_file:
            if conversation_manager.load_conversation(selected_file):
                cli.display_info(f"Loaded conversation from {selected_file}")
            else:
                cli.display_error(f"Failed to load conversation")
    except Exception as e:
        cli.display_error(f"Error loading conversation: {str(e)}")


def change_model(chat_engine: ChatEngine, model_name: str) -> None:
    """Change the AI model
    
    Args:
        chat_engine: The chat engine instance
        model_name: The name of the model to switch to
    """
    try:
        chat_engine.set_model(model_name)
        cli.display_info(f"Model changed to {model_name} ({chat_engine.model.provider})")
    except ValueError as e:
        cli.display_error(str(e))


def list_available_models() -> None:
    """List all available models"""
    try:
        supported_models = ModelFactory.get_supported_models()
        
        cli.console.print("[bold blue]Available Models:[/bold blue]")
        for provider, models in supported_models.items():
            cli.console.print(f"\n[bold]{provider}:[/bold]")
            for model in models:
                cli.console.print(f"  • {model}")
    except Exception as e:
        cli.display_error(f"Error listing models: {str(e)}")


def display_token_usage(chat_engine: ChatEngine) -> None:
    """Display token usage statistics
    
    Args:
        chat_engine: The chat engine instance
    """
    usage = chat_engine.get_token_usage()
    
    cli.console.print("[bold blue]Token Usage:[/bold blue]")
    cli.console.print(f"Prompt tokens: {usage['prompt_tokens']}")
    cli.console.print(f"Completion tokens: {usage['completion_tokens']}")
    cli.console.print(f"Total tokens: {usage['total_tokens']}")


def display_history(chat_engine: ChatEngine) -> None:
    """Display conversation history
    
    Args:
        chat_engine: The chat engine instance
    """
    history = chat_engine.get_conversation_history()
    if not history:
        cli.display_info("No conversation history")
        return
    
    cli.console.print("[bold blue]Conversation History:[/bold blue]")
    for message in history:
        if message["role"] == "system":
            cli.console.print(f"\n[bold yellow]System:[/bold yellow] {message['content']}")
        elif message["role"] == "user":
            cli.console.print(f"\n[bold green]You:[/bold green] {message['content']}")
        elif message["role"] == "assistant":
            cli.console.print(f"\n[bold blue]AI:[/bold blue] {message['content']}")


if __name__ == "__main__":
    app()