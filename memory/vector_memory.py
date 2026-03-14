from sentence_transformers import SentenceTransformer
import numpy as np

class VectorMemory:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Load a lightweight pre-trained model for embeddings
        # This will download the model (~80MB) on first run
        self.model = SentenceTransformer(model_name)
        self.memories = []
        self.vectors = []

    def store_memory(self, text):
        """Encodes text into a vector and stores it."""
        vector = self.model.encode([text])[0]
        self.memories.append(text)
        self.vectors.append(vector)
        return f"Stored: {text[:50]}..."

    def search_context(self, query, top_k=2):
        """Searches for the most relevant stored memories based on cosine similarity."""
        if not self.vectors:
            return []
        
        query_vector = self.model.encode([query])[0]
        
        # Calculate cosine similarity
        similarities = [
            np.dot(query_vector, v) / (np.linalg.norm(query_vector) * np.linalg.norm(v))
            for v in self.vectors
        ]
        
        # Get indices of top_k most similar memories
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = [self.memories[i] for i in top_indices]
        
        return results
