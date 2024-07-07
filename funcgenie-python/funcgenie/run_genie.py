from flask import Flask, request, jsonify
from .phantom import phantom_functions

def create_genie_flask_routes(app):
    @app.route('/phantom-functions', methods=['GET'])
    def get_phantom_functions():
        sanitized_functions = {
            func_name: {
                **func_info,
                "function": {key: value for key, value in func_info["function"].items() if key != "implementation"}
            }
            for func_name, func_info in phantom_functions.items()
        }
        return jsonify(sanitized_functions)

    @app.route('/call-phantom-function', methods=['POST'])
    def call_phantom_function():
        data = request.json
        func_name = data.get('function_name')
        func_params = data.get('parameters', {})
        
        if func_name not in phantom_functions:
            return jsonify({"error": "Function not found"}), 404
        
        func_info = phantom_functions[func_name]
        
        # Ensure the "implementation" key is available within the "function" key
        if "function" not in func_info or "implementation" not in func_info["function"]:
            return jsonify({"error": "Function implementation not found in phantom function information"}), 400
        
        func = func_info["function"]["implementation"]
        
        try:
            result = func(**func_params)
            return jsonify({
                "result": result,
                "function_name": func_info["function"]["name"],
                "parameters_used": func_params
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400

def run_genie(port=1881):
    """
    The `genie` server acts as a powerful entity, ready to handle requests and invoke the registered phantom functions.
    It simplifies the process of managing and interacting with these functions, making it feel like your commands are granted by a genie.
    """
    app = Flask(__name__)
    create_genie_flask_routes(app)
    app.run(debug=True, port=port)
