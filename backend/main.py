from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

history = {}

class AskRequest(BaseModel):
    doc_id: str
    question: str

@app.post("/upload")
async def upload(file: UploadFile):
    doc_id = str(uuid.uuid4())
    history[doc_id] = {"filename": file.filename, "summary": "mock summary"}
    return {"doc_id": doc_id, "summary": "mock summary"}

@app.post("/ask")
async def ask(request: AskRequest):
    return {"doc_id": request.doc_id, "question": request.question, "answer": "mock answer"}

@app.get("/history")
async def get_history():
    return history

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
