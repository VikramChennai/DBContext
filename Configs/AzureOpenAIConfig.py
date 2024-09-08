import os
from dotenv import load_dotenv
from openai import AzureOpenAI, AsyncAzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Get values from environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

syncAzureOpenAIClient = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

asyncAzureOpenAIClient = AsyncAzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)


