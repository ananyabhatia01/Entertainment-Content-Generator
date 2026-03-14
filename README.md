# Agentic AI Entertainment Planner (ReAct Architecture)

This project satisfies the university requirement to build a "Planner Agent" that orchestrates complex tasks via a **multi-step reasoning loop**, validates resource availability using **mock interface tools**, and outputs a **detailed execution schedule**.

## 🧠 Architecture Setup

We migrated the logic to the **LangChain ReAct Paradigm** (Reason and Act). 
*   **The Model**: Google Gemini 1.5-flash
*   **The Orchestrator**: LangChain's `AgentExecutor`
*   **Memory**: Local Vector Embeddings (SentenceTransformers)

Instead of a static script running tasks sequentially, the Agent now:
1.  **Thinks**: Evaluates the goal and explicitly confirms tool existence.
2.  **Acts**: Calls Python-based mock functions.
3.  **Observes**: Reads the mock outputs and plans the next step.

## 🛠️ Mock Interface Tools

For stability and to meet grading criteria, this version uses **pure Python Mock Tools**. 
These are defined in `tools/mock_tools.py` using LangChain's `@tool` decorator:
- `fetch_trending_movies`
- `get_movie_metadata`
- `write_movie_review`
- `generate_publishing_schedule`

*(Note: Because these are standard LangChain tools, they can be swapped out for real APIs (like TMDb) by replacing the mock returns with `requests.get()` logic at any time.)*

## 🚀 Running the Project

1. Install the pinned, stable dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit Interface:
   ```bash
   streamlit run app.py
   ```

3. **In the UI**: Enter your Google Gemini API key to activate the reasoning loop. Watch the "Agent's Brain" section to see the live ReAct logic as it runs!
