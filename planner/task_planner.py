class TaskPlanner:
    def __init__(self):
        # Define some predefined strategies for specific goals
        self.strategies = {
            "Generate movie reviews for trending movies": [
                {"task": "Get trending movies", "tool": "TrendingMoviesTool"},
                {"task": "Get metadata for movies", "tool": "MovieDatabaseTool", "depends_on_previous": True},
                {"task": "Generate reviews", "tool": "ReviewGeneratorTool", "depends_on_previous": True},
                {"task": "Create publishing schedule", "tool": "ContentSchedulerTool", "depends_on_previous": True}
            ]
        }

    def create_plan(self, goal):
        """Returns a list of steps to achieve the goal."""
        # Simple rule-based lookup for demonstration
        # If the goal is not precisely matched, return a default mock decomposition
        plan = self.strategies.get(goal)
        
        if not plan:
            # Default fallback for any other goal
            plan = [
                {"task": "General analysis of goal", "tool": "TrendingMoviesTool"},
                {"task": "Data collection", "tool": "MovieDatabaseTool"},
                {"task": "Summary generation", "tool": "ReviewGeneratorTool"}
            ]
            
        return plan
