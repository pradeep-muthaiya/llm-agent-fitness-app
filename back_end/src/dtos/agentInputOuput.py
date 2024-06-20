#from pydantic import BaseModel, Field
from typing import List
from pydantic import BaseModel, Field
from langchain_core.pydantic_v1 import BaseModel as BaseModelResponse
from langchain_core.pydantic_v1 import Field as FieldResponse

class AgentInput(BaseModel):
    query: str = Field(description="Textual query of a list of foods")

# class AgentOutput(BaseModel):
#     foodList: List[str] = Field(description="list of all the foods that were consumed")
#     protein: int = Field(description="The total amount of protein consumed")
#     calories: int = Field(description="The total amount of calories consumed")
    
class AgentOutput(BaseModel):
    query: str = Field(description="initial query asked")
    calories: int = Field(description="The total amount of calories consumed")
    output: str = Field(description="list of all the foods that were consumed")
    
# class Response(BaseModel):
#     answer: str = Field(description="The final answer to respond to the user")
#     total_calories: str = Field(description="The total number of calories in all of the foods combined")
#     total_protein: str = Field(description="The total amount of protein in all of the foods combined")

class Response(BaseModelResponse):
    foodList: List[str] = FieldResponse(description="a list of all the foods that the user inputted")
    calorieList: List[int] = FieldResponse(description="A list of the number of calories in each food the user submitted")
    proteinList: List[int] = FieldResponse(description="A list of the protein that was in each food the user submitted")
