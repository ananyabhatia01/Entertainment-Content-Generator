import os
from dotenv import load_dotenv
from agents.planner_agent import PlannerAgent

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

agent = PlannerAgent(api_key)
try:
    response = agent.orchestrate_plan("Generate a weekly schedule of Movie Reviews for 2 trending movies.")
    print("FINISHED")
    print(response)
except Exception as e:
    import traceback
    traceback.print_exc()
