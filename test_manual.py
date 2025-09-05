#!/usr/bin/env python3
"""
Manual test script for CLI Chat Tool

This script provides a simple way to test the CLI Chat Tool without running the full application.
It tests key components individually to ensure they're working correctly.
"""

import os
import sys
from rich.console import Console

# Import our modules
from chat_engine import ChatEngine
from cli_interface import CLIInterface
from config import Config
from ml_models import ModelFactory
from conversation import ConversationManager

# Initialize console
console = Console()


def test_config():
    """Test the Config class"""
    console.print("\n[bold blue]Testing Config...[/bold blue]")
    
    config = Config()
    console.print(f"Default model: {config.default_model}")
    console.print(f"Default system message: {config.default_system_message}")
    
    # Test saving and loading config
    config.default_model = "test-model"
    config.default_system_message = "Test system message"
    config.save_config()
    
    # Load config
    new_config = Config()
    console.print(f"Loaded model: {new_config.default_model}")
    console.print(f"Loaded system message: {new_config.default_system_message}")
    
    # Reset config
    config.default_model = "gpt-3.5-turbo"
    config.default_system_message = "You are a helpful assistant."
    config.save_config()
    
    console.print("[green]Config test completed[/green]")


def test_model_factory():
    """Test the ModelFactory class"""
    console.print("\n[bold blue]Testing ModelFactory...[/bold blue]")
    
    # Get supported models
    models = ModelFactory.get_supported_models()
    console.print("Supported models:")
    for provider, model_list in models.items():
        console.print(f"\n[bold]{provider}:[/bold]")
        for model in model_list:
            console.print(f"  • {model}")
    
    # Check if API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        console.print("[yellow]Warning: OPENAI_API_KEY not set. Skipping model creation test.[/yellow]")
        return
    
    # Create a model
    try:
        model = ModelFactory.create_model("gpt-3.5-turbo")
        console.print(f"Created model: {model.__class__.__name__}")
        console.print(f"Model provider: {model.provider}")
    except Exception as e:
        console.print(f"[red]Error creating model: {str(e)}[/red]")
    
    console.print("[green]ModelFactory test completed[/green]")


def test_cli_interface():
    """Test the CLIInterface class"""
    console.print("\n[bold blue]Testing CLIInterface...[/bold blue]")
    
    cli = CLIInterface()
    
    # Test displaying welcome message
    cli.display_welcome()
    
    # Test displaying help
    cli.display_help()
    
    # Test displaying messages
    cli.display_info("This is an info message")
    cli.display_error("This is an error message")
    cli.display_ai_response("This is an AI response with **markdown** support")
    
    console.print("[green]CLIInterface test completed[/green]")


def main():
    """Run all tests"""
    console.print("[bold]Running manual tests for CLI Chat Tool[/bold]")
    
    # Run tests
    test_config()
    test_model_factory()
    test_cli_interface()
    
    console.print("\n[bold green]All tests completed![/bold green]")


if __name__ == "__main__":
    main()