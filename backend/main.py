from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import logging
from app.services import huggingface_service

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VisuLex API", description="API для анализа документов с использованием Hugging Face моделей")

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Хранилище документов (в реальном проекте используйте базу данных)
documents = {}

class AskRequest(BaseModel):
    doc_id: str
    question: str

class DocumentInfo(BaseModel):
    doc_id: str
    filename: str
    summary: str
    text_length: int
    file_type: str

@app.post("/upload", response_model=DocumentInfo)
async def upload(file: UploadFile):
    """Загружает и обрабатывает документ с помощью Hugging Face моделей"""
    try:
        logger.info(f"Загрузка файла: {file.filename}, тип: {file.content_type}")
        
        # Читаем содержимое файла
        file_content = await file.read()
        
        # Обрабатываем документ с помощью Hugging Face
        result = huggingface_service.process_document(file_content, file.content_type or "text/plain")
        
        # Генерируем уникальный ID
        doc_id = str(uuid.uuid4())
        
        # Сохраняем информацию о документе
        document_info = {
            "doc_id": doc_id,
            "filename": file.filename,
            "summary": result.get("summary", "Не удалось создать содержание"),
            "text_length": len(result.get("text", "")),
            "file_type": file.content_type or "text/plain",
            "text": result.get("text", ""),
            "embeddings": result.get("embeddings", None)
        }
        
        documents[doc_id] = document_info
        
        logger.info(f"Документ {doc_id} успешно обработан")
        logger.info(f"Всего документов в памяти: {len(documents)}")
        
        return DocumentInfo(**document_info)
        
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")

@app.post("/ask")
async def ask(request: AskRequest):
    """Отвечает на вопросы по документу с помощью Hugging Face QA модели"""
    try:
        # Проверяем, существует ли документ
        logger.info(f"Поиск документа {request.doc_id} в {len(documents)} документах")
        if request.doc_id not in documents:
            logger.error(f"Документ {request.doc_id} не найден. Доступные: {list(documents.keys())}")
            raise HTTPException(status_code=404, detail="Документ не найден")
        
        document = documents[request.doc_id]
        question = request.question
        
        logger.info(f"Вопрос по документу {request.doc_id}: {question}")
        
        # Получаем ответ с помощью Hugging Face модели
        qa_result = huggingface_service.answer_question(
            question=question,
            context=document["text"]
        )
        
        response = {
            "doc_id": request.doc_id,
            "question": question,
            "answer": qa_result["answer"],
            "confidence": qa_result["confidence"],
            "summary": document["summary"]
        }
        
        logger.info(f"Ответ сгенерирован с уверенностью: {qa_result['confidence']:.2f}")
        
        return response
        
    except Exception as e:
        logger.error(f"Ошибка при получении ответа: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения ответа: {str(e)}")

@app.get("/history")
async def get_history():
    """Возвращает историю всех загруженных документов"""
    try:
        # Возвращаем только основную информацию о документах
        history = {}
        for doc_id, doc_info in documents.items():
            history[doc_id] = {
                "filename": doc_info["filename"],
                "summary": doc_info["summary"],
                "file_type": doc_info["file_type"],
                "text_length": doc_info["text_length"]
            }
        
        return history
        
    except Exception as e:
        logger.error(f"Ошибка при получении истории: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения истории: {str(e)}")

@app.get("/document/{doc_id}")
async def get_document(doc_id: str):
    """Возвращает детальную информацию о конкретном документе"""
    try:
        if doc_id not in documents:
            raise HTTPException(status_code=404, detail="Документ не найден")
        
        return documents[doc_id]
        
    except Exception as e:
        logger.error(f"Ошибка при получении документа {doc_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения документа: {str(e)}")

@app.get("/")
def root():
    """Проверка состояния API"""
    return {
        "message": "VisuLex API работает с Hugging Face моделями! 🚀",
        "status": "active",
        "models_loaded": len(huggingface_service._models_cache) > 0
    }

@app.get("/health")
async def health_check():
    """Детальная проверка состояния API и моделей"""
    try:
        # Проверяем состояние Hugging Face сервиса
        models_status = {
            "text_model": "text_model" in huggingface_service._models_cache,
            "qa_model": "deepset/roberta-base-squad2" in huggingface_service._models_cache,
            "embedding_model": huggingface_service.embedding_model is not None
        }
        
        return {
            "status": "healthy",
            "device": huggingface_service.device,
            "models": models_status,
            "documents_count": len(documents),
            "api_version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Ошибка проверки здоровья: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
