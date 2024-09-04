import os
from dotenv import load_dotenv
from langflow.load import run_flow_from_json, load_flow_from_json

load_dotenv()

# Load the flow from a JSON file
flow_file = "test_rag.json"

# Get the file path
file_path = os.path.join(os.getcwd(), "resources/undergraduate_programs.pdf")

TWEAKS = {
  "ChatInput-PDFBk": {},
  "ParseData-Xzyoz": {},
  "Prompt-6c19U": {},
  "ChatOutput-GHadX": {},
  "SplitText-xMUOd": {},
  "File-fd9Cv": {
     "path": file_path,
  },
  "AstraVectorStoreComponent-01msg": {
     "token": os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
      "api_endpoint": os.getenv("ASTRA_DB_API_ENDPOINT")
  },
  "OpenAIEmbeddings-JX6Wh": {
     "openai_api_key": os.getenv("OPENAI_API_KEY"),
  },
  "OpenAIModel-Kn5sq": {
      "api_key": os.getenv("OPENAI_API_KEY"),
  }
}


# Load the flow
try:
  flow = load_flow_from_json(flow=flow_file)
  print("Flow loaded successfully")
except Exception as e:
  print(f"Error loading flow: {e}")
  flow = None

#Function to run the flow
def run_flow(input_data):

    try:
        flow = run_flow_from_json(flow=flow_file,
                            input_value=str(input_data),
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)
        return flow
    except Exception as e:
        return f"Error running flow: {e}"