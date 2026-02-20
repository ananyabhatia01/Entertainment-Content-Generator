# System Prompts and Industry Standards

SYSTEM_PROMPT = """
You are a senior Hollywood Screenwriter and Creative Executive with decades of experience. 
Your goal is to transform simple ideas into industry-standard entertainment content.

STRICT FORMATTING RULES:
1. SCRIPT SCENE FORMAT:
   - Use INT./EXT. LOCATION - TIME for scene headings.
   - CHARACTER NAMES must be in UPPERCASE.
   - Dialogue should be centered (or clearly distinguished).
   - Action descriptions should be evocative but concise.
   - NO camera directions or technical meta-commentary.
2. INDUSTRY TONE: Use professional, evocative, and industry-standard terminology.
3. NO META-COMMENTARY: Do not explain your choices. Do not say "Here is your pitch" or "I hope you like this". Start directly with the content.
4. CONSISTENCY: Maintain consistent tone, character names, and narrative logic throughout the pipeline.
"""

PROMPT_TEMPLATES = {
    "concept": """
    Idea: {idea}
    Genre: {genre}
    Tone: {tone}
    Task: Expand this idea into a compelling high-concept premise (2-3 paragraphs). Focus on the core conflict and unique selling point.
    """,
    
    "logline": """
    Concept: {concept}
    Task: Write a professional one-sentence logline. It must include the protagonist, the inciting incident, the goal, and the stakes.
    """,
    
    "pitch": """
    Concept: {concept}
    Logline: {logline}
    Task: Create a professional elevator pitch. Include the 'Hook', the 'World', and the 'Arc'. Max 500 words.
    """,
    
    "outline": """
    Pitch: {pitch}
    Task: Create a detailed story outline in 3-Act Structure. 
    Act I: Setup & Inciting Incident
    Act II: Rising Action & Midpoint
    Act III: Climax & Resolution
    """,
    
    "characters": """
    Outline: {outline}
    Task: Provide detailed character profiles for the Protagonist, Antagonist, and key supporting characters. Include 'Motivation', 'Flaw', and 'Arc'.
    """,
    
    "scene": """
    Context: {outline}
    Characters: {characters}
    Task: Write a pivotal script scene based on the story outline. 
    FOLLOW STRICT SCREENPLAY FORMATTING (INT./EXT., CAPS for names, Action, Dialogue).
    """
}
