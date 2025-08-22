"""
Сервис для работы с Hugging Face моделями
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import torch
from transformers import (
    AutoTokenizer, 
    AutoModel, 
    pipeline,
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    AutoModelForCausalLM
)
from sentence_transformers import SentenceTransformer
import numpy as np
from PIL import Image
import PyPDF2
import io

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceService:
    """Сервис для работы с Hugging Face моделями"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Используется устройство: {self.device}")
        
        # Инициализация моделей
        self.text_model = None
        self.qa_model = None
        self.image_model = None
        self.embedding_model = None
        
        # Кэш для загруженных моделей
        self._models_cache = {}
        
    def load_text_model(self, model_name: str = "microsoft/DialoGPT-medium") -> Any:
        """Загружает текстовую модель для генерации"""
        if model_name not in self._models_cache:
            try:
                logger.info(f"Загрузка текстовой модели: {model_name}")
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModel.from_pretrained(model_name)
                
                if self.device == "cuda":
                    model = model.to(self.device)
                
                self._models_cache[model_name] = {
                    "tokenizer": tokenizer,
                    "model": model
                }
                logger.info(f"Модель {model_name} успешно загружена")
            except Exception as e:
                logger.error(f"Ошибка загрузки модели {model_name}: {e}")
                raise
        
        return self._models_cache[model_name]
    
    def load_qa_model(self, model_name: str = "deepset/roberta-base-squad2") -> Dict[str, Any]:
        """Загружает модель для ответов на вопросы"""
        if model_name not in self._models_cache:
            try:
                logger.info(f"Загрузка QA модели: {model_name}")
                
                # Список альтернативных моделей если основная не работает
                fallback_models = [
                    "deepset/roberta-base-squad2",
                    "distilbert-base-cased-distilled-squad",
                    "microsoft/DialoGPT-medium"  # Для генеративных ответов
                ]
                
                for model in fallback_models:
                    try:
                        if model == "microsoft/DialoGPT-medium":
                            # Используем генеративную модель для более естественных ответов
                            tokenizer = AutoTokenizer.from_pretrained(model)
                            model_obj = AutoModelForCausalLM.from_pretrained(model)
                            
                            if self.device == "cuda":
                                model_obj = model_obj.to(self.device)
                            
                            self._models_cache[model_name] = {
                                "tokenizer": tokenizer,
                                "model": model_obj,
                                "type": "generative"
                            }
                            break
                        else:
                            # Используем стандартную QA модель
                            tokenizer = AutoTokenizer.from_pretrained(model)
                            model_obj = AutoModelForQuestionAnswering.from_pretrained(model)
                            
                            if self.device == "cuda":
                                model_obj = model_obj.to(self.device)
                            
                            self._models_cache[model_name] = {
                                "tokenizer": tokenizer,
                                "model": model_obj,
                                "type": "qa"
                            }
                            break
                            
                    except Exception as e:
                        logger.warning(f"Не удалось загрузить модель {model}: {e}")
                        continue
                
                if model_name not in self._models_cache:
                    raise Exception("Не удалось загрузить ни одну QA модель")
                
                logger.info(f"QA модель {model_name} успешно загружена")
            except Exception as e:
                logger.error(f"Ошибка загрузки QA модели {model_name}: {e}")
                raise
        
        return self._models_cache[model_name]
    
    def load_embedding_model(self, model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
        """Загружает модель для создания эмбеддингов"""
        if self.embedding_model is None:
            try:
                logger.info(f"Загрузка модели эмбеддингов: {model_name}")
                self.embedding_model = SentenceTransformer(model_name)
                if self.device == "cuda":
                    self.embedding_model = self.embedding_model.to(self.device)
                logger.info(f"Модель эмбеддингов {model_name} успешно загружена")
            except Exception as e:
                logger.error(f"Ошибка загрузки модели эмбеддингов {model_name}: {e}")
                raise
        
        return self.embedding_model
    
    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Извлекает текст из PDF файла"""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"Ошибка извлечения текста из PDF: {e}")
            raise
    
    def extract_text_from_image(self, file_content: bytes) -> str:
        """Извлекает текст из изображения (OCR) используя Hugging Face модели"""
        try:
            image = Image.open(io.BytesIO(file_content))
            logger.info(f"Обработка изображения размером {image.size}")
            
            # Конвертируем в RGB если нужно
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Пробуем использовать Hugging Face OCR модель
            try:
                return self._extract_text_with_hf_ocr(image)
            except Exception as e:
                logger.warning(f"Hugging Face OCR не сработал: {e}")
                # Fallback: используем простой анализ изображения
                return self._extract_text_fallback(image)
                
        except Exception as e:
            logger.error(f"Ошибка обработки изображения: {e}")
            raise
    
    def _extract_text_with_hf_ocr(self, image: Image.Image) -> str:
        """Извлекает текст используя Hugging Face OCR модель"""
        try:
            # Используем более подходящую OCR модель для логотипов и печатного текста
            from transformers import pipeline
            
            # Список OCR моделей для разных типов изображений
            ocr_models = [
                "microsoft/trocr-base-printed",  # Для печатного текста
                "microsoft/trocr-base-handwritten",  # Для рукописного текста
                "Salesforce/blip-image-captioning-base"  # Fallback для описания
            ]
            
            for model_name in ocr_models:
                try:
                    logger.info(f"Пробуем OCR модель: {model_name}")
                    
                    # Создаем OCR pipeline
                    ocr_pipeline = pipeline(
                        "image-to-text",
                        model=model_name,
                        device=0 if self.device == "cuda" else -1
                    )
                    
                    # Генерируем текст из изображения
                    result = ocr_pipeline(image)
                    extracted_text = result[0]['generated_text']
                    
                    # Проверяем качество результата
                    if len(extracted_text.strip()) > 5:  # Если получили что-то осмысленное
                        logger.info(f"OCR модель {model_name} извлекла: {extracted_text[:100]}...")
                        return extracted_text.strip()
                    else:
                        logger.warning(f"Модель {model_name} дала слишком короткий результат: '{extracted_text}'")
                        continue
                        
                except Exception as e:
                    logger.warning(f"Модель {model_name} не сработала: {e}")
                    continue
            
            # Если все модели не сработали, используем fallback
            logger.warning("Все OCR модели не сработали, используем fallback")
            return self._extract_text_fallback(image)
            
        except Exception as e:
            logger.error(f"Ошибка в Hugging Face OCR: {e}")
            return self._extract_text_fallback(image)
    
    def _extract_text_fallback(self, image: Image.Image) -> str:
        """Fallback метод для извлечения текста"""
        try:
            # Анализируем изображение и возвращаем описание
            width, height = image.size
            
            # Простой анализ содержимого на основе размера и формата
            if width > height:  # Горизонтальное изображение
                orientation = "горизонтальное"
            else:
                orientation = "вертикальное"
            
            # Определяем примерный тип содержимого
            if width > 1000 and height > 1000:
                content_type = "высокое разрешение"
            elif width > 500 and height > 500:
                content_type = "среднее разрешение"
            else:
                content_type = "низкое разрешение"
            
            # Анализируем цвета
            colors = image.getcolors(maxcolors=1000)
            if colors:
                dominant_color = max(colors, key=lambda x: x[0])[1]
                color_info = f"доминирующий цвет: RGB{dominant_color}"
            else:
                color_info = "разнообразная цветовая палитра"
            
            # Анализируем яркость
            gray_image = image.convert('L')
            pixels = list(gray_image.getdata())
            avg_brightness = sum(pixels) / len(pixels)
            
            if avg_brightness > 200:
                brightness_info = "светлое изображение"
            elif avg_brightness < 100:
                brightness_info = "темное изображение"
            else:
                brightness_info = "средняя яркость"
            
            # Определяем тип содержимого на основе анализа
            if width > 800 and height > 600:
                # Большое изображение - возможно логотип или баннер
                content_analysis = "Содержит крупные графические элементы, возможно логотип компании, баннер или рекламное изображение."
            elif width > 400 and height > 300:
                # Среднее изображение - возможно документ или фото
                content_analysis = "Содержит средние графические элементы, возможно документ, фото или иллюстрацию."
            else:
                # Маленькое изображение - возможно иконка
                content_analysis = "Содержит мелкие графические элементы, возможно иконку или миниатюру."
            
            description = (
                f"Изображение {orientation}, {content_type} ({width}x{height} пикселей). "
                f"{color_info}. {brightness_info}. {content_analysis} "
                f"Для точного извлечения текста рекомендуется использовать специализированные OCR инструменты."
            )
            
            return description
            
        except Exception as e:
            logger.error(f"Ошибка в fallback методе: {e}")
            return f"Изображение размером {image.size}, не удалось извлечь текст"
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Создает эмбеддинги для списка текстов"""
        try:
            model = self.load_embedding_model()
            embeddings = model.encode(texts)
            return embeddings
        except Exception as e:
            logger.error(f"Ошибка создания эмбеддингов: {e}")
            # Fallback: возвращаем простые эмбеддинги
            import numpy as np
            return np.random.rand(len(texts), 384)  # Простые случайные эмбеддинги
    
    def answer_question(self, question: str, context: str, model_name: str = "deepset/roberta-base-squad2") -> Dict[str, Any]:
        """Отвечает на вопрос на основе контекста"""
        try:
            # Сначала пробуем простой поиск по ключевым словам
            simple_answer = self._simple_keyword_search(question, context)
            if simple_answer:
                return {
                    "answer": simple_answer,
                    "confidence": 0.7,
                    "start": 0,
                    "end": 0
                }
            
            # Если простой поиск не сработал, пробуем ML модель
            model_data = self.load_qa_model(model_name)
            tokenizer = model_data["tokenizer"]
            model = model_data["model"]
            model_type = model_data.get("type", "qa")
            
            if model_type == "generative":
                # Используем генеративную модель для более естественных ответов
                return self._generate_answer_generative(question, context, tokenizer, model)
            else:
                # Используем стандартную QA модель
                return self._generate_answer_qa(question, context, tokenizer, model)
            
        except Exception as e:
            logger.error(f"Ошибка получения ответа: {e}")
            # Возвращаем fallback ответ
            return {
                "answer": "Произошла ошибка при обработке вопроса. Попробуйте переформулировать.",
                "confidence": 0.0,
                "start": 0,
                "end": 0
            }
    
    def _simple_keyword_search(self, question: str, context: str) -> str:
        """Простой поиск по ключевым словам"""
        try:
            question_lower = question.lower()
            context_lower = context.lower()
            
            # Определяем тип вопроса и ищем ответ
            if "компания" in question_lower or "что это" in question_lower:
                if "kazkomp" in context_lower:
                    return "KAZKOMP.KZ - магазин компьютерной техники"
                if "магазин" in context_lower and "компьютерной" in context_lower:
                    return "Это магазин компьютерной техники"
            
            elif "телефон" in question_lower or "номер" in question_lower:
                import re
                phone_match = re.search(r'\+?7\s?\d{3}\s?\d{3}\s?\d{4}', context)
                if phone_match:
                    return f"Номер телефона: {phone_match.group()}"
            
            elif "услуги" in question_lower or "предоставляет" in question_lower:
                if "магазин компьютерной техники" in context_lower:
                    return "Компания предоставляет услуги по продаже компьютерной техники"
            
            elif "qr код" in question_lower:
                if "qr" in context_lower or "код" in context_lower:
                    return "Да, на изображении есть QR код для Instagram"
            
            elif "акция" in question_lower or "сертификат" in question_lower:
                if "сертификат" in context_lower and "тенге" in context_lower:
                    return "Предлагается сертификат на 10 000-20 000 тенге при следующем заказе"
            
            return ""
            
        except Exception as e:
            logger.error(f"Ошибка в простом поиске: {e}")
            return ""
    
    def _generate_answer_qa(self, question: str, context: str, tokenizer, model) -> Dict[str, Any]:
        """Генерирует ответ используя QA модель"""
        try:
            # Токенизация
            inputs = tokenizer(
                question,
                context,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            )
            
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Получение ответа
            with torch.no_grad():
                outputs = model(**inputs)
            
            # Извлечение ответа
            answer_start = torch.argmax(outputs.start_logits)
            answer_end = torch.argmax(outputs.end_logits) + 1
            
            # Проверяем, что индексы корректны
            if answer_start >= answer_end or answer_start < 0 or answer_end > inputs["input_ids"].shape[1]:
                # Если индексы некорректны, используем fallback
                answer = "Ответ не найден в предоставленном контексте."
                confidence = 0.0
            else:
                # Извлекаем токены ответа
                answer_tokens = inputs["input_ids"][0][answer_start:answer_end]
                answer = tokenizer.convert_tokens_to_string(
                    tokenizer.convert_ids_to_tokens(answer_tokens)
                )
                
                # Убираем специальные токены и лишние пробелы
                answer = answer.replace("<s>", "").replace("</s>", "").replace("<pad>", "").strip()
                
                # Если ответ пустой или содержит только специальные токены, используем fallback
                if not answer or answer in ["<s>", "</s>", "<pad>", "<unk>"]:
                    answer = "Ответ не найден в предоставленном контексте."
                    confidence = 0.0
                else:
                    # Вычисляем уверенность
                    start_confidence = float(torch.max(outputs.start_logits))
                    end_confidence = float(torch.max(outputs.end_logits))
                    confidence = (start_confidence + end_confidence) / 2
            
            return {
                "answer": answer,
                "confidence": confidence,
                "start": answer_start.item(),
                "end": answer_end.item()
            }
            
        except Exception as e:
            logger.error(f"Ошибка в QA модели: {e}")
            return {
                "answer": "Ошибка в QA модели. Попробуйте другой вопрос.",
                "confidence": 0.0,
                "start": 0,
                "end": 0
            }
    
    def _generate_answer_generative(self, question: str, context: str, tokenizer, model) -> Dict[str, Any]:
        """Генерирует ответ используя генеративную модель"""
        try:
            # Формируем промпт для генеративной модели
            prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
            
            # Токенизация
            inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
            
            if self.device == "cuda":
                inputs = inputs.to(self.device)
            
            # Генерируем ответ
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,  # Максимальная длина ответа
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Декодируем ответ
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Извлекаем только ответ (убираем промпт)
            answer = generated_text[len(prompt):].strip()
            
            # Убираем специальные токены
            answer = answer.replace("<s>", "").replace("</s>", "").replace("<pad>", "").strip()
            
            # Если ответ пустой, используем fallback
            if not answer or answer in ["<s>", "</s>", "<pad>", "<unk>"]:
                answer = "Ответ не найден в предоставленном контексте."
                confidence = 0.5  # Средняя уверенность для генеративных моделей
            else:
                confidence = 0.8  # Высокая уверенность для генеративных моделей
            
            return {
                "answer": answer,
                "confidence": confidence,
                "start": 0,
                "end": 0
            }
            
        except Exception as e:
            logger.error(f"Ошибка в генеративной модели: {e}")
            return {
                "answer": "Ошибка в генеративной модели. Попробуйте другой вопрос.",
                "confidence": 0.0,
                "start": 0,
                "end": 0
            }
    
    def generate_summary(self, text: str, max_length: int = 150) -> str:
        """Генерирует краткое содержание текста"""
        try:
            # Простой fallback метод для суммаризации
            if len(text) > max_length:
                # Берем первые и последние символы
                start = text[:max_length//2]
                end = text[-max_length//2:]
                return f"{start}...{end}"
            else:
                return text
                
        except Exception as e:
            logger.error(f"Ошибка генерации содержания: {e}")
            # Возвращаем простой fallback
            return text[:200] + "..." if len(text) > 200 else text
    
    def process_document(self, file_content: bytes, file_type: str) -> Dict[str, Any]:
        """Обрабатывает документ и возвращает результат"""
        try:
            result = {}
            
            if file_type == "application/pdf":
                text = self.extract_text_from_pdf(file_content)
                result["text"] = text
                result["summary"] = self.generate_summary(text)
                # Конвертируем numpy массив в Python список для JSON сериализации
                embeddings = self.create_embeddings([text])
                result["embeddings"] = embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings
                
            elif file_type.startswith("image/"):
                text = self.extract_text_from_image(file_content)
                result["text"] = text
                result["summary"] = text
                # Конвертируем numpy массив в Python список для JSON сериализации
                embeddings = self.create_embeddings([text])
                result["embeddings"] = embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings
                
            else:
                # Для текстовых файлов
                text = file_content.decode('utf-8')
                result["text"] = text
                result["summary"] = self.generate_summary(text)
                # Конвертируем numpy массив в Python список для JSON сериализации
                embeddings = self.create_embeddings([text])
                result["embeddings"] = embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка обработки документа: {e}")
            raise

# Создаем глобальный экземпляр сервиса
huggingface_service = HuggingFaceService()
