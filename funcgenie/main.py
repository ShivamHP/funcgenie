# import requests
import json
from agent import Agent
from pathway.xpacks.llm.vector_store import VectorStoreClient

if __name__ == "__main__":
    # query = "Add one new book to the library named 'Hetvi is best' by Shivam Pachchigar."
    query = "Which books are available in the library?"
    vector_client = VectorStoreClient(
        host="127.0.0.1",
        port=8765,
    )
    vector_results = vector_client(query=query, k=3)
    LibraryAgent = Agent(tools=[json.loads(obj['text']) for obj in vector_results])
    answer = LibraryAgent.chat_completion_request(messages=[{"role": "user", "content": query}])
    print("\nAnswer:")
    print(answer)