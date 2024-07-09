from flask import Flask, request, jsonify
from agent import Agent
from pathway.xpacks.llm.vector_store import VectorStoreClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

PATHWAY_HOST = os.getenv("PATHWAY_HOST")
PATHWAY_PORT = os.getenv("PATHWAY_PORT")

CLIENT_HOST = os.getenv("CLIENT_HOST")
CLIENT_PORT = os.getenv("CLIENT_PORT")

app = Flask(__name__)

vector_client = VectorStoreClient(
    host=PATHWAY_HOST,
    port=PATHWAY_PORT,
)

myAgent = Agent()


@app.route("/query", methods=["POST"])
def query_library():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        vector_results = vector_client(
            query=query,
        )
        answer = myAgent.chat_completion_request(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert chatbot that has access to some functions to resolve user queries.\
                    Use them when you feel right. The user should not be aware of the functions you are using.",
                },
                {
                    "role": "user",
                    "content": query,
                }
            ],
            tools=[json.loads(obj["text"]) for obj in vector_results],
        )
        return jsonify({"answer": answer}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1411)
