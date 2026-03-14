import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from tools.mock_tools import fetch_trending_movies, get_movie_metadata, write_movie_review, generate_publishing_schedule

class PlannerAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=api_key,
            temperature=0
        )
        self.tools = [
            fetch_trending_movies, 
            get_movie_metadata, 
            write_movie_review, 
            generate_publishing_schedule
        ]
        
        # This is a custom ReAct prompt tailored to the professor's rubric.
        # It explicitly asks the agent to validate tools as part of its thought process.
        template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

You are an Entertainment Planner Agent. Your goal is to orchestrate complex Entertainment tasks through a multi-step reasoning loop.
When you receive a goal, you must:
1. Decompose the objective into actionable steps.
2. Explicitly validate resource (tool) availability in your Thought process BEFORE executing any tools. State which tools you will need to accomplish the task.
3. Use the tools to gather data, write content, and generate a final detailed execution schedule.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do. First, validate the tools you need.
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final schedule.
Final Answer: the final answer to the original input question (the final schedule)

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        self.prompt = PromptTemplate.from_template(template)
        
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        # We set return_intermediate_steps=True so we can display the "thought process" in the UI
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True, 
            return_intermediate_steps=True,
            handle_parsing_errors=True
        )

    def orchestrate_plan(self, goal: str):
        """Runs the agent's full reasoning loop."""
        response = self.agent_executor.invoke({"input": goal})
        return response
