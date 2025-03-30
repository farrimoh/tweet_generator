import streamlit as st
from models import TweetGenerator
import os

st.set_page_config(
    page_title="Tweet Generator 🐦",
    page_icon="🐦",
    layout="wide"
)

st.title("Tweet Generator 🐦")

# Model selection
model_type = st.sidebar.selectbox(
    "Select Model Type",
    ["ollama", "huggingface"],
    help="Choose between Ollama (local) or Hugging Face (cloud) model"
)

if model_type == "huggingface":
    api_token = st.sidebar.text_input(
        "Hugging Face API Token",
        type="password",
        help="Enter your Hugging Face API token"
    )
    if api_token:
        os.environ["HUGGINGFACE_API_TOKEN"] = api_token
    model_name = st.sidebar.text_input(
        "Hugging Face Model Name",
        value="meta-llama/Llama-2-7b-chat-hf",
        help="Enter the Hugging Face model repository ID"
    )
else:
    model_name = st.sidebar.text_input(
        "Ollama Model Name",
        value="llama2",
        help="Enter the Ollama model name"
    )

# Main interface
text = st.text_area(
    "Enter your text to generate tweets from:",
    height=150,
    placeholder="Type or paste your text here..."
)

num_tweets = st.slider(
    "Number of tweets to generate:",
    min_value=1,
    max_value=5,
    value=3,
    help="Select how many tweets you want to generate"
)

if st.button("Generate Tweets 🚀"):
    if not text:
        st.warning("Please enter some text to generate tweets from!")
    else:
        try:
            with st.spinner("Generating tweets..."):
                generator = TweetGenerator(model_type=model_type, model_name=model_name)
                tweets = generator.generate_tweets(text, num_tweets)
                
                st.success(f"Generated {len(tweets)} tweets! 🎉")
                
                for i, tweet in enumerate(tweets, 1):
                    st.markdown(f"### Tweet {i} 🐦")
                    st.write(tweet)
                    st.markdown("---")
                    
        except Exception as e:
            st.error(f"Error generating tweets: {str(e)}")
            if model_type == "huggingface" and not api_token:
                st.info("Please provide your Hugging Face API token in the sidebar to use Hugging Face models.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and LangChain") 