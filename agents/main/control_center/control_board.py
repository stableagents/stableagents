# # controlboard.py

from llms import LLM_Switcher, ModelInterface

# Example models
model1 = ModelInterface("Model1", "https://api.model1.com")
model2 = ModelInterface("Model2", "https://api.model2.com")
model3 = ModelInterface("Model3", "https://api.model3.com")

# List of models to switch between
models = [model1, model2, model3]

def control_board(query):
    """
    Orchestrates the process of handling user queries by using the LLM switcher.
    """
    switcher = LLM_Switcher(models)
    response = switcher.switch_and_request(query)
    if response:
        # Process the response as needed
        # For demonstration, we'll just return the response as is
        return response
    else:
        return {"error": "No model could handle the request."}

if __name__ == "__main__":
    # Example usage
    query = "What is the meaning of life?"
    result = control_board(query)
    print(result)
