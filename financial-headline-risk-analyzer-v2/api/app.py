from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model_logic import predict_headline

app = FastAPI(title="Financial Headline Risk API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    headline: str

@app.get("/")
def health():
    return {"ok": True, "message": "Financial Headline Risk API is running."}

@app.post("/analyze")
def analyze(payload: AnalyzeRequest):
    return predict_headline(payload.headline)
