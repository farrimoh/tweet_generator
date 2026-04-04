"""
Streamlit UI for Text-to-Audio Converter application.
"""
import streamlit as st
from typing import Optional

from service import TextToAudioService
from llm_client import AzureOpenAILLMClient


# Configure page
st.set_page_config(
    page_title="Text-to-Audio Converter",
    page_icon="🎵",
    layout="wide"
)


class TextToAudioUI:
    """Handles the Streamlit user interface for the text-to-audio converter."""
    
    def __init__(self):
        """Initialize the UI with the service layer."""
        try:
            self.service = TextToAudioService()
        except EnvironmentError as e:
            st.error(str(e))
            st.stop()
        except Exception as e:
            st.error(f"Error initializing application: {str(e)}")
            st.stop()
    
    def render_header(self) -> None:
        """Render the application header."""
        st.title("🎵 Text-to-Audio Converter")
        st.markdown("Convert text from PDFs or web pages to audio using Azure Text-to-Speech")
    
    def render_sidebar(self) -> tuple:
        """Render the sidebar configuration and return selected options."""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Voice selection
            voice_options = self.service.get_available_voices()
            selected_voice_name = st.selectbox(
                "Select Voice",
                options=list(voice_options.keys()),
                index=0
            )
            selected_voice = voice_options[selected_voice_name]
            self.service.set_voice(selected_voice)
            
            # Speech rate
            speech_rate = st.slider("Speech Rate", 0.5, 2.0, 1.0, 0.1)
            
            # Audio optimization toggle
            optimize_for_audio = st.checkbox(
                "Optimize text for audio (LLM)", value=True,
                help="Use AI to make small adjustments for natural listening."
            )
            
            return selected_voice, speech_rate, optimize_for_audio
    
    def render_input_section(self) -> tuple:
        """Render the input section and return text content and metadata."""
        st.header("📄 Input Source")
        
        # Initialize session state for input method
        if "input_method" not in st.session_state:
            st.session_state.input_method = "Upload PDF"
        
        input_method = st.radio(
            "Choose input method:",
            ["Upload PDF", "Enter URL", "Direct Text Input"],
            key="input_method_radio"
        )
        
        # Clear URL session state when switching methods
        if input_method != "Enter URL" and "url_text_content" in st.session_state:
            if st.session_state.input_method != input_method:
                st.session_state.url_text_content = ""
                st.session_state.url_source_name = ""
        
        st.session_state.input_method = input_method
        
        text_content = ""
        source_name = ""
        source_type = "text"
        
        if input_method == "Upload PDF":
            text_content, source_name, source_type = self._handle_pdf_input()
        elif input_method == "Enter URL":
            text_content, source_name, source_type = self._handle_url_input()
        else:
            text_content, source_name, source_type = self._handle_text_input()
        
        return text_content, source_name, source_type
    
    def _handle_pdf_input(self) -> tuple:
        """Handle PDF file upload."""
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload a PDF file to extract text from"
        )
        
        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                try:
                    text_content = self.service.extract_text_from_pdf(uploaded_file)
                    return text_content, uploaded_file.name, "pdf"
                except Exception as e:
                    st.error(str(e))
                    return "", "", "pdf"
        
        return "", "", "pdf"
    
    def _handle_url_input(self) -> tuple:
        """Handle URL input."""
        url = st.text_input(
            "Enter URL:",
            placeholder="https://example.com/article",
            help="Enter a URL to extract text from a webpage"
        )
        
        # Initialize session state for URL text if not exists
        if "url_text_content" not in st.session_state:
            st.session_state.url_text_content = ""
        if "url_source_name" not in st.session_state:
            st.session_state.url_source_name = ""
        
        if url and st.button("Extract Text from URL"):
            with st.spinner("Extracting text from URL..."):
                try:
                    text_content = self.service.extract_text_from_url(url)
                    # Store in session state to persist across reruns
                    st.session_state.url_text_content = text_content
                    st.session_state.url_source_name = url
                    st.success("✅ Text extracted successfully!")
                    
                    # Show preview of extracted text
                    if text_content:
                        preview = text_content[:200] + "..." if len(text_content) > 200 else text_content
                        st.info(f"**Preview:** {preview}")
                    
                    return text_content, url, "url"
                except Exception as e:
                    st.error(str(e))
                    st.session_state.url_text_content = ""
                    st.session_state.url_source_name = ""
                    return "", url, "url"
        
        # Return stored values if available
        if st.session_state.url_text_content:
            return st.session_state.url_text_content, st.session_state.url_source_name, "url"
        
        return "", "", "url"
    
    def _handle_text_input(self) -> tuple:
        """Handle direct text input."""
        text_content = st.text_area(
            "Enter text:",
            height=300,
            placeholder="Enter or paste your text here...",
            help="Enter the text you want to convert to audio"
        )
        return text_content, "", "text"
    
    def render_output_section(
        self, 
        text_content: str, 
        source_name: str, 
        source_type: str, 
        speech_rate: float,
        optimize_for_audio: bool
    ) -> None:
        """Render the audio output section."""
        st.header("🎵 Audio Output")
        
        if not text_content:
            st.info("👆 Please provide text input using one of the methods on the left")
            return
        
        # Display text preview and statistics
        self._render_text_preview(text_content)
        
        # Convert to audio button
        if st.button("🎵 Convert to Audio", type="primary"):
            self._handle_audio_conversion(text_content, source_name, source_type, speech_rate, optimize_for_audio)
    
    def _render_text_preview(self, text_content: str) -> None:
        """Render text preview and statistics."""
        with st.expander("📖 Extracted Text Preview", expanded=False):
            st.text_area("Text Content", text_content, height=200, disabled=True)
        
        # Text statistics
        stats = self.service.get_text_statistics(text_content)
        st.info(
            f"**Text Statistics:**\n"
            f"- Characters: {stats['characters']:,}\n"
            f"- Words: {stats['words']:,}\n"
            f"- Lines: {stats['lines']:,}"
        )
    
    def _handle_audio_conversion(
        self, 
        text_content: str, 
        source_name: str, 
        source_type: str, 
        speech_rate: float,
        optimize_for_audio: bool
    ) -> None:
        """Handle the audio conversion process."""
        with st.spinner("Converting text to audio... This may take a moment."):
            try:
                # Initialize LLM client if optimization is enabled
                llm_client = None
                if optimize_for_audio:
                    try:
                        llm_client = AzureOpenAILLMClient()
                    except Exception as e:
                        st.warning(f"Could not initialize LLM for text optimization: {str(e)}")
                        st.info("Proceeding without text optimization...")
                
                # Convert text to audio
                audio_data_list, file_paths = self.service.convert_text_to_audio(
                    text=text_content,
                    source_name=source_name,
                    source_type=source_type,
                    speech_rate=speech_rate,
                    optimize_for_audio=optimize_for_audio,
                    llm_client=llm_client
                )
                
                # Render results
                self._render_audio_results(audio_data_list, file_paths, source_name, source_type)
                
            except Exception as e:
                st.error(f"❌ Error during audio conversion: {str(e)}")
                st.error("Please check your Azure Speech Service configuration and try again.")
        
    def _render_audio_results(
        self, 
        audio_data_list: list, 
        file_paths: list, 
        source_name: str, 
        source_type: str
    ) -> None:
        """Render the audio conversion results."""
        st.success(f"✅ Audio conversion completed! Generated {len(audio_data_list)} audio segment(s)")
        
        # Show saved files info
        if file_paths:
            output_info = self.service.get_output_info(file_paths)
            st.info(f"💾 Audio files saved to: `{output_info['directory']}/`")
            for filename in output_info['files']:
                st.text(f"📁 {filename}")
        
        # Render audio players and download buttons
        for i, audio_data in enumerate(audio_data_list):
            st.subheader(f"Audio Segment {i + 1}")
            st.audio(audio_data, format="audio/wav")
            
            # Download button
            if file_paths:
                filename = output_info['files'][i] if i < len(output_info['files']) else f"segment_{i+1}.wav"
            else:
                filename = f"audio_segment_{i + 1}.wav"
            
            st.download_button(
                label=f"⬇️ Download Segment {i + 1}",
                data=audio_data,
                file_name=filename,
                mime="audio/wav"
            )
    
    def render_footer(self) -> None:
        """Render the application footer."""
        st.markdown("---")
        st.markdown(
            "🛠️ Built with Streamlit, Azure Speech, Azure OpenAI & LangChain"
        )
    
    def run(self) -> None:
        """Run the complete Streamlit application."""
        self.render_header()
        
        # Sidebar configuration
        selected_voice, speech_rate, optimize_for_audio = self.render_sidebar()
        
        # Main content area
        col1, col2 = st.columns([1, 1])
        
        with col1:
            text_content, source_name, source_type = self.render_input_section()
        
        with col2:
            self.render_output_section(text_content, source_name, source_type, speech_rate, optimize_for_audio)
        
        self.render_footer()


def main():
    """Main application entry point."""
    app = TextToAudioUI()
    app.run()


if __name__ == "__main__":
    main()
