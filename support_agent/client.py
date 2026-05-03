import asyncio

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

class SupportAgent:
    def __init__(self):
        self.model = ChatOpenAI(model='gpt-5.4-mini')

    async def handle_query(self, query: str) -> str:
        response = await self.model.ainvoke([query])
        return response
    
if __name__ == "__main__":
    agent = SupportAgent()

    query = "How do I reset my password?"
    response = asyncio.run(agent.handle_query(query))
    print(f"Support Agent Response: {response}")    