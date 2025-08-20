import boto3
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse

# Load AWS credentials from .env (keep your access keys safe!)
load_dotenv()

AWS_REGION = "us-east-1"             
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"           

if not MODEL_ID:
    raise ValueError("MODEL_ID is not set")

# Bedrock client
client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

app = FastAPI()

def create_body_json(prompt: str):
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10240,
        "system": "",
        "messages": [{"role": "user", "content": prompt}]
    })

@app.get("/")
def root():
    return {"message": "Backend running! Use /bedrock-chat?query=... to chat with Claude 3.7"}

@app.get("/bedrock-chat")
def bedrock_chat(query: str = Query(...)):
    try:
        body_json = create_body_json(query)
        response = client.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=body_json
        )
        message = json.loads(response['body'].read().decode('utf-8'))
        return PlainTextResponse(message['content'][0]['text'])
    except Exception as e:
        return PlainTextResponse(f"Error calling Bedrock: {str(e)}")
