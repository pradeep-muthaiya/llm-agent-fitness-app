from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
import requests
import os

class FoodLookupToolInput(BaseModel):
    query: str = Field(description="The food you wish to look up")

def FoodLookup(query: str) -> dict:
    "Function to lookup food nutrion facts"
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': os.environ['APPLICATION_ID'],
        'x-app-key':os.environ['APPLICATION_KEY'],
    #  'x-remote-user-id': 0
    }
    body = {
        "query": query
    }
    response = requests.post(url=url, headers=headers, json=body)
    return response.json()

def createFoodLookupTool():
    return StructuredTool(
        name="FoodLookUpTool",
        description="Food Lookup Tool",
        args_schema=FoodLookupToolInput,
        func=FoodLookup,
        verbose=True
    )
