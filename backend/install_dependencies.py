#!/usr/bin/env python3
"""
Скрипт для установки зависимостей Hugging Face
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Выполняет команду и выводит результат"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} завершено успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при {description.lower()}: {e}")
        print(f"   stderr: {e.stderr}")
        return False

def check_python_version():
    """Проверяет версию Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Требуется Python 3.8 или выше")
        print(f"   Текущая версия: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python версия: {version.major}.{version.minor}.{version.micro}")
    return True

def install_requirements():
    """Устанавливает зависимости из requirements.txt"""
    if not os.path.exists("requirements.txt"):
        print("❌ Файл requirements.txt не найден")
        return False
    
    return run_command("pip install -r requirements.txt", "Установка зависимостей")

def test_imports():
    """Проверяет, что основные библиотеки импортируются"""
    print("🔍 Проверка импорта библиотек...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
        
        import sentence_transformers
        print(f"✅ Sentence Transformers: {sentence_transformers.__version__}")
        
        import numpy
        print(f"✅ NumPy: {numpy.__version__}")
        
        import PIL
        print(f"✅ Pillow: {PIL.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def create_cache_directory():
    """Создает директорию для кэша моделей"""
    cache_dir = "./models_cache"
    try:
        os.makedirs(cache_dir, exist_ok=True)
        print(f"✅ Директория кэша создана: {cache_dir}")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания директории кэша: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Установка зависимостей для VisuLex с Hugging Face")
    print("=" * 60)
    
    # Проверяем версию Python
    if not check_python_version():
        sys.exit(1)
    
    # Создаем директорию кэша
    create_cache_directory()
    
    # Устанавливаем зависимости
    if not install_requirements():
        print("❌ Установка зависимостей не удалась")
        sys.exit(1)
    
    # Проверяем импорты
    if not test_imports():
        print("❌ Проверка импорта не удалась")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Все зависимости установлены успешно!")
    print("\n💡 Теперь вы можете:")
    print("   1. Запустить сервер: python run.py")
    print("   2. Протестировать API: python test_api.py")
    print("   3. Открыть документацию: README_HUGGINGFACE.md")
    
    print("\n⚠️  Важные замечания:")
    print("   - При первом запуске будут загружены модели (~3-4GB)")
    print("   - Убедитесь, что у вас достаточно места на диске")
    print("   - Для лучшей производительности используйте GPU")

if __name__ == "__main__":
    main()
