import json
from fastapi import APIRouter
from langserve import add_routes
from dtos.agentInputOuput import AgentInput, AgentOutput, Response
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from service.agent import resource_access_agent, create_agent
from service.tool import createFoodLookupTool
    
router = APIRouter()

# system_prompt = (
#     "You are a helpful AI bot."
#     "That is skilled at calculating calories and nutrion facts based on text input."
#     "You have a tool that is able to find caloric information based on a string query."
#     "Your job is to return the total calories and grams of protein consumed given the following food:"
#     "{query}"
# )

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             system_prompt
#         ),
#         MessagesPlaceholder(variable_name="agent_scratchpad")
#     ]
# )

system_prompt = (
    "You are a helpful AI bot."
    "That is skilled at calculating calories and nutrion facts based on text input."
    "You have a tool that is able to find caloric information based on a string query."
    "Your job is to return the total calories and grams of protein consumed given the following food"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# @router.post("/query")
# def invoke_food_agent(data: AgentInput):
#     agent = resource_access_agent(prompt).with_types(input_type = AgentInput)
#     result = agent.invoke(data.model_dump())
#     return {
#         "result": result
#     }

# add_routes(
#     router,
#     resource_access_agent(prompt).with_types(input_type = AgentInput, output_type=AgentOutput),
#     path='/query'
# )

# add_routes(
#     router,
#     create_agent(prompt, tools=[createFoodLookupTool()], response=[Response]),
#     path='/query'
# )

@router.post("/query")
def invoke_food_agent(data: AgentInput):
    agent = create_agent(prompt, tools=[createFoodLookupTool()], response=[Response])
    result = agent.invoke(data.model_dump())
    return result