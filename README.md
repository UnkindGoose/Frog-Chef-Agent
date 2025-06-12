# 🐸Frog-Chef-Agent
Repository contains files for LangGraph agent, that can describe recipes from mealDB. It supports English and Russian language and uses LanceDB vector storage to store meals.

## Contents

There are 4 main .py files required to run this agent:
- [run_inference.py](./run_inference.py) contains function to run the agent and test input.
- [models.py](./models.py) contains commands to set up 2 models - their chains and tools. The models are:
  - main LLM that acts as a chef;
  - translator LLM.
- [storage.py](./storage.py) contains commands to connect to local vector storage (LanceDB).
- [graph.py](./graph.py) contains graph nodes, routers and overall structure.

To set up vector storage, [setup_db.py](./setup_db.py) script was used.

## Usage

```cmd
git clone https://github.com/UnkindGoose/Frog-Chef-Agent.git
cd Frog-Chef-Agent
pip install -r requirements.txt
```

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
- [ ] Make API
- [ ] Make UI
