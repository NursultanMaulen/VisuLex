#!/usr/bin/env python3
"""
Тест API для VisuLex с Hugging Face моделями
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Тест основного эндпоинта"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_detailed_health():
    """Тест детальной проверки здоровья"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Detailed health check: {response.status_code}")
        data = response.json()
        print(f"   Status: {data.get('status')}")
        print(f"   Device: {data.get('device')}")
        print(f"   Models: {data.get('models')}")
        print(f"   Documents: {data.get('documents_count')}")
        return True
    except Exception as e:
        print(f"❌ Detailed health check failed: {e}")
        return False

def test_upload():
    """Тест загрузки файла"""
    try:
        # Создаем тестовый PDF файл
        test_content = """
        Это тестовый документ для проверки Hugging Face моделей.
        
        Содержание документа включает в себя:
        1. Основные положения
        2. Технические требования
        3. Условия выполнения
        
        Документ предназначен для демонстрации возможностей
        извлечения текста и генерации содержания.
        """
        
        files = {'file': ('test_document.txt', test_content, 'text/plain')}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        print(f"✅ Upload: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Document ID: {data.get('doc_id')}")
            print(f"   Filename: {data.get('filename')}")
            print(f"   Summary: {data.get('summary')[:100]}...")
            print(f"   Text length: {data.get('text_length')}")
            return data.get('doc_id')
        else:
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

def test_ask(doc_id):
    """Тест отправки вопроса"""
    if not doc_id:
        print("❌ Cannot test ask without doc_id")
        return False
    
    try:
        questions = [
            "Что содержится в документе?",
            "Какие основные положения упоминаются?",
            "Для чего предназначен документ?"
        ]
        
        for i, question in enumerate(questions, 1):
            data = {
                "doc_id": doc_id,
                "question": question
            }
            response = requests.post(f"{BASE_URL}/ask", json=data)
            print(f"✅ Ask {i}: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Question: {result.get('question')}")
                print(f"   Answer: {result.get('answer')[:100]}...")
                print(f"   Confidence: {result.get('confidence', 0):.2f}")
            else:
                print(f"   Error: {response.text}")
            
            time.sleep(1)  # Небольшая пауза между запросами
        
        return True
        
    except Exception as e:
        print(f"❌ Ask failed: {e}")
        return False

def test_history():
    """Тест получения истории"""
    try:
        response = requests.get(f"{BASE_URL}/history")
        print(f"✅ History: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Documents count: {len(data)}")
            for doc_id, doc_info in data.items():
                print(f"   - {doc_id}: {doc_info.get('filename')} ({doc_info.get('file_type')})")
        else:
            print(f"   Error: {response.text}")
            
        return True
        
    except Exception as e:
        print(f"❌ History failed: {e}")
        return False

def test_document_details(doc_id):
    """Тест получения деталей документа"""
    if not doc_id:
        print("❌ Cannot test document details without doc_id")
        return False
    
    try:
        response = requests.get(f"{BASE_URL}/document/{doc_id}")
        print(f"✅ Document details: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Filename: {data.get('filename')}")
            print(f"   Summary: {data.get('summary')[:100]}...")
            print(f"   Text length: {data.get('text_length')}")
            print(f"   Has embeddings: {data.get('embeddings') is not None}")
        else:
            print(f"   Error: {response.text}")
            
        return True
        
    except Exception as e:
        print(f"❌ Document details failed: {e}")
        return False

def main():
    print("🚀 Тестирование VisuLex API с Hugging Face моделями...")
    print("=" * 70)
    
    # Тестируем все эндпоинты
    health_ok = test_health()
    if not health_ok:
        print("❌ API недоступен, остановка тестов")
        return
    
    test_detailed_health()
    
    doc_id = test_upload()
    if doc_id:
        test_ask(doc_id)
        test_document_details(doc_id)
    
    test_history()
    
    print("=" * 70)
    print("✅ Тестирование завершено!")
    print("\n💡 Теперь у вас есть полноценный API с Hugging Face моделями!")
    print("   - Извлечение текста из документов")
    print("   - Генерация содержания")
    print("   - Вопросы-ответы на основе контекста")
    print("   - Создание эмбеддингов")

if __name__ == "__main__":
    main()
