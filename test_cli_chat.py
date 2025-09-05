#!/usr/bin/env python3
"""
Test suite for CLI Chat Tool
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules to test
from chat_engine import ChatEngine
from cli_interface import CLIInterface
from config import Config
from ml_models import ModelFactory, OpenAIModel, BaseModel, ModelResponse


class TestChatEngine(unittest.TestCase):
    """Test the ChatEngine class"""

    def setUp(self):
        """Set up test environment"""
        self.engine = ChatEngine()
        # Mock the model to avoid API calls
        self.engine.model = MagicMock()
        mock_response = ModelResponse(
            text="Test response",
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        )
        self.engine.model.generate_response.return_value = mock_response

    def test_initialization(self):
        """Test ChatEngine initialization"""
        self.assertIsNotNone(self.engine.model)
        history = self.engine.get_conversation_history()
        if history:  # Check if there's a system message
            self.assertEqual(history[0]["role"], "system")

    def test_set_model(self):
        """Test setting a new model"""
        with patch('ml_models.ModelFactory.create_model') as mock_create_model:
            mock_model = MagicMock()
            mock_create_model.return_value = mock_model
            
            self.engine.set_model("gpt-4")
            mock_create_model.assert_called_once_with("gpt-4")
            self.assertEqual(self.engine.model, mock_model)

    def test_set_system_message(self):
        """Test setting a system message"""
        self.engine.set_system_message("New system message")
        history = self.engine.get_conversation_history()
        self.assertEqual(history[0]["content"], "New system message")

    def test_clear_history(self):
        """Test clearing chat history"""
        # Add some messages
        self.engine.send_message("Hello")
        
        # Clear history
        self.engine.clear_history()
        
        # Should only have the system message if one was set
        history = self.engine.get_conversation_history()
        if self.engine.system_message:
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0]["role"], "system")
        else:
            self.assertEqual(len(history), 0)

    def test_send_message(self):
        """Test sending a message"""
        response = self.engine.send_message("Hello")
        
        # Check that the message was added to history
        history = self.engine.get_conversation_history()
        self.assertEqual(history[-2]["role"], "user")
        self.assertEqual(history[-2]["content"], "Hello")
        
        # Check that the response was added to history
        self.assertEqual(history[-1]["role"], "assistant")
        self.assertEqual(history[-1]["content"], "Test response")
        
        # Check that the response was returned
        self.assertEqual(response, "Test response")

    def test_get_token_usage(self):
        """Test getting token usage"""
        # Send a message to update token usage
        self.engine.send_message("Hello")
        
        # Check token usage
        usage = self.engine.get_token_usage()
        self.assertEqual(usage["prompt_tokens"], 10)
        self.assertEqual(usage["completion_tokens"], 5)
        self.assertEqual(usage["total_tokens"], 15)


class TestCLIInterface(unittest.TestCase):
    """Test the CLIInterface class"""

    def setUp(self):
        """Set up test environment"""
        self.cli = CLIInterface()

    def test_initialization(self):
        """Test CLIInterface initialization"""
        self.assertIsNotNone(self.cli.console)
        self.assertIn("/help", self.cli.commands)
        self.assertIn("/exit", self.cli.commands)

    def test_register_command(self):
        """Test registering a command"""
        test_handler = lambda x: f"Handled {x}"
        # The register_command method only updates existing commands
        existing_command = "/clear"
        self.cli.register_command(existing_command, test_handler)
        
        self.assertEqual(self.cli.commands[existing_command], test_handler)

    @patch('rich.prompt.Prompt.ask')
    def test_get_user_input(self, mock_ask):
        """Test getting user input"""
        mock_ask.return_value = "Test input"
        
        input_text = self.cli.get_user_input()
        self.assertEqual(input_text, "Test input")

    def test_process_command_exit(self):
        """Test processing exit command"""
        result = self.cli.process_command("/exit")
        self.assertTrue(result)

    def test_process_command_unknown(self):
        """Test processing unknown command"""
        with patch.object(self.cli, 'display_error') as mock_display_error:
            result = self.cli.process_command("/unknown")
            mock_display_error.assert_called_once()
            self.assertFalse(result)


class TestModelFactory(unittest.TestCase):
    """Test the ModelFactory class"""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_create_openai_model(self):
        """Test creating an OpenAI model"""
        model = ModelFactory.create_model("gpt-3.5-turbo")
        self.assertIsInstance(model, OpenAIModel)

    def test_create_invalid_model(self):
        """Test creating an invalid model"""
        with self.assertRaises(ValueError):
            ModelFactory.create_model("invalid-model")

    def test_get_supported_models(self):
        """Test getting supported models"""
        models = ModelFactory.get_supported_models()
        self.assertIsInstance(models, dict)
        self.assertIn("OpenAI", models)


if __name__ == "__main__":
    unittest.main()