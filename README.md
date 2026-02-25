# Nomad Cosmic

**Nomad Cosmic** is an AI-powered production pipeline designed to transform simple creative seeds into professional entertainment assets. It utilizes **Retrieval-Augmented Generation (RAG)** and a **Vector Database** to maintain narrative consistency throughout the storytelling process.

##  Features

- **Multi-Stage Pipeline**: Concept ⮕ Logline ⮕ Pitch ⮕ Outline ⮕ Characters ⮕ Script Scene.
- **Narrative Memory**: Uses **FAISS** and **Sentence-Transformers** to ensure the AI remembers plot points and character names.
- **Industry Standards**: Generates script scenes in professional screenplay format.
- **Resilient Logic**: Implements exponential backoff to handle API rate limits gracefully.
- **Premium UI**: Sleek, reactive dashboard built with Streamlit.

## Tech Stack

- **Core**: Python 3.9+
- **LLM**: Google Gemini 2.5 Flash
- **Vector DB**: FAISS
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Frontend**: Streamlit

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ananyabhatia01/nomad-cosmic.git
   cd nomad-cosmic
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add your [Google Gemini API Key](https://aistudio.google.com/):
     ```text
     GEMINI_API_KEY=your_api_key_here
     ```

## How to Run

Launch the application using Streamlit:
```bash
streamlit run app.py
```

## Architecture

The project follows a modular High-Level Design (HLD):
- **UI Tier**: Streamlit Dashboard.
- **Logic Tier**: Content Pipeline Orchestrator.
- **Memory Tier**: FAISS Vector Store + RAG Loop.
- **Intelligence Layer**: Google Gemini API integration.

---