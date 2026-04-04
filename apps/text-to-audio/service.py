"""
Core business logic orchestrating the text-to-audio conversion process.
"""
from typing import List, Tuple
import os
from datetime import datetime

# Set USER_AGENT environment variable to avoid warnings from web scraping libraries
if 'USER_AGENT' not in os.environ:
    os.environ['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 TextToAudio/1.0'

from audio_processor import AudioProcessor, get_available_voices
from text_processor import TextExtractor, TextProcessor


class TextToAudioService:
    """Main service class orchestrating the text-to-audio conversion."""
    
    def __init__(self):
        """Initialize the service with all required components."""
        self.audio_processor = AudioProcessor()
        self.text_extractor = TextExtractor()
        self.text_processor = TextProcessor()
    
    def get_available_voices(self) -> dict:
        """Get available voices for TTS."""
        return get_available_voices()
    
    def set_voice(self, voice_name: str) -> None:
        """Set the voice for speech synthesis."""
        self.audio_processor.set_voice(voice_name)
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file."""
        return self.text_extractor.extract_from_pdf(pdf_file)
    
    def extract_text_from_url(self, url: str) -> str:
        """Extract text from URL."""
        return self.text_extractor.extract_from_url(url)
    
    def get_text_statistics(self, text: str) -> dict:
        """Get statistics about the text."""
        return self.text_processor.get_text_statistics(text)
    
    def convert_text_to_audio(
        self, 
        text: str, 
        source_name: str = "", 
        source_type: str = "text",
        speech_rate: float = 1.0,
        optimize_for_audio: bool = True,
        llm_client=None,
        custom_instructions: str = None
    ) -> Tuple[List[bytes], List[str]]:
        """
        Convert text to audio files, optionally optimizing text for audio using LLM.

        Args:
            text: Text to convert
            source_name: Name of the source (filename, URL, etc.)
            source_type: Type of source ('pdf', 'url', 'text')
            speech_rate: Speech rate multiplier
            optimize_for_audio: Whether to optimize text for audio using LLM
            llm_client: LLM client instance (required if optimize_for_audio is True)
            custom_instructions: Custom instruction for text optimization (optional)

        Returns:
            Tuple of (audio_data_list, file_paths_list)
        """
        # Optionally optimize text for audio
        if optimize_for_audio and llm_client is not None:
            text = self.text_processor.optimize_text_for_audio(
                text, llm_client, custom_instructions=custom_instructions
            )

        # Create safe filename and session folder
        base_filename = self.text_processor.create_safe_filename(source_name, source_type)
        session_folder = self._create_session_folder(base_filename)
        
        # Split text into chunks
        text_chunks = self.text_processor.split_text_for_tts(text, max_length=5000)
        
        # Convert each chunk to audio
        audio_data_list = []
        file_paths = []
        
        for i, chunk in enumerate(text_chunks):
            try:
                # Generate file path within the session folder
                file_path = self._generate_session_file_path(
                    session_folder, base_filename, i, len(text_chunks)
                )
                
                # Convert to audio
                audio_data = self.audio_processor.synthesize_text(
                    text=chunk,
                    output_path=file_path,
                    speech_rate=speech_rate
                )
                
                audio_data_list.append(audio_data)
                file_paths.append(file_path)
                
            except Exception as e:
                raise Exception(f"Error converting chunk {i+1} to audio: {str(e)}")
        
        return audio_data_list, file_paths
    
    def get_output_info(self, file_paths: List[str]) -> dict:
        """Get information about output files."""
        return {
            "directory": self.audio_processor.output_directory,
            "files": [os.path.basename(path) for path in file_paths],
            "total_files": len(file_paths)
        }
    
    def get_chunk_count(self, text: str) -> int:
        """Get the number of chunks the text will be split into."""
        chunks = self.text_processor.split_text_for_tts(text, max_length=5000)
        return len(chunks)

    def _create_session_folder(self, base_filename: str) -> str:
        """Create a session folder for organizing output files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_name = f"{base_filename}_{timestamp}"
        session_folder = os.path.join(self.audio_processor.output_directory, session_name)
        
        # Create the folder if it doesn't exist
        os.makedirs(session_folder, exist_ok=True)
        
        return session_folder
    
    def _generate_session_file_path(self, session_folder: str, base_filename: str, chunk_index: int, total_chunks: int) -> str:
        """Generate file path for a chunk within the session folder."""
        if total_chunks == 1:
            filename = f"{base_filename}.wav"
        else:
            # Pad chunk numbers with zeros for proper sorting
            padding = len(str(total_chunks))
            filename = f"{base_filename}_part_{chunk_index + 1:0{padding}d}_of_{total_chunks}.wav"
        
        return os.path.join(session_folder, filename)