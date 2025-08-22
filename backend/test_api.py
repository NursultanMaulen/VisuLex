#!/usr/bin/env python3
"""
Простой тест API для проверки работоспособности
"""

import requests
import json

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

def test_upload():
    """Тест загрузки файла"""
    try:
        # Создаем тестовый файл
        files = {'file': ('test.txt', 'This is a test file content', 'text/plain')}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        print(f"✅ Upload: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.json().get('doc_id')
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

def test_ask(doc_id):
    """Тест отправки вопроса"""
    if not doc_id:
        print("❌ Cannot test ask without doc_id")
        return False
    
    try:
        data = {
            "doc_id": doc_id,
            "question": "What is this document about?"
        }
        response = requests.post(f"{BASE_URL}/ask", json=data)
        print(f"✅ Ask: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Ask failed: {e}")
        return False

def test_history():
    """Тест получения истории"""
    try:
        response = requests.get(f"{BASE_URL}/history")
        print(f"✅ History: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ History failed: {e}")
        return False

def main():
    print("🚀 Тестирование API...")
    print("=" * 50)
    
    # Тестируем все эндпоинты
    health_ok = test_health()
    if not health_ok:
        print("❌ API недоступен, остановка тестов")
        return
    
    doc_id = test_upload()
    if doc_id:
        test_ask(doc_id)
    
    test_history()
    
    print("=" * 50)
    print("✅ Тестирование завершено!")

if __name__ == "__main__":
    main()
