from langdetect import detect
from langchain_core.messages import HumanMessage
from utils.graph import graph
from fastapi import FastAPI
from pydantic import BaseModel

'''
Function to run the graph.
It detects user's language and runs the graph with user's message and detected language as input.
Agent only supports English and Russian.
'''

def run_inference(message: str):
    language = detect(message) if detect(message) in ['en', 'ru'] else 'en'
    result = graph.invoke({'messages': [HumanMessage(message)], 'language':language})
    
    response = {'reply':result['messages'][-1].content}
    
    if 'image' in result and result['image'] is not None:
        response['image'] = result['image']
    
    return response

'''
FastAPI endpoint
'''

app = FastAPI()

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(input: ChatInput):
    return run_inference(input.message)

# '''
# Test Input
# '''

# test_input = "Как приготовить блины?"
# test_output = run_inference(test_input)

# print("_"*50)
# print(test_output)
# print("_"*50)
# print(f"Model output:\n{test_output['messages'][-1].content}\nQuery Language: {test_output['language']}")