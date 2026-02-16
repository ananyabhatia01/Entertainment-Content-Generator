import os
import google.generativeai as genai
from dotenv import load_dotenv
from engine.prompts import SYSTEM_PROMPT

load_dotenv()

class LLMClient:
    """
    Client for interacting with Google's Gemini LLM.
    Handles API configuration and basic generation requests.
    """
    def __init__(self):
        # Load API key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("Please provide a valid GEMINI_API_KEY in the .env file.")
        
        # Configure the generative AI model with industry-specific system instructions
        genai.configure(api_key=api_key)
        self.genai = genai
        self.SYSTEM_PROMPT = SYSTEM_PROMPT
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT
        )

    def generate(self, prompt, temperature=0.7, retries=3):
        """
        Generates content with automatic retry logic for rate limits.
        """
        import time
        for attempt in range(retries):
            try:
                print(f"[DEBUG] Sending request to Gemini (Attempt {attempt+1})...")
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=temperature,
                    )
                )
                print(f"[DEBUG] Gemini responded successfully. Length: {len(response.text)}")
                return response.text
            except Exception as e:
                error_msg = str(e)
                print(f"[DEBUG] Gemini Error: {error_msg}")
                
                # Check for rate limit error (429)
                if "429" in error_msg or "quota" in error_msg.lower():
                    if attempt < retries - 1:
                        wait_time = (attempt + 1) * 2  # Exponential-ish backoff
                        print(f"[DEBUG] Rate limit hit. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                
                return f"Error generating content: {error_msg}"
        return "Error: Maximum retries exceeded for rate limit."
