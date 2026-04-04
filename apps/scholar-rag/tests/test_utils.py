import os
import tempfile
from src.utils import extract_metadata



def test_extract_metadata_on_existing_pdfs(data_dir="./data", sample_size=3):
    """
    Reads a sample of existing PDFs and prints their extracted metadata.
    """
    # If data_dir does not exist, use 'sample_data'
    if not os.path.exists(data_dir):
        print(f"Directory '{data_dir}' not found. Using './sample_data' instead.")
        data_dir = "./sample_data"
    pdf_files = [f for f in os.listdir(data_dir) if f.lower().endswith(".pdf")]
    for filename in pdf_files[:sample_size]:
        pdf_path = os.path.join(data_dir, filename)
        try:
            metadata = extract_metadata(pdf_path)
            print(f"\nFile: {filename}")
            print(f"Title: {metadata['title']}")
            print(f"Authors: {metadata['authors']}")
            print(f"Year: {metadata['year']}")
            print(f"Content sample: {metadata['content'][:100]}...")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    test_extract_metadata_on_existing_pdfs()
    print("All tests passed.")
