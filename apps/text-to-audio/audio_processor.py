"""
Audio processing logic for text-to-speech conversion using Azure Cognitive Services.
"""
import azure.cognitiveservices.speech as speechsdk
import os
from typing import Optional, List
from dotenv import load_dotenv


class AudioProcessor:
    """Handles text-to-speech conversion using Azure Speech Services."""
    
    def __init__(self):
        """Initialize the audio processor with Azure credentials from environment."""
        load_dotenv()
        
        # Get credentials from environment
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")
        
        if not speech_key or not speech_region:
            raise EnvironmentError(
                "Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION in .env file"
            )
        
        # Setup speech config
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, 
            region=speech_region
        )
        self.speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
        
        # Create output directory
        self.output_directory = "audio_output"
        os.makedirs(self.output_directory, exist_ok=True)
    
    def set_voice(self, voice_name: str) -> None:
        """Set the voice for speech synthesis."""
        self.speech_config.speech_synthesis_voice_name = voice_name
    
    def generate_file_path(self, base_filename: str, segment_index: int = 0, total_segments: int = 1) -> str:
        """Generate file path for audio segment."""
        if total_segments == 1:
            filename = f"{base_filename}.wav"
        else:
            filename = f"{base_filename}_part_{segment_index + 1}.wav"
        
        return os.path.join(self.output_directory, filename)
    
    def synthesize_text(
        self, 
        text: str, 
        output_path: str, 
        speech_rate: float = 1.0
    ) -> Optional[bytes]:
        """
        Convert text to speech and save to output path.
        
        Args:
            text: Text to convert to speech
            output_path: Path where to save the audio file
            speech_rate: Speech rate multiplier (0.5 to 2.0)
            
        Returns:
            Audio data as bytes if successful, None otherwise
        """
        try:
            # Create audio config with direct output to final location
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            # Apply speech rate using SSML if not default
            if speech_rate != 1.0:
                result = self._synthesize_with_ssml(text, speech_rate, synthesizer)
            else:
                result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                # Read the saved file and return as bytes
                with open(output_path, "rb") as f:
                    return f.read()
            else:
                raise Exception(f"Speech synthesis failed: {result.reason}")
                
        except Exception as e:
            raise Exception(f"Error in text-to-speech conversion: {str(e)}")
    
    def _synthesize_with_ssml(
        self, 
        text: str, 
        speech_rate: float, 
        synthesizer: speechsdk.SpeechSynthesizer
    ) -> speechsdk.SpeechSynthesisResult:
        """Synthesize text using SSML for speech rate control."""
        rate_percent = f"{int(speech_rate * 100)}%"
        ssml_text = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <voice name="{self.speech_config.speech_synthesis_voice_name}">
                <prosody rate="{rate_percent}">
                    {text}
                </prosody>
            </voice>
        </speak>
        """
        return synthesizer.speak_ssml_async(ssml_text).get()


def get_available_voices() -> dict:
    """Get available Azure neural voices."""
    return {
        "Aria (Female, US)": "en-US-AriaNeural",
        "Guy (Male, US)": "en-US-GuyNeural",
        "Jenny (Female, US)": "en-US-JennyNeural",
        "Davis (Male, US)": "en-US-DavisNeural",
        "Emma (Female, US)": "en-US-EmmaNeural"
    }
