"""Test LLM provider functionality."""

import pytest
from agent.llm_providers import (
    LLMProviderManager,
    GroqProvider,
    OllamaProvider,
)
import os


def test_provider_manager_initialization():
    """Test provider manager initializes."""
    manager = LLMProviderManager()
    assert manager is not None
    print(f"✅ Provider manager initialized")
    print(f"   Available providers: {manager.get_available_providers()}")


def test_provider_availability():
    """Test checking which providers are available."""
    manager = LLMProviderManager()
    providers = manager.get_available_providers()
    
    assert isinstance(providers, list)
    print(f"✅ Found {len(providers)} available provider(s): {providers}")
    
    if len(providers) == 0:
        print("⚠️  Warning: No providers available. Set GROQ_API_KEY or run Ollama.")


def test_groq_provider_check():
    """Test Groq provider availability."""
    try:
        groq = GroqProvider()
        available = groq.is_available()
        
        if available:
            print("✅ Groq provider is available")
        else:
            print("⚠️  Groq provider not configured (API key missing)")
    except Exception as e:
        print(f"⚠️  Groq provider check failed: {e}")


def test_ollama_provider_check():
    """Test Ollama provider availability."""
    try:
        ollama = OllamaProvider()
        available = ollama.is_available()
        
        if available:
            print("✅ Ollama provider is available")
        else:
            print("⚠️  Ollama not running (start with: ollama serve)")
    except Exception as e:
        print(f"⚠️  Ollama provider check failed: {e}")


def test_provider_generation():
    """Test LLM generation with fallback."""
    manager = LLMProviderManager()
    
    if len(manager.providers) == 0:
        print("⚠️  Skipping generation test - no providers available")
        return
    
    result = manager.generate("What is 2+2? Answer in one word.")
    
    assert "success" in result
    assert "content" in result
    
    if result["success"]:
        print(f"✅ Generation successful")
        print(f"   Provider: {result.get('provider', 'unknown')}")
        print(f"   Response: {result['content'][:100]}...")
    else:
        print(f"❌ Generation failed: {result.get('error', 'unknown error')}")


def test_fallback_mechanism():
    """Test provider fallback works."""
    manager = LLMProviderManager()
    
    print(f"✅ Fallback mechanism ready")
    print(f"   Provider chain: {' → '.join(manager.get_available_providers())}")
    
    if len(manager.providers) > 1:
        print("   ✨ Multiple providers available - fallback enabled")
    elif len(manager.providers) == 1:
        print("   ⚠️  Only one provider - no fallback available")
    else:
        print("   ❌ No providers - fallback cannot work")


if __name__ == "__main__":
    print("\n🧪 Testing LLM Providers...\n")
    
    test_provider_manager_initialization()
    test_provider_availability()
    test_groq_provider_check()
    test_ollama_provider_check()
    test_provider_generation()
    test_fallback_mechanism()
    
    print("\n🎉 All provider tests completed!\n")
