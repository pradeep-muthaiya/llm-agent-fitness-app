from pydantic import BaseModel, Field

class AgentInput(BaseModel):
    query: str = Field(description="Textual query of a list of foods")

class AgentOutput(BaseModel):
    foodList: dict = Field(description="list of all the foods that were consumed")
    
    
