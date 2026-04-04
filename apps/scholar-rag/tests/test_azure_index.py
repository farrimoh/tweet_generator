import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient

def test_index_exists(index_name="research-papers"):
    """
    Test if the Azure Cognitive Search index exists and has the expected fields.
    Also print all field names and the index length.
    """
    load_dotenv()
    endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_API_KEY")
    assert endpoint and api_key, "Azure Search endpoint or API key not set in environment variables."

    index_client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))
    indexes = [idx.name for idx in index_client.list_indexes()]
    assert index_name in indexes, f"Index '{index_name}' does not exist."

    index = index_client.get_index(index_name)
    field_names = [field.name for field in index.fields]
    expected_fields = {"id", "title", "authors", "year", "content", "file_path"}
    assert expected_fields.issubset(set(field_names)), f"Index fields missing: {expected_fields - set(field_names)}"

    print(f"Index '{index_name}' exists and has all expected fields.")
    print(f"All field names: {field_names}")

    # Print index length (number of documents)
    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(api_key))
    count = search_client.get_document_count()
    print(f"Index '{index_name}' contains {count} documents.")

if __name__ == "__main__":
    test_index_exists()
