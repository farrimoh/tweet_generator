# 🐦 Tweet Generator for Research Labs & LLM Learners

Easily draft a connected thread of up to 5 tweets to share new papers and findings. Perfect for research labs and anyone learning to use local LLMs like LLaMA 3 — explore prompt design, app building, and local inference all in one simple project.

---

## ⚙️ How It Works

- **Runs locally:** Powered by Ollama serving LLaMA 3 models on your machine—no API keys, no data leaves your system.
- **Flexible interfaces:** Use the Streamlit web app or the command-line tool.
- **Ideal for:** Science communication and LLM experimentation.

---

## 📋 Prerequisites

- Python 3.8 or higher  
- Ollama installed

---

## 🚀 Installation

1. **Install Ollama:**
   - **Windows/macOS:** [Download Ollama](https://ollama.ai/download)
   - **Linux:**  
     ```bash
     curl https://ollama.ai/install.sh | sh
     ```

2. **Pull the Llama 3 model:**
   ```bash
   ollama pull llama3
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔍 Test Your Ollama Setup

Check your Ollama installation:

```bash
python test_ollama.py
```

This script will:
- Test the Ollama connection
- Verify the model is available
- Run a sample prompt

---

## 🛠️ Troubleshooting Ollama

**Port error with `ollama serve`?**  
Ollama may already be running. Try:

```bash
# Windows
taskkill /F /IM ollama.exe

# Linux/Mac
pkill ollama
```
Then restart `ollama serve`.

**Ollama not responding?**
- Ensure the service is running
- Restart your computer if needed
- Confirm the llama3 model is pulled:
  ```bash
  ollama pull llama3
  ```

---

## 🎮 Running the Application

### 🌐 Web Interface (Streamlit)

1. Start Ollama
2. Launch the app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to the displayed URL (usually http://localhost:8501)

### 💻 Command Line Interface

1. Start Ollama
2. Run:
   ```bash
   python cli.py
   ```
3. Follow the prompts

---

## 📖 Usage

### Web Interface

1. Enter your text
2. Select number of tweets (1–5)
3. Click **Generate Tweets**
4. View your thread

### Command Line

1. Run the program
2. Enter your text (press Enter twice to finish)
3. Enter number of tweets
4. View your thread
5. Optionally, generate more tweets


---

## ⚠️ Note

Make sure Ollama is running before starting the app. The application uses LangChain’s Ollama integration to communicate with your local Ollama instance.
