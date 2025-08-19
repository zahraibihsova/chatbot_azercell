# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from models.bedrock_client import get_llm_response

# router = APIRouter()

# class ChatRequest(BaseModel):
#     user_id: str
#     query: str

# @router.post("/chat")
# def chat(request: ChatRequest):
#     try:
#         response = get_llm_response(request.query)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Bedrock error: {str(e)}")
