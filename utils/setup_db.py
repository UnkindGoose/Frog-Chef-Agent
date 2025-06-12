import os
import pandas as pd
import lancedb

from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import LanceDB

'''
Run if vector database wasn't created yet.
This script creates vector db from the list of meals from mealdb.
Embedding model can be changed in .env files.
'''

embedding_model = os.environ['EMBEDDING_MODEL']
mealdb = pd.read_csv('utils/mealdb.csv')

db = lancedb.connect("frog-chef-db")
embedding = OllamaEmbeddings(model=embedding_model)

meal_store = LanceDB.from_texts(mealdb["Meals"].tolist(), embedding, connection=db, table_name="meals")

