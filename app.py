import streamlit as st
import time
import os
from dotenv import load_dotenv
from engine.pipeline import ContentPipeline

# Load environment variables early
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Nomad Cosmic | Entertainment GenAI",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
    }
    .output-section {
        background-color: #1a1c24;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
    }
    .script-text {
        font-family: 'Courier New', Courier, monospace;
        background-color: #f4f4f4;
        color: #333;
        padding: 30px;
        border-radius: 5px;
        white-space: pre-wrap;
    }
    h1, h2, h3 {
        color: #ff4b4b !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'outputs' not in st.session_state:
    st.session_state.outputs = {}

def init_pipeline():
    try:
        st.session_state.pipeline = ContentPipeline()
        return True
    except Exception as e:
        st.error(f"Initialization Failed: {e}")
        return False

# Attempt auto-init if API key is present
api_key = os.getenv("GEMINI_API_KEY")
if not st.session_state.pipeline and api_key and api_key != "your_gemini_api_key_here":
    init_pipeline()

# Sidebar - Controls
with st.sidebar:
    st.title("🎬 Nomad Cosmic")
    st.subheader("Design Your Masterpiece")
    st.divider()
    
    genre = st.selectbox("Select Genre", 
                        ["Sci-Fi", "Thriller", "Drama", "Comedy", "Horror", "Fantasy", "Action"])
    
    tone = st.selectbox("Select Tone", 
                       ["Serious", "Emotional", "Dark", "Humorous", "Suspenseful", "Poetic"])
    
    output_type = st.selectbox("Pipeline Target", 
                              ["Full Pipeline", "Pitch Only", "Script Scene Only", "Logline & Concept"])
    
    st.divider()
    st.info("Ensuring industry-standard screenplay formatting and narrative logic.")

# Main UI
st.title("Entertainment Content Generator")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    idea_input = st.text_area("Enter your seed idea or topic:", 
                             placeholder="A story about a time-traveling historian who accidentally deletes their own existence...",
                             height=150)
    
    generate_btn = st.button("GENERATE CONTENT")

with col2:
    st.markdown("### Process Status")
    status_placeholder = st.empty()
    if st.session_state.pipeline:
        st.success("✅ System Ready (API Connected)")
    else:
        st.warning("⚠️ Waiting for API Key configuration in .env")

# Generation Logic
if generate_btn:
    if not idea_input:
        st.warning("Please enter an idea first.")
    else:
        if not st.session_state.pipeline:
            init_pipeline()
            
        if st.session_state.pipeline:
            with st.spinner("Brainstorming with GenAI..."):
                try:
                    if output_type == "Full Pipeline":
                        st.session_state.outputs = st.session_state.pipeline.run_full_pipeline(idea_input, genre, tone)
                    else:
                        # Specific stage logic
                        if "Pitch" in output_type:
                            concept = st.session_state.pipeline.run_stage('concept', {'idea': idea_input, 'genre': genre, 'tone': tone})
                            logline = st.session_state.pipeline.run_stage('logline', {'concept': concept})
                            pitch = st.session_state.pipeline.run_stage('pitch', {'concept': concept, 'logline': logline})
                            st.session_state.outputs = {'concept': concept, 'logline': logline, 'pitch': pitch}
                        elif "Scene" in output_type:
                            concept = st.session_state.pipeline.run_stage('concept', {'idea': idea_input, 'genre': genre, 'tone': tone})
                            outline = st.session_state.pipeline.run_stage('outline', {'pitch': concept})
                            chars = st.session_state.pipeline.run_stage('characters', {'outline': outline})
                            scene = st.session_state.pipeline.run_stage('scene', {'outline': outline, 'characters': chars})
                            st.session_state.outputs = {'scene': scene}
                        else:
                            concept = st.session_state.pipeline.run_stage('concept', {'idea': idea_input, 'genre': genre, 'tone': tone})
                            logline = st.session_state.pipeline.run_stage('logline', {'concept': concept})
                            st.session_state.outputs = {'concept': concept, 'logline': logline}
                    
                    if not st.session_state.outputs or all(v == "" for v in st.session_state.outputs.values()):
                         st.error("Model returned empty results. Please check your API key or idea input.")
                    else:
                         st.success("Generation Complete!")
                         st.rerun() # Ensure the UI updates immediately
                except Exception as e:
                    st.error(f"Generation Error: {str(e)}")

# Results Display
if st.session_state.outputs:
    st.markdown("---")
    
    for stage, content in st.session_state.outputs.items():
        with st.expander(f"✨ {stage.upper()}", expanded=(stage in ['pitch', 'scene'])):
            if stage == 'scene':
                st.markdown(f'<div class="script-text">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="output-section">{content}</div>', unsafe_allow_html=True)
            
            # Refine Button
            if st.button(f"Regenerate {stage.capitalize()}", key=f"regen_{stage}"):
                with st.spinner(f"Rewriting {stage}..."):
                    new_output = st.session_state.pipeline.run_stage(stage, {'idea': idea_input, 'genre': genre, 'tone': tone, 'concept': st.session_state.outputs.get('concept', ''), 'logline': st.session_state.outputs.get('logline', ''), 'pitch': st.session_state.outputs.get('pitch', ''), 'outline': st.session_state.outputs.get('outline', ''), 'characters': st.session_state.outputs.get('characters', '')})
                    st.session_state.outputs[stage] = new_output
                    st.rerun()

    # Memory Viewer & Reset
    with st.sidebar:
        st.divider()
        if st.checkbox("Show Memory (Vector DB Contents)"):
            if st.session_state.pipeline:
                st.write(st.session_state.pipeline.db.get_all_history())
            else:
                st.write("Memory is empty.")
        
        if st.button("🔄 Reset Application"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
