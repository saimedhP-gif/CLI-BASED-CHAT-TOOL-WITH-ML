#!/usr/bin/env python3
"""
Chat Engine - Handles interactions with AI language models
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

from dotenv import load_dotenv
from ml_models import ModelFactory, BaseModel, ModelResponse

# Load environment variables
load_dotenv()


class ChatEngine:
    """Handles interactions with AI language models"""
    
    def __init__(self, model: str = "gpt-3.5-turbo", system_message: str = ""):
        """Initialize the chat engine
        
        Args:
            model: The AI model to use
            system_message: The system message to set context
        """
        self.model_name = model
        self.system_message = system_message
        self.conversation_history = []
        self.token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        
        # Initialize the model
        self.model = ModelFactory.create_model(model)
        
        # Add system message if provided
        if system_message:
            self.conversation_history.append({"role": "system", "content": system_message})
    
    def set_model(self, model_name: str) -> None:
        """Change the AI model
        
        Args:
            model_name: The new model to use
        
        Raises:
            ValueError: If the model is not supported
        """
        try:
            # Create a new model instance
            self.model = ModelFactory.create_model(model_name)
            self.model_name = model_name
        except ValueError as e:
            # Get supported models
            supported_models = ModelFactory.get_supported_models()
            flat_models = [model for provider_models in supported_models.values() for model in provider_models]
            
            raise ValueError(f"Model '{model_name}' is not supported. Supported models: {', '.join(flat_models)}")
    
    def set_system_message(self, system_message: str) -> None:
        """Set or update the system message
        
        Args:
            system_message: The new system message
        """
        # Remove existing system message if any
        self.conversation_history = [msg for msg in self.conversation_history if msg["role"] != "system"]
        
        # Add new system message
        if system_message:
            self.conversation_history.insert(0, {"role": "system", "content": system_message})
        
        self.system_message = system_message
    
    def clear_history(self) -> None:
        """Clear the conversation history"""
        self.conversation_history = []
        
        # Re-add system message if it exists
        if self.system_message:
            self.conversation_history.append({"role": "system", "content": self.system_message})
    
    def send_message(self, message: str) -> str:
        """Send a message to the AI model and get a response
        
        Args:
            message: The user message to send
        
        Returns:
            The AI model's response
        
        Raises:
            Exception: If there's an error communicating with the API
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            # Generate response using the model
            model_response = self.model.generate_response(self.conversation_history)
            
            # Extract the response text
            ai_message = model_response.text
            
            # Update token usage statistics
            if model_response.usage:
                self.token_usage["prompt_tokens"] += model_response.usage["prompt_tokens"]
                self.token_usage["completion_tokens"] += model_response.usage["completion_tokens"]
                self.token_usage["total_tokens"] += model_response.usage["total_tokens"]
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            return ai_message
        
        except Exception as e:
            # Remove the user message from history on error
            self.conversation_history.pop()
            raise Exception(f"Error communicating with AI: {str(e)}")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history
        
        Returns:
            The conversation history as a list of message dictionaries
        """
        return self.conversation_history
    
    def get_token_usage(self) -> Dict[str, int]:
        """Get token usage statistics
        
        Returns:
            A dictionary with token usage statistics
        """
        return self.token_usage
    
    def save_conversation(self, filename: str) -> None:
        """Save the conversation history to a file
        
        Args:
            filename: The name of the file to save to
        """
        # Create a dictionary with metadata and conversation
        data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.model_name,
            "provider": self.model.provider,
            "token_usage": self.token_usage,
            "conversation": self.conversation_history
        }
        
        # Save to file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)