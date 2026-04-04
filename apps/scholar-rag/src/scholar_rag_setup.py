"""
Azure AI Search Setup with PDF Processing

This script demonstrates how to:
1. Set up Azure AI Search
2. Process PDF files from the data directory
3. Extract metadata (title, authors, year)
4. Create and populate an Azure Search index

Prerequisites:
- Azure AI Search service
- Azure OpenAI service
- Python packages: azure-search-documents, azure-identity, PyPDF2, python-dotenv
"""

import os
import re
from typing import Dict, Any
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)
from PyPDF2 import PdfReader
from utils import extract_metadata, safe_document_id  # change to absolute import


def setup_search_client() -> tuple[SearchIndexClient, str]:
    """Initialize Azure AI Search client and configuration.
    
    Returns:
        tuple: (SearchIndexClient instance, index_name)
    """
    # Load environment variables
    load_dotenv()
    
    # Azure AI Search configuration
    search_service_name = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
    search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = "research-papers"
    
    # Create search client
    credential = AzureKeyCredential(search_api_key)
    index_client = SearchIndexClient(
        endpoint=search_service_name,
        credential=credential
    )
    
    return index_client, index_name


def create_search_index(index_client: SearchIndexClient, index_name: str) -> None:
    """Create or update the search index with defined schema.
    
    Args:
        index_client: Azure Search Index Client
        index_name: Name of the index to create
    """
    # Define index fields
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String, searchable=True),
        SearchableField(name="authors", type=SearchFieldDataType.String, searchable=True),
        SimpleField(name="year", type=SearchFieldDataType.Int32),
        SearchableField(name="content", type=SearchFieldDataType.String, searchable=True),
        SimpleField(name="file_path", type=SearchFieldDataType.String)
    ]
    
    # Create the index
    index = SearchIndex(name=index_name, fields=fields)
    try:
        result = index_client.create_or_update_index(index)
        print(f"Index {result.name} created/updated successfully")
    except Exception as e:
        print(f"Error creating index: {e}")

        def process_and_upload_pdfs(
            search_client: SearchClient,
            data_dir: str = "./data"
        ) -> None:
            """Process PDF files and upload them to the search index.
            
            Args:
                search_client: Azure Search Client
                data_dir: Directory containing PDF files
            """
            # If data_dir does not exist, use 'sample_data'
            if not os.path.exists(data_dir):
                print(f"Directory '{data_dir}' not found. Using './sample_data' instead.")
                data_dir = "./sample_data"

            for filename in os.listdir(data_dir):
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(data_dir, filename)
                    try:
                        metadata = extract_metadata(pdf_path)
                        document = {
                            "id": safe_document_id(filename),
                            "file_path": pdf_path,
                            **metadata
                        }
                        search_client.upload_documents(documents=[document])
                        print(f"Processed and uploaded: {filename}")
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")


def verify_index_population(search_client: SearchClient) -> None:
    """Verify that documents were successfully uploaded to the index.
    
    Args:
        search_client: Azure Search Client
    """
    # Count documents
    result = search_client.get_document_count()
    print(f"Number of documents in index: {result}")
    
    # Display sample documents
    results = search_client.search(search_text="*", select=["title", "authors", "year"])
    print("\nSample documents in index:")
    for result in results:
        print(f"\nTitle: {result['title']}")
        print(f"Authors: {result['authors']}")
        print(f"Year: {result['year']}")
        print("---")


def main():
    """Main function to run the PDF processing and indexing pipeline."""
    # Setup
    index_client, index_name = setup_search_client()
    
    # Create index
    create_search_index(index_client, index_name)
    
    # Initialize search client for document uploads
    search_client = SearchClient(
        endpoint=os.getenv('AZURE_SEARCH_SERVICE_ENDPOINT'),
        index_name=index_name,
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
    )
    endpoint = os.getenv('AZURE_SEARCH_SERVICE_ENDPOINT')
    print(f"endpoint: {endpoint}")
    print(f"index_name: {index_name}")
    print(f"credential: {os.getenv('AZURE_SEARCH_API_KEY')}")
    # Process and upload PDFs
    process_and_upload_pdfs(search_client)
    
    # Verify results
    verify_index_population(search_client)


if __name__ == "__main__":
    main()