from langchain_ollama import OllamaLLM
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TweetGenerator:
    def __init__(self, model_type: str = "ollama", model_name: str = "llama3"):
        """
        Initialize the tweet generator with either Ollama or Hugging Face model.
        
        Args:
            model_type (str): Either "ollama" or "huggingface"
            model_name (str): Name of the model to use
        """
        self.model_type = model_type
        self.model_name = model_name
        self.llm = self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the appropriate model based on model_type."""
        if self.model_type == "ollama":
            return OllamaLLM(model=self.model_name)
        elif self.model_type == "huggingface":
            # Try to get token from environment variable or .env file
            hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
            if not hf_token:
                raise ValueError(
                    "HUGGINGFACE_API_TOKEN not found. Please set it in your environment "
                    "or create a .env file with HUGGINGFACE_API_TOKEN=your_token_here"
                )
            return HuggingFaceHub(
                repo_id=self.model_name,
                model_kwargs={"temperature": 0.7},
                huggingfacehub_api_token=hf_token
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def generate_tweets(self, text: str, num_tweets: int, prompt_template: Optional[str] = None) -> list:
        """
        Generate tweets from input text.
        
        Args:
            text (str): Input text to generate tweets from
            num_tweets (int): Number of tweets to generate
            prompt_template (str, optional): Custom prompt template
            
        Returns:
            list: Generated tweets
        """
        if prompt_template is None:
            prompt_template = """Based on the following text, generate {num_tweets} engaging tweets. 
            Make them concise, informative, and engaging. Each tweet should be under 280 characters.
            Format the response as a JSON array of strings.
            
            Text: {text}
            
            Tweets:"""
        
        try:
            # Create prompt template
            template = PromptTemplate(
                input_variables=["text", "num_tweets"],
                template=prompt_template
            )
            
            # Generate the prompt
            prompt = template.format(text=text, num_tweets=num_tweets)
            
            # Generate response
            response = self.llm.invoke(prompt)
            
            # Clean up the response
            generated_text = response.strip('[]').split('\n')
            tweets = [tweet.strip().strip('"') for tweet in generated_text if tweet.strip()]
            
            return tweets
        except Exception as e:
            raise Exception(f"Error generating tweets: {str(e)}") 