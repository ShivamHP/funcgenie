import inspect
from functools import wraps
from typing import get_type_hints

# Dictionary to store decorated functions
phantom_functions = {}

def phantom(func):
    """
    Functions decorated with `@phantom` are enhanced with metadata, making them more powerful and accessible.
    These functions are registered and managed by the `genie` server, allowing them to be called remotely as if by magic.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Store function information inside the wrapper
    func_name = func.__name__
    func_doc = func.__doc__ or ""
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = signature.parameters

    parameters = {
        "type": "object",
        "properties": {},
        "required": []
    }

    for name, param in params.items():
        param_info = {
            "type": type_hints.get(name, str).__name__,  # Get the type hint if available, default to 'str'
            "description": ""
        }
        if param_info["type"] == "int":
            param_info["type"] = "integer"
        elif param_info["type"] == "str":
            param_info["type"] = "string"
        elif param_info["type"] == "bool":
            param_info["type"] = "boolean"
        if param.default is param.empty:
            parameters["required"].append(name)
        else:
            param_info["default"] = str(param.default)

        parameters["properties"][name] = param_info

    phantom_functions[func_name] = {
        "type": "function",
        "function": {
            "name": func_name,
            "description": func_doc,
            "parameters": parameters,
            "implementation": func  # Store the actual function reference
        }
    }

    return wrapper
