#!/usr/bin/env python3
"""
Machine Learning Models - Handles integration with various AI language models
"""

import os
from typing import List, Dict, Any, Optional, Union
from abc import ABC, abstractmethod

from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys
openai_api_key = os.getenv("OPENAI_API_KEY", "sk-placeholder")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

# Only create the OpenAI client if we need it (lazy initialization)
client = None


class ModelResponse:
    """Standardized response from any model"""
    
    def __init__(self, text: str, usage: Dict[str, int] = None):
        """Initialize a model response
        
        Args:
            text: The response text
            usage: Token usage statistics
        """
        self.text = text
        self.usage = usage or {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


class BaseModel(ABC):
    """Base class for all language models"""
    
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]]) -> ModelResponse:
        """Generate a response from the model
        
        Args:
            messages: The conversation history
        
        Returns:
            A ModelResponse object
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the model name
        
        Returns:
            The model name
        """
        pass
    
    @property
    @abstractmethod
    def provider(self) -> str:
        """Get the model provider
        
        Returns:
            The model provider
        """
        pass


class OpenAIModel(BaseModel):
    """OpenAI language model"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize an OpenAI model
        
        Args:
            model_name: The name of the OpenAI model to use
        """
        self._model_name = model_name
        
        # List of supported models
        self.supported_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        
        # Validate model name
        if model_name not in self.supported_models:
            raise ValueError(f"Model '{model_name}' is not supported. Supported models: {', '.join(self.supported_models)}")
    
    def generate_response(self, messages: List[Dict[str, str]]) -> ModelResponse:
        """Generate a response from the OpenAI model
        
        Args:
            messages: The conversation history
        
        Returns:
            A ModelResponse object
        
        Raises:
            Exception: If there's an error communicating with the API
        """
        try:
            # For testing or when no API key is available
            if openai_api_key == "sk-placeholder" or openai_api_key == "your_openai_api_key_here":
                # Return a mock response for testing
                return ModelResponse(
                    text="This is a mock response. Please set a valid OPENAI_API_KEY in the .env file to get actual AI responses.",
                    usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
                )
            
            # Lazy initialization of the OpenAI client
            global client
            if client is None:
                client = OpenAI(api_key=openai_api_key)
                
            # Send the conversation to the API using the new client format
            response = client.chat.completions.create(
                model=self._model_name,
                messages=messages
            )
            
            # Extract the response content
            text = response.choices[0].message.content
            
            # Extract usage statistics
            usage = None
            if hasattr(response, "usage"):
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            
            return ModelResponse(text=text, usage=usage)
        
        except Exception as e:
            error_str = str(e)
            # Handle specific error cases with user-friendly messages
            if "insufficient_quota" in error_str:
                error_message = "Your OpenAI API key has exceeded its quota. Please check your billing details at https://platform.openai.com/account/billing or use a different API key."
            else:
                error_message = f"Error communicating with OpenAI: {error_str}"
            
            raise Exception(error_message)
    
    @property
    def name(self) -> str:
        """Get the model name
        
        Returns:
            The model name
        """
        return self._model_name
    
    @property
    def provider(self) -> str:
        """Get the model provider
        
        Returns:
            The model provider
        """
        return "OpenAI"


class GeminiModel(BaseModel):
    """Google's Gemini language model"""
    
    def __init__(self, model_name: str = "gemini-pro"):
        """Initialize a Gemini model
        
        Args:
            model_name: The name of the Gemini model to use
        """
        self._model_name = model_name
        
        # List of supported models
        self.supported_models = ["gemini-pro", "gemini-pro-vision", "gemini-1.5-flash"]
        
        # Validate model name
        if model_name not in self.supported_models:
            raise ValueError(f"Model '{model_name}' is not supported. Supported models: {', '.join(self.supported_models)}")
    
    def generate_response(self, messages: List[Dict[str, str]]) -> ModelResponse:
        """Generate a response from the Gemini model
        
        Args:
            messages: The conversation history
        
        Returns:
            A ModelResponse object
        
        Raises:
            Exception: If there's an error communicating with the API
        """
        try:
            if not gemini_api_key:
                return ModelResponse(
                    text="Please set a valid GEMINI_API_KEY in the .env file to use Gemini models.",
                    usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
                )
            
            # Initialize Gemini model and chat
            model = genai.GenerativeModel(self._model_name)
            chat = model.start_chat()
            
            # Process all messages in the conversation history
            for message in messages:
                role = message["role"]
                content = message["content"]
                
                if role == "system":
                    # Add system message as a user message with [System] prefix
                    chat.send_message(f"[System] {content}")
                elif role == "user":
                    chat.send_message(content)
                elif role == "assistant":
                    # Skip assistant messages as they're already in the history
                    continue
            
            # Get the response from the last message
            response = chat.last
            if not response:
                # If no response in history, send the last user message again
                last_user_message = next((msg["content"] for msg in reversed(messages) if msg["role"] == "user"), None)
                if last_user_message:
                    response = chat.send_message(last_user_message)
                else:
                    raise Exception("No user messages found in conversation history")
            
            # Extract response text
            text = response.text
            
            # Gemini doesn't provide token usage, so we'll estimate
            last_user_message = next((msg["content"] for msg in reversed(messages) if msg["role"] == "user"), "")
            usage = {
                "prompt_tokens": len(last_user_message.split()),
                "completion_tokens": len(text.split()),
                "total_tokens": len(last_user_message.split()) + len(text.split())
            }
            
            return ModelResponse(text=text, usage=usage)
            
        except Exception as e:
            error_str = str(e)
            if "invalid_api_key" in error_str.lower():
                error_message = "Invalid Gemini API key. Please check your GEMINI_API_KEY in the .env file."
            elif "quota_exceeded" in error_str.lower():
                error_message = "Your Gemini API key has exceeded its quota. Please check your quota limits or use a different API key."
            else:
                error_message = f"Error communicating with Gemini: {error_str}"
            raise Exception(error_message)
    
    @property
    def name(self) -> str:
        """Get the model name
        
        Returns:
            The model name
        """
        return self._model_name
    
    @property
    def provider(self) -> str:
        """Get the model provider
        
        Returns:
            The model provider
        """
        return "Google"


class ModelFactory:
    """Factory for creating language models"""
    
    @staticmethod
    def create_model(model_name: str) -> BaseModel:
        """Create a language model
        
        Args:
            model_name: The name of the model to create
        
        Returns:
            A BaseModel instance
        
        Raises:
            ValueError: If the model is not supported
        """
        # OpenAI models
        openai_models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        
        # Gemini models
        gemini_models = ["gemini-pro", "gemini-pro-vision", "gemini-1.5-flash"]
        
        if model_name in openai_models:
            return OpenAIModel(model_name=model_name)
        elif model_name in gemini_models:
            return GeminiModel(model_name=model_name)
        
        raise ValueError(f"Model '{model_name}' is not supported")
    
    @staticmethod
    def get_supported_models() -> Dict[str, List[str]]:
        """Get a list of supported models grouped by provider
        
        Returns:
            A dictionary of supported models grouped by provider
        """
        return {
            "OpenAI": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            "Google": ["gemini-pro", "gemini-pro-vision", "gemini-1.5-flash"],
            # Add other providers here
        }