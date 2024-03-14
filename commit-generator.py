import streamlit as st
import pieces_os_client as pos_client
from datetime import datetime
import requests

# Initialize variables
pieces_os_version = None
asset_ids = {}  # Asset ids for any list or search
assets_are_models = False
current_asset = {}
parser = None
query = ""


# Initialize the ApiClient globally
configuration = pos_client.Configuration(host="http://localhost:1000")
api_client = pos_client.ApiClient(configuration)
api_instance = pos_client.ModelsApi(api_client)

# Get models
api_response = api_instance.models_snapshot()
models = {model.name: model.id for model in api_response.iterable if model.cloud or model.downloading}

# Set default model
default_model_name = "GPT-4 Chat Model"
model_id = models[default_model_name]
models_name = list(models.keys())
default_model_index = models_name.index(default_model_name)


# Streamlit UI 
st.title('Commit Message Suggestion Tool')

# system_prompt = "Analyze the code changes below and suggest a few appropriate Git commit messages"
prompt = "Generate a commit message for the following changes. Remember to follow the git commit message best practices and don't exceed 72 character and your answer must be between two quotes in one sentence :\n{changes_summary}"

# Select model
selected_model = st.selectbox("Select Your model", list(models.keys()), index=default_model_index)

# Create a text input for the user to enter their code
code = st.text_area('Enter your code here:')

# Append the code snippet and the prompt text
user_question = code + prompt 


# # Create a button for the user to generate a commit message
if st.button('Generate Commit Messages'):

    question = pos_client.QGPTQuestionInput(
        query=user_question,
        relevant = {"iterable": []},
        model=model_id,
    )

    question_json = question.to_json()

    # Send a POST request to the /qgpt/question endpoint
    response = requests.post('http://localhost:1000/qgpt/question', data=question_json)

    # Parse the response
    response_data = response.json()

    # Create an instance of the QGPTQuestionOutput model using the response data
    question_output = pos_client.QGPTQuestionOutput(**response_data)

    # Now you can access the answers from
    answers = question_output.answers.iterable[0].text


    # Assuming 'response' is your response data
    st.write(answers)