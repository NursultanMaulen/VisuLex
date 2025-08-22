# VisuLex с Hugging Face моделями 🚀

Этот проект интегрирует Hugging Face модели для анализа документов, извлечения текста, генерации содержания и ответов на вопросы.

## 🎯 Возможности

- **📄 Извлечение текста** из PDF, изображений и текстовых файлов
- **📝 Генерация содержания** с помощью BART модели
- **❓ Вопросы-ответы** на основе контекста документа
- **🔍 Создание эмбеддингов** для семантического поиска
- **🖼️ Обработка изображений** (базовая поддержка)

## 🛠️ Установка

### 1. Создание виртуального окружения

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

**⚠️ Важно:** Некоторые модели могут быть большими (1-3GB). Убедитесь, что у вас достаточно места на диске.

### 3. Проверка установки

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
```

## 🚀 Запуск

### 1. Запуск сервера

```bash
python run.py
```

Сервер запустится на `http://localhost:8000`

### 2. Проверка работоспособности

```bash
python test_api.py
```

## 📊 Используемые модели

### 1. Модель для вопросов-ответов

- **Название:** `deepset/roberta-base-squad2`
- **Размер:** ~500MB
- **Назначение:** Отвечает на вопросы на основе контекста
- **Язык:** Английский

### 2. Модель для эмбеддингов

- **Название:** `all-MiniLM-L6-v2`
- **Размер:** ~90MB
- **Назначение:** Создает векторные представления текста
- **Размерность:** 384

### 3. Модель для суммаризации

- **Название:** `facebook/bart-large-cnn`
- **Размер:** ~1.6GB
- **Назначение:** Генерирует краткое содержание текста
- **Язык:** Английский

### 4. Текстовая модель

- **Название:** `microsoft/DialoGPT-medium`
- **Размер:** ~1.5GB
- **Назначение:** Генерация текста и диалогов
- **Язык:** Английский

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в папке `backend`:

```bash
# Основные настройки
DEBUG=false
LOG_LEVEL=INFO

# Hugging Face настройки
HF_CACHE_DIR=./models_cache
HF_OFFLINE=false

# Производительность
USE_CUDA=true
MODEL_PRECISION=float32

# Ограничения
MAX_FILE_SIZE=52428800  # 50MB в байтах
MAX_TEXT_LENGTH=10000
```

### Настройка моделей

Отредактируйте `config.py` для изменения моделей по умолчанию:

```python
DEFAULT_QA_MODEL = "your-qa-model"
DEFAULT_EMBEDDING_MODEL = "your-embedding-model"
DEFAULT_SUMMARY_MODEL = "your-summary-model"
```

## 📡 API Эндпоинты

### 1. Загрузка документа

```http
POST /upload
Content-Type: multipart/form-data

file: [binary]
```

**Ответ:**

```json
{
  "doc_id": "uuid",
  "filename": "document.pdf",
  "summary": "Краткое содержание...",
  "text_length": 1500,
  "file_type": "application/pdf"
}
```

### 2. Вопрос по документу

```http
POST /ask
Content-Type: application/json

{
  "doc_id": "uuid",
  "question": "Что содержится в документе?"
}
```

**Ответ:**

```json
{
  "doc_id": "uuid",
  "question": "Что содержится в документе?",
  "answer": "Ответ на основе контекста...",
  "confidence": 0.85,
  "summary": "Краткое содержание..."
}
```

### 3. История документов

```http
GET /history
```

### 4. Детали документа

```http
GET /document/{doc_id}
```

### 5. Проверка здоровья

```http
GET /health
```

## 💡 Примеры использования

### Python клиент

```python
import requests

# Загрузка документа
with open("document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/upload", files=files)
    doc_data = response.json()
    doc_id = doc_data["doc_id"]

# Вопрос по документу
question_data = {
    "doc_id": doc_id,
    "question": "Какие основные положения?"
}
response = requests.post("http://localhost:8000/ask", json=question_data)
answer = response.json()
print(f"Ответ: {answer['answer']}")
```

### cURL

```bash
# Загрузка файла
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload

# Вопрос
curl -X POST -H "Content-Type: application/json" \
  -d '{"doc_id":"uuid","question":"Что в документе?"}' \
  http://localhost:8000/ask
```

## 🔍 Отладка

### Логи

Логи выводятся в консоль с уровнем INFO. Для изменения уровня:

```bash
export LOG_LEVEL=DEBUG
python run.py
```

### Проверка моделей

```bash
curl http://localhost:8000/health
```

### Мониторинг памяти

```python
import psutil
import torch

# Использование GPU
if torch.cuda.is_available():
    print(f"GPU память: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")

# Использование RAM
print(f"RAM: {psutil.virtual_memory().percent}%")
```

## ⚠️ Ограничения и рекомендации

### Производительность

- **CPU:** Модели работают медленнее на CPU
- **GPU:** Рекомендуется NVIDIA GPU с 4GB+ памяти
- **RAM:** Минимум 8GB, рекомендуется 16GB+

### Размер файлов

- **Максимум:** 50MB (настраивается)
- **Рекомендуется:** PDF до 20MB, изображения до 10MB

### Языки

- **По умолчанию:** Английский
- **Многоязычные модели:** Можно заменить в конфигурации

## 🚀 Развитие проекта

### Добавление новых моделей

1. Добавьте модель в `config.py`
2. Создайте метод в `HuggingFaceService`
3. Обновите API эндпоинты

### Поддержка новых форматов

1. Добавьте обработчик в `process_document`
2. Обновите `SUPPORTED_FILE_TYPES`
3. Добавьте тесты

### Оптимизация

- Используйте `torch.float16` для экономии памяти
- Включите `torch.compile()` для ускорения (PyTorch 2.0+)
- Используйте кэширование моделей

## 📚 Полезные ссылки

- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [PyTorch документация](https://pytorch.org/docs/)
- [Sentence Transformers](https://www.sbert.net/)
- [FastAPI документация](https://fastapi.tiangolo.com/)

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи сервера
2. Убедитесь, что все зависимости установлены
3. Проверьте доступность интернета для загрузки моделей
4. Создайте issue в репозитории

---

**Удачного использования Hugging Face моделей в VisuLex! 🎉**
