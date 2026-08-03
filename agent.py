from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from tools import get_exchange_rate

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

finance_agent = create_agent(
    model=llm,
    tools=[get_exchange_rate],
)