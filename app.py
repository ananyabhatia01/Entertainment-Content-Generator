import streamlit as st
import os
from dotenv import load_dotenv

# Import our custom modules
from agents.planner_agent import PlannerAgent
from memory.vector_memory import VectorMemory

# Load environment variables if they exist
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Agentic AI Entertainment Planner",
    page_icon="🎬",
    layout="wide"
)

# Premium UI Styling
st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stTextInput>div>div>input { background-color: #1e293b; color: white; border: 1px solid #334155; }
    .stButton>button { background: linear-gradient(90deg, #4f46e5, #7c3aed); color: white; border: none; font-weight: bold; }
    .step-log { font-family: monospace; background: #1e293b; padding: 10px; border-radius: 5px; margin-bottom: 5px;}
    .thought-label { color: #f59e0b; font-weight: bold; }
    .action-label { color: #3b82f6; font-weight: bold; }
    .result-label { color: #10b981; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("Agentic AI Entertainment Planner (ReAct Pattern)")
st.markdown("---")

# Sidebar for API Configuration
st.sidebar.title("🛠️ Configuration")
st.sidebar.markdown("**University Project Requirements:**")
st.sidebar.markdown("Multi-step Reasoning Loop")
st.sidebar.markdown("Autonomous Decomposition")
st.sidebar.markdown("Validates Mock Interfaces")
st.sidebar.markdown("Generates Execution Schedule")

# Get API Key from Environment Variables
gemini_key = os.getenv("GOOGLE_API_KEY")

if not gemini_key:
    st.error("Missing Google Gemini API Key. Please add `GOOGLE_API_KEY=your_key` to your `.env` file.")
    st.stop()

# Initialize Systems
if 'memory' not in st.session_state:
    st.session_state.memory = VectorMemory()

# UI Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("Provide High-Level Goal")
    user_goal = st.text_input(
        "Enter your entertainment goal:",
        "Generate a weekly schedule of Movie Reviews for 2 trending movies."
    )
    
    run_btn = st.button("Run Agentic Reasoning Loop")

    if run_btn:
        st.session_state.run_log = []
        st.session_state.final_output = None
        
        with st.spinner("Agent is planning, validating tools, and executing..."):
            agent = PlannerAgent(gemini_key)
            
            try:
                # The LangChain AgentExecutor returns the final output and intermediate steps
                response = agent.orchestrate_plan(user_goal)
                st.session_state.final_output = response.get("output", "")
                st.session_state.run_log = response.get("intermediate_steps", [])
                
                # Store the final result in vector memory
                st.session_state.memory.store_memory(f"Goal: {user_goal} -> Final Output: {st.session_state.final_output[:200]}")
                st.success("Reasoning loop successfully completed!")
            except Exception as e:
                st.error(f"Agent encountered an error: {e}")

with col2:
    st.header("Agent's 'Brain' (Execution Logs)")
    
    if 'run_log' in st.session_state and st.session_state.run_log:
         for step in st.session_state.run_log:
             action, observation = step
             
             with st.container():
                 st.markdown(f'<div class="step-log">', unsafe_allow_html=True)
                 st.markdown(f'<span class="thought-label"> Thought/Action:</span> Calling `{action.tool}` with input: `{action.tool_input}`', unsafe_allow_html=True)
                 if hasattr(action, 'log'):
                      st.markdown(f'<div style="color: #94a3b8; font-size: 0.9em;">... {action.log.split("Action:")[0].strip()}</div>', unsafe_allow_html=True)
                 st.markdown(f'<span class="result-label"> Observation:</span> {str(observation)[:150]}...', unsafe_allow_html=True)
                 st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("🔍 Context Memory")
    search_query = st.text_input("Query Semantic Memory:", "What was scheduled?")
    if search_query and 'memory' in st.session_state:
        mem_results = st.session_state.memory.search_context(search_query)
        for m in mem_results:
            st.info(f" {m}")

st.markdown("---")
if 'final_output' in st.session_state and st.session_state.final_output:
    st.header("🏆 Final Execution Schedule")
    st.markdown(f"**Goal**: {user_goal}")
    st.markdown("### Generated Output:")
    st.markdown(st.session_state.final_output)
