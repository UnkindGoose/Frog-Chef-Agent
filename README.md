# 🐸Frog-Chef-Agent

<img alt="Frog-Chef" src="./images/frog.png" width="200"/>

Repository contains files for LangGraph agent, that can describe recipes from mealDB. It supports English and Russian language and uses LanceDB vector storage to store meals.

## Contents

There are 4 main .py files required to run this agent:
- [run_inference.py](./run_inference.py) contains function to run the agent and test input.
- [models.py](./models.py) contains commands to set up 2 models - their chains and tools. The models are:
  - main LLM that acts as a chef;
  - translator LLM.
- [storage.py](./storage.py) contains commands to connect to local vector storage (LanceDB).
- [graph.py](./graph.py) contains graph nodes, routers and overall structure.

.env file contains customizable variables that control agent behaviour

You don't need to create vectore storage yourself after cloning this repository, but you can see how it was set up in [setup_db.py](./setup_db.py) script.

## Usage

To try this agent, simply create Python 3.10 venv. From that venv run commands below to install the repository and dependencies:

```cmd
git clone https://github.com/UnkindGoose/Frog-Chef-Agent.git
cd Frog-Chef-Agent
pip install -r requirements.txt
```

To run API and make a POST request use:

```cmd
fastapi dev run_inference.py
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d "{\"message\":\"Your message\"}"
```

You can also just open run_inference.py and uncomment the test input lines while commenting the FastAPI lines.

```Python
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
```

After that just run the script with desired input.

## Customization

To make changes in agent behavior, you can change .env variables. It contains variables that control which model is used for specific task and their system prompts.

#### Models used:
- Main model: qwen3:1.7b
- Translator model: gemma3:4b
- Embedding model: nomic-embed-text


Current implementation is displayed below:

```.env
MODEL_NAME="qwen3:1.7b"
TRANSLATOR_MODEL_NAME="gemma3:4b"
EMBEDDING_MODEL="nomic-embed-text:latest"
TRANSLATOR_PROMPT="Переведи текст рецепта с английского на русский. В своем ответе выведи только перевод изначального текста."
LLM_PROMPT="You are a cheerful frog chef who helps users with recipes and ingredients. Answer in a friendly, humorous tone but stay on point. You can help user with different recipes, if they ask you. Only pass meal name to the tools, without any other words."
```

## TODO

- [x] Add Russian language support
- [x] Make API
- [ ] Make UI that will show images of requested meals
