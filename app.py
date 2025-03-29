import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import json

def generate_tweets(text, num_tweets, prompt_template):
    # Initialize Ollama
    llm = OllamaLLM(model="llama3")
    
    try:
        # Generate the prompt
        prompt = prompt_template.format(text=text, num_tweets=num_tweets)
        
        # Generate response
        response = llm.invoke(prompt)
        
        # Clean up the response to ensure it's valid JSON
        generated_text = response.strip('[]').split('\n')
        tweets = [tweet.strip().strip('"') for tweet in generated_text if tweet.strip()]
        
        return tweets
    except Exception as e:
        st.error(f"Error generating tweets: {str(e)}")
        return []

def main():
    st.title("Tweet Generator using Llama 2")
    st.write("Generate engaging tweets from your text using AI")
    
    # Create tabs for main interface and prompt editing
    tab1, tab2 = st.tabs(["Generate Tweets", "Edit Prompt Template"])
    
    with tab1:
        # Text input
        input_text = st.text_area("Enter your text here:", height=200)
        
        # Number of tweets selector
        num_tweets = st.slider("Number of tweets to generate:", 1, 5, 1)
        
        if st.button("Generate Tweets"):
            if input_text:
                with st.spinner("Generating tweets..."):
                    # Get the current prompt template from session state
                    prompt_template = PromptTemplate(
                        input_variables=["text", "num_tweets"],
                        template=st.session_state.get('prompt_template', """Based on the following text, generate {num_tweets} engaging tweets. 
                        Make them concise, informative, and engaging. Each tweet should be under 280 characters.
                        Format the response as a JSON array of strings.
                        
                        Text: {text}
                        
                        Tweets:""")
                    )
                    
                    tweets = generate_tweets(input_text, num_tweets, prompt_template)
                    
                    if tweets:
                        st.subheader("Generated Tweets:")
                        for i, tweet in enumerate(tweets, 1):
                            st.write(f"Tweet {i}: {tweet}")
            else:
                st.warning("Please enter some text first!")
    
    with tab2:
        st.subheader("Edit Prompt Template")
        st.write("Customize how the AI generates tweets by editing the prompt template below.")
        st.write("Use {text} for the input text and {num_tweets} for the number of tweets.")
        
        # Initialize prompt template in session state if not exists
        if 'prompt_template' not in st.session_state:
            st.session_state.prompt_template = """Based on the following text, generate {num_tweets} engaging tweets. 
            Make them concise, informative, and engaging. Each tweet should be under 280 characters.
            Format the response as a JSON array of strings.
            
            Text: {text}
            
            Tweets:"""
        
        # Prompt template editor
        new_template = st.text_area(
            "Prompt Template:",
            value=st.session_state.prompt_template,
            height=300,
            help="Edit the prompt template. Use {text} for input text and {num_tweets} for number of tweets."
        )
        
        # Validate and save the template
        if st.button("Save Template"):
            try:
                # Test if the template is valid
                test_prompt = new_template.format(text="test", num_tweets=1)
                st.session_state.prompt_template = new_template
                st.success("Prompt template saved successfully!")
            except Exception as e:
                st.error(f"Invalid template: {str(e)}")
                st.info("Please make sure you include both {text} and {num_tweets} placeholders.")
        
        # Show current template preview
        st.subheader("Template Preview")
        st.write("This is how your template will look with sample values:")
        st.code(new_template.format(text="Sample text", num_tweets=2), language="text")

if __name__ == "__main__":
    main() 