##LLM Model
import os
os.environ["AZURE_OPENAI_API_KEY"] = "XXXXXXXXXX"
os.environ["AZURE_OPENAI_ENDPOINT"] = "XXXXXXXX"
os.environ["AZURE_OPENAI_API_VERSION"] = "XXXXX"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "XXXXXX"



from langchain_openai import AzureChatOpenAI
 
model = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    temperature=0.0
)