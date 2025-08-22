#!/usr/bin/env python3
"""
Тестирование OCR функциональности для изображений
"""

import requests
import json
import time

def test_ocr_functionality():
    """Тестирует OCR функциональность для изображений"""
    
    # URL бэкенда
    base_url = "http://localhost:8000"
    
    print("🧪 Тестирование OCR функциональности...")
    
    # Тест 1: Проверка здоровья API
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ API работает")
            health_data = response.json()
            print(f"   Статус: {health_data.get('status')}")
            print(f"   Модели: {health_data.get('models')}")
        else:
            print(f"❌ API недоступен: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения к API: {e}")
        return
    
    # Тест 2: Загрузка изображения для OCR
    print("\n📤 Загрузка изображения для OCR...")
    try:
        with open("test.jpg", "rb") as f:
            files = {"file": ("test.jpg", f, "image/jpg")}
            response = requests.post(f"{base_url}/upload", files=files)
            
        if response.status_code == 200:
            upload_data = response.json()
            doc_id = upload_data["doc_id"]
            print(f"✅ Изображение загружено, doc_id: {doc_id}")
            print(f"   Сводка: {upload_data['summary'][:200]}...")
        else:
            print(f"❌ Ошибка загрузки: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return
    except Exception as e:
        print(f"❌ Ошибка при загрузке изображения: {e}")
        return
    
    # Тест 3: Тестирование вопросов по изображению
    questions = [
        "Что это за компания?",
        "Какой номер телефона указан?",
        "Какие услуги предоставляет компания?",
        "Есть ли QR код на изображении?",
        "Какая акция предлагается?"
    ]
    
    print(f"\n❓ Тестирование вопросов по изображению...")
    for i, question in enumerate(questions, 1):
        print(f"\n   Вопрос {i}: {question}")
        try:
            response = requests.post(
                f"{base_url}/ask",
                json={"doc_id": doc_id, "question": question}
            )
            
            if response.status_code == 200:
                answer_data = response.json()
                answer = answer_data.get("answer", "")
                confidence = answer_data.get("confidence", 0)
                
                # Проверяем, что ответ не содержит специальные токены
                if "<s>" in answer or "</s>" in answer or "<pad>" in answer:
                    print(f"   ❌ Ответ содержит специальные токены: {answer}")
                elif not answer or answer == "Ответ не найден в предоставленном контексте.":
                    print(f"   ⚠️  Ответ не найден: {answer}")
                else:
                    print(f"   ✅ Ответ: {answer[:150]}...")
                    print(f"      Уверенность: {confidence:.2f}")
            else:
                print(f"   ❌ Ошибка: {response.status_code}")
                print(f"      Ответ: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Ошибка при отправке вопроса: {e}")
        
        # Небольшая пауза между вопросами
        time.sleep(1)
    
    # Тест 4: Получение деталей изображения
    print(f"\n🔍 Анализ извлеченного текста...")
    try:
        response = requests.get(f"{base_url}/document/{doc_id}")
        if response.status_code == 200:
            doc_data = response.json()
            text = doc_data.get("text", "")
            print(f"   Длина извлеченного текста: {len(text)} символов")
            print(f"   Первые 300 символов: {text[:300]}...")
            
            # Анализ ключевых элементов
            key_elements = [
                "KAZKOMP.KZ", "магазин", "компьютерной", "техники",
                "Куаныш", "707", "068", "2050", "сертификат", "тенге"
            ]
            
            print(f"\n   Поиск ключевых элементов:")
            for element in key_elements:
                if element.lower() in text.lower():
                    print(f"      ✅ '{element}' найден в тексте")
                else:
                    print(f"      ❌ '{element}' НЕ найден в тексте")
                    
        else:
            print(f"   ❌ Не удалось получить документ: {response.status_code}")
            print(f"      Ответ: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка при получении документа: {e}")
    
    print("\n🎯 Тестирование OCR завершено!")

if __name__ == "__main__":
    test_ocr_functionality()
