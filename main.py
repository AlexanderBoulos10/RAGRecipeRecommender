from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from query import query_rag
from pydantic import BaseModel
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequestString(BaseModel):
    query_text: str

@app.post("/recipeQuery")
def get_recipe(request:QueryRequestString):
    query_text = request.query_text
    if not query_text:
        return {"error": "No query provided"}
    string_response = query_rag(query_text)
    json_response = json.loads(string_response)
    return json_response

@app.post("/ingredientQuery")
def get_recipe(request:QueryRequestString):
    query_text = request.query_text
    if not query_text:
        return {"error": "No query provided"}
    string_response = query_rag(query_text, False)
    json_response = json.loads(string_response)
    return json_response