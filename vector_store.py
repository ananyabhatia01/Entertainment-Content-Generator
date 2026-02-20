import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, dimension=384):
        self.index = faiss.IndexFlatL2(dimension)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.metadata = []

    def add_content(self, content, stage):
        """Adds a piece of generated content to the vector store with stage metadata."""
        embedding = self.model.encode([content])[0]
        self.index.add(np.array([embedding]).astype('float32'))
        self.metadata.append({"stage": stage, "content": content})

    def search_context(self, query, top_k=3):
        """Retrieves relevant history for context continuity."""
        if self.index.ntotal == 0:
            return ""
        
        query_embedding = self.model.encode([query])[0]
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        
        context = []
        for idx in indices[0]:
            if idx != -1:
                item = self.metadata[idx]
                context.append(f"Stage: {item['stage']}\nContent: {item['content']}")
        
        return "\n\n---\n\n".join(context)

    def get_all_history(self):
        return self.metadata
