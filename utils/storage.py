import os
import lancedb
from langchain_community.vectorstores import LanceDB
from langchain_ollama.embeddings import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

''' 
Connecting to Data Base
'''

embedding_model = os.getenv('EMBEDDING_MODEL')

db = lancedb.connect("frog-chef-db")
embedding = OllamaEmbeddings(model=embedding_model)

meal_store = LanceDB(connection=db, embedding=embedding, table_name="meals")


__all__=['meal_store']