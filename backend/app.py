import boto3
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse

# Load .env variables
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
MODEL_ID = os.getenv("MODEL_ID") 

if not MODEL_ID:
    raise ValueError("MODEL_ID is not set in .env")
if not AWS_REGION:
    raise ValueError("AWS_REGION is not set in .env")

# Build boto3 client dynamically
boto3_kwargs = {"region_name": AWS_REGION}
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    boto3_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
    boto3_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

# Bedrock client
client = boto3.client("bedrock-runtime", **boto3_kwargs)

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
