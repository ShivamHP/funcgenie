# FuncGenie: Make your app AI powered

Welcome to **FuncGenie**, the magical Python package that transforms your functions into powerful, automated tools ready to be invoked by an intelligent Large Language Model (LLM). With FuncGenie, you can seamlessly integrate and manage your functions, allowing for automated execution in response to dynamic queries.

<img src="funcgenie.gif" width="800" height="400" alt="funcgenie demo">

## What is FuncGenie?

FuncGenie consists of two core components:

1. **Phantom Functions**: Functions decorated with `@phantom` are enhanced with metadata, making them more powerful and accessible. These functions are registered and managed by the `genie` server, allowing them to be called remotely as if by magic.

2. **Genie Server**: The `genie` server acts as a powerful entity, ready to handle requests and invoke the registered phantom functions. It simplifies the process of managing and interacting with these functions, making it feel like your commands are granted by a genie.

## Key Features

- **Automated Function Management**: Decorate your functions with `@phantom` to automatically register them with the genie server.
- **Seamless Integration**: Easily integrate the genie server into your existing Flask app.
- **Enhanced Metadata**: Phantom functions include detailed metadata, making them ideal for automated invocation by an LLM.
- **RESTful API**: Expose your phantom functions via a simple RESTful API, allowing for remote invocation and automation.

## Installation

You can install FuncGenie directly from a GitHub repository:

```bash
pip install git+https://github.com/ShivamHP/funcgenie.git#subdirectory=funcgenie-python
```

## Usage

### Step 1: Decorate Your Functions
Use the @phantom decorator to enhance and register your functions:
```python
from funcgenie import phantom

@phantom
def add_book(title: str, author: str):
    """Add a new book to the library."""
    return {"title": title, "author": author}

@phantom
def get_books():
    """Get the list of all books."""
    return books
```

### Step 2: Integrate the Genie server
Integrate the genie server into your Flask app:
```python
from flask import Flask
from funcgenie import create_genie_routes

app = Flask(__name__)

# Register genie routes
create_genie_routes(app)

@app.route('/')
def home():
    return "Welcome to the Library Books Management App!"

if __name__ == "__main__":
    app.run(port=5000)
```

Now that's all is needed for you to make your app AI powered!

## How to run the funcgenie app

Needs to be filled

## Run your app using AI:

```
curl -X POST http://localhost:1411/query \
     -H "Content-Type: application/json" \
     -d '{"query": "How many books are there in the library?"}'
```

## Why to use OpenAI?

OpenAI provides this functionality where in you can ask the LLM to give you a function call based on the user's query and available functions.

## Why to use Pathway?

In large applications, there can be a lot of phantom functions. If all the phantom functions are sent in every API to OpenAI, it will result in huge cost due to the amount of tokens consumed by phantom functions. 
Pathway gets the query and sends only 3 functions which are relevant to the query by doing similarity search, this way, we can save a lot of input tokens.