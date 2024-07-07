# FuncGenie

A package for running a Flask server with decorated functions.

## Installation

```bash
pip install git+https://github.com/Shivam/funcgenie.git#subdirectory=funcgenie-python
```

## Usage

1. If you are not using a web server in your current application, you can start the genie server by calling the `run_genie()` method.

```python
from funcgenie import phantom, run_genie

@phantom
def greet(name: str = "World"):
    return f"Hello, {name}!"

if __name__ == "__main__":
    run_genie(port=5000)
```

2. If you are using a Flask app already, you can just register the routes required by funcgenie in your exisiting Flask app. By this way, you don't need to run another web server just for funcgenie. You can checkout our library-app example under `examples/library-app.py`

```python
from flask import Flask, jsonify
from funcgenie import phantom, create_genie_flask_routes

app = Flask(__name__)

# Register genie routes
create_genie_flask_routes(app)
```
We would add this functionality to other frameworks like Django and FastAPI in future :)