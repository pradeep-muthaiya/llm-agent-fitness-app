from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from service.tool import createFoodLookupTool
import os
import json

def read_secrets(config_file):
    with open(config_file, "r") as file:
        data = file.read()
        data = json.loads(data)
        file.close()
        for item in data:
            os.environ[item] = data[item]
    
def resource_access_agent(prompt) -> AgentExecutor:
    read_secrets("secrets.json")
    llm = ChatOpenAI()
    tools = [createFoodLookupTool()]
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor