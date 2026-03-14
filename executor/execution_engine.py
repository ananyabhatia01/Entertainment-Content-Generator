import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class ExecutionEngine:
    def __init__(self, memory_system, gemini_api_key):
        self.memory = memory_system
        self.gemini_api_key = gemini_api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key)
        self.tools = {}
        self.logs = []

    def register_tool(self, name, tool_instance):
        self.tools[name] = tool_instance

    def _generate_review(self, movie_metadata):
        """Uses LangChain/LLM to generate a real review based on metadata."""
        prompt = PromptTemplate(
            input_variables=["metadata"],
            template="Generate a 2-3 sentence engaging movie review for this movie based on its metadata: {metadata}"
        )
        chain = prompt | self.llm
        response = chain.invoke({"metadata": str(movie_metadata)})
        return response.content

    def run_plan(self, plan):
        self.logs = []
        context_data = None
        results = {}

        for step in plan:
            task = step["task"]
            tool_name = step["tool"]
            
            log_entry = {"task": task, "tool": tool_name, "status": "Running", "result": None}
            self.logs.append(log_entry)
            
            try:
                if tool_name == "TrendingMoviesTool":
                    result = self.tools["TrendingMoviesTool"].get_trending_movies()
                    context_data = result # List of titles
                
                elif tool_name == "MovieDatabaseTool":
                    # Fetch metadata for each movie found in the previous step
                    result = {}
                    for title in context_data:
                        result[title] = self.tools["TMDBTool"].get_movie_details(title)
                    context_data = result # Dict of metadata
                
                elif tool_name == "ReviewGeneratorTool":
                    # Generate reviews using the LLM
                    result = {}
                    for title, metadata in context_data.items():
                        result[title] = self._generate_review(metadata)
                    context_data = result # Dict of reviews
                
                elif tool_name == "ContentSchedulerTool":
                    # Logic-based scheduling
                    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                    result = {days[i % 5]: f"Post: {list(context_data.keys())[i % len(context_data)]} - {list(context_data.values())[i % len(context_data)]}" 
                             for i in range(len(context_data))}
                
                else:
                    result = "Tool execution skipped/unknown"

                log_entry["status"] = "Success"
                log_entry["result"] = str(result)[:200] + "..."
                results[task] = result
                self.memory.store_memory(f"Step {task} completed: {str(result)[:100]}")

            except Exception as e:
                log_entry["status"] = "Failed"
                log_entry["result"] = str(e)
                break

        return results, self.logs
