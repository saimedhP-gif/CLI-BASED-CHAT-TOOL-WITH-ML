#!/usr/bin/env python3
"""
Conversation Manager - Handles conversation history and user interaction
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from chat_engine import ChatEngine


class ConversationManager:
    """Manages conversation history and user interaction"""
    
    def __init__(self, chat_engine: ChatEngine, console: Console):
        """Initialize the conversation manager
        
        Args:
            chat_engine: The chat engine to use
            console: The rich console for output
        """
        self.chat_engine = chat_engine
        self.console = console
        self.conversation_dir = "conversations"
        
        # Create conversations directory if it doesn't exist
        os.makedirs(self.conversation_dir, exist_ok=True)
    
    def save_conversation(self, filename: Optional[str] = None) -> str:
        """Save the current conversation to a file
        
        Args:
            filename: The filename to save to (optional)
        
        Returns:
            The path to the saved file
        """
        if not filename:
            # Generate a filename based on the current date and time
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        # Ensure the filename has a .json extension
        if not filename.endswith(".json"):
            filename += ".json"
        
        # Create the full path
        filepath = os.path.join(self.conversation_dir, filename)
        
        # Save the conversation
        self.chat_engine.save_conversation(filepath)
        
        return filepath
    
    def load_conversation(self, filepath: str) -> bool:
        """Load a conversation from a file
        
        Args:
            filepath: The path to the file to load
        
        Returns:
            True if the conversation was loaded successfully, False otherwise
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Clear current conversation history
            self.chat_engine.clear_history()
            
            # Set the model
            if "model" in data:
                self.chat_engine.set_model(data["model"])
            
            # Load the conversation history
            for message in data["conversation"]:
                self.chat_engine.conversation_history.append(message)
            
            # Load token usage if available
            if "token_usage" in data:
                self.chat_engine.token_usage = data["token_usage"]
            
            return True
        
        except Exception as e:
            self.console.print(f"[bold red]Error loading conversation: {str(e)}[/bold red]")
            return False
    
    def list_conversations(self) -> List[str]:
        """List all saved conversations
        
        Returns:
            A list of conversation filenames
        """
        if not os.path.exists(self.conversation_dir):
            return []
        
        # Get all JSON files in the conversations directory
        files = [f for f in os.listdir(self.conversation_dir) if f.endswith(".json")]
        files.sort(reverse=True)  # Sort by newest first
        
        return files
    
    def display_conversation_info(self, filepath: str) -> None:
        """Display information about a conversation
        
        Args:
            filepath: The path to the conversation file
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Extract metadata
            timestamp = data.get("timestamp", "Unknown")
            model = data.get("model", "Unknown")
            provider = data.get("provider", "Unknown")
            message_count = len(data.get("conversation", []))
            token_usage = data.get("token_usage", {"total_tokens": 0})["total_tokens"]
            
            # Format the timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = timestamp
            
            # Display the information
            self.console.print(Panel.fit(
                f"Timestamp: {formatted_time}\n"
                f"Model: {model} ({provider})\n"
                f"Messages: {message_count}\n"
                f"Total Tokens: {token_usage}",
                title=f"Conversation: {os.path.basename(filepath)}",
                border_style="blue"
            ))
        
        except Exception as e:
            self.console.print(f"[bold red]Error reading conversation: {str(e)}[/bold red]")
    
    def interactive_load(self) -> bool:
        """Interactively load a conversation
        
        Returns:
            True if a conversation was loaded, False otherwise
        """
        # List available conversations
        files = self.list_conversations()
        
        if not files:
            self.console.print("[bold yellow]No saved conversations found[/bold yellow]")
            return False
        
        # Display the list of conversations
        self.console.print("[bold blue]Available conversations:[/bold blue]")
        for i, filename in enumerate(files):
            self.console.print(f"[{i+1}] {filename}")
        
        # Ask the user to select a conversation
        choice = Prompt.ask("Enter the number of the conversation to load (or 'cancel')", default="cancel")
        
        if choice.lower() == "cancel":
            return False
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(files):
                filepath = os.path.join(self.conversation_dir, files[index])
                
                # Display information about the conversation
                self.display_conversation_info(filepath)
                
                # Confirm loading
                if Confirm.ask("Load this conversation?"):
                    return self.load_conversation(filepath)
        except ValueError:
            pass
        
        self.console.print("[bold yellow]Conversation loading cancelled[/bold yellow]")
        return False