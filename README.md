# Tweet Generator 

A powerful tool that generates engaging tweets using AI models. Built with LangChain and supporting both Ollama and Hugging Face models.

## 📋 Prerequisites

- Python 3.8 or higher
- Ollama installed and running (for local model usage)
- Hugging Face API token (for cloud model usage)

## 🚀 Installation

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

3. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tweet_generator.git
   cd tweet_generator
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. For Hugging Face usage, set up your API token:
   ```bash
   export HUGGINGFACE_API_TOKEN=your_token_here
   ```

## 🔍 Testing

To test if Ollama is working correctly:
```bash
python test_ollama.py
```

### ⚠️ Troubleshooting Ollama Service

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
   - Make sure the llama2 model is pulled:
     ```bash
     ollama pull llama2
     ```

## 🎮 Running the Application

### 🌐 Web Interface

Run the Streamlit app:
```bash
streamlit run app.py
```

### 💻 Command Line Interface

Run the CLI version:
```bash
python cli.py
```

Follow the interactive prompts:
- Enter your text (press Enter twice to finish)
- Specify the number of tweets you want to generate (1-5)
- Choose whether to generate more tweets

## 📖 Usage

1. Enter your text in the input field
2. Select the number of tweets to generate (1-5)
3. Choose your preferred model type (Ollama or Hugging Face)
4. Click "Generate Tweets" or run the CLI command
5. View your generated tweets!

## ✨ Features

- Support for both local (Ollama) and cloud (Hugging Face) models
- Web interface with Streamlit
- Command-line interface with rich formatting
- Customizable number of tweets
- Beautiful UI with emojis and modern design
- Error handling and user feedback

## ⚠️ Notes and Troubleshooting

### Ollama
- Make sure Ollama is running before using the application
- Default model is "llama2"
- You can change the model in the sidebar or CLI arguments

### Hugging Face
- Requires a valid API token
- Token can be provided via environment variable or CLI argument
- Default model is "meta-llama/Llama-2-7b-chat-hf"
- You can use any other model from Hugging Face Hub

### Common Issues
- If you get connection errors with Ollama, ensure the service is running
- For Hugging Face errors, verify your API token is valid
- Check your internet connection when using cloud models

## 📝 License

MIT License - feel free to use this project for your own purposes!
