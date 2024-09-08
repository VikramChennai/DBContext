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

import asyncio

# Test the Azure OpenAI setup with a simple async call
async def test_azure_openai_setup():
    try:
        # Create a simple completion request using the async client
        response = await asyncAzureOpenAIClient.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, can you hear me?"}
            ]
        )
        
        # Print the response
        print("Azure OpenAI API async test response:")
        print(response.choices[0].message.content)
        print("\nAsync API call successful!")
    except Exception as e:
        print(f"Error occurred while testing async Azure OpenAI API: {str(e)}")

# Run the async test function
asyncio.run(test_azure_openai_setup())

