# import boto3
# import json
# import os
# from dotenv import load_dotenv

# load_dotenv()

# REGION = os.getenv("AWS_REGION")
# ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
# SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# MODEL_ID = os.getenv("MODEL_ID")

# bedrock = boto3.client(
#     "bedrock-runtime",
#     region_name=REGION,
#     aws_access_key_id=ACCESS_KEY,
#     aws_secret_access_key=SECRET_KEY
# )

# def get_llm_response(prompt: str):
#     """
#     Works with Claude 3.7 Sonnet on AWS Bedrock.
#     """
#     payload = {
#         "input": prompt,          # 🔑 must use "input"
#         "max_tokens_to_sample": 512,
#         "temperature": 0.7
#     }

#     response = bedrock.invoke_model(
#         modelId=MODEL_ID,
#         body=json.dumps(payload),
#         contentType="application/json",
#         accept="application/json"
#     )

#     result = response["body"].read().decode("utf-8")
#     try:
#         # Claude Sonnet responses have "completion"
#         return json.loads(result)["completion"]
#     except Exception:
#         return result
