from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent, create_openai_functions_agent
from service.tool import createFoodLookupTool
import os
import json
from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.agents import AgentActionMessageLog, AgentFinish

def read_secrets(config_file):
    with open(config_file, "r") as file:
        data = file.read()
        data = json.loads(data)
        file.close()
        for item in data:
            os.environ[item] = data[item]

def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the Response function was invoked, return to the user with the function inputs
    if name == "Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )

def create_agent(prompt, tools, response):
    read_secrets("secrets.json")
    llm = ChatOpenAI(temperature=0)
    tools_response = tools + response
    llm_with_tools = llm.bind_functions(tools_response)
    agent = (
        {
            "query": lambda x: x["query"],
            # Format agent scratchpad from intermediate steps
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | parse
    )
    agent_executor = AgentExecutor(tools=tools, agent=agent, verbose=True)
    return agent_executor
    
def resource_access_agent(prompt) -> AgentExecutor:
    read_secrets("secrets.json")
    llm = ChatOpenAI()
    tools = [createFoodLookupTool()]
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor