from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
import os
import json
from dotenv import load_dotenv
import boto3

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

MODEL_ID = os.getenv("MODEL_ID")
KB_ID = os.getenv("BEDROCK_KB_ID")
REGION = os.getenv("AWS_DEFAULT_REGION")

if not MODEL_ID or not REGION:
    raise ValueError("MODEL_ID or AWS_DEFAULT_REGION missing in .env")

# Bedrock clients
client = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
agent_client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

app = FastAPI()

def create_body_json(prompt: str):
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10240,
        "system": "",
        "messages": [{"role": "user", "content": prompt}],
    })

def retrieve_from_kb(query: str) -> str:
    try:
        res = agent_client.retrieve(
            knowledgeBaseId=KB_ID,
            retrievalQuery={"text": query},
        )
        if "retrievalResults" in res and len(res["retrievalResults"]) > 0:
            return res["retrievalResults"][0]["content"]["text"]
        return ""
    except Exception as e:
        print("Error retrieving from KB:", str(e))
        return ""

@app.get("/bedrock-chat")
def bedrock_chat(
    query: str = Query(...),
    use_kb: bool = Query(False, description="Set true to use Azercell KB, false for normal chatbot")
):
    try:
        kb_text = retrieve_from_kb(query) if use_kb else ""
        body_json = create_body_json(query if not kb_text else f"Use the following info:\n{kb_text}\n\nUser query: {query}")
        response = client.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=body_json,
        )
        message = json.loads(response["body"].read().decode("utf-8"))
        return PlainTextResponse(message["content"][0]["text"])
    except Exception as e:
        return PlainTextResponse(f"Error calling Bedrock: {str(e)}")
