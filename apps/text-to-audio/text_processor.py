"""
Text processing utilities for extracting and processing text from various sources.
"""
import os
import tempfile
from typing import Optional, List
from urllib.parse import urlparse
import re
from datetime import datetime

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextExtractor:
    """Handles text extraction from various sources."""
    
    @staticmethod
    def extract_from_pdf(pdf_file) -> Optional[str]:
        """Extract text from PDF using langchain."""
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.read())
                tmp_file_path = tmp_file.name
            
            # Use langchain PDF loader
            loader = PyPDFLoader(tmp_file_path)
            pages = loader.load()
            
            # Combine all pages
            text = "\n".join([page.page_content for page in pages])
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def extract_from_url(url: str) -> Optional[str]:
        """Extract text from URL using langchain."""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Please enter a valid URL")
            
            # Use langchain web loader with proper headers
            loader = WebBaseLoader(
                url,
                header_template={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 TextToAudio/1.0'
                }
            )
            documents = loader.load()
            
            # Combine all documents
            text = "\n".join([doc.page_content for doc in documents])


            text = re.sub(r'\n\s*\n+', '\n', text.strip())
            # Clean up text        
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from URL: {str(e)}")


class TextProcessor:
    """Handles text processing and chunking."""
    
    @staticmethod
    def split_text_for_tts(text: str, max_length: int = 5000) -> List[str]:
        """Split text into chunks suitable for TTS."""
        if not text:
            return []
        
        # Use langchain text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_length,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        return chunks
    
    @staticmethod
    def _create_session_folder(base_path: str, source_name: str = "", source_type: str = "text") -> str:
        """Create a unique session folder for audio files."""
        safe_name = TextProcessor.create_safe_filename(source_name, source_type)
        session_folder = os.path.join(base_path, safe_name)
        
        # Ensure unique folder name if it already exists
        counter = 1
        original_folder = session_folder
        while os.path.exists(session_folder):
            session_folder = f"{original_folder}_{counter}"
            counter += 1
        
        # Create the folder
        os.makedirs(session_folder, exist_ok=True)
        return session_folder
    
    @staticmethod
    def create_safe_filename(source_name: str, source_type: str = "text") -> str:
        """Create a safe filename based on source."""
        if source_type == "pdf" and source_name:
            # Remove .pdf extension and clean the name
            base_name = os.path.splitext(source_name)[0]
        elif source_type == "url" and source_name:
            # Extract meaningful part from URL
            parsed = urlparse(source_name)
            # Try to get a meaningful name from the URL path
            path_parts = [part for part in parsed.path.split('/') if part]
            if path_parts:
                base_name = path_parts[-1]
                # Remove file extensions
                base_name = os.path.splitext(base_name)[0]
            else:
                # Use domain name if no meaningful path
                base_name = parsed.netloc.replace('www.', '')
        else:
            # Default name for direct text input
            base_name = f"text_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Clean the filename - remove invalid characters
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', base_name)
        safe_name = re.sub(r'_+', '_', safe_name)  # Replace multiple underscores with single
        safe_name = safe_name.strip('_')  # Remove leading/trailing underscores
        
        # Ensure it's not too long
        if len(safe_name) > 50:
            safe_name = safe_name[:50]
        
        return safe_name if safe_name else f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    @staticmethod
    def get_text_statistics(text: str) -> dict:
        """Get statistics about the text."""
        return {
            "characters": len(text),
            "words": len(text.split()),
            "lines": len(text.split('\n'))
        }
    
    @staticmethod
    def optimize_text_for_audio(text: str, llm_client, custom_instructions: str = "") -> str:
        """
        Send the text to an LLM with a prompt to optimize it for audio learning material.
        The LLM should make only small adjustments for natural listening, not change the meaning/content.
        Args:
            text: The original text to optimize
            llm_client: An object with an `ask(prompt, text)` method or similar
            custom_instructions: Additional custom instructions to include in the prompt
        Returns:
            The optimized text as returned by the LLM
        """
        prompt = (
            "You are an expert at preparing text for audio narration. "
            "Optimize the following text for listening as a learning material. "
            "Do not change the meaning or content, but make small adjustments so it sounds natural and clear when read aloud. "
            "Keep all information, but improve flow, add brief pauses where needed, and clarify any awkward phrasing. "
            "Return only the improved text. Avoid using any markdown or formatting tags. "
        )
        if custom_instructions:
            prompt += f" {custom_instructions.strip()}"

        return llm_client.ask(prompt, text)
