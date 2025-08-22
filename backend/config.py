"""
Конфигурация для VisuLex с Hugging Face моделями
"""

import os
from typing import Dict, Any

class Config:
    """Конфигурация приложения"""
    
    # Основные настройки
    APP_NAME = "VisuLex"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Настройки Hugging Face
    HF_CACHE_DIR = os.getenv("HF_CACHE_DIR", "./models_cache")
    HF_OFFLINE = os.getenv("HF_OFFLINE", "false").lower() == "true"
    
    # Модели по умолчанию
    DEFAULT_QA_MODEL = "deepset/roberta-base-squad2"
    DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    DEFAULT_SUMMARY_MODEL = "facebook/bart-large-cnn"
    DEFAULT_TEXT_MODEL = "microsoft/DialoGPT-medium"
    
    # Настройки обработки документов
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "50 * 1024 * 1024"))  # 50MB
    MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "10000"))
    SUPPORTED_FILE_TYPES = [
        "application/pdf",
        "text/plain",
        "text/markdown",
        "image/jpeg",
        "image/png",
        "image/gif"
    ]
    
    # Настройки эмбеддингов
    EMBEDDING_DIMENSION = 384  # для all-MiniLM-L6-v2
    MAX_EMBEDDING_LENGTH = 512
    
    # Настройки QA
    QA_MAX_LENGTH = 512
    QA_STRIDE = 128
    
    # Настройки суммаризации
    SUMMARY_MAX_LENGTH = 150
    SUMMARY_MIN_LENGTH = 30
    
    # Настройки логирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Настройки производительности
    USE_CUDA = os.getenv("USE_CUDA", "true").lower() == "true"
    MODEL_PRECISION = os.getenv("MODEL_PRECISION", "float32")  # float16 для экономии памяти
    
    @classmethod
    def get_model_config(cls, model_type: str) -> Dict[str, Any]:
        """Возвращает конфигурацию для конкретного типа модели"""
        
        configs = {
            "qa": {
                "model_name": cls.DEFAULT_QA_MODEL,
                "max_length": cls.QA_MAX_LENGTH,
                "stride": cls.QA_STRIDE,
                "return_overflowing_tokens": True,
                "padding": True,
                "truncation": True
            },
            "embedding": {
                "model_name": cls.DEFAULT_EMBEDDING_MODEL,
                "max_length": cls.EMBEDDING_DIMENSION,
                "normalize_embeddings": True
            },
            "summary": {
                "model_name": cls.DEFAULT_SUMMARY_MODEL,
                "max_length": cls.SUMMARY_MAX_LENGTH,
                "min_length": cls.SUMMARY_MIN_LENGTH,
                "do_sample": False,
                "num_beams": 4
            },
            "text": {
                "model_name": cls.DEFAULT_TEXT_MODEL,
                "max_length": 100,
                "do_sample": True,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        return configs.get(model_type, {})
    
    @classmethod
    def validate_config(cls) -> bool:
        """Проверяет корректность конфигурации"""
        try:
            # Проверяем существование директории кэша
            os.makedirs(cls.HF_CACHE_DIR, exist_ok=True)
            
            # Проверяем размеры файлов
            if cls.MAX_FILE_SIZE <= 0:
                raise ValueError("MAX_FILE_SIZE должен быть положительным")
            
            if cls.MAX_TEXT_LENGTH <= 0:
                raise ValueError("MAX_TEXT_LENGTH должен быть положительным")
            
            return True
            
        except Exception as e:
            print(f"Ошибка конфигурации: {e}")
            return False

# Создаем глобальный экземпляр конфигурации
config = Config()
