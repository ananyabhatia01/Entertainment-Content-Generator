import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
    print("Invoking...")
    res = llm.invoke("Hello, who are you?")
    print("Success:", res.content)
except Exception as e:
    import traceback
    traceback.print_exc()
