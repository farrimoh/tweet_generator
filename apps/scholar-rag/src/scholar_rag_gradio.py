import gradio as gr
import os
from dotenv import load_dotenv
from scholar_rag import get_answer, setup_clients  

# Load environment variables
load_dotenv()

# Initialize the RAG pipeline clients
search_client, openai_client = setup_clients()
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def process_question(question):
    """Process a question through the RAG pipeline and return the answer."""
    try:
        answer = get_answer(question, search_client, openai_client, deployment_name)
        return answer
    except Exception as e:
        return f"Error processing question: {str(e)}"

# Create the Gradio interface
demo = gr.Interface(
    fn=process_question,
    inputs=gr.Textbox(
        lines=3,
        placeholder="Enter your research question here...",
        label="Question"
    ),
    outputs=gr.Textbox(
        lines=10,
        label="Answer"
    ),
    title="📚 Scholar RAG - Research Assistant",
    description="Ask questions about your research papers and get AI-powered answers based on the content.",
    examples=[
        ["What are key parameters in determining size of Carboxysomes"],
        ["Which factors are identified to control HBV dimorphism?"],
        ["Does encapsulating cardo increase or decrease size of Nanoshells?"]
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch(share=True)