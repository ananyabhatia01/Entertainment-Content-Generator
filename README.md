# Entertainment Content Generator (MVP)

A specialized GenAI application for entertainment professionals.

## Features
- **Industry Pipeline**: Idea → Concept → Logline → Pitch → Story Outline → Character Profiles → Script Scenes.
- **Industry Standard Formatting**: Script scenes are generated in standard screenplay format.
- **Context Persistence**: Uses FAISS Vector Database to maintain continuity across multiple generation steps.
- **Customizable**: Select Genre, Tone, and Output Type.

## Tech Stack
- **Backend**: Python
- **LLM**: Google Gemini API (model: `gemini-1.5-pro`)
- **Vector DB**: FAISS
- **Frontend**: Streamlit
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)

## Setup Instructions

1. **Clone the project** to your local machine.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key**:
   - Open the `.env` file.
   - Replace `your_gemini_api_key_here` with your actual Google Gemini API Key.
4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Enter a seed idea (e.g., "A thriller about a silent assassin who starts hearing voices").
2. Choose your genre and tone.
3. Select "Full Pipeline" to generate the entire package or specific stages.
4. Review the generated content in the formatted sections.
5. Use the "Regenerate" button to refine specific sections while maintaining context.
