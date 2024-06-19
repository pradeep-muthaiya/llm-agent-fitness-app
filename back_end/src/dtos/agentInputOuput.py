from pydantic.v1 import BaseModel, Field
from typing import List

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
    
