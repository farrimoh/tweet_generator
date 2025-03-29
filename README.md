# Tweet Generator with Llama 3

A tweet generation tool using LangChain, Ollama, and Llama 3. Available in both Streamlit web interface and command-line versions.

## Prerequisites

1. Python 3.8 or higher
2. Ollama installed on your system

## Installation

1. Install Ollama:
   - Windows: Download and install from [Ollama's official website](https://ollama.ai/download)
   - Linux: Run the following command:
     ```bash
     curl https://ollama.ai/install.sh | sh
     ```
   - macOS: Download and install from [Ollama's official website](https://ollama.ai/download)

2. Pull the Llama 3 model:
   ```bash
   ollama pull llama3
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Testing Ollama Installation

Before running the application, you can test if Ollama is working correctly:

```bash
python test_ollama.py
```

This will:
1. Test the connection to Ollama
2. Verify the model is available
3. Try a simple prompt to ensure everything is working

### Troubleshooting Ollama Service

If you encounter issues with the Ollama service:

1. If you get a port error when running `ollama serve`:
   - Ollama might already be running in the background
   - Try these steps:
     ```bash
     # Windows
     taskkill /F /IM ollama.exe
     
     # Linux/Mac
     pkill ollama
     ```
   - Then try running `ollama serve` again

2. If Ollama isn't responding:
   - Check if the service is running
   - Try restarting your computer
   - Make sure the llama3 model is pulled:
     ```bash
     ollama pull llama3
     ```

## Running the Application

### Web Interface (Streamlit)

1. Make sure Ollama is running in the background
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

### Command Line Interface

1. Make sure Ollama is running in the background
2. Run the CLI version:
   ```bash
   python cli.py
   ```
3. Follow the interactive prompts:
   - Enter your text (press Enter twice to finish)
   - Specify the number of tweets to generate (1-5)
   - Choose whether to generate more tweets

## Usage

### Web Interface
1. Enter your text in the input text area
2. Select the number of tweets you want to generate (1-5)
3. Click "Generate Tweets"
4. View your generated tweets

### Command Line
1. Run the program
2. Enter your text when prompted (press Enter twice to finish)
3. Enter the number of tweets you want to generate
4. View the generated tweets
5. Choose whether to generate more tweets

## Features

- Generate 1-5 tweets from input text
- Uses LangChain with Ollama and Llama 3 for natural language generation
- Structured prompt templates for better tweet generation
- Available in both web and command-line interfaces
- Real-time tweet generation
- Interactive command-line interface
- Option to generate multiple sets of tweets in one session

## Note

Make sure Ollama is running before starting either version of the application. The application uses LangChain's Ollama integration to communicate with the local Ollama instance.
