#!/usr/bin/env python3
"""
Test script to verify Gemini Flash 1.5 integration
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml_models import ModelFactory, GeminiModel

def test_gemini_flash():
    """Test Gemini Flash 1.5 model"""
    print("Testing Gemini Flash 1.5 integration...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Create Gemini Flash 1.5 model
        model = ModelFactory.create_model("gemini-1.5-flash")
        print(f"✓ Successfully created model: {model.name} ({model.provider})")
        
        # Test with a simple message
        test_messages = [
            {"role": "user", "content": "Hello! Please respond with 'Gemini Flash 1.5 is working correctly!'"}
        ]
        
        print("Sending test message...")
        response = model.generate_response(test_messages)
        
        print(f"✓ Response received: {response.text}")
        print(f"✓ Token usage: {response.usage}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_supported_models():
    """Test that gemini-1.5-flash is in supported models"""
    print("\nTesting supported models...")
    
    supported = ModelFactory.get_supported_models()
    gemini_models = supported.get("Google", [])
    
    if "gemini-1.5-flash" in gemini_models:
        print("✓ gemini-1.5-flash found in supported models")
        print(f"  Google models: {gemini_models}")
        return True
    else:
        print("✗ gemini-1.5-flash not found in supported models")
        print(f"  Google models: {gemini_models}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("GEMINI FLASH 1.5 TEST")
    print("=" * 50)
    
    # Test 1: Check supported models
    models_ok = test_supported_models()
    
    # Test 2: Test actual model functionality
    if models_ok:
        flash_ok = test_gemini_flash()
    else:
        flash_ok = False
    
    print("\n" + "=" * 50)
    if models_ok and flash_ok:
        print("🎉 ALL TESTS PASSED! Gemini Flash 1.5 is ready to use.")
    else:
        print("❌ SOME TESTS FAILED. Please check the errors above.")
    print("=" * 50)
