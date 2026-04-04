"""
LLM client for Azure OpenAI GPT endpoints.
"""
import os
import requests
from dotenv import load_dotenv

class AzureOpenAILLMClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        if not all([self.api_key, self.endpoint, self.deployment]):
            raise EnvironmentError("Missing Azure OpenAI credentials in .env file")

    def ask(self, prompt, text):
        url = f"{self.endpoint}openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        data = {
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            "max_tokens": 2048,
            "temperature": 0.3
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
