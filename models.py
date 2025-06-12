import os
import requests
from typing import Annotated

from langgraph.types import Command
from langchain_ollama.chat_models import ChatOllama
from langchain_core.tools import tool, InjectedToolCallId
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage

from storage import meal_store

''' 
Loading neccessary models and declaring system prompts
'''

model = os.environ['MODEL_NAME']
translator_model = os.environ['TRANSLATOR_MODEL_NAME']


translator_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            os.environ['TRANSLATOR_PROMPT'],
        ),
        (
            "user", 
            "Переведи текст рецепта с английского на русский:\n{input}"
        ),
    ]
)

system_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            os.environ['LLM_PROMPT'],
        ),
        ("placeholder",  "{input}"),
    ]
)

'''
Declaring tool to get the desired meal information from database
'''

@tool
def find_closest_meal(tool_call_id: Annotated[str, InjectedToolCallId], meal_query: str) -> dict:
    """If user asks for a meal recipe, run this tool with meal name in English.
    
        Input:
        tool_call_id - id of tool call,
        Meal Name in English
        
        Returns:
        Meal_Recipe_Information: string
    """
    #print("Started find meal tool")
    docs = meal_store.similarity_search(meal_query, k=1)
    
    if docs:
        meal_name = docs[0].page_content
    else:
        return
        
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
    response = requests.get(url)
    data = response.json()
    
    meals = data.get("meals")
    if not meals:
        return "Meal Not Found"
    
    meal = meals[0]
    
    ingredients_str = ''
    for i in range(1, 21):
        if meal['strIngredient' + str(i)] not in ['', None]:
            ingredients_str += f"{str(i)}. {meal['strIngredient' + str(i)]:<20} {meal['strMeasure' + str(i)]}\n" 
        else:
            pass
        
    
    result = {
        "name": meal['strMeal'],
        "category": meal['strCategory'],
        "origin country": meal['strArea'],
        "ingredients": ingredients_str,
        "instructions": meal['strInstructions']
    }
    
    print(result)
    
    return Command(update={
        "image": meal['strMealThumb'],

        "messages": [
            ToolMessage(
                result,
                tool_call_id=tool_call_id
            )
        ]
    })
    
'''
Declaring 2 models:

llm - main model for text generation as a frog-chef🐸
translator - translates model output if user query's and AI message's languages aren't equal
'''
 
llm = ChatOllama(
    model=model,
    temperature=0.7
).bind_tools([find_closest_meal])

translator = ChatOllama(model=translator_model, temperature=0)

llm_chain_proxy = system_prompt | llm

translation_chain_proxy = translator_prompt | translator

__all__=["llm_chain_proxy", "translation_chain_proxy", "find_closest_meal"]