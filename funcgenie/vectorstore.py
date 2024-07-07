import pathway as pw
from langchain_community.embeddings.openai import OpenAIEmbeddings
from pathway.xpacks.llm.vector_store import VectorStoreServer, VectorStoreClient
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

def load_phantom_functions():
    response = requests.get('http://127.0.0.1:5000/phantom-functions')
    if response.status_code != 200:
        raise Exception("Unable to retrieve phantom functions")
    phantom_functions = response.json()
    
    directory = 'phantom_functions'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for key, value in phantom_functions.items():
        file_path = os.path.join(directory, f"{key}.json")
        with open(file_path, 'w') as file:
            json.dump(value, file, indent=4)

data_sources = []
data_sources.append(
    pw.io.fs.read(
        "./phantom_functions",
        format="binary",
        mode="streaming",
        with_metadata=True,
    )
)


PATHWAY_PORT = 8765

embeddings_model = OpenAIEmbeddings()

vector_server = VectorStoreServer.from_langchain_components(
    *data_sources,
    embedder=embeddings_model,
)

if __name__ == "__main__":
    load_phantom_functions()
    vector_server.run_server(host="127.0.0.1", port=PATHWAY_PORT, threaded=False, with_cache=False)