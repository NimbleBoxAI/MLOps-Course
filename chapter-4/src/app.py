from fastapi import FastAPI
from model import get_answer

app = FastAPI(title="Question Answering App")


@app.get("/")
async def home_page():
	return {"message": "Welcome to MLOps World"}


@app.get("/predict")
async def get_prediction(question: str, context: str):
    result =  get_answer(question, context)
    return {"answer": result}