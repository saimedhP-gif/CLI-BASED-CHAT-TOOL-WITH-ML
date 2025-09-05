#!/usr/bin/env python3
"""
CLI Interface - Handles the command-line interface for the chat tool
"""

import os
import sys
from typing import List, Dict, Any, Optional, Callable

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live

# Initialize console for rich text formatting
console = Console()


class CLIInterface:
    """Handles the command-line interface for the chat tool"""
    
    def __init__(self):
        """Initialize the CLI interface"""
        self.console = Console()
        self.commands = {
            "/help": self.display_help,
            "/exit": self.exit_app,
            "/quit": self.exit_app,
            "/clear": None,  # Will be set by the main app
            "/save": None,  # Will be set by the main app
            "/load": None,  # Will be set by the main app
            "/model": None,  # Will be set by the main app
            "/models": None,  # Will be set by the main app
            "/system": None,  # Will be set by the main app
            "/tokens": None,  # Will be set by the main app
            "/history": None,  # Will be set by the main app
        }
    
    def register_command(self, command: str, handler: Callable) -> None:
        """Register a command handler
        
        Args:
            command: The command to register (e.g., "/clear")
            handler: The function to call when the command is used
        """
        if command in self.commands:
            self.commands[command] = handler
    
    def display_welcome(self) -> None:
        """Display welcome message and instructions"""
        self.console.print(Panel.fit(
            "[bold blue]CLI Chat Tool[/bold blue]\n"
            "Chat with AI language models directly from your terminal.\n"
            "Type [bold green]/help[/bold green] to see available commands.",
            title="Welcome",
            border_style="blue"
        ))
    
    def display_help(self, *args) -> None:
        """Display help information"""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="green")
        help_table.add_column("Description")
        
        help_table.add_row("/help", "Show this help message")
        help_table.add_row("/exit or /quit", "Exit the application")
        help_table.add_row("/clear", "Clear the conversation history")
        help_table.add_row("/save <filename>", "Save the conversation to a file")
        help_table.add_row("/load", "Load a saved conversation")
        help_table.add_row("/model <model_name>", "Change the AI model")
        help_table.add_row("/models", "List available AI models")
        help_table.add_row("/system <message>", "Set a system message")
        help_table.add_row("/tokens", "Show token usage statistics")
        help_table.add_row("/history", "Show conversation history")
        
        self.console.print(help_table)
    
    def exit_app(self, *args) -> bool:
        """Exit the application
        
        Returns:
            True to indicate the app should exit
        """
        self.console.print("[bold blue]Goodbye![/bold blue]")
        return True
    
    def get_user_input(self) -> str:
        """Get input from the user
        
        Returns:
            The user's input
        """
        return Prompt.ask("\n[bold green]You[/bold green]")
    
    def display_ai_response(self, response: str) -> None:
        """Display the AI's response
        
        Args:
            response: The AI's response text
        """
        self.console.print("\n[bold blue]AI[/bold blue]")
        self.console.print(Markdown(response))
    
    def display_error(self, error_message: str) -> None:
        """Display an error message
        
        Args:
            error_message: The error message to display
        """
        self.console.print(f"[bold red]Error: {error_message}[/bold red]")
    
    def display_info(self, message: str) -> None:
        """Display an informational message
        
        Args:
            message: The message to display
        """
        self.console.print(f"[bold yellow]{message}[/bold yellow]")
    
    def display_thinking(self, message: str = "Thinking") -> Live:
        """Display a thinking/loading indicator
        
        Args:
            message: The message to display while thinking
            
        Returns:
            A Live context manager for the progress indicator
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn(f"[bold blue]{message}...[/bold blue]"),
            transient=True
        )
        live = Live(progress, refresh_per_second=10)
        live.start()
        progress.add_task("thinking", total=None)
        return live
    
    def process_command(self, user_input: str) -> bool:
        """Process a command from the user
        
        Args:
            user_input: The user's input
            
        Returns:
            True if the app should exit, False otherwise
        """
        if not user_input.startswith("/"):
            return False
        
        # Split the input into command and arguments
        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Check if the command is registered
        if command in self.commands and self.commands[command] is not None:
            result = self.commands[command](args)
            return result if result is not None else False
        else:
            self.display_error(f"Unknown command: {command}")
            return False