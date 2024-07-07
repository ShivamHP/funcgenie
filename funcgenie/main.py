import requests
from agent import Agent

# Function to retrieve phantom functions from Genie server
def get_phantom_functions():
    response = requests.get('http://127.0.0.1:5000/phantom-functions')
    return [value for value in response.json().values()]

def test():
    tools = get_phantom_functions()
    print(Agent().chat_completion_request(messages=[{"role": "user", "content": "Which books are available in the library?"}], tools=tools))
    
if __name__ == "__main__":
    test()