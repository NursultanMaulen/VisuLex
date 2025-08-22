#!/usr/bin/env python3
"""
Тестирование исправлений в QA модели
"""

import requests
import json

def test_qa_fix():
    """Тестирует исправления в QA модели"""
    
    # URL бэкенда
    base_url = "http://localhost:8000"
    
    print("🧪 Тестирование исправлений в QA модели...")
    
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
    
    # Тест 2: Загрузка тестового файла
    print("\n📤 Загрузка тестового файла...")
    try:
        with open("RUS_CV_Nursultan_Maulen.pdf", "rb") as f:
            files = {"file": ("test.pdf", f, "application/pdf")}
            response = requests.post(f"{base_url}/upload", files=files)
            
        if response.status_code == 200:
            upload_data = response.json()
            doc_id = upload_data["doc_id"]
            print(f"✅ Файл загружен, doc_id: {doc_id}")
            print(f"   Сводка: {upload_data['summary'][:100]}...")
        else:
            print(f"❌ Ошибка загрузки: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return
    except Exception as e:
        print(f"❌ Ошибка при загрузке файла: {e}")
        return
    
    # Тест 3: Тестирование вопросов
    questions = [
        "Who is Nursultan?",
        "What is he studying?",
        "What is his GPA?",
        "What courses did he take?"
    ]
    
    print(f"\n❓ Тестирование вопросов...")
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
                    print(f"   ✅ Ответ: {answer[:100]}...")
                    print(f"      Уверенность: {confidence:.2f}")
            else:
                print(f"   ❌ Ошибка: {response.status_code}")
                print(f"      Ответ: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Ошибка при отправке вопроса: {e}")
    
    # Тест 4: Попробуем простой поиск по тексту
    print(f"\n🔍 Тестирование простого поиска по тексту...")
    try:
        # Сначала проверим историю
        response = requests.get(f"{base_url}/history")
        if response.status_code == 200:
            history = response.json()
            print(f"   История документов: {list(history.keys())}")
            if doc_id in history:
                print(f"   ✅ Документ {doc_id} найден в истории")
            else:
                print(f"   ❌ Документ {doc_id} НЕ найден в истории")
        else:
            print(f"   ❌ Не удалось получить историю: {response.status_code}")
        
        # Получаем детали документа
        response = requests.get(f"{base_url}/document/{doc_id}")
        if response.status_code == 200:
            doc_data = response.json()
            text = doc_data.get("text", "")
            print(f"   Длина текста: {len(text)} символов")
            print(f"   Первые 200 символов: {text[:200]}...")
            
            # Простой поиск по ключевым словам
            if "Nursultan" in text:
                print("   ✅ 'Nursultan' найден в тексте")
            if "Computer Systems" in text:
                print("   ✅ 'Computer Systems' найден в тексте")
            if "GPA" in text:
                print("   ✅ 'GPA' найден в тексте")
                
        else:
            print(f"   ❌ Не удалось получить документ: {response.status_code}")
            print(f"      Ответ: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка при получении документа: {e}")
    
    print("\n🎯 Тестирование завершено!")

if __name__ == "__main__":
    test_qa_fix()
