from langchain_ollama import OllamaLLM
import sys
import requests
import time

def check_ollama_running():
    try:
        response = requests.get("http://localhost:11434/api/version")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def test_ollama():
    print("\n=== Testing Ollama Installation ===\n")
    
    # Check if Ollama is running
    if not check_ollama_running():
        print("Ollama is not running. Please start Ollama by running:")
        print("ollama serve")
        print("\nIf you get a port error, try these steps:")
        print("1. Check if Ollama is already running in the background")
        print("2. If needed, restart your computer")
        print("3. Or try running: taskkill /F /IM ollama.exe (Windows) or pkill ollama (Linux/Mac)")
        return False
    
    try:
        # Try to initialize Ollama
        print("1. Testing Ollama connection...")
        llm = OllamaLLM(model="llama3")  # Changed from llama3 to llama2
        
        # Try a simple prompt
        print("2. Testing model response...")
        test_prompt = "Say 'Hello, Ollama is working!' in one line."
        response = llm.invoke(test_prompt)
        
        print("\nSuccess! Ollama is working correctly.")
        print("\nTest Response:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print("\nError: Ollama is not working correctly.")
        print(f"Error message: {str(e)}")
        print("\nPlease check:")
        print("1. Is Ollama installed?")
        print("2. Is the llama2 model pulled? (Try running 'ollama pull llama2')")
        print("3. If needed, try restarting Ollama")
        return False

if __name__ == "__main__":
    test_ollama() 