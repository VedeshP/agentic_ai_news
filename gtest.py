from langchain_google_genai import ChatGoogleGenerativeAI

import os
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")
print(google_api_key)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    # api_key=google_api_key,
    verbose=True,
    temperature=0.7,
)

res = llm.invoke("how to get a 3d shoulders with dumbbells - explain in detail")
print(res)