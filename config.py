#!/usr/bin/env python3
"""
Configuration module for CLI Chat Tool
"""

import os
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config(BaseModel):
    """Configuration class for CLI Chat Tool"""
    
    # Default configuration values
    default_model: str = "gpt-3.5-turbo"
    default_system_message: str = "You are a helpful AI assistant."
    config_file: str = "config.json"
    
    def __init__(self, **data):
        """Initialize configuration
        
        Loads configuration from file if it exists, otherwise uses defaults
        """
        super().__init__(**data)
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file if it exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                
                # Update configuration values
                for key, value in config_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
            except Exception as e:
                print(f"Error loading configuration: {str(e)}")
    
    def save_config(self) -> None:
        """Save configuration to file"""
        config_data = self.dict()
        
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
    
    def update(self, **kwargs) -> None:
        """Update configuration values
        
        Args:
            **kwargs: Key-value pairs to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Save updated configuration
        self.save_config()