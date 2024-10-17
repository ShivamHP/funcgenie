from openai import OpenAI
import os
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt
import requests
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL")
CLIENT_HOST = os.getenv("CLIENT_HOST")
CLIENT_PORT = os.getenv("CLIENT_PORT")


class Agent:
    def __init__(self, tools=[]):
        self.openai = OpenAI()

    @retry(
        wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3)
    )
    def chat_completion_request(
        self, messages, tools=[], max_iterations=3, tool_choice="auto", model=LLM_MODEL
    ):
        while max_iterations > 0:
            try:
                response = self.openai.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice=tool_choice,
                )
                print(messages)
                if not response.choices[0].message.tool_calls:
                    return response.choices[0].message.content
                else:
                    max_iterations -= 1
                    if max_iterations == 0:
                        return response.choices[0].message.content
                    url = f"http://{CLIENT_HOST}:{CLIENT_PORT}/call-phantom-function"
                    payload = {
                        "function_name": response.choices[0]
                        .message.tool_calls[0]
                        .function.name,
                        "parameters": json.loads(
                            response.choices[0].message.tool_calls[0].function.arguments
                        ),
                    }
                    headers = {"Content-Type": "application/json"}
                    res = requests.post(url, json=payload, headers=headers)

                    if res.status_code == 200:
                        messages.append(
                            {
                                "role": "system",
                                "content": f"After executing this function: {response.choices[0].message.tool_calls[0].function.name}, we got response: {res.json()['result']}",
                            }
                        )
                        tool_choice = "none" # This is to prevent the agent from using tools again.
                    else:
                        messages.append(
                            {
                                "role": "assistant",
                                "content": ".",
                            }
                        )
                        tool_choice = "none"
            except Exception as e:
                print("Unable to generate ChatCompletion response")
                print(f"Exception: {e}")
                return e
