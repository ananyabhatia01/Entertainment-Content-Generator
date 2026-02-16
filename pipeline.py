from engine.llm_client import LLMClient
from engine.vector_store import VectorStore
from engine.prompts import PROMPT_TEMPLATES

class ContentPipeline:
    def __init__(self):
        self.llm = LLMClient()
        self.db = VectorStore()
        self.history = {}

    def run_stage(self, stage, inputs):
        """Runs a specific stage of the pipeline."""
        # Get context from Vector DB
        context = self.db.search_context(f"Previous content for {stage}")
        
        # Prepare template
        template = PROMPT_TEMPLATES[stage]
        prompt = template.format(**inputs)
        
        # Inject context if available
        if context:
            full_prompt = f"Background Context from previous stages:\n{context}\n\nNew Task:\n{prompt}"
        else:
            full_prompt = prompt

        output = self.llm.generate(full_prompt)
        
        # Store in Vector DB if successful
        if "Error" not in output:
            self.db.add_content(output, stage)
            self.history[stage] = output
        
        return output

    def run_full_pipeline(self, base_idea, genre, tone):
        results = {}
        
        # 1. Concept
        results['concept'] = self.run_stage('concept', {'idea': base_idea, 'genre': genre, 'tone': tone})
        
        # 2. Logline
        results['logline'] = self.run_stage('logline', {'concept': results['concept']})
        
        # 3. Pitch
        results['pitch'] = self.run_stage('pitch', {'concept': results['concept'], 'logline': results['logline']})
        
        # 4. Outline
        results['outline'] = self.run_stage('outline', {'pitch': results['pitch']})
        
        # 5. Characters
        results['characters'] = self.run_stage('characters', {'outline': results['outline']})
        
        # 6. Scene
        results['scene'] = self.run_stage('scene', {'outline': results['outline'], 'characters': results['characters']})
        
        return results
