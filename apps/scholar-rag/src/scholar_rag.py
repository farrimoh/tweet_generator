import os
import logging
from typing import Optional
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from utils import sanitize_key  # import the sanitize_key function

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def setup_clients() -> tuple[SearchClient, AzureOpenAI]:
    """Initialize Azure AI Search and OpenAI clients.
    
    Returns:
        tuple: (SearchClient instance, AzureOpenAI instance)
    """
    logger.debug("Loading environment variables.")
    load_dotenv()
    
    # Azure AI Search configuration
    search_service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
    search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = "research-papers"
    
    # Azure OpenAI configuration
    openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    logger.debug("Initializing Azure AI Search client.")
    search_client = SearchClient(
        endpoint=search_service_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(search_api_key)
    )
    
    logger.debug("Initializing Azure OpenAI client.")
    openai_client = AzureOpenAI(
        api_key=openai_api_key,
        api_version="2023-05-15",
        azure_endpoint=openai_endpoint
    )
    
    return search_client, openai_client

def get_answer(
    question: str,
    search_client: SearchClient,
    openai_client: AzureOpenAI,
    deployment_name: str,
    top_k: int = 3
) -> str:
    """Implement RAG pipeline to answer questions based on research papers.
    
    Args:
        question: User's question
        search_client: Azure Search Client
        openai_client: Azure OpenAI Client
        deployment_name: Name of the deployed model
        top_k: Number of documents to retrieve
        
    Returns:
        str: Generated answer
    """
    logger.info("Searching for relevant documents.")
    search_results = search_client.search(
        search_text=question,
        select=["title", "authors", "content"],
        top=top_k
    )
    
    context = ""
    for result in search_results:
        # Sanitize document key if needed (example usage)
        if 'id' in result:
            result['id'] = sanitize_key(result['id'])
        context += f"Title: {result['title']}\n"
        context += f"Authors: {result['authors']}\n"
        context += f"Content: {result['content']}\n\n"
    
    logger.info("Generating answer using Azure OpenAI.")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that answers questions based on the provided research papers. "
                      "Use only the information from the provided context to answer the question. "
                      "If you don't know the answer, say so."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]
    
    response = openai_client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def interactive_qa(
    search_client: SearchClient,
    openai_client: AzureOpenAI,
    deployment_name: str
) -> None:
    """Run interactive question-answering session.
    
    Args:
        search_client: Azure Search Client
        openai_client: Azure OpenAI Client
        deployment_name: Name of the deployed model
    """
    logger.info("Interactive Question-Answering Session started.")
    logger.info("Enter 'quit' to exit")
    logger.info("-" * 50)
    
    while True:
        question = input("\nEnter your question: ")
        if question.lower() == 'quit':
            logger.info("Exiting interactive session.")
            break
        
        answer = get_answer(question, search_client, openai_client, deployment_name)
        logger.info(f"Answer: {answer}")

def main():
    """Main function to run the RAG pipeline."""
    try:
        logger.debug("Setting up clients.")
        search_client, openai_client = setup_clients()
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        logger.debug("Clients set up successfully.")
        sample_question = "What are the main findings of the research papers about machine learning?"
        logger.info(f"Testing with sample question: {sample_question}")
        logger.debug("Calling get_answer for sample question.")
        answer = get_answer(sample_question, search_client, openai_client, deployment_name)
        logger.info(f"Answer: {answer}")
        
        logger.debug("Starting interactive QA session.")
        interactive_qa(search_client, openai_client, deployment_name)
        
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    # Set logger to debug for main flow
    logger.setLevel(logging.DEBUG)
    main()
