from langdetect import detect
from langchain_core.messages import HumanMessage
from graph import graph

'''
Function to run the graph.
It detects user's language and runs the graph with user's message and detected language as input.
Agent only supports English and Russian.
'''

def run_messages(messages: str):
    language = detect(messages) if detect(messages) in ['en', 'ru'] else 'en'
    return graph.invoke({'messages': [HumanMessage(messages)], 'language':language})

'''
Test Input
'''

test_input = "Как приготовить блины?"
test_output = run_messages(test_input)

print("_"*50)
print(test_output)
print("_"*50)
print(f"Model output:\n{test_output['messages'][-1].content}\nQuery Language: {test_output['language']}")